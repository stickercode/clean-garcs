[README.md](https://github.com/user-attachments/files/35010864/README.md)
# GARCS — Gamified Adaptive Reading Comprehension System

GARCS is a web-based reading comprehension platform designed to provide Grade 5–10 learners with reading activities and questions guided by their recorded performance. It combines a skill-aware, rule-based adaptive question-selection mechanism with progress tracking and gamification features.

The system tracks three comprehension skills:

- **Literal** — understanding information stated directly in a text.
- **Inferential** — drawing conclusions and interpreting information from a text.
- **Critical** — evaluating, analyzing, and making judgments about textual information.

GARCS maintains a separate mastery value for each skill. After a learner answers a question, the system updates the relevant skill state and uses the resulting mastery information to guide the next question's skill and difficulty.



---

## Features

### Adaptive reading assessment

- Maintains separate mastery estimates for literal, inferential, and critical comprehension.
- Classifies mastery into **Weak**, **Developing**, and **Strong** bands.
- Prioritizes the learner's weakest skill during adaptive question selection.
- Uses a configured exploration probability to introduce variation in skill selection.
- Maps mastery to a target question difficulty and applies fallback/relaxation rules when the preferred skill–difficulty combination is unavailable.
- Avoids serving questions the learner has already answered, subject to the assessment and passage-selection rules.

### Learner accounts and progress

- Student registration and login.
- Assessment-session creation and response recording.
- Per-skill mastery and points tracking.
- Progress history and earned-badge display.
- CSV export of recorded assessment responses for research analysis.

### Gamification

- Points for correct answers.
- Additional points when a learner moves to a higher mastery band.
- Achievement badges for implemented milestones, including three consecutive correct answers, reaching a Strong skill band, and completing five passages.

### Reading library

- Book and chapter listing.
- Chapter reading-progress tracking.
- Progress status for books, including not started, in progress, and completed.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| ORM / database access | Flask-SQLAlchemy, SQLAlchemy |
| Local database | SQLite |
| Production database | PostgreSQL (including Supabase-hosted PostgreSQL) |
| Frontend | HTML, CSS, JavaScript |
| Cross-origin requests | Flask-CORS |
| Password hashing | Werkzeug security utilities |
| Environment configuration | python-dotenv |
| Automated tests | pytest |

The backend imports the adaptive logic from `mastery.py` and `sequencing.py`.

---

## Repository Structure

The application expects the frontend directory to be a sibling of the backend directory because Flask serves frontend files using a path relative to the backend application file.

```text
GARCS/
├── backend/
│   ├── app.py
│   ├── mastery.py
│   ├── sequencing.py
│   ├── test_garcs_core.py       # if included in your checkout
│   ├── requirements.txt        # if included in your checkout
│   └── instance/                # local SQLite database is created here
├── frontend/
│   ├── login.html
│   ├── registration.html
│   ├── dashboard.html
│   ├── library.html
│   ├── progress.html
│   ├── ...
├── .env                         # local environment variables; do not commit
└── README.md
```

Keep the actual filenames and any additional project scripts already present in your repository. The structure above describes the expected application layout; it is not a claim that every optional file is included in every branch.

---

## Requirements

- Python 3.10 or later (use the Python version selected for your deployment environment).
- `pip` and `venv`.
- SQLite for local development, or a reachable PostgreSQL database for production.

The backend code imports Flask, Flask-SQLAlchemy, Flask-CORS, SQLAlchemy, python-dotenv, and Werkzeug. PostgreSQL deployments also need a compatible PostgreSQL DBAPI driver, such as `psycopg[binary]`.

If the repository has a maintained `requirements.txt`, install from that file rather than maintaining a separate dependency list:

```bash
python -m pip install -r requirements.txt
```

If no dependency file exists yet, install the packages used by the application and your selected database driver:

```bash
python -m pip install Flask Flask-SQLAlchemy Flask-Cors SQLAlchemy python-dotenv "psycopg[binary]" pytest
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd GARCS
```

### 2. Create and activate a virtual environment

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r backend/requirements.txt
```

If your `requirements.txt` is stored elsewhere, adjust the path. If the repository does not yet contain one, use the package-install command in the Requirements section.

### 4. Configure the database

For local development, leave `DATABASE_URL` unset. The backend is configured to use a SQLite database in its `instance` directory.

For PostgreSQL, create a `.env` file in the directory from which the backend loads environment variables, or export the variable in your shell:

```dotenv
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE
```

Use the connection string supplied by your PostgreSQL provider. Keep credentials private. Do not commit `.env` or paste production database credentials into source code.

### 5. Start the backend

From the backend directory:

```bash
cd backend
python app.py
```

The Flask development server starts using the application's configured host and port. Use it for local development only; use a production WSGI server for deployment.

### 6. Open GARCS

Open the local address printed by Flask in your browser. The application defines frontend pages for login, registration, dashboard, library, and learner progress.

---

## Database Notes

- When `DATABASE_URL` is not configured, GARCS uses SQLite for local development.
- When `DATABASE_URL` is configured, GARCS is intended to connect to PostgreSQL.
- The application calls SQLAlchemy's `db.create_all()` during database initialization. This creates missing tables but **does not perform schema migrations or add new columns to existing tables**.
- Back up your database before changing model definitions or running scripts that modify data.
- Do not run local initialization or import scripts against the production database unless you have verified their behavior and intentionally selected the production connection string.

For schema changes to an existing database, use a deliberate migration process rather than assuming `create_all()` will update existing tables.

---

## Adaptive Model Overview

The adaptive process can be summarized as:

```text
Learner submits an answer
          |
          v
Identify the question's comprehension skill
          |
          v
Update that skill's mastery value
          |
          v
Classify mastery: Weak / Developing / Strong
          |
          v
Choose a skill (weakest-skill priority with exploration)
          |
          v
Map mastery to target question difficulty
          |
          v
Find an unanswered question
          |
          v
Apply fallback if the preferred item is unavailable
          |
          v
Return the next question to the learner
```

The mastery model and sequencing policy are implemented separately:

- `mastery.py` contains skill-state definitions, mastery updates, mastery-band classification, and mastery-to-difficulty mapping.
- `sequencing.py` contains adaptive skill/question selection and difficulty-relaxation behavior.
- `app.py` connects these components to the database, assessment API, progress features, and frontend.

The model is intended to provide interpretable, rule-based personalization. Mastery values are internal estimates used by the application; they should not automatically be interpreted as externally validated reading-comprehension scores or calibrated probabilities of answering correctly.

---

## Main Application Routes

### Frontend pages

| Route | Purpose |
|---|---|
| `/` | Login page |
| `/login` | Login page |
| `/register` | Student registration page |
| `/dashboard` | Learner dashboard |
| `/library` | Reading library |
| `/progress` | Learner progress |

### API routes

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/api/register` | Register a student account |
| `POST` | `/api/login` | Verify login credentials |
| `POST` | `/api/session/start` | Start an assessment session |
| `GET` | `/api/assessment/passages` | Retrieve assessment passages and questions |
| `GET` | `/api/question/next` | Retrieve the next adaptive question |
| `POST` | `/api/answer` | Submit an answer and record its result/mastery update |
| `GET` | `/api/progress/<student_id>` | Retrieve learner mastery, points, badges, and history |
| `GET` | `/api/library/books` | Retrieve library books and learner reading progress |
| `GET` | `/api/library/books/<book_id>` | Retrieve a book and its chapters |
| `GET`, `POST`, `PUT` | `/api/library/books/<book_id>/progress` | Retrieve or update reading progress |
| `GET` | `/api/export` | Export assessment responses as CSV |

The API uses JSON request/response bodies for the relevant endpoints. The login endpoint returns a student identifier; subsequent assessment and progress requests use the relevant student/session identifiers as expected by each endpoint. Consult the route implementation in `backend/app.py` for exact request fields and response schemas before integrating another client.

---

## Running Automated Tests

Run the backend test suite from the backend directory:

```bash
cd backend
python -m pytest -v
```

To run the core GARCS tests specifically:

```bash
python -m pytest test_garcs_core.py -v
```

Tests should use an isolated test database and must not point to the live production database. Review the test configuration before running tests if environment variables are loaded from a local `.env` file.

---

## Data Export

The application provides:

```text
GET /api/export
```

The endpoint returns a CSV export of recorded assessment responses. The export includes learner/question identifiers, skill and difficulty labels, correctness, response-time and reread fields, mastery before and after the response, and timestamp information.

Treat exported learner records as confidential research data. Remove direct identifiers before sharing or publishing results, and follow the study's applicable consent, privacy, and data-retention requirements.

---

## Deployment

GARCS can use a PostgreSQL connection through `DATABASE_URL`, which is suitable for a hosted PostgreSQL service such as Supabase. A typical deployment requires:

1. A hosted PostgreSQL database.
2. The production `DATABASE_URL` configured as a private environment variable in the hosting provider.
3. All Python dependencies installed during the build.
4. A production WSGI server (for example, Gunicorn) configured to load the Flask `app` object from the backend application module.
5. The frontend directory included in the deployed repository at the expected relative path.

Do not use Flask's `debug=True` development server as the public production server. Configure the hosting provider's start command and working directory to match the repository layout. Confirm that the production database is selected before deploying any data-import or schema-initialization operation.

---

## Security and Privacy Reminders

- Never commit `.env`, database credentials, API keys, or private exports.
- Use HTTPS in production.
- Restrict access to database and research exports.
- Do not use real learner data in automated tests unless it has been appropriately anonymized and approved for that purpose.
- The current API design passes student identifiers in requests; this should not be treated as a substitute for robust authorization. Before production use with sensitive learner records, ensure that every endpoint verifies that the requester is authorized to access the referenced student data.
- Follow applicable institutional ethics requirements and Philippine data-protection requirements when collecting, storing, exporting, or sharing learner information.

---

## Project Scope

GARCS focuses on literal, inferential, and critical reading comprehension. It provides adaptive question sequencing, learner progress tracking, a reading library, and gamification features. Its current mastery mechanism is rule-based and PFA-inspired; it is not a trained machine-learning system. The application supports reading practice and records learner interactions, but the existence of adaptive behavior or increased points does not by itself establish improved reading comprehension or educational effectiveness.

---

## Contributing / Development Workflow

1. Create a feature branch before making changes.
2. Keep adaptive logic in `mastery.py` and `sequencing.py` rather than duplicating it in frontend code.
3. Add or update automated tests when changing mastery, sequencing, API, or gamification behavior.
4. Run the test suite before merging or deploying.
5. Review database changes and back up production data before applying them.
6. Keep credentials, learner information, and generated research exports out of Git.

---

## License

No license information was provided with this project documentation. Unless a license is added to the repository, all rights remain with the respective copyright holders. Add a `LICENSE` file before distributing or reusing the source code under an open-source license.
