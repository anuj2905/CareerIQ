import sqlite3
from pathlib import Path


# ============================================================
# DATABASE PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIRECTORY = PROJECT_ROOT / "data"

DATABASE_PATH = DATA_DIRECTORY / "careeriq.db"


# ============================================================
# GET DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Create and return a SQLite database connection.
    """

    DATA_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():
    """
    Create all CareerIQ database tables if they do not exist.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # ====================================================
        # STUDENT PROFILE
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS student_profiles (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT,

                resume_text TEXT,

                resume_file_name TEXT,

                resume_file_size INTEGER,

                created_at TEXT DEFAULT CURRENT_TIMESTAMP,

                updated_at TEXT DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        # ====================================================
        # EDUCATION
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS education (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                student_id INTEGER NOT NULL,

                education TEXT NOT NULL,

                FOREIGN KEY (student_id)
                    REFERENCES student_profiles(id)
                    ON DELETE CASCADE

            )
            """
        )

        # ====================================================
        # SKILLS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS skills (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                student_id INTEGER NOT NULL,

                skill TEXT NOT NULL,

                FOREIGN KEY (student_id)
                    REFERENCES student_profiles(id)
                    ON DELETE CASCADE

            )
            """
        )

        # ====================================================
        # PROJECTS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                student_id INTEGER NOT NULL,

                project TEXT NOT NULL,

                FOREIGN KEY (student_id)
                    REFERENCES student_profiles(id)
                    ON DELETE CASCADE

            )
            """
        )

        # ====================================================
        # EXPERIENCE
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS experience (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                student_id INTEGER NOT NULL,

                experience TEXT NOT NULL,

                FOREIGN KEY (student_id)
                    REFERENCES student_profiles(id)
                    ON DELETE CASCADE

            )
            """
        )

        # ====================================================
        # CERTIFICATIONS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS certifications (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                student_id INTEGER NOT NULL,

                certification TEXT NOT NULL,

                FOREIGN KEY (student_id)
                    REFERENCES student_profiles(id)
                    ON DELETE CASCADE

            )
            """
        )

        # ====================================================
        # COMPANY
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                company_name TEXT NOT NULL,

                email TEXT,

                website TEXT,

                industry TEXT,

                location TEXT,

                description TEXT,

                logo_url TEXT,

                created_at TEXT DEFAULT CURRENT_TIMESTAMP,

                updated_at TEXT DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        # ====================================================
        # JOBS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                company_id INTEGER NOT NULL,

                title TEXT NOT NULL,

                description TEXT NOT NULL,

                location TEXT,

                employment_type TEXT,

                experience_required REAL DEFAULT 0,

                education_required TEXT,

                salary_min REAL,

                salary_max REAL,

                status TEXT DEFAULT 'active',

                created_at TEXT DEFAULT CURRENT_TIMESTAMP,

                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (company_id)
                    REFERENCES companies(id)
                    ON DELETE CASCADE

            )
            """
        )

        # ====================================================
        # JOB SKILLS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS job_skills (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                job_id INTEGER NOT NULL,

                skill TEXT NOT NULL,

                FOREIGN KEY (job_id)
                    REFERENCES jobs(id)
                    ON DELETE CASCADE

            )
            """
        )

        # ====================================================
        # JOB APPLICATIONS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS job_applications (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                job_id INTEGER NOT NULL,

                student_id INTEGER NOT NULL,

                match_score REAL,

                application_status TEXT DEFAULT 'applied',

                applied_at TEXT DEFAULT CURRENT_TIMESTAMP,

                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (job_id)
                    REFERENCES jobs(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (student_id)
                    REFERENCES student_profiles(id)
                    ON DELETE CASCADE,

                UNIQUE(job_id, student_id)

            )
            """
        )

        # ====================================================
        # COMMIT CHANGES
        # ====================================================

        connection.commit()

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


# ============================================================
# DATABASE TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print("       CareerIQ Database")
    print("==========================================")
    print()

    initialize_database()

    print(
        "Database initialized successfully."
    )

    print(
        f"Database location: {DATABASE_PATH}"
    )

    print()
    print("==========================================")