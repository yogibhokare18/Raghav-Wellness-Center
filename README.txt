# Raghav Wellness Center

A web-based Wellness Center Management System built using **Python, Flask, MySQL, HTML, CSS, and JavaScript**.

This application allows clients to explore wellness services, register their details, and request appointments. Administrators can manage appointments, view registered clients, and manage the service catalogue through an admin dashboard.

## Features

- Public home page
- Active wellness service catalogue
- Client registration
- Appointment booking requests
- Admin login with password hashing
- Admin dashboard with appointment status updates
- Client directory
- Add and hide wellness services
- MySQL database integration
- Responsive website interface

## Technology Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Database:** MySQL
- **Template Engine:** Jinja2
- **Version Control:** Git and GitHub

## Project Structure

```text
Raghav-Wellness-Center/
├── app.py
├── database.sql
├── requirements.txt
├── setup_admin.py
├── templates/
├── static/
├── README.md
└── .gitignore
```

*Note: This structure shows the main project files. Your actual project may contain additional files and folders.*

## Local Setup (Windows)

Follow these steps to run the project on your local Windows computer.

### Step 1: Install and Check MySQL

Make sure MySQL Server is installed and running.

The project uses port `3306` by default. If your MySQL Server uses port `3307`, configure `DB_PORT` accordingly.

### Step 2: Create the Database

Open MySQL Workbench or Command Prompt and log in to MySQL:

```bash
mysql -u root -p
```

Run the SQL file from the MySQL prompt using the actual path to your project:

```sql
SOURCE C:/path/to/Raghav-Wellness-Center/database.sql;
```

Alternatively, open `database.sql` in MySQL Workbench and execute it.

**Important:** Replace the example path above with your actual project path. The application creates its tables automatically when it starts, according to the project configuration.

### Step 3: Open the Project Folder

Open Command Prompt in your project directory:

```bat
cd "C:\path\to\Wellness_Management_System"
```

Replace the example path with your actual project folder path.

### Step 4: Create and Activate a Virtual Environment

Create the virtual environment using Python 3.12:

```bat
py -3.12 -m venv venv
```

Activate it in Command Prompt:

```bat
venv\Scripts\activate.bat
```

If you are using PowerShell instead, run:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

Install the required Python packages:

```bash
python -m pip install -r requirements.txt
```

### Step 6: Configure Database Credentials

Set the environment variables in the same Command Prompt session.

Replace `Yogi` with your actual MySQL password. Do not share your password publicly.

```bat
set DB_HOST=127.0.0.1
set DB_USER=root
set DB_PASSWORD=Yogi
set DB_NAME=wellness_center
set DB_PORT=3306
```

If your MySQL Server uses port `3307`, use:

```bat
set DB_PORT=3307
```

If the MySQL root account has no password, use:

```bat
set DB_PASSWORD=Yogi
```

For PowerShell, use:

```powershell
$env:DB_HOST="127.0.0.1"
$env:DB_USER="root"
$env:DB_PASSWORD="Yogi"
$env:DB_NAME="wellness_center"
$env:DB_PORT="3306"
```

These variables apply to the current terminal session. Set them again in any new terminal that needs them.

### Step 7: Start the Application

Run:

```bash
python app.py
```

Keep the terminal open while using the website.

Open the following URL in your browser:

http://127.0.0.1:5000/

Stop the server with `Ctrl + C` when needed.

### Step 8: Create the Admin Account

Open a second terminal in the project directory.

Activate the same virtual environment and configure the same database environment variables in that terminal.

Then run:

```bash
python setup_admin.py
```

Enter an admin username and a strong password containing at least 10 characters.

The setup script is intended to store the password as a hash rather than plain text.

**Security tip:** Never commit your real admin password to GitHub.

### Step 9: Test the Application

With the Flask server running, test these pages:

| Page | Local URL |
|---|---|
| Home | http://127.0.0.1:5000/ |
| Services | http://127.0.0.1:5000/services |
| Client Registration | http://127.0.0.1:5000/register |
| Book Appointment | http://127.0.0.1:5000/book |
| Admin Login | http://127.0.0.1:5000/admin/login |
| Admin Dashboard | http://127.0.0.1:5000/admin |

These URLs work on your computer while the local Flask server is running. They are not public website links.

## Troubleshooting

**Access denied for root**

- Verify `DB_USER` and `DB_PASSWORD`.
- Make sure the credentials match your MySQL configuration.

**Cannot connect to MySQL**

- Check whether MySQL Server is running.
- Verify that `DB_HOST` and `DB_PORT` are correct.

**Unknown database**

- Run `database.sql` first.
- Verify that the configured database name is `wellness_center`.

**Missing Python module**

- Activate the virtual environment.
- Run `python -m pip install -r requirements.txt`.

**Port already in use**

- Stop the other application using port `5000`, or configure Flask to use another available port.

## Security Notes

This project is intended as a learning and demonstration application.

Before using it in production:

- Configure a strong, private `FLASK_SECRET_KEY`.
- Store credentials and secrets in environment variables.
- Never upload `.env` files or real passwords to GitHub.
- Disable Flask debug mode in production.
- Add CSRF protection and rate limiting.
- Configure HTTPS.
- Review authentication, authorization, and data privacy requirements.
- Do not expose real client information publicly.
- Use appropriate database permissions instead of relying on a root account for production.

## Future Improvements

- Deploy the application to a hosting platform.
- Add automated tests.
- Improve form validation and error handling.
- Add appointment search and filtering.
- Improve mobile accessibility.

## Disclaimer

This project is intended for educational and demonstration purposes. Review the code, configuration, and security controls before using it with real clients.
