from flask import Flask, render_template, request, flash, redirect, url_for
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pooj@162000", 
    database="hospitaldb"
)

cursor = db.cursor()

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_hospital'
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Fetch real-time statistics
    cursor.execute("SELECT COUNT(*) FROM Patient")
    total_patients = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Doctor")
    total_doctors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Appointment")
    total_appointments = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM room WHERE availability = 1")
    available_rooms = cursor.fetchone()[0]

    return render_template('dashboard.html', 
                           total_patients=total_patients, 
                           total_doctors=total_doctors, 
                           total_appointments=total_appointments, 
                           available_rooms=available_rooms)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        phone = request.form['phone']
        address = request.form['address']

        query = "INSERT INTO Patient (name, age, gender, phone, address) VALUES (%s, %s, %s, %s, %s)"
        values = (name, age, gender, phone, address)

        try:
            cursor.execute(query, values)
            db.commit()
            flash("✅ Patient Added Successfully!", "success")
        except mysql.connector.Error as err:
            db.rollback()
            if err.errno == 1062:
                flash("❌ Error: Patient with this phone number already exists!", "danger")
            else:
                flash(f"❌ Database Error: {err.msg}", "danger")

        return redirect(url_for('add_patient'))

    return render_template('add_patient.html')

@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        phone = request.form['phone']

        query = "INSERT INTO Doctor (name, specialization, phone) VALUES (%s, %s, %s)"
        values = (name, specialization, phone)

        try:
            cursor.execute(query, values)
            db.commit()
            flash("✅ Doctor Added Successfully!", "success")
        except mysql.connector.Error as err:
            db.rollback()
            if err.errno == 1062:
                flash("❌ Error: Doctor with this phone number already exists!", "danger")
            else:
                flash(f"❌ Database Error: {err.msg}", "danger")

        return redirect(url_for('add_doctor'))

    return render_template('add_doctor.html')

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date = request.form['date']
        time = request.form['time']

        query = """INSERT INTO Appointment 
                   (patient_id, doctor_id, appointment_date, appointment_time)
                   VALUES (%s, %s, %s, %s)"""

        values = (patient_id, doctor_id, date, time)

        try:
            cursor.execute(query, values)
            db.commit()
            flash("✅ Appointment Booked!", "success")
        except mysql.connector.Error as err:
            db.rollback()
            flash(f"❌ Database Error: {err.msg}", "danger")

        return redirect(url_for('appointment'))

    cursor.execute("SELECT patient_id, name FROM Patient")
    patients = cursor.fetchall()

    cursor.execute("SELECT doctor_id, name FROM Doctor")
    doctors = cursor.fetchall()

    return render_template('appointment.html', patients=patients, doctors=doctors)

@app.route('/billing', methods=['GET', 'POST'])
def billing():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        amount = request.form['amount']
        status = request.form['status']

        query = "INSERT INTO billing (patient_id, total_amount, payment_status, bill_date) VALUES (%s, %s, %s, CURDATE())"
        values = (patient_id, amount, status)

        try:
            cursor.execute(query, values)
            db.commit()
            flash("✅ Bill Generated!", "success")
        except mysql.connector.Error as err:
            db.rollback()
            flash(f"❌ Database Error: {err.msg}", "danger")

        return redirect(url_for('billing'))

    cursor.execute("SELECT patient_id, name FROM Patient")
    patients = cursor.fetchall()

    return render_template('billing.html', patients=patients)

@app.route('/admission', methods=['GET', 'POST'])
def admission():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        room_id = request.form['room_id']
        admission_date = request.form['admission_date']

        # Start a transaction to ensure both insertion and room update happen together
        try:
            # 1. Insert into admission table
            query_insert = "INSERT INTO admission (patient_id, room_id, admission_date) VALUES (%s, %s, %s)"
            cursor.execute(query_insert, (patient_id, room_id, admission_date))
            
            # 2. Update room availability to 0 (unavailable)
            query_update = "UPDATE room SET availability = 0 WHERE room_id = %s"
            cursor.execute(query_update, (room_id,))
            
            db.commit()
            flash("✅ Patient Admitted Successfully!", "success")
        except mysql.connector.Error as err:
            db.rollback()
            flash(f"❌ Database Error: {err.msg}", "danger")

        return redirect(url_for('admission'))

    # GET request - fetch patients and available rooms for dropdowns
    cursor.execute("SELECT patient_id, name FROM Patient")
    patients = cursor.fetchall()

    # Fetch only rooms that are available (availability = 1)
    cursor.execute("SELECT room_id, room_type FROM room WHERE availability = 1")
    rooms = cursor.fetchall()

    return render_template('admission.html', patients=patients, rooms=rooms)

@app.route('/rooms', methods=['GET', 'POST'])
def rooms():
    if request.method == 'POST':
        room_type = request.form['room_type']
        
        query = "INSERT INTO room (room_type, availability) VALUES (%s, 1)"
        try:
            cursor.execute(query, (room_type,))
            db.commit()
            flash("✅ Room Added Successfully!", "success")
        except mysql.connector.Error as err:
            db.rollback()
            flash(f"❌ Database Error: {err.msg}", "danger")
            
        return redirect(url_for('rooms'))
        
    # GET request - fetch all rooms
    cursor.execute("SELECT room_id, room_type, availability FROM room")
    all_rooms = cursor.fetchall()
    
    return render_template('rooms.html', rooms=all_rooms)

@app.route('/medical_records', methods=['GET', 'POST'])
def medical_records():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        diagnosis = request.form['diagnosis']
        treatment = request.form['treatment']
        record_date = request.form['record_date']
        
        query = "INSERT INTO medical_record (patient_id, diagnosis, treatment, record_date) VALUES (%s, %s, %s, %s)"
        try:
            cursor.execute(query, (patient_id, diagnosis, treatment, record_date))
            db.commit()
            flash("✅ Medical Record Added Successfully!", "success")
        except mysql.connector.Error as err:
            db.rollback()
            flash(f"❌ Database Error: {err.msg}", "danger")
            
        return redirect(url_for('medical_records'))
        
    # GET request - fetch patients
    cursor.execute("SELECT patient_id, name FROM Patient")
    patients = cursor.fetchall()
    
    # Optional: Fetch existing records to display
    cursor.execute("""
        SELECT m.record_id, p.name, m.diagnosis, m.treatment, m.record_date 
        FROM medical_record m 
        JOIN Patient p ON m.patient_id = p.patient_id
        ORDER BY m.record_date DESC
    """)
    records = cursor.fetchall()
    
    return render_template('medical_records.html', patients=patients, records=records)

if __name__ == "__main__":
    app.run(debug=True)