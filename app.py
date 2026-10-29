import os
from functools import wraps
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-local-secret-before-deployment")

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "127.0.0.1"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "Yogi"),
    "database": os.environ.get("DB_NAME", "wellness_center"),
    "port": int(os.environ.get("DB_PORT", "3306")),
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_id"):
            flash("Please log in as admin first.", "warning")
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)
    return wrapped

def init_db():
    """Create tables. Run after creating the database using database.sql."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(120) NOT NULL,
            description TEXT NOT NULL,
            duration_minutes INT NOT NULL DEFAULT 60,
            price DECIMAL(10,2) NOT NULL DEFAULT 0,
            active TINYINT(1) NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(120) NOT NULL,
            email VARCHAR(150) NOT NULL UNIQUE,
            phone VARCHAR(25) NOT NULL,
            gender VARCHAR(30) DEFAULT '',
            dob DATE NULL,
            address VARCHAR(255) DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(80) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            client_id INT NOT NULL,
            service_id INT NOT NULL,
            appointment_date DATE NOT NULL,
            appointment_time TIME NOT NULL,
            notes VARCHAR(500) DEFAULT '',
            status ENUM('Pending','Confirmed','Completed','Cancelled') NOT NULL DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_appointment_client FOREIGN KEY (client_id) REFERENCES clients(id),
            CONSTRAINT fk_appointment_service FOREIGN KEY (service_id) REFERENCES services(id)
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM services")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO services (name, description, duration_minutes, price) VALUES (%s,%s,%s,%s)",
            [
                ("Yoga & Meditation", "Gentle movement, breathing, and mindfulness session.", 60, 500),
                ("Nutrition Consultation", "Personalised general nutrition and wellness guidance.", 45, 700),
                ("Relaxation Therapy", "A calming relaxation session to support wellbeing.", 60, 900),
            ],
        )
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/")
def home():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, description, duration_minutes, price FROM services WHERE active=1 ORDER BY id")
    services = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", services=services)

@app.route("/services")
def services():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, description, duration_minutes, price FROM services WHERE active=1 ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("services.html", services=rows)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        gender = request.form.get("gender", "").strip()
        dob = request.form.get("dob") or None
        address = request.form.get("address", "").strip()
        if not full_name or not email or not phone:
            flash("Please fill in all required fields.", "danger")
            return render_template("register.html")
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO clients (full_name,email,phone,gender,dob,address) VALUES (%s,%s,%s,%s,%s,%s)",
                (full_name, email, phone, gender, dob, address),
            )
            conn.commit()
            flash("Registration successful! You can now book an appointment using your email.", "success")
            return redirect(url_for("book_appointment", email=email))
        except mysql.connector.IntegrityError:
            flash("This email is already registered. Please use the appointment form.", "warning")
        finally:
            cur.close()
            conn.close()
    return render_template("register.html")

@app.route("/book", methods=["GET", "POST"])
def book_appointment():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id,name,description,duration_minutes,price FROM services WHERE active=1 ORDER BY name")
    service_rows = cur.fetchall()
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        service_id = request.form.get("service_id", type=int)
        appt_date = request.form.get("appointment_date", "")
        appt_time = request.form.get("appointment_time", "")
        notes = request.form.get("notes", "").strip()
        if not all([full_name, email, phone, service_id, appt_date, appt_time]):
            flash("Please complete all required appointment fields.", "danger")
        else:
            try:
                date_value = datetime.strptime(appt_date, "%Y-%m-%d").date()
                if date_value < datetime.now().date():
                    flash("Please choose today or a future date.", "danger")
                else:
                    cur2 = conn.cursor()
                    cur2.execute("SELECT id FROM clients WHERE email=%s", (email,))
                    client = cur2.fetchone()
                    if client:
                        client_id = client[0]
                        cur2.execute("UPDATE clients SET full_name=%s, phone=%s WHERE id=%s", (full_name, phone, client_id))
                    else:
                        cur2.execute("INSERT INTO clients (full_name,email,phone) VALUES (%s,%s,%s)", (full_name,email,phone))
                        client_id = cur2.lastrowid
                    cur2.execute("SELECT id FROM services WHERE id=%s AND active=1", (service_id,))
                    if not cur2.fetchone():
                        flash("Please choose a valid service.", "danger")
                    else:
                        cur2.execute(
                            "INSERT INTO appointments (client_id,service_id,appointment_date,appointment_time,notes) VALUES (%s,%s,%s,%s,%s)",
                            (client_id,service_id,appt_date,appt_time,notes),
                        )
                        conn.commit()
                        flash("Appointment request received! The admin will review it.", "success")
                        cur2.close()
                        cur.close()
                        conn.close()
                        return redirect(url_for("home"))
                    cur2.close()
            except ValueError:
                flash("Please enter a valid appointment date.", "danger")
            except Error:
                conn.rollback()
                flash("Could not save the appointment. Please try again.", "danger")
    cur.close()
    conn.close()
    return render_template("book.html", services=service_rows, today=datetime.now().date().isoformat())

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id,username,password_hash FROM admins WHERE username=%s", (username,))
        admin = cur.fetchone()
        cur.close()
        conn.close()
        if admin and check_password_hash(admin["password_hash"], password):
            session.clear()
            session["admin_id"] = admin["id"]
            session["admin_username"] = admin["username"]
            return redirect(url_for("admin_dashboard"))
        flash("Invalid username or password.", "danger")
    return render_template("admin_login.html")

@app.route("/admin")
@login_required
def admin_dashboard():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) AS total FROM clients")
    total_clients = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) AS total FROM appointments WHERE status='Pending'")
    pending_appointments = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) AS total FROM services WHERE active=1")
    active_services = cur.fetchone()["total"]
    cur.execute("""
        SELECT a.id, c.full_name, c.email, c.phone, s.name AS service_name,
               a.appointment_date, TIME_FORMAT(a.appointment_time,'%H:%i') AS appointment_time,
               a.status, a.notes
        FROM appointments a
        JOIN clients c ON c.id=a.client_id
        JOIN services s ON s.id=a.service_id
        ORDER BY a.appointment_date DESC, a.appointment_time DESC
        LIMIT 100
    """)
    appointments = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("admin_dashboard.html", total_clients=total_clients,
        pending_appointments=pending_appointments, active_services=active_services,
        appointments=appointments)

@app.route("/admin/appointments/<int:appointment_id>/status", methods=["POST"])
@login_required
def update_appointment_status(appointment_id):
    status = request.form.get("status", "")
    allowed = {"Pending", "Confirmed", "Completed", "Cancelled"}
    if status not in allowed:
        abort(400)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE appointments SET status=%s WHERE id=%s", (status, appointment_id))
    conn.commit()
    cur.close()
    conn.close()
    flash("Appointment status updated.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/clients")
@login_required
def admin_clients():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id,full_name,email,phone,gender,dob,address,created_at FROM clients ORDER BY id DESC")
    clients = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("admin_clients.html", clients=clients)

@app.route("/admin/services", methods=["GET", "POST"])
@login_required
def admin_services():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        duration = request.form.get("duration_minutes", type=int)
        price = request.form.get("price", type=float)
        if name and description and duration and duration > 0 and price is not None and price >= 0:
            cur.execute("INSERT INTO services (name,description,duration_minutes,price) VALUES (%s,%s,%s,%s)",
                        (name,description,duration,price))
            conn.commit()
            flash("Service added.", "success")
            cur.close()
            conn.close()
            return redirect(url_for("admin_services"))
        flash("Enter valid service details.", "danger")
    cur.execute("SELECT id,name,description,duration_minutes,price,active FROM services ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("admin_services.html", services=rows)

@app.route("/admin/services/<int:service_id>/toggle", methods=["POST"])
@login_required
def toggle_service(service_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE services SET active=IF(active=1,0,1) WHERE id=%s", (service_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash("Service availability updated.", "success")
    return redirect(url_for("admin_services"))

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    # Create tables only after the database itself has been created.
    try:
        init_db()
        print("Database tables checked/created successfully.")
    except Error as exc:
        print("Database connection failed:", exc)
        print("Check database.sql and DB_CONFIG / environment variables.")
    app.run(debug=True)
