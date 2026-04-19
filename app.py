from flask import Flask, render_template, request
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pooj@162000", 
    database="hospitaldb"
)

cursor = db.cursor()

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

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

        cursor.execute(query, values)
        db.commit()

        return "✅ Patient Added Successfully!"

    return render_template('add_patient.html')

@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        phone = request.form['phone']

        query = "INSERT INTO Doctor (name, specialization, phone) VALUES (%s, %s, %s)"
        values = (name, specialization, phone)

        cursor.execute(query, values)
        db.commit()

        return "✅ Doctor Added Successfully!"

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

        cursor.execute(query, values)
        db.commit()

        return "✅ Appointment Booked!"

    return render_template('appointment.html')

@app.route('/billing', methods=['GET', 'POST'])
def billing():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        amount = request.form['amount']
        status = request.form['status']

        query = "INSERT INTO Billing (patient_id, amount, payment_status, bill_date) VALUES (%s, %s, %s, CURDATE())"
        values = (patient_id, amount, status)

        cursor.execute(query, values)
        db.commit()

        return "✅ Bill Generated!"

    return render_template('billing.html')

if __name__ == "__main__":
    app.run(debug=True)