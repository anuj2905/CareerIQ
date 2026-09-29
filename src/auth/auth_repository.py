import hashlib
import hmac
import secrets

from src.database.database import get_connection


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password: str) -> str:
    """
    Hash a password using PBKDF2-HMAC-SHA256.
    Format:
        salt_hex:hash_hex
    """

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        120_000
    )

    return salt.hex() + ":" + password_hash.hex()


def verify_password(
    password: str,
    stored_hash: str
) -> bool:
    """
    Verify a password against the stored PBKDF2 hash.
    """

    try:
        salt_hex, hash_hex = stored_hash.split(":")

        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)

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
# DATABASE CONNECTION
# ============================================================

def get_auth_connection():
    """
    Use the same PostgreSQL connection used by the rest
    of CareerIQ.

    This replaces the old SQLite connection.
    """

    return get_connection()


# ============================================================
# INITIALIZE / VERIFY AUTH DATABASE
# ============================================================

def initialize_auth_database():
    """
    Verify that the authentication tables already exist
    in Supabase PostgreSQL.

    The tables are NOT created here because the schema
    has already been created in Supabase.
    """

    connection = get_auth_connection()
    cursor = connection.cursor()

    try:
        required_tables = [
            "users",
            "student_accounts",
            "company_accounts"
        ]

        for table in required_tables:
            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = %s
                ) AS exists
                """,
                (table,)
            )

            result = cursor.fetchone()

            if not result["exists"]:
                raise RuntimeError(
                    f"Required authentication table '{table}' "
                    f"does not exist in Supabase."
                )

    finally:
        connection.close()


# ============================================================
# USER SIGN UP
# ============================================================

def create_user(
    email: str,
    password: str,
    role: str
):
    """
    Create a new CareerIQ user.

    Supported roles:
        student
        company
    """

    email = email.strip().lower()
    role = role.strip().lower()

    if not email:
        raise ValueError("Email is required.")

    if not password:
        raise ValueError("Password is required.")

    if role not in ["student", "company"]:
        raise ValueError("Invalid account type.")

    if len(password) < 8:
        raise ValueError(
            "Password must contain at least 8 characters."
        )

    connection = get_auth_connection()
    cursor = connection.cursor()

    try:
        password_hash = hash_password(password)

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

    except Exception as error:

        connection.rollback()

        # PostgreSQL unique constraint
        # error handling
        error_message = str(error).lower()

        if (
            "duplicate key" in error_message
            or "unique constraint" in error_message
            or "users_email_key" in error_message
        ):
            raise ValueError(
                "An account with this email already exists."
            )

        raise

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
    """
    Authenticate a CareerIQ user.

    Returns:
        {
            "id": ...,
            "email": ...,
            "role": ...
        }

    Returns None if authentication fails.
    """

    email = email.strip().lower()
    role = role.strip().lower()

    connection = get_auth_connection()
    cursor = connection.cursor()

    try:

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

    finally:
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

    try:

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

        return result is not None

    finally:
        connection.close()


# ============================================================
# GET USER'S COMPANY
# ============================================================

def get_user_company(
    user_id: int
):
    """
    Return the company connected to a user.

    One company account can own one company.
    """

    connection = get_auth_connection()
    cursor = connection.cursor()

    try:

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

    finally:
        connection.close()

    if company is None:
        return None

    return dict(company)


# ============================================================
# GET USER COMPANIES
# ============================================================

def get_user_companies(
    user_id: int
):
    """
    Kept for compatibility with existing CareerIQ code.
    """

    connection = get_auth_connection()
    cursor = connection.cursor()

    try:

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

    finally:
        connection.close()

    return [
        dict(company)
        for company in companies
    ]


# ============================================================
# LINK COMPANY TO USER
# ============================================================

def link_company_to_user(
    user_id: int,
    company_id: int
):
    """
    Link a company to a company account.

    A company account can have only one company.
    """

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

    except Exception as error:

        connection.rollback()

        error_message = str(error).lower()

        if (
            "duplicate key" in error_message
            or "unique constraint" in error_message
        ):
            raise ValueError(
                "Could not link company to account: "
                "the company is already linked."
            )

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
    """
    Get a user by ID.
    """

    connection = get_auth_connection()
    cursor = connection.cursor()

    try:

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

    finally:
        connection.close()

    if user is None:
        return None

    return dict(user)


# ============================================================
# INITIALIZE / VERIFY
# ============================================================

initialize_auth_database()