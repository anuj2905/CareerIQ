import os
import re

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# DATABASE URL
# ============================================================

DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set in the .env file."
    )


# ============================================================
# POSTGRESQL CURSOR ADAPTER
# ============================================================

class CareerIQCursor:
    """
    Small compatibility wrapper around PostgreSQL cursor.

    Existing CareerIQ repository code currently uses:

        ?
        row["column"]
        cursor.lastrowid

    PostgreSQL normally uses:

        %s
        dictionary rows
        RETURNING id

    This wrapper allows the existing repository code
    to continue working while we migrate the database.
    """

    def __init__(self, connection):
        self.connection = connection

        self.cursor = connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        self.lastrowid = None

    # --------------------------------------------------------
    # Convert SQLite placeholders to PostgreSQL placeholders
    # --------------------------------------------------------

    @staticmethod
    def _convert_placeholders(sql: str) -> str:

        return sql.replace("?", "%s")

    # --------------------------------------------------------
    # Execute
    # --------------------------------------------------------

    def execute(self, sql, parameters=None):

        sql = self._convert_placeholders(sql)

        clean_sql = sql.strip()

        self.lastrowid = None

        # ----------------------------------------------------
        # PostgreSQL does not provide cursor.lastrowid.
        #
        # Existing CareerIQ code expects it after INSERT.
        #
        # Add RETURNING id automatically.
        # ----------------------------------------------------

        if (
            clean_sql.upper().startswith("INSERT")
            and "RETURNING" not in clean_sql.upper()
        ):

            sql = sql.rstrip().rstrip(";")

            sql = f"{sql} RETURNING id"

            if parameters is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(
                    sql,
                    parameters
                )

            row = self.cursor.fetchone()

            if row is not None:
                self.lastrowid = row["id"]

            return

        # ----------------------------------------------------
        # Normal query
        # ----------------------------------------------------

        if parameters is None:

            self.cursor.execute(sql)

        else:

            self.cursor.execute(
                sql,
                parameters
            )

    # --------------------------------------------------------
    # Fetch one
    # --------------------------------------------------------

    def fetchone(self):

        return self.cursor.fetchone()

    # --------------------------------------------------------
    # Fetch all
    # --------------------------------------------------------

    def fetchall(self):

        return self.cursor.fetchall()

    # --------------------------------------------------------
    # Row count
    # --------------------------------------------------------

    @property
    def rowcount(self):

        return self.cursor.rowcount

    # --------------------------------------------------------
    # Close
    # --------------------------------------------------------

    def close(self):

        self.cursor.close()


# ============================================================
# POSTGRESQL CONNECTION ADAPTER
# ============================================================

class CareerIQConnection:
    """
    PostgreSQL connection wrapper used by CareerIQ.
    """

    def __init__(self, connection):

        self.connection = connection

    # --------------------------------------------------------
    # Cursor
    # --------------------------------------------------------

    def cursor(self):

        return CareerIQCursor(
            self.connection
        )

    # --------------------------------------------------------
    # Commit
    # --------------------------------------------------------

    def commit(self):

        self.connection.commit()

    # --------------------------------------------------------
    # Rollback
    # --------------------------------------------------------

    def rollback(self):

        self.connection.rollback()

    # --------------------------------------------------------
    # Close
    # --------------------------------------------------------

    def close(self):

        self.connection.close()

    # --------------------------------------------------------
    # Context manager
    # --------------------------------------------------------

    def __enter__(self):

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):

        if exc_type:

            self.rollback()

        else:

            self.commit()

        self.close()


# ============================================================
# GET DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Create a PostgreSQL connection to Supabase.

    The connection string is read from:

        DATABASE_URL

    inside the .env file.
    """

    try:

        connection = psycopg2.connect(
            DATABASE_URL
        )

        return CareerIQConnection(
            connection
        )

    except Exception as e:

        raise RuntimeError(
            "Could not connect to Supabase PostgreSQL. "
            f"Database error: {e}"
        ) from e


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():
    """
    Verify that the CareerIQ PostgreSQL database is reachable.

    The actual tables are already created in Supabase,
    so this function does NOT recreate the schema.

    It exists because repositories.py currently calls:

        initialize_database()
    """

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            "SELECT 1 AS connected"
        )

        result = cursor.fetchone()

        cursor.close()

        if not result:

            raise RuntimeError(
                "Database connection test failed."
            )

        print(
            "CareerIQ database connected successfully."
        )

    except Exception as e:

        raise RuntimeError(
            "CareerIQ could not connect to "
            "Supabase PostgreSQL."
        ) from e

    finally:

        if connection is not None:

            connection.close()


# ============================================================
# DATABASE STATUS
# ============================================================

def test_database_connection():
    """
    Simple database connection test.

    Returns True when Supabase PostgreSQL is reachable.
    """

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            "SELECT 1 AS test"
        )

        result = cursor.fetchone()

        cursor.close()

        return (
            result is not None
            and result["test"] == 1
        )

    except Exception:

        return False

    finally:

        if connection is not None:

            connection.close()


# ============================================================
# DATABASE INFORMATION
# ============================================================

def get_database_info():
    """
    Return basic information about the connected
    PostgreSQL database.
    """

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                current_database() AS database_name,
                current_user AS database_user,
                version() AS version
            """
        )

        result = cursor.fetchone()

        cursor.close()

        return result

    finally:

        if connection is not None:

            connection.close()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print("       CareerIQ PostgreSQL Test")
    print("==========================================")
    print()

    try:

        if test_database_connection():

            print(
                "✅ Supabase PostgreSQL connection successful."
            )

            info = get_database_info()

            if info:

                print(
                    "Database:",
                    info["database_name"]
                )

                print(
                    "User:",
                    info["database_user"]
                )

            print()
            print(
                "CareerIQ database is ready."
            )

        else:

            print(
                "❌ Database connection failed."
            )

    except Exception as e:

        print(
            "❌ Database error:"
        )

        print(e)

    print()