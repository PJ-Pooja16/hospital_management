# MediCare - Hospital Management System

A comprehensive, web-based Hospital Management System designed to handle patient information, hospital operations, and clinical records. The system enables authorized users to securely manage centralized data, facilitating efficient coordination across different units of the hospital.

## 🌟 Features

This application features a beautiful, dynamic, and responsive user interface with the following modules:

* **📊 Live Analytics Dashboard**: Real-time metric cards displaying total registered patients, doctors, scheduled appointments, and currently available hospital rooms.
* **🏥 Room Management**: Add hospital rooms (General Ward, ICU, Operation Theater) and track their real-time availability.
* **🛏️ Patient Admissions**: Smart room booking system that assigns patients to available rooms and automatically updates the room's occupancy status to prevent double-booking.
* **📅 Appointment Scheduling**: Seamlessly book appointments by selecting existing patients and doctors from intelligent dropdown menus.
* **🩺 Medical Records & Prescriptions**: 
  * Log patient diagnoses and prescribed treatments.
  * **Edit Records**: Fully editable records to easily correct mistakes or update conditions.
  * **Downloadable Prescriptions**: Automatically generate professionally formatted, hospital-branded prescription pads that instantly open your browser's "Save as PDF" dialog.
* **👥 Staff & Patient Registration**: Securely register new patients and doctors into the system.
* **💳 Billing System**: Generate financial bills and track patient payment status.

## 🛠️ Technology Stack

* **Backend**: Python 3, Flask framework
* **Database**: MySQL (via `mysql-connector-python`)
* **Frontend**: HTML5, CSS3 (Custom responsive styling), FontAwesome Icons, Google Fonts (Inter)

## ⚙️ Installation & Setup

1. **Clone the repository** (or download the project folder).
2. **Install Python Dependencies**:
   Make sure you have Python installed, then run:
   ```bash
   pip install flask mysql-connector-python
   ```
3. **Database Setup**:
   - Install MySQL Server on your machine.
   - Create a database named `hospitaldb`.
   - Ensure the database credentials in `app.py` match your local MySQL setup. By default, it expects:
     - Host: `localhost`
     - User: `root`
     - Password: `Pooj@162000`
   - Run the provided SQL queries (or use the application to auto-generate rows if the tables are empty).
4. **Run the Application**:
   Navigate to the project directory in your terminal and run:
   ```bash
   python app.py
   ```
   *(On some Windows systems, you may need to run `py app.py` instead)*
5. **Access the Portal**: Open your web browser and go to `http://127.0.0.1:5000`.

## 🗄️ Database Schema Overview

The system uses a highly relational MySQL database structure:
* `Patient` (patient_id, name, age, gender, phone, address)
* `Doctor` (doctor_id, name, specialization, phone)
* `Appointment` (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, status)
* `room` (room_id, room_type, availability)
* `admission` (admission_id, patient_id, room_id, admission_date, discharge_date)
* `medical_record` (record_id, patient_id, diagnosis, treatment, record_date)
* `billing` (bill_id, patient_id, total_amount, payment_status, bill_date)

---
*Built as a fully-featured, production-ready hospital administration portal.*
