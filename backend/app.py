"""
app_phase3.py -- GARCS Phase 3: API layer.

Builds directly on the Phase 1 data model (Student/Passage/Question/Response/
StudentSkillState) and wires it to the Phase 2 rule-based engine
(mastery.py + sequencing.py) via the routes specified in the roadmap's
Phase 3 table:

    /api/register          POST  (extended with password hashing)
    /api/login             POST  (new)
    /api/session/start     POST  (new)
    /api/question/next     GET   (new)
    /api/answer            POST  (new)
    /api/progress/<id>     GET   (new)
    /api/export            GET   (extended for the new Response schema)

/api/predict and /api/passage/<grade> are intentionally NOT present here --
per the roadmap, they're deprecated from the live MVP path.

HOW TO USE THIS FILE
---------------------------------------------------------------------------
1. Put this file, mastery.py, sequencing.py, and seed.py in the same
   backend/ folder, and rename this file to app.py (replacing your Phase 1
   app.py -- the models are identical, this just adds the routes).
2. If you already ran the Phase 1 version and have a database.db with the
   OLD schema (Student without a real password_hash usage, or missing
   rows), delete database.db and re-run seed.py -- SQLite's db.create_all()
   only creates missing tables, it will NOT add new columns to a table
   that already exists on disk.
3. Run `python seed.py` once to populate Passage/Question.
4. Run `python app.py` and hit the endpoints below.

DESIGN DECISIONS WORTH KNOWING ABOUT
---------------------------------------------------------------------------
- Password hashing uses werkzeug.security (generate_password_hash /
  check_password_hash) instead of the roadmap's suggested Flask-Bcrypt.
  Werkzeug ships as a Flask dependency already, so this avoids adding a
  new pip package for a thesis MVP. Swap to Flask-Bcrypt later if you
  want, the call sites are isolated to register()/login().
- No server-side session/cookie state. /api/login verifies credentials
  and returns student_id, but every subsequent call (question/next,
  answer, progress) takes student_id explicitly as a request field/query
  param, matching how /api/register already returns student_id today.
  This sidesteps Flask-CORS + cross-origin cookie configuration
  (supports_credentials=True server-side, credentials:'include' on every
  fetch client-side) which is a common source of silent bugs for a
  frontend/backend served from different ports during local dev. If your
  panel or adviser wants real session-cookie auth, that's a clean Phase 4
  follow-up, not a Phase 3 blocker.
- "Answered questions" = every Question this student has ever answered
  (queried from Response), not scoped to a single login session, since
  Chapter 3.6.4's schema has no Session/attempt-session table. This means
  a student won't be re-served the same question across days, which is
  the more defensible behavior for a mastery-tracking system anyway.
- Points are awarded here (fixed +10 per correct answer, +25 bonus for
  moving up a mastery band) because the roadmap's Phase 3 table itself
  says /api/answer should "award points/badges." Full badge RULES (e.g.
  "3 correct in a row") are still Phase 5 -- /api/progress/<id> already
  returns a `badges` field, just empty for now, so Phase 5 only needs to
  populate it, not change the response shape.
"""

import csv
import io
# from operator import or_
from sqlalchemy import inspect, or_, text

import random
from datetime import datetime

from flask import Flask, request, jsonify, send_file, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

from mastery import (
    SkillState,
    SKILLS,
    classify_band,
    target_difficulty,
    update_mastery,
)
from sequencing import pick_next_question, relax_difficulty

# =====================================
# APP SETUP
# =====================================
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path="",
    instance_path=str(BASE_DIR / "instance"),
    instance_relative_config=True,
)
DATABASE_FILE = Path(app.instance_path) / "database.db"
DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_FILE}"

db = SQLAlchemy(app)
from pathlib import Path

# print("=" * 60)
# print("INSTANCE:", app.instance_path)
# print("DATABASE:", Path(app.instance_path) / "database.db")
# print("=" * 60)

CORS(app)


# =====================================
# DATABASE MODELS  (Chapter 3.6.4 schema — unchanged from Phase 1)
# =====================================
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    student_number = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    grade = db.Column(db.Integer)
    password_hash = db.Column(db.String(200))


class Passage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text)
    grade_band = db.Column(db.Integer)

class LibraryBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200))
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    grade_band = db.Column(db.Integer)
    cover_image = db.Column(db.String(500))
    is_featured = db.Column(db.Boolean, default=False)

    chapters = db.relationship(
        "LibraryChapter",
        backref="book",
        lazy=True,
        cascade="all, delete-orphan"
    )

class LibraryChapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(
        db.Integer,
        db.ForeignKey("library_book.id"),
        nullable=False
    )

    chapter_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    passage_id = db.Column(
        db.Integer,
        db.ForeignKey("passage.id"),
        nullable=False
    )

    chapter_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

class ReadingProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    passage_id = db.Column(
        db.Integer,
        db.ForeignKey("passage.id"),
        nullable=True
    )

    book_id = db.Column(
        db.Integer,
        db.ForeignKey("library_book.id"),
        nullable=False
    )

    chapter_id = db.Column(
        db.Integer,
        db.ForeignKey("library_chapter.id"),
        nullable=True
    )
    current_chapter = db.Column(db.Integer, default=1)
    completed_chapters = db.Column(db.Integer, default=0)
    progress_percent = db.Column(db.Float, default=0)
    reading_position = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passage_id = db.Column(db.Integer, db.ForeignKey('passage.id'))
    prompt = db.Column(db.Text)
    choices = db.Column(db.JSON)
    correct_index = db.Column(db.Integer)
    skill_tag = db.Column(db.String(20))
    difficulty = db.Column(db.String(10))


class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    session_id = db.Column(
        db.Integer,
        db.ForeignKey('assessment_session.id'),
        nullable=True
    )
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    skill_tag = db.Column(db.String(20))
    difficulty = db.Column(db.String(10))
    is_correct = db.Column(db.Boolean)
    response_time_sec = db.Column(db.Float)
    reread_count = db.Column(db.Integer, default=0)
    mastery_before = db.Column(db.Float)
    mastery_after = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class StudentSkillState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    skill_tag = db.Column(db.String(20))
    mastery = db.Column(db.Float, default=0.50)
    points = db.Column(db.Integer, default=0)

class AssessmentSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer,
        db.ForeignKey('student.id'),
        nullable=False
    )
    started_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    completed_at = db.Column(db.DateTime, nullable=True)
    question_count = db.Column(db.Integer, default=0)


# with app.app_context():
#     db.create_all()
with app.app_context():
    db.create_all()

    progress_columns = {
        column["name"]
        for column in inspect(db.engine).get_columns("reading_progress")
    }
    progress_column_definitions = {
        "book_id": "INTEGER",
        "chapter_id": "INTEGER",
        "progress_percent": "FLOAT DEFAULT 0",
        "reading_position": "INTEGER DEFAULT 0",
        "updated_at": "DATETIME",
    }
    with db.engine.begin() as connection:
        for column_name, column_definition in progress_column_definitions.items():
            if column_name not in progress_columns:
                connection.execute(text(
                    f"ALTER TABLE reading_progress ADD COLUMN "
                    f"{column_name} {column_definition}"
                ))

    print("DATABASE URI:", app.config["SQLALCHEMY_DATABASE_URI"])
    print("DATABASE ENGINE URL:", db.engine.url)
    print("DATABASE FILE:", db.engine.url.database)


# =====================================
# GAMIFICATION / BADGE HELPERS
# =====================================

POINTS_CORRECT = 10
POINTS_BAND_UP = 25
BAND_RANK = {
    "Weak": 0,
    "Developing": 1,
    "Strong": 2
}


# -------------------------------------------------
# BADGE DEFINITIONS
# -------------------------------------------------
BADGE_RULES = {
    "three_in_a_row": {
        "name": "3 Correct in a Row",
        "icon": "local_fire_department",
    },
    "first_strong": {
        "name": "First Strong Skill",
        "icon": "workspace_premium",
    },
    "five_passages": {
        "name": "5 Passages Completed",
        "icon": "auto_stories",
    },
}


# -------------------------------------------------
# BADGE RULE: 3 CORRECT IN A ROW
# -------------------------------------------------
def has_three_correct_in_a_row(student_id):
    """
    Returns True if the student's three most recent
    recorded responses were all correct.
    """

    recent_responses = (
        Response.query
        .filter_by(student_id=student_id)
        .order_by(Response.timestamp.desc(), Response.id.desc())
        .limit(3)
        .all()
    )

    if len(recent_responses) < 3:
        return False

    return all(response.is_correct for response in recent_responses)


# -------------------------------------------------
# BADGE RULE: FIRST STRONG SKILL
# -------------------------------------------------
def has_first_strong_skill(student_id):
    """
    Returns True once at least one reading skill has
    reached the Strong mastery band.
    """

    strong_skill = (
        StudentSkillState.query
        .filter(
            StudentSkillState.student_id == student_id,
            StudentSkillState.mastery >= 0.70
        )
        .first()
    )

    return strong_skill is not None


# -------------------------------------------------
# BADGE RULE: 5 PASSAGES COMPLETED
# -------------------------------------------------
def get_completed_passage_count(student_id):
    """
    A passage is considered completed only when the
    student has answered every question belonging to
    that passage.

    This uses all historical responses for the student,
    not just the current assessment session.
    """

    passage_rows = (
        db.session.query(Passage.id)
        .join(
            Question,
            Question.passage_id == Passage.id
        )
        .distinct()
        .all()
    )

    completed_count = 0

    for row in passage_rows:
        passage_id = row[0]

        # All questions belonging to this passage
        question_ids = {
            question.id
            for question in Question.query.filter_by(
                passage_id=passage_id
            ).all()
        }

        if not question_ids:
            continue

        # Questions this student has answered
        answered_ids = {
            response.question_id
            for response in Response.query.filter(
                Response.student_id == student_id,
                Response.question_id.in_(question_ids)
            ).all()
        }

        # Passage is complete only if every question
        # belonging to it has been answered.
        if question_ids.issubset(answered_ids):
            completed_count += 1

    return completed_count


def has_five_completed_passages(student_id):
    """
    Returns True once the student has completely answered
    all questions from at least five different passages.
    """

    return get_completed_passage_count(student_id) >= 5


# -------------------------------------------------
# GET ALL BADGES EARNED BY A STUDENT
# -------------------------------------------------
def get_student_badges(student_id):
    """
    Calculates all badges currently earned by the student.

    No badge database table is required for this MVP.
    """

    badges = []

    if has_three_correct_in_a_row(student_id):
        badges.append({
            "id": "three_in_a_row",
            "name": BADGE_RULES["three_in_a_row"]["name"],
            "icon": BADGE_RULES["three_in_a_row"]["icon"],
        })

    if has_first_strong_skill(student_id):
        badges.append({
            "id": "first_strong",
            "name": BADGE_RULES["first_strong"]["name"],
            "icon": BADGE_RULES["first_strong"]["icon"],
        })

    if has_five_completed_passages(student_id):
        badges.append({
            "id": "five_passages",
            "name": BADGE_RULES["five_passages"]["name"],
            "icon": BADGE_RULES["five_passages"]["icon"],
        })

    return badges


# -------------------------------------------------
# FIND NEWLY EARNED BADGES
# -------------------------------------------------
def get_new_badges(previous_badges, current_badges):
    """
    Compares badge lists before and after an answer so
    /api/answer can tell the frontend which badge was
    newly unlocked.
    """

    previous_ids = {
        badge["id"]
        for badge in previous_badges
    }

    return [
        badge
        for badge in current_badges
        if badge["id"] not in previous_ids
    ]


# =====================================
# SERVE FRONTEND
# =====================================
@app.route("/")
def home():
    return send_file(BASE_DIR.parent / "frontend" / "login.html")


@app.route("/login")
def login_page():
    return send_file(BASE_DIR.parent / "frontend" / "login.html")


@app.route("/dashboard")
def dashboard_page():
    return send_file(BASE_DIR.parent / "frontend" / "dashboard.html")


@app.route("/library")
def library():
    return send_file(BASE_DIR.parent / "frontend" / "library.html")


@app.route("/progress")
def progress_page():
    return send_file(BASE_DIR.parent / "frontend" / "progress.html")

@app.route("/register")
def register_page():
    return send_file(BASE_DIR.parent / "frontend" / "registration.html")


# =====================================
# AUTH
# =====================================
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json or {}

    print("=== REGISTER DEBUG ===")
    print("DB URL:", db.engine.url)
    print("DB FILE:", db.engine.url.database)
    print("INSTANCE:", app.instance_path)
    print("REQUEST DATA:", data)

    username = data.get("username", "").strip()
    student_number = data.get("student_number", "").strip()
    email = data.get("email", "").strip()
    grade = data.get("grade")
    password = data.get("password", "")

    if not username or not student_number or grade is None or not password:
        return jsonify({
            "error": "Missing required registration fields"
        }), 400

    if Student.query.filter_by(username=username).first():
        return jsonify({"error": "username_already_exists"}), 409

    if Student.query.filter_by(student_number=student_number).first():
        return jsonify({"error": "student_number_already_exists"}), 409

    if Student.query.filter_by(email=email).first():
        return jsonify({"error": "email_already_exists"}), 409

    student = Student(
        username=username,
        student_number=student_number,
        email=email or None,
        grade=int(grade),
        password_hash=generate_password_hash(password)
    )

    db.session.add(student)

    print("ABOUT TO COMMIT")
    print("DB URL:", db.engine.url)
    print("DB FILE:", db.engine.url.database)

    try:
        db.session.commit()
        print("COMMIT SUCCESS")
    except Exception as e:
        print("COMMIT ERROR:", repr(e))
        db.session.rollback()
        raise

    return jsonify({
        "message": "registration_successful",
        "student_id": student.id
    }), 201



@app.route('/api/login', methods=['POST'])
def login():
    data = request.json or {}

    identifier = data.get("email") or data.get("username") or data.get("student_number")
    password = data.get("password", "")

    student = Student.query.filter(
        or_(
            Student.email == identifier,
            Student.student_number == identifier,
            Student.username == identifier
        )
    ).first()

    if not student:
        return jsonify({"error": "student_not_found"}), 404

    if (
        not student.password_hash
        or not check_password_hash(student.password_hash, password)
    ):
        return jsonify({"error": "invalid credentials"}), 401

    return jsonify({
        "student_id": student.id,
        "name": student.username,
        "grade": student.grade
    })

# =====================================
# SESSION START -- ensures skill states exist (idempotent, safe to call every login)
# =====================================
@app.route('/api/session/start', methods=['POST'])
def session_start():
    data = request.json or {}
    student_id = data.get("student_id")

    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "student not found"}), 404

    # Make sure all skill states exist.
    existing = {
        s.skill_tag
        for s in StudentSkillState.query.filter_by(
            student_id=student_id
        ).all()
    }

    for skill in SKILLS:
        if skill not in existing:
            db.session.add(
                StudentSkillState(
                    student_id=student_id,
                    skill_tag=skill
                )
            )

    # Create a NEW assessment session.
    assessment = AssessmentSession(
        student_id=student_id,
        question_count=0
    )

    db.session.add(assessment)
    db.session.commit()

    return jsonify({
        "student_id": int(student_id),
        "session_id": assessment.id,
        "question_limit": 10,
        "ready": True
    })


# =====================================
# ENGINE HELPERS -- bridge DB rows <-> mastery.py's plain SkillState dataclass
# =====================================
def _load_states(student_id):
    """Build {skill_tag: SkillState} from DB rows for sequencing.py to consume."""
    states = {}
    for row in StudentSkillState.query.filter_by(student_id=student_id).all():
        attempts = Response.query.filter_by(student_id=student_id, skill_tag=row.skill_tag).count()
        correct = Response.query.filter_by(student_id=student_id, skill_tag=row.skill_tag, is_correct=True).count()
        states[row.skill_tag] = SkillState(
            student_id=student_id,
            skill_tag=row.skill_tag,
            mastery=row.mastery,
            attempts=attempts,
            correct_count=correct,
        )
    return states


def _fetch_candidates(skill_tag, difficulty, passage_id=None):
    query = Question.query.filter_by(
        skill_tag=skill_tag,
        difficulty=difficulty
    )

    if passage_id is not None:
        query = query.filter_by(passage_id=passage_id)

    return query.all()


def _serialize_library_book(book):
    chapters = sorted(book.chapters, key=lambda chapter: chapter.chapter_number)
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "description": book.description,
        "category": book.category,
        "grade_band": book.grade_band,
        "cover_image": book.cover_image,
        "is_featured": book.is_featured,
        "chapters": [
            {
                "id": chapter.id,
                "book_id": chapter.book_id,
                "chapter_number": chapter.chapter_number,
                "title": chapter.title,
                "content": chapter.content,
            }
            for chapter in chapters
        ],
    }


def _serialize_reading_progress(progress):
    if not progress:
        return None

    return {
        "id": progress.id,
        "student_id": progress.student_id,
        "book_id": progress.book_id,
        "chapter_id": progress.chapter_id,
        "current_chapter": progress.current_chapter,
        "completed_chapters": progress.completed_chapters or 0,
        "progress_percent": progress.progress_percent or 0,
        "reading_position": progress.reading_position or 0,
        "completed": bool(progress.completed),
        "updated_at": progress.updated_at.isoformat() if progress.updated_at else None,
    }


@app.route('/api/library/books/<int:book_id>')
def get_library_book(book_id):
    book = LibraryBook.query.get(book_id)
    if not book:
        return jsonify({"error": "book not found"}), 404

    return jsonify(_serialize_library_book(book))


@app.route('/api/library/books/<int:book_id>/progress', methods=['GET', 'POST', 'PUT'])
def library_book_progress(book_id):
    book = LibraryBook.query.get(book_id)
    if not book:
        return jsonify({"error": "book not found"}), 404

    data = request.get_json(silent=True) or {}
    student_id = data.get("student_id") if request.method != "GET" else request.args.get("student_id", type=int)
    try:
        student_id = int(student_id)
    except (TypeError, ValueError):
        return jsonify({"error": "valid student_id required"}), 400

    if not Student.query.get(student_id):
        return jsonify({"error": "student not found"}), 404

    progress = ReadingProgress.query.filter_by(
        student_id=student_id,
        book_id=book_id,
    ).first()

    if request.method == 'GET':
        return jsonify({"progress": _serialize_reading_progress(progress)})

    chapter_id = data.get("chapter_id")
    current_chapter = data.get("current_chapter")
    try:
        chapter_id = int(chapter_id)
        current_chapter = int(current_chapter)
    except (TypeError, ValueError):
        return jsonify({"error": "chapter_id and current_chapter are required"}), 400

    chapter = LibraryChapter.query.filter_by(id=chapter_id, book_id=book_id).first()
    if not chapter or chapter.chapter_number != current_chapter:
        return jsonify({"error": "chapter does not belong to book"}), 400

    try:
        progress_percent = float(data.get("progress_percent", 0))
        reading_position = int(data.get("reading_position", 0))
        completed_chapters = int(data.get("completed_chapters", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "progress values must be numeric"}), 400

    if not 0 <= progress_percent <= 100 or reading_position < 0 or completed_chapters < 0:
        return jsonify({"error": "invalid progress values"}), 400

    completed_chapters = min(completed_chapters, len(book.chapters))
    if not progress:
        legacy_passage = Passage.query.order_by(Passage.id).first()
        progress = ReadingProgress(
            student_id=student_id,
            book_id=book_id,
            passage_id=legacy_passage.id if legacy_passage else None,
        )
        db.session.add(progress)

    progress.chapter_id = chapter.id
    progress.current_chapter = chapter.chapter_number
    progress.completed_chapters = completed_chapters
    progress.progress_percent = progress_percent
    progress.reading_position = reading_position
    progress.completed = bool(data.get("completed", False))
    progress.updated_at = datetime.utcnow()

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "unable to save reading progress"}), 500

    return jsonify({"progress": _serialize_reading_progress(progress)}), 200


@app.route('/api/library/books')
def get_library_books():
    student_id = request.args.get("student_id", type=int)

    if not student_id:
        return jsonify({
            "error": "student_id required"
        }), 400

    student = Student.query.get(student_id)

    if not student:
        return jsonify({
            "error": "student not found"
        }), 404

    books = LibraryBook.query.order_by(LibraryBook.id).all()

    result = []

    for book in books:

        chapter_count = LibraryChapter.query.filter_by(
            book_id=book.id
        ).count()

        progress = ReadingProgress.query.filter_by(
            student_id=student_id,
            book_id=book.id
        ).first()

        completed_chapters = (
            progress.completed_chapters
            if progress else 0
        )

        if chapter_count > 0:
            progress_percent = round(
                completed_chapters / chapter_count * 100
            )
        else:
            progress_percent = 0

        if progress_percent == 0:
            completion_state = "Not Started"
        elif progress_percent >= 100:
            completion_state = "Completed"
        else:
            completion_state = "In Progress"

        grade_labels = {
            1: "Grades 3–5",
            2: "Grades 6–8",
            3: "Grades 9–12"
        }

        result.append({
            "id": book.id,
            "title": book.title,
            "description": book.description,
            "category": book.category,
            "grade_band": grade_labels.get(
                book.grade_band,
                "All Grades"
            ),
            "chapter_count": chapter_count,
            "completed_chapters": completed_chapters,
            "progress_percent": progress_percent,
            "completion_state": completion_state,
            "cover_image": book.cover_image,
            "is_featured": book.is_featured
        })

    return jsonify(result)

@app.route('/api/assessment/passages')
def assessment_passages():
    passages = []
    for passage in Passage.query.order_by(Passage.id).all():
        questions = []
        for question in Question.query.filter_by(passage_id=passage.id).order_by(Question.id).all():
            questions.append({
                "id": question.id,
                "type": {
                    "literal": "literal",
                    "inferential": "inferential",
                    "critical": "main_idea",
                }.get(question.skill_tag, question.skill_tag),
                "q": question.prompt,
                "choices": question.choices or [],
                "correct": question.correct_index,
                "skill_tag": question.skill_tag,
                "difficulty": question.difficulty,
            })

        grade_band = passage.grade_band or 1
        grades = {1: [3, 4, 5], 2: [6, 7, 8], 3: [9, 10, 11, 12]}.get(grade_band, [grade_band * 3])
        difficulty = {1: 0, 2: 1, 3: 2}.get(grade_band, 1)
        word_count = len((passage.body or "").split())
        read_minutes = f"{max(1, word_count // 120)}-{max(2, word_count // 120 + 1)}"

        passages.append({
            "id": passage.id,
            "title": passage.title,
            "genre": "Reading",
            "genreEmoji": "📖",
            "wordCount": max(word_count, 120),
            "readMinutes": read_minutes,
            "grades": grades,
            "difficulty": difficulty,
            "text": passage.body or "",
            "questions": questions,
        })

    return jsonify(passages)


# =====================================
# ADAPTIVE QUESTION SELECTION
# ONE PASSAGE AT A TIME
# =====================================
@app.route('/api/question/next')
# =====================================
# ADAPTIVE QUESTION SELECTION
# ONE PASSAGE AT A TIME
# WITH UNSEEN-PASSAGE PRIORITY
# =====================================
@app.route('/api/question/next')
def question_next():
    student_id = request.args.get("student_id", type=int)
    session_id = request.args.get("session_id", type=int)

    # -------------------------------------------------
    # VALIDATE STUDENT
    # -------------------------------------------------
    if not student_id or not Student.query.get(student_id):
        return jsonify({
            "error": "valid student_id required"
        }), 400

    # -------------------------------------------------
    # VALIDATE SESSION
    # -------------------------------------------------
    if not session_id:
        return jsonify({
            "error": "valid session_id required"
        }), 400

    assessment = AssessmentSession.query.filter_by(
        id=session_id,
        student_id=student_id
    ).first()

    if not assessment:
        return jsonify({
            "error": "assessment session not found"
        }), 404

    # -------------------------------------------------
    # HARD LIMIT: 10 QUESTIONS PER ASSESSMENT
    # -------------------------------------------------
    if assessment.question_count >= 10:

        if not assessment.completed_at:
            assessment.completed_at = datetime.utcnow()
            db.session.commit()

        return jsonify({
            "done": True,
            "message": "Assessment complete. You answered 10 questions.",
            "question_count": assessment.question_count,
            "question_limit": 10
        })

    # -------------------------------------------------
    # LOAD CURRENT MASTERY STATES
    # -------------------------------------------------
    states = _load_states(student_id)

    if not states:
        return jsonify({
            "error": "skill states not initialized — call /api/session/start first"
        }), 400

    # -------------------------------------------------
    # QUESTIONS ALREADY ANSWERED IN THIS ASSESSMENT
    #
    # These are excluded so the same question cannot be
    # served twice during the current assessment.
    # -------------------------------------------------
    answered_ids = [
        r.question_id
        for r in Response.query.filter_by(
            student_id=student_id,
            session_id=session_id
        ).all()
    ]

    answered_set = set(answered_ids)

    # -------------------------------------------------
    # FIND PASSAGES THE STUDENT HAS ALREADY ENCOUNTERED
    #
    # A passage is considered "encountered" if the student
    # has answered at least one question belonging to it
    # in ANY previous assessment.
    #
    # This is intentionally NOT limited to the current
    # session.
    # -------------------------------------------------
    seen_passage_rows = (
        db.session.query(Question.passage_id)
        .join(
            Response,
            Response.question_id == Question.id
        )
        .filter(
            Response.student_id == student_id,
            Question.passage_id.isnot(None)
        )
        .distinct()
        .all()
    )

    seen_passage_ids = {
        row[0]
        for row in seen_passage_rows
        if row[0] is not None
    }

    # -------------------------------------------------
    # GET ALL PASSAGES THAT HAVE QUESTIONS
    # -------------------------------------------------
    all_passage_ids = {
        row[0]
        for row in (
            db.session.query(Question.passage_id)
            .filter(Question.passage_id.isnot(None))
            .distinct()
            .all()
        )
        if row[0] is not None
    }

    # -------------------------------------------------
    # DETERMINE WHETHER THERE ARE STILL UNSEEN PASSAGES
    #
    # If there are unseen passages, they MUST be preferred.
    #
    # If every passage has already been encountered, the
    # passage pool resets and previously seen passages may
    # be used again.
    # -------------------------------------------------
    unseen_passage_ids = all_passage_ids - seen_passage_ids

    passage_pool_has_unseen = bool(unseen_passage_ids)

    # -------------------------------------------------
    # CURRENT PASSAGE
    #
    # The current passage is determined from the most
    # recently answered question in this assessment.
    #
    # This allows the frontend to keep displaying the same
    # passage while its unanswered questions remain.
    # -------------------------------------------------
    latest_response = (
        Response.query
        .filter_by(
            student_id=student_id,
            session_id=session_id
        )
        .order_by(Response.id.desc())
        .first()
    )

    current_passage_id = None

    if latest_response:
        latest_question = Question.query.get(
            latest_response.question_id
        )

        if latest_question:
            current_passage_id = latest_question.passage_id

    # -------------------------------------------------
    # HELPER: FETCH QUESTIONS FOR A SPECIFIC PASSAGE
    # -------------------------------------------------
    def fetch_current_passage(skill_tag, difficulty):
        return _fetch_candidates(
            skill_tag,
            difficulty,
            current_passage_id
        )

    # -------------------------------------------------
    # HELPER: FETCH ONLY QUESTIONS FROM UNSEEN PASSAGES
    #
    # This is the important part that prevents the system
    # from repeatedly selecting the same few passages.
    # -------------------------------------------------
    def fetch_unseen_candidates(skill_tag, difficulty):
        candidates = _fetch_candidates(
            skill_tag,
            difficulty
        )

        return [
            q for q in candidates
            if (
                q.id not in answered_set
                and q.passage_id in unseen_passage_ids
            )
        ]

    # -------------------------------------------------
    # HELPER: FETCH ANY UNANSWERED QUESTION FROM AN
    # UNSEEN PASSAGE
    # -------------------------------------------------
    def fetch_any_unseen_question():
        if not unseen_passage_ids:
            return None

        candidates = (
            Question.query
            .filter(
                Question.passage_id.in_(unseen_passage_ids),
                ~Question.id.in_(answered_ids or [-1])
            )
            .all()
        )

        if candidates:
            return random.choice(candidates)

        return None

    # -------------------------------------------------
    # HELPER: FETCH ANY UNANSWERED QUESTION
    #
    # Used only after the unseen passage pool has been
    # exhausted.
    # -------------------------------------------------
    def fetch_any_unanswered_question():
        candidates = (
            Question.query
            .filter(
                ~Question.id.in_(answered_ids or [-1])
            )
            .all()
        )

        if candidates:
            return random.choice(candidates)

        return None

    # -------------------------------------------------
    # SELECT QUESTION
    # -------------------------------------------------
    question = None
    skill_tag = None
    difficulty = None
    new_passage = False

    # =================================================
    # CASE 1:
    # THERE IS A CURRENT PASSAGE
    # =================================================
    if current_passage_id is not None:

        # -------------------------------------------------
        # FIRST: CONTINUE CURRENT PASSAGE
        #
        # IMPORTANT:
        # Once a passage has started, the student stays
        # with that passage until there are no unanswered
        # questions left in it.
        # -------------------------------------------------
        question, skill_tag, difficulty = pick_next_question(
            states,
            fetch_current_passage,
            answered_ids
        )

        # -------------------------------------------------
        # FALLBACK 1:
        # RELAX DIFFICULTY BUT STAY IN CURRENT PASSAGE
        # -------------------------------------------------
        if question is None:

            tried = {difficulty}
            relaxed = relax_difficulty(difficulty)

            while (
                question is None
                and relaxed
                and relaxed not in tried
            ):
                tried.add(relaxed)

                candidates = [
                    q
                    for q in _fetch_candidates(
                        skill_tag,
                        relaxed,
                        current_passage_id
                    )
                    if q.id not in answered_set
                ]

                if candidates:
                    question = random.choice(candidates)
                    difficulty = relaxed
                else:
                    relaxed = relax_difficulty(relaxed)

        # -------------------------------------------------
        # FALLBACK 2:
        # ANY UNANSWERED QUESTION FROM CURRENT PASSAGE
        #
        # We still do NOT leave the passage.
        # -------------------------------------------------
        if question is None:

            remaining = (
                Question.query
                .filter(
                    Question.passage_id == current_passage_id,
                    ~Question.id.in_(answered_ids or [-1])
                )
                .all()
            )

            if remaining:
                question = random.choice(remaining)
                skill_tag = question.skill_tag
                difficulty = question.difficulty

        # -------------------------------------------------
        # CURRENT PASSAGE IS EXHAUSTED
        #
        # Only now may the system select another passage.
        # -------------------------------------------------
        if question is None:

            new_passage = True

            # =============================================
            # PRIORITY 1:
            # SELECT FROM AN UNSEEN PASSAGE
            # =============================================
            if passage_pool_has_unseen:

                # -----------------------------------------
                # Adaptive selection:
                # weakest skill + target difficulty,
                # but restricted to unseen passages.
                # -----------------------------------------
                question, skill_tag, difficulty = pick_next_question(
                    states,
                    fetch_unseen_candidates,
                    answered_ids
                )

                # -----------------------------------------
                # FALLBACK 3:
                # RELAX DIFFICULTY WHILE STAYING WITHIN
                # UNSEEN PASSAGES
                # -----------------------------------------
                if question is None:

                    tried = {difficulty}
                    relaxed = relax_difficulty(difficulty)

                    while (
                        question is None
                        and relaxed
                        and relaxed not in tried
                    ):
                        tried.add(relaxed)

                        candidates = [
                            q
                            for q in _fetch_candidates(
                                skill_tag,
                                relaxed
                            )
                            if (
                                q.id not in answered_set
                                and q.passage_id in unseen_passage_ids
                            )
                        ]

                        if candidates:
                            question = random.choice(candidates)
                            difficulty = relaxed
                        else:
                            relaxed = relax_difficulty(relaxed)

                # -----------------------------------------
                # FALLBACK 4:
                # ANY UNANSWERED QUESTION FROM AN
                # UNSEEN PASSAGE
                # -----------------------------------------
                if question is None:

                    question = fetch_any_unseen_question()

                    if question:
                        skill_tag = question.skill_tag
                        difficulty = question.difficulty

            # =============================================
            # PRIORITY 2:
            # ALL PASSAGES HAVE BEEN SEEN
            #
            # Reset the passage pool.
            # Previously encountered passages can now
            # appear again, but questions already answered
            # in THIS assessment remain excluded.
            # =============================================
            if question is None:

                question, skill_tag, difficulty = pick_next_question(
                    states,
                    _fetch_candidates,
                    answered_ids
                )

                # -----------------------------------------
                # FALLBACK 5:
                # GLOBAL DIFFICULTY RELAXATION
                # -----------------------------------------
                if question is None:

                    tried = {difficulty}
                    relaxed = relax_difficulty(difficulty)

                    while (
                        question is None
                        and relaxed
                        and relaxed not in tried
                    ):
                        tried.add(relaxed)

                        candidates = [
                            q
                            for q in _fetch_candidates(
                                skill_tag,
                                relaxed
                            )
                            if q.id not in answered_set
                        ]

                        if candidates:
                            question = random.choice(candidates)
                            difficulty = relaxed
                        else:
                            relaxed = relax_difficulty(relaxed)

                # -----------------------------------------
                # FALLBACK 6:
                # ANY UNANSWERED QUESTION
                # -----------------------------------------
                if question is None:

                    question = fetch_any_unanswered_question()

                    if question:
                        skill_tag = question.skill_tag
                        difficulty = question.difficulty

    # =================================================
    # CASE 2:
    # FIRST QUESTION OF THE ASSESSMENT
    # =================================================
    else:

        new_passage = True

        # -------------------------------------------------
        # PRIORITY 1:
        # IF UNSEEN PASSAGES EXIST, THE FIRST QUESTION
        # MUST COME FROM AN UNSEEN PASSAGE.
        # -------------------------------------------------
        if passage_pool_has_unseen:

            question, skill_tag, difficulty = pick_next_question(
                states,
                fetch_unseen_candidates,
                answered_ids
            )

            # -------------------------------------------------
            # FALLBACK 1:
            # RELAX DIFFICULTY WITHIN UNSEEN PASSAGES
            # -------------------------------------------------
            if question is None:

                tried = {difficulty}
                relaxed = relax_difficulty(difficulty)

                while (
                    question is None
                    and relaxed
                    and relaxed not in tried
                ):
                    tried.add(relaxed)

                    candidates = [
                        q
                        for q in _fetch_candidates(
                            skill_tag,
                            relaxed
                        )
                        if (
                            q.id not in answered_set
                            and q.passage_id in unseen_passage_ids
                        )
                    ]

                    if candidates:
                        question = random.choice(candidates)
                        difficulty = relaxed
                    else:
                        relaxed = relax_difficulty(relaxed)

            # -------------------------------------------------
            # FALLBACK 2:
            # ANY QUESTION FROM AN UNSEEN PASSAGE
            # -------------------------------------------------
            if question is None:

                question = fetch_any_unseen_question()

                if question:
                    skill_tag = question.skill_tag
                    difficulty = question.difficulty

        # -------------------------------------------------
        # PRIORITY 2:
        # ALL PASSAGES HAVE ALREADY BEEN ENCOUNTERED
        #
        # Start using the passage pool again.
        # -------------------------------------------------
        if question is None:

            question, skill_tag, difficulty = pick_next_question(
                states,
                _fetch_candidates,
                answered_ids
            )

            # -------------------------------------------------
            # FALLBACK 3:
            # RELAX DIFFICULTY
            # -------------------------------------------------
            if question is None:

                tried = {difficulty}
                relaxed = relax_difficulty(difficulty)

                while (
                    question is None
                    and relaxed
                    and relaxed not in tried
                ):
                    tried.add(relaxed)

                    candidates = [
                        q
                        for q in _fetch_candidates(
                            skill_tag,
                            relaxed
                        )
                        if q.id not in answered_set
                    ]

                    if candidates:
                        question = random.choice(candidates)
                        difficulty = relaxed
                    else:
                        relaxed = relax_difficulty(relaxed)

            # -------------------------------------------------
            # FALLBACK 4:
            # ANY UNANSWERED QUESTION
            # -------------------------------------------------
            if question is None:

                question = fetch_any_unanswered_question()

                if question:
                    skill_tag = question.skill_tag
                    difficulty = question.difficulty

    # =================================================
    # NO QUESTION AVAILABLE
    # =================================================
    if question is None:

        return jsonify({
            "done": True,
            "message": "No unanswered questions remain in the bank.",
            "question_count": assessment.question_count,
            "question_limit": 10
        })

    # -------------------------------------------------
    # GET PASSAGE FOR SELECTED QUESTION
    # -------------------------------------------------
    passage = Passage.query.get(question.passage_id)

    if not passage:
        return jsonify({
            "error": "passage not found for selected question"
        }), 404

    # -------------------------------------------------
    # DETERMINE WHETHER THIS QUESTION STARTS A NEW
    # PASSAGE
    # -------------------------------------------------
    if current_passage_id is None:
        new_passage = True
    elif question.passage_id != current_passage_id:
        new_passage = True
    else:
        new_passage = False

    # -------------------------------------------------
    # RESPONSE
    # -------------------------------------------------
    return jsonify({
        "question_id": question.id,
        "prompt": question.prompt,
        "choices": question.choices or [],
        "skill_tag": skill_tag,
        "difficulty": difficulty,

        "question_number": assessment.question_count + 1,
        "question_limit": 10,

        # Frontend should only replace the displayed
        # passage when this is True.
        "new_passage": new_passage,

        "passage": {
            "id": passage.id,
            "title": passage.title,
            "body": passage.body or "",
        }
    })

# =====================================
# ANSWER SUBMISSION
# Logs Response, updates mastery,
# awards points, and evaluates badges
# =====================================
@app.route('/api/answer', methods=['POST'])
def answer():

    data = request.json or {}

    student_id = data.get("student_id")
    session_id = data.get("session_id")
    question_id = data.get("question_id")
    chosen_index = data.get("chosen_index")

    response_time_sec = data.get(
        "response_time_sec",
        0.0
    )

    reread_count = data.get(
        "reread_count",
        0
    )

    # =================================================
    # VALIDATE STUDENT
    # =================================================
    if not student_id:
        return jsonify({
            "error": "valid student_id required"
        }), 400

    student = Student.query.get(student_id)

    if not student:
        return jsonify({
            "error": "student not found"
        }), 404

    # =================================================
    # VALIDATE SESSION
    # =================================================
    if not session_id:
        return jsonify({
            "error": "valid session_id required"
        }), 400

    assessment = AssessmentSession.query.filter_by(
        id=session_id,
        student_id=student_id
    ).first()

    if not assessment:
        return jsonify({
            "error": "assessment session not found"
        }), 404

    # =================================================
    # HARD LIMIT: 10 QUESTIONS PER ASSESSMENT
    # =================================================
    if assessment.question_count >= 10:

        if not assessment.completed_at:
            assessment.completed_at = datetime.utcnow()
            db.session.commit()

        return jsonify({
            "error": "assessment already completed"
        }), 400

    # =================================================
    # VALIDATE QUESTION
    # =================================================
    if not question_id:
        return jsonify({
            "error": "question_id required"
        }), 400

    question = Question.query.get(question_id)

    if not question:
        return jsonify({
            "error": "question not found"
        }), 404

    # =================================================
    # VALIDATE ANSWER INDEX
    # =================================================
    if chosen_index is None:
        return jsonify({
            "error": "chosen_index required"
        }), 400

    try:
        chosen_index = int(chosen_index)
    except (TypeError, ValueError):
        return jsonify({
            "error": "chosen_index must be an integer"
        }), 400

    if not question.choices:
        return jsonify({
            "error": "question has no answer choices"
        }), 400

    if (
        chosen_index < 0
        or chosen_index >= len(question.choices)
    ):
        return jsonify({
            "error": "chosen_index is outside the available choices"
        }), 400

    # =================================================
    # PREVENT DUPLICATE ANSWERING
    #
    # The frontend should normally never submit the same
    # question twice, but this protects the database if
    # the request is accidentally repeated.
    # =================================================
    existing_response = Response.query.filter_by(
        student_id=student_id,
        session_id=session_id,
        question_id=question_id
    ).first()

    if existing_response:
        return jsonify({
            "error": "question already answered in this assessment"
        }), 409

    # =================================================
    # GET STUDENT'S SKILL STATE
    # =================================================
    skill_row = StudentSkillState.query.filter_by(
        student_id=student_id,
        skill_tag=question.skill_tag
    ).first()

    if not skill_row:
        return jsonify({
            "error": (
                "skill state not initialized — "
                "call /api/session/start first"
            )
        }), 400

    # =================================================
    # CAPTURE BADGES BEFORE THIS ANSWER
    # =================================================
    badges_before = get_student_badges(student_id)

    # =================================================
    # CHECK ANSWER
    # =================================================
    is_correct = (
        chosen_index == question.correct_index
    )

    # =================================================
    # UPDATE MASTERY
    # =================================================
    mastery_before = skill_row.mastery

    mastery_after = update_mastery(
        mastery_before,
        is_correct,
        question.difficulty
    )

    band_before = classify_band(
        mastery_before
    )

    band_after = classify_band(
        mastery_after
    )

    # =================================================
    # CALCULATE POINTS
    #
    # Correct answer = +10
    # Moving up mastery band = +25 bonus
    # =================================================
    points_earned = (
        POINTS_CORRECT
        if is_correct
        else 0
    )

    leveled_up = (
        BAND_RANK[band_after.value]
        >
        BAND_RANK[band_before.value]
    )

    if leveled_up:
        points_earned += POINTS_BAND_UP

    # =================================================
    # UPDATE STUDENT SKILL STATE
    # =================================================
    skill_row.mastery = mastery_after

    skill_row.points = (
        (skill_row.points or 0)
        + points_earned
    )

    # =================================================
    # LOG RESPONSE
    # =================================================
    response = Response(
        session_id=session_id,
        student_id=student_id,
        question_id=question_id,
        skill_tag=question.skill_tag,
        difficulty=question.difficulty,
        is_correct=is_correct,
        response_time_sec=response_time_sec,
        reread_count=reread_count,
        mastery_before=mastery_before,
        mastery_after=mastery_after,
    )

    db.session.add(response)

    # =================================================
    # UPDATE ASSESSMENT QUESTION COUNT
    # =================================================
    assessment.question_count += 1

    # =================================================
    # COMPLETE ASSESSMENT AT 10 QUESTIONS
    # =================================================
    if assessment.question_count >= 10:
        assessment.completed_at = datetime.utcnow()

    # =================================================
    # SAVE EVERYTHING
    # =================================================
    try:
        db.session.commit()

    except Exception as e:
        db.session.rollback()

        print(
            "ANSWER COMMIT ERROR:",
            repr(e)
        )

        return jsonify({
            "error": "unable to save answer"
        }), 500

    # =================================================
    # CALCULATE BADGES AFTER ANSWER
    # =================================================
    badges_after = get_student_badges(
        student_id
    )

    newly_earned_badges = get_new_badges(
        badges_before,
        badges_after
    )

    # =================================================
    # PASSAGE COMPLETION STATUS
    #
    # Determine whether the passage associated with this
    # question has now been completely answered.
    # =================================================
    passage_completed = False
    completed_passage_count = 0

    if question.passage_id is not None:

        passage_question_ids = {
            q.id
            for q in Question.query.filter_by(
                passage_id=question.passage_id
            ).all()
        }

        answered_passage_question_ids = {
            r.question_id
            for r in Response.query.filter(
                Response.student_id == student_id,
                Response.question_id.in_(
                    passage_question_ids
                )
            ).all()
        }

        if (
            passage_question_ids
            and
            passage_question_ids.issubset(
                answered_passage_question_ids
            )
        ):
            passage_completed = True

    # Only calculate this when the badge could potentially
    # be relevant. This also keeps the response useful to
    # the frontend.
    if len(badges_after) >= 0:
        completed_passage_count = (
            get_completed_passage_count(
                student_id
            )
        )

    # =================================================
    # RESPONSE
    # =================================================
    return jsonify({

        # ---------------------------------------------
        # ANSWER RESULT
        # ---------------------------------------------
        "is_correct": is_correct,
        "correct_index": question.correct_index,

        # ---------------------------------------------
        # MASTERY
        # ---------------------------------------------
        "mastery_before": round(
            mastery_before,
            3
        ),

        "mastery_after": round(
            mastery_after,
            3
        ),

        "band_before": (
            band_before.value
        ),

        "band_after": (
            band_after.value
        ),

        "leveled_up": leveled_up,

        # ---------------------------------------------
        # POINTS
        # ---------------------------------------------
        "points_earned": points_earned,

        # ---------------------------------------------
        # ASSESSMENT PROGRESS
        # ---------------------------------------------
        "question_count": (
            assessment.question_count
        ),

        "question_limit": 10,

        "assessment_completed": (
            assessment.completed_at is not None
        ),

        # ---------------------------------------------
        # PASSAGE / QUEST PROGRESS
        # ---------------------------------------------
        "passage_id": question.passage_id,

        "passage_completed": passage_completed,

        "completed_passage_count": (
            completed_passage_count
        ),

        # ---------------------------------------------
        # BADGES
        # ---------------------------------------------
        "badges": badges_after,

        "newly_earned_badges": (
            newly_earned_badges
        ),
    })


# =====================================
# PROGRESS / DASHBOARD DATA
# =====================================
@app.route('/api/progress/<int:student_id>')
def progress_api(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "student not found"}), 404

    rows = StudentSkillState.query.filter_by(student_id=student_id).all()
    skills = []
    total_points = 0
    for row in rows:
        band = classify_band(row.mastery)
        skills.append({
            "skill_tag": row.skill_tag,
            "mastery": round(row.mastery, 3),
            "band": band.value,
            "next_difficulty": target_difficulty(row.mastery),
            "points": row.points,
        })
        total_points += row.points or 0

    history_rows = (
        Response.query
        .filter_by(student_id=student_id)
        .order_by(Response.timestamp.asc(), Response.id.asc())
        .all()
    )

    history = [
        {
            "timestamp": row.timestamp.isoformat(),
            "skill_tag": row.skill_tag,
            "mastery_before": round(row.mastery_before, 3),
            "mastery_after": round(row.mastery_after, 3),
        }
        for row in history_rows
    ]

    return jsonify({
        "student_id": student_id,
        "name": student.username,
        "grade": student.grade,
        "skills": skills,
        "total_points": total_points,
        "badges": get_student_badges(student_id),
        "history": history,
    })


# =====================================
# EXPORT (Chapter 3.8 evaluation data)
# =====================================
@app.route('/api/export')
def export():
    rows = Response.query.all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "student_id", "passage_id", "question_id", "skill_tag", "difficulty",
        "is_correct", "response_time_sec", "reread_count",
        "mastery_before", "mastery_after", "timestamp",
    ])
    for r in rows:
        q = Question.query.get(r.question_id)
        writer.writerow([
            r.student_id,
            q.passage_id if q else "",
            r.question_id,
            r.skill_tag,
            r.difficulty,
            r.is_correct,
            r.response_time_sec,
            r.reread_count,
            r.mastery_before,
            r.mastery_after,
            r.timestamp,
        ])

    resp = make_response(output.getvalue())
    resp.headers["Content-Disposition"] = "attachment; filename=garcs_responses.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp


# NOTE: /api/predict and /api/passage/<grade> are intentionally absent.
# Per the roadmap, they're deprecated from the live MVP path -- the
# EdNet/ML strand is fully out of scope, so there is nothing left to serve
# from those routes.


if __name__ == "__main__":
    app.run(debug=True)
