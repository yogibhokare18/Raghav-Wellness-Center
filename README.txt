WELLNESS MANAGEMENT SYSTEM — LOCAL SETUP (Windows)

FEATURES
- Public home page and active service catalogue
- Client registration
- Appointment requests
- Admin login
- Admin dashboard with appointment status updates
- Client directory
- Add/hide services
- MySQL database

PROJECT STRUCTURE
Wellness_Management_System/
  app.py
  database.sql
  requirements.txt
  setup_admin.py
  templates/
  static/

STEP 1 — Install/check MySQL
Make sure MySQL Server is running. This project defaults to port 3306.
If your MySQL is on port 3307, set DB_PORT=3307 before running commands.

STEP 2 — Create the database
Open MySQL Workbench or log in from CMD:
  mysql -u root -p
Then run the contents of database.sql:
  SOURCE C:/path/to/Wellness_Management_System/database.sql;
Alternatively, open database.sql in MySQL Workbench and execute it.
Only create the database; app.py creates the tables automatically on startup.

STEP 3 — Open terminal in the project folder
  cd "C:\path\to\Wellness_Management_System"

STEP 4 — Create and activate virtual environment
  py -3.12 -m venv venv
  .\venv\Scripts\Activate.ps1
If PowerShell blocks activation, use Command Prompt:
  venv\Scripts\activate.bat

STEP 5 — Install packages
  python -m pip install -r requirements.txt

STEP 6 — Set database credentials for the current CMD session
Replace YOUR_MYSQL_PASSWORD with your real MySQL root password:
  set DB_HOST=127.0.0.1
  set DB_USER=root
  set DB_PASSWORD=YOUR_MYSQL_PASSWORD
  set DB_NAME=wellness_center
  set DB_PORT=3306
If root has no password, set DB_PASSWORD= (empty).
Do not put your real password in screenshots or share it.
For PowerShell, use:
  $env:DB_HOST="127.0.0.1"
  $env:DB_USER="root"
  $env:DB_PASSWORD="YOUR_MYSQL_PASSWORD"
  $env:DB_NAME="wellness_center"
  $env:DB_PORT="3306"

STEP 7 — Start the app once to create tables
  python app.py
Keep this terminal open. Visit http://127.0.0.1:5000 in your browser.
Stop the server with Ctrl+C when needed.

STEP 8 — Create admin account (in a second terminal)
Activate the same venv and set the same DB environment variables in that terminal.
Then run:
  python setup_admin.py
Choose an admin username and a strong password of at least 10 characters.
The password is stored as a hash, not plain text.

STEP 9 — Test
- Home: http://127.0.0.1:5000/
- Services: http://127.0.0.1:5000/services
- Register: http://127.0.0.1:5000/register
- Book appointment: http://127.0.0.1:5000/book
- Admin login: http://127.0.0.1:5000/admin/login
- Dashboard: http://127.0.0.1:5000/admin

TROUBLESHOOTING
- Access denied for root: check DB_PASSWORD and DB_USER.
- Can't connect: verify MySQL is running and DB_PORT is correct.
- Unknown database: run database.sql first.
- If an import is missing: activate venv and pip install -r requirements.txt.

SECURITY NOTES
This is a learning/demo starter project. Before production deployment, configure a strong FLASK_SECRET_KEY,
use environment variables, disable debug mode, add CSRF protection and rate limiting, configure HTTPS,
and review privacy/access-control requirements. Do not expose real client information publicly.
