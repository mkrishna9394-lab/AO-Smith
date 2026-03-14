<<<<<<< HEAD
# AO-Smith
=======
# AO Smith Production Monitoring - Flask + MariaDB

A modular Flask application inspired by the reference dashboards you shared.

## Features
- Dark industrial dashboard UI similar to your screenshots
- Modular Flask app factory structure
- MariaDB-ready schema
- Station-wise production monitoring
- Report API for:
  - today's completed batches by station
  - number of delays
  - delay reasons
  - total delay time by reason
- Separate pages for Home, Time Sheet, Plan Entry, and Reports

## Suggested Folder Structure
```text
ao_smith_flask_app/
│── app/
│   ├── dashboard/
│   ├── reports/
│   ├── stations/
│   ├── static/
│   └── templates/
│── config.py
│── run.py
│── schema.sql
│── seed_data.sql
│── requirements.txt
└── .env.example
```

## Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Update `.env` with your MariaDB credentials.

## Create Database
Run these in MariaDB:
```sql
SOURCE schema.sql;
SOURCE seed_data.sql;
```

## Run App
```bash
python run.py
```

## Example Report Requirement Covered
For station 10, the report shows:
- how many batches produced today
- how many delays happened
- what reasons caused the delay
- how much total delay time happened for each reason

## Recommended Next Enhancements
- Login and role-based access
- Shift-wise reporting
- Filters by line, station, date range, and model
- Charts for delay trends and OEE
- Export to Excel/PDF
- Live machine integration from PLC / MQTT / OPC UA / Modbus

## GitHub Push to `krishna` branch
Because I cannot directly push to your GitHub branch from here, use these commands from your project folder:

```bash
git init
git remote add origin <YOUR_GITHUB_REPO_URL>
git checkout -b krishna
git add .
git commit -m "Initial AO Smith Flask monitoring app"
git push -u origin krishna
```

If your repo already exists locally:
```bash
git checkout krishna
git add .
git commit -m "Add AO Smith Flask monitoring app"
git push origin krishna
```
>>>>>>> 155a4ad (Initial AO Smith Flask monitoring app)
