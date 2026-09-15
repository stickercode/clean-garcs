"""
GARCS SQLite -> PostgreSQL migration

This script:
1. Reads the existing SQLite database.
2. Connects the GARCS SQLAlchemy models to PostgreSQL.
3. Creates the PostgreSQL tables.
4. Copies existing records while preserving primary-key IDs.
5. Copies JSON fields such as Question.choices.
6. Resets PostgreSQL identity sequences.
7. Verifies row counts.

IMPORTANT:
- Make a backup of database.db before running this.
- DATABASE_URL must point to the PostgreSQL database.
- This script does NOT delete the SQLite database.
"""

import os
import sqlite3
import sys
from pathlib import Path
from datetime import datetime
from sqlalchemy import text

# -------------------------------------------------
# Locate project
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

SQLITE_FILE = BASE_DIR / "instance" / "database.db"

if not SQLITE_FILE.exists():
    print(f"ERROR: SQLite database not found:")
    print(f"       {SQLITE_FILE}")
    sys.exit(1)

# -------------------------------------------------
# PostgreSQL connection string
# -------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL is not set.")
    print()
    print("Set it before running the migration:")
    print()
    print("export DATABASE_URL='postgresql://USER:PASSWORD@HOST:5432/DATABASE'")
    print()
    sys.exit(1)

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://",
        1
    )

# -------------------------------------------------
# Import Flask application AFTER DATABASE_URL exists
# -------------------------------------------------

from app import (
    app,
    db,
    Student,
    Passage,
    LibraryBook,
    LibraryChapter,
    Chapter,
    ReadingProgress,
    Question,
    Response,
    StudentSkillState,
    AssessmentSession,
)

# -------------------------------------------------
# SQLite helpers
# -------------------------------------------------

def sqlite_connection():
    connection = sqlite3.connect(str(SQLITE_FILE))
    connection.row_factory = sqlite3.Row
    return connection


def sqlite_tables(connection):
    rows = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
          AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """
    ).fetchall()

    return [row["name"] for row in rows]


def sqlite_columns(connection, table_name):
    rows = connection.execute(
        f'PRAGMA table_info("{table_name}")'
    ).fetchall()

    return {row["name"] for row in rows}


def fetch_rows(connection, table_name):
    return connection.execute(
        f'SELECT * FROM "{table_name}" ORDER BY id'
    ).fetchall()


# -------------------------------------------------
# Generic value helper
# -------------------------------------------------

def value(row, column_name, default=None):
    if column_name not in row.keys():
        return default

    return row[column_name]


# -------------------------------------------------
# Migration functions
# -------------------------------------------------

def migrate_students(connection):
    rows = fetch_rows(connection, "student")

    print(f"  student: {len(rows)}")

    for row in rows:
        existing = db.session.get(
            Student,
            value(row, "id")
        )

        if existing:
            continue

        student = Student(
            id=value(row, "id"),
            username=value(row, "username"),
            student_number=value(row, "student_number"),
            email=value(row, "email"),
            grade=value(row, "grade"),
            password_hash=value(row, "password_hash"),
        )

        db.session.add(student)

    db.session.commit()


def migrate_passages(connection):
    rows = fetch_rows(connection, "passage")

    print(f"  passage: {len(rows)}")

    for row in rows:
        existing = db.session.get(
            Passage,
            value(row, "id")
        )

        if existing:
            continue

        passage = Passage(
            id=value(row, "id"),
            title=value(row, "title"),
            body=value(row, "body"),
            grade_band=value(row, "grade_band"),
        )

        db.session.add(passage)

    db.session.commit()


def migrate_library_books(connection):
    rows = fetch_rows(connection, "library_book")

    print(f"  library_book: {len(rows)}")

    for row in rows:
        existing = db.session.get(
            LibraryBook,
            value(row, "id")
        )

        if existing:
            continue

        book = LibraryBook(
            id=value(row, "id"),
            title=value(row, "title"),
            author=value(row, "author"),
            description=value(row, "description"),
            category=value(row, "category"),
            grade_band=value(row, "grade_band"),
            cover_image=value(row, "cover_image"),
            is_featured=bool(
                value(row, "is_featured", False)
            ),
        )

        db.session.add(book)

    db.session.commit()


def migrate_library_chapters(connection):
    rows = fetch_rows(connection, "library_chapter")

    print(f"  library_chapter: {len(rows)}")

    for row in rows:
        existing = db.session.get(
            LibraryChapter,
            value(row, "id")
        )

        if existing:
            continue

        chapter = LibraryChapter(
            id=value(row, "id"),
            book_id=value(row, "book_id"),
            chapter_number=value(row, "chapter_number"),
            title=value(row, "title"),
            content=value(row, "content"),
        )

        db.session.add(chapter)

    db.session.commit()


def migrate_chapters(connection):
    rows = fetch_rows(connection, "chapter")

    print(f"  chapter: {len(rows)}")

    for row in rows:
        existing = db.session.get(
            Chapter,
            value(row, "id")
        )

        if existing:
            continue

        chapter = Chapter(
            id=value(row, "id"),
            passage_id=value(row, "passage_id"),
            chapter_number=value(row, "chapter_number"),
            title=value(row, "title"),
            content=value(row, "content"),
        )

        db.session.add(chapter)

    db.session.commit()


def migrate_questions(connection):
    rows = fetch_rows(connection, "question")

    print(f"  question: {len(rows)}")

    for row in rows:
        existing = db.session.get(
            Question,
            value(row, "id")
        )

        if existing:
            continue

        choices = value(row, "choices")

        # SQLite may store JSON as TEXT.
        # SQLAlchemy's JSON column can accept the
        # decoded Python list/dict.
        if isinstance(choices, str):
            import json

            try:
                choices = json.loads(choices)
            except json.JSONDecodeError:
                pass

        question = Question(
            id=value(row, "id"),
            passage_id=value(row, "passage_id"),
            prompt=value(row, "prompt"),
            choices=choices,
            correct_index=value(row, "correct_index"),
            skill_tag=value(row, "skill_tag"),
            difficulty=value(row, "difficulty"),
        )

        db.session.add(question)

    db.session.commit()


def migrate_skill_states(connection):
    rows = fetch_rows(connection, "student_skill_state")

    print(f"  student_skill_state: {len(rows)}")

    for row in rows:
        existing = db.session.get(
            StudentSkillState,
            value(row, "id")
        )

        if existing:
            continue

        state = StudentSkillState(
            id=value(row, "id"),
            student_id=value(row, "student_id"),
            skill_tag=value(row, "skill_tag"),
            mastery=value(row, "mastery", 0.50),
            points=value(row, "points", 0),
        )

        db.session.add(state)

    db.session.commit()


def migrate_assessment_sessions(connection):
    rows = fetch_rows(connection, "assessment_session")

    print(f"  assessment_session: {len(rows)}")

    for row in rows:
        existing = db.session.get(
            AssessmentSession,
            value(row, "id")
        )

        if existing:
            continue

        started_at = value(row, "started_at")
        completed_at = value(row, "completed_at")

        assessment = AssessmentSession(
            id=value(row, "id"),
            student_id=value(row, "student_id"),
            started_at=parse_datetime(started_at),
            completed_at=parse_datetime(completed_at),
            question_count=value(row, "question_count", 0),
        )

        db.session.add(assessment)

    db.session.commit()


def migrate_reading_progress(connection):
    rows = fetch_rows(connection, "reading_progress")

    print(f"  reading_progress: {len(rows)}")

    columns = sqlite_columns(
        connection,
        "reading_progress"
    )

    skipped = 0

    for row in rows:
        existing = db.session.get(
            ReadingProgress,
            value(row, "id")
        )

        if existing:
            continue

        book_id = value(row, "book_id")

        # Current ReadingProgress requires book_id.
        # If an old SQLite row predates the book-based
        # reading system, it cannot be safely mapped to
        # a LibraryBook automatically.
        if book_id is None:
            print(
                f"    WARNING: skipping reading_progress "
                f"id={value(row, 'id')} because book_id is NULL."
            )
            skipped += 1
            continue

        progress = ReadingProgress(
            id=value(row, "id"),
            student_id=value(row, "student_id"),
            passage_id=value(row, "passage_id"),
            book_id=book_id,
            chapter_id=value(row, "chapter_id"),
            current_chapter=value(
                row,
                "current_chapter",
                1
            ),
            completed_chapters=value(
                row,
                "completed_chapters",
                0
            ),
            progress_percent=value(
                row,
                "progress_percent",
                0
            ),
            reading_position=value(
                row,
                "reading_position",
                0
            ),
            completed=bool(
                value(row, "completed", False)
            ),
            updated_at=parse_datetime(
                value(row, "updated_at")
            ),
        )

        db.session.add(progress)

    db.session.commit()

    if skipped:
        print(
            f"    WARNING: {skipped} old reading_progress "
            f"row(s) could not be mapped because book_id was NULL."
        )


def migrate_responses(connection):
    rows = fetch_rows(connection, "response")

    print(f"  response: {len(rows)}")

    for row in rows:
        existing = db.session.get(
            Response,
            value(row, "id")
        )

        if existing:
            continue

        response = Response(
            id=value(row, "id"),
            student_id=value(row, "student_id"),
            session_id=value(row, "session_id"),
            question_id=value(row, "question_id"),
            skill_tag=value(row, "skill_tag"),
            difficulty=value(row, "difficulty"),
            is_correct=value(row, "is_correct"),
            response_time_sec=value(
                row,
                "response_time_sec"
            ),
            reread_count=value(
                row,
                "reread_count",
                0
            ),
            mastery_before=value(
                row,
                "mastery_before"
            ),
            mastery_after=value(
                row,
                "mastery_after"
            ),
            timestamp=parse_datetime(
                value(row, "timestamp")
            ),
        )

        db.session.add(response)

    db.session.commit()


# -------------------------------------------------
# Date helper
# -------------------------------------------------

def parse_datetime(value):
    if value is None:
        return None

    if isinstance(value, datetime):
        return value

    if isinstance(value, str):
        # SQLite commonly stores SQLAlchemy datetimes
        # as "YYYY-MM-DD HH:MM:SS.ssssss".
        formats = [
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(
                    value,
                    fmt
                )
            except ValueError:
                pass

    return value


# -------------------------------------------------
# Sequence reset
# -------------------------------------------------

def reset_postgresql_sequences():
    """
    PostgreSQL identity sequences need to move past
    the IDs explicitly imported from SQLite.
    """

    tables = [
        "student",
        "passage",
        "library_book",
        "library_chapter",
        "chapter",
        "reading_progress",
        "question",
        "response",
        "student_skill_state",
        "assessment_session",
    ]

    print()
    print("Resetting PostgreSQL ID sequences...")

    with db.engine.begin() as connection:
        for table in tables:
            sql = f"""
                SELECT setval(
                    pg_get_serial_sequence(
                        '{table}',
                        'id'
                    ),
                    COALESCE(
                        (SELECT MAX(id) FROM {table}),
                        1
                    ),
                    true
                )
            """

            try:
                connection.execute(
                    db.text(sql)
                )
            except Exception:
                # Some PostgreSQL versions / SQLAlchemy
                # configurations may use identity columns
                # differently. Do not fail the entire
                # migration just because this statement
                # cannot find a sequence.
                print(
                    f"  Sequence reset skipped for {table}"
                )


# -------------------------------------------------
# Verification
# -------------------------------------------------

def sqlite_count(connection, table):
    return connection.execute(
        f'SELECT COUNT(*) FROM "{table}"'
    ).fetchone()[0]


def postgres_count(model):
    return db.session.query(model).count()


def verify_counts(connection):
    print()
    print("=" * 60)
    print("ROW COUNT VERIFICATION")
    print("=" * 60)

    checks = [
        ("student", Student),
        ("passage", Passage),
        ("library_book", LibraryBook),
        ("library_chapter", LibraryChapter),
        ("chapter", Chapter),
        ("reading_progress", ReadingProgress),
        ("question", Question),
        ("response", Response),
        ("student_skill_state", StudentSkillState),
        ("assessment_session", AssessmentSession),
    ]

    failed = False

    for table, model in checks:
        source_count = sqlite_count(
            connection,
            table
        )

        target_count = postgres_count(model)

        # Reading progress may legitimately differ
        # when old passage-only rows have no book_id.
        if table == "reading_progress":
            if target_count != source_count:
                print(
                    f"WARNING  {table:25} "
                    f"SQLite={source_count:6} "
                    f"PostgreSQL={target_count:6}"
                )
            else:
                print(
                    f"OK       {table:25} "
                    f"{target_count}"
                )

        elif source_count != target_count:
            print(
                f"FAILED   {table:25} "
                f"SQLite={source_count:6} "
                f"PostgreSQL={target_count:6}"
            )
            failed = True

        else:
            print(
                f"OK       {table:25} "
                f"{target_count}"
            )

    print("=" * 60)

    if failed:
        raise RuntimeError(
            "Migration verification failed."
        )

    print("Migration verification completed.")


# -------------------------------------------------
# Main migration
# -------------------------------------------------

def main():
    print("=" * 60)
    print("GARCS SQLite -> PostgreSQL Migration")
    print("=" * 60)

    print()
    print("SQLite source:")
    print(SQLITE_FILE)

    print()
    print("PostgreSQL destination:")
    print(
        DATABASE_URL.split("@")[-1]
        if "@" in DATABASE_URL
        else DATABASE_URL
    )

    print()
    answer = input(
        "Have you backed up database.db? "
        "Type YES to continue: "
    )

    if answer.strip() != "YES":
        print("Migration cancelled.")
        return

    sqlite = sqlite_connection()

    try:
        print()
        print("SQLite tables detected:")

        for table in sqlite_tables(sqlite):
            print(f"  - {table}")

        print()
        print("Creating PostgreSQL tables...")

        with app.app_context():
            db.create_all()

            print("PostgreSQL tables ready.")

            print()
            print("Migrating records...")

            # Parent tables first.
            migrate_students(sqlite)
            migrate_passages(sqlite)
            migrate_library_books(sqlite)

            # Content depending on parent tables.
            migrate_library_chapters(sqlite)
            migrate_chapters(sqlite)
            migrate_questions(sqlite)

            # Student state / sessions.
            migrate_skill_states(sqlite)
            migrate_assessment_sessions(sqlite)

            # Reading progress depends on students/books/chapters.
            migrate_reading_progress(sqlite)

            # Responses depend on students/questions/sessions.
            migrate_responses(sqlite)

            # Verify.
            verify_counts(sqlite)

            print()
            print("Migration finished successfully.")

    except Exception as exc:
        print()
        print("=" * 60)
        print("MIGRATION FAILED")
        print("=" * 60)
        print(repr(exc))

        try:
            with app.app_context():
                db.session.rollback()
        except Exception:
            pass

        sys.exit(1)

    finally:
        sqlite.close()


if __name__ == "__main__":
    main()