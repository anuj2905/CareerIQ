import hashlib
import hmac
import secrets
import sqlite3
from pathlib import Path


# ============================================================
# DATABASE LOCATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_PATH = (
    PROJECT_ROOT
    / "data"
    / "careeriq.db"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_auth_connection():
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    # Enable foreign key support
    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


# ============================================================
# INITIALIZE AUTH TABLES
# ============================================================

def initialize_auth_database():

    connection = get_auth_connection()
    cursor = connection.cursor()

    # --------------------------------------------------------
    # USERS
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
                CHECK(role IN ('student', 'company')),
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # --------------------------------------------------------
    # COMPANY ACCOUNTS
    #
    # IMPORTANT:
    # One company account can be connected to ONLY ONE company.
    #
    # Existing databases may still have the older
    # UNIQUE(user_id, company_id) rule.
    #
    # Therefore the application also checks this rule before
    # creating/linking a company.
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS company_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            company_id INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE,

            FOREIGN KEY(company_id)
                REFERENCES companies(id)
                ON DELETE CASCADE,

            UNIQUE(user_id, company_id)
        )
        """
    )

    # --------------------------------------------------------
    # STUDENT ACCOUNTS
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS student_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            student_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    connection.commit()
    connection.close()


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password: str) -> str:

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        120_000
    )

    return (
        salt.hex()
        + ":"
        + password_hash.hex()
    )


def verify_password(
    password: str,
    stored_hash: str
) -> bool:

    try:

        salt_hex, hash_hex = (
            stored_hash.split(":")
        )

        salt = bytes.fromhex(
            salt_hex
        )

        expected_hash = bytes.fromhex(
            hash_hex
        )

        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            120_000
        )

        return hmac.compare_digest(
            actual_hash,
            expected_hash
        )

    except Exception:

        return False


# ============================================================
# USER SIGN UP
# ============================================================

def create_user(
    email: str,
    password: str,
    role: str
):

    email = email.strip().lower()
    role = role.strip().lower()

    if not email:
        raise ValueError(
            "Email is required."
        )

    if not password:
        raise ValueError(
            "Password is required."
        )

    if role not in [
        "student",
        "company"
    ]:
        raise ValueError(
            "Invalid account type."
        )

    if len(password) < 8:
        raise ValueError(
            "Password must contain at least 8 characters."
        )

    connection = get_auth_connection()
    cursor = connection.cursor()

    try:

        password_hash = hash_password(
            password
        )

        cursor.execute(
            """
            INSERT INTO users (
                email,
                password_hash,
                role
            )
            VALUES (?, ?, ?)
            """,
            (
                email,
                password_hash,
                role
            )
        )

        user_id = cursor.lastrowid

        # ----------------------------------------------------
        # STUDENT ACCOUNT
        # ----------------------------------------------------

        if role == "student":

            cursor.execute(
                """
                INSERT INTO student_accounts (
                    user_id
                )
                VALUES (?)
                """,
                (user_id,)
            )

        connection.commit()

        return user_id

    except sqlite3.IntegrityError:

        connection.rollback()

        raise ValueError(
            "An account with this email already exists."
        )

    finally:

        connection.close()


# ============================================================
# LOGIN
# ============================================================

def authenticate_user(
    email: str,
    password: str,
    role: str
):

    email = email.strip().lower()
    role = role.strip().lower()

    connection = get_auth_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            email,
            password_hash,
            role
        FROM users
        WHERE email = ?
        AND role = ?
        """,
        (
            email,
            role
        )
    )

    user = cursor.fetchone()

    connection.close()

    if user is None:
        return None

    if not verify_password(
        password,
        user["password_hash"]
    ):
        return None

    return {
        "id": user["id"],
        "email": user["email"],
        "role": user["role"]
    }


# ============================================================
# CHECK WHETHER USER ALREADY HAS A COMPANY
# ============================================================

def user_has_company(
    user_id: int
) -> bool:

    connection = get_auth_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM company_accounts
        WHERE user_id = ?
        LIMIT 1
        """,
        (user_id,)
    )

    result = cursor.fetchone()

    connection.close()

    return result is not None


# ============================================================
# GET USER'S COMPANY
#
# Since one company account can own only one company,
# this returns a single company.
# ============================================================

def get_user_company(
    user_id: int
):

    connection = get_auth_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            c.id,
            c.company_name,
            c.email,
            c.website,
            c.industry,
            c.location,
            c.description,
            c.logo_url,
            c.created_at,
            c.updated_at
        FROM companies c
        INNER JOIN company_accounts ca
            ON c.id = ca.company_id
        WHERE ca.user_id = ?
        ORDER BY c.created_at DESC
        LIMIT 1
        """,
        (user_id,)
    )

    company = cursor.fetchone()

    connection.close()

    if company is None:
        return None

    return dict(company)


# ============================================================
# GET USER COMPANIES
#
# Kept for compatibility with existing code.
# In the new architecture this will normally return
# zero or one company.
# ============================================================

def get_user_companies(
    user_id: int
):

    connection = get_auth_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            c.id,
            c.company_name,
            c.email,
            c.website,
            c.industry,
            c.location,
            c.description,
            c.logo_url,
            c.created_at,
            c.updated_at
        FROM companies c
        INNER JOIN company_accounts ca
            ON c.id = ca.company_id
        WHERE ca.user_id = ?
        ORDER BY c.created_at DESC
        """,
        (user_id,)
    )

    companies = cursor.fetchall()

    connection.close()

    return [
        dict(company)
        for company in companies
    ]


# ============================================================
# LINK COMPANY TO USER
#
# IMPORTANT:
# A company account can have ONLY ONE company.
# ============================================================

def link_company_to_user(
    user_id: int,
    company_id: int
):

    connection = get_auth_connection()
    cursor = connection.cursor()

    try:

        # ----------------------------------------------------
        # CHECK EXISTING COMPANY
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                company_id
            FROM company_accounts
            WHERE user_id = ?
            LIMIT 1
            """,
            (user_id,)
        )

        existing = cursor.fetchone()

        if existing is not None:

            existing_company_id = existing["company_id"]

            if existing_company_id == company_id:

                return True

            raise ValueError(
                "This account already has a registered company. "
                "One company is allowed per company account."
            )

        # ----------------------------------------------------
        # LINK COMPANY
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT INTO company_accounts (
                user_id,
                company_id
            )
            VALUES (?, ?)
            """,
            (
                user_id,
                company_id
            )
        )

        connection.commit()

        return True

    except sqlite3.IntegrityError as error:

        connection.rollback()

        raise ValueError(
            f"Could not link company to account: {error}"
        )

    finally:

        connection.close()


# ============================================================
# GET USER
# ============================================================

def get_user(
    user_id: int
):

    connection = get_auth_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            email,
            role
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    connection.close()

    if user is None:
        return None

    return dict(user)


# ============================================================
# INITIALIZE
# ============================================================

initialize_auth_database()