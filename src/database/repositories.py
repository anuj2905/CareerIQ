from typing import List, Optional

from .database import (
    get_connection,
    initialize_database
)

from .models import (
    StudentProfile,
    Company,
    Job,
    JobApplication
)


# ============================================================
# INITIALIZE DATABASE
# ============================================================

initialize_database()


# ============================================================
# STUDENT ACCOUNT / PROFILE HELPERS
# ============================================================

def get_student_id_for_user(
    user_id: int
) -> Optional[int]:
    """
    Return the student_profiles.id linked to a users.id.

    The relationship is:

        users.id
            ↓
        student_accounts.user_id
            ↓
        student_accounts.student_id
            ↓
        student_profiles.id
    """

    if user_id is None:
        return None

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT student_id
            FROM student_accounts
            WHERE user_id = ?
            LIMIT 1
            """,
            (user_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return row["student_id"]

    finally:
        connection.close()


def link_student_to_user(
    user_id: int,
    student_id: int
) -> bool:
    """
    Link a student profile to an authenticated user.

    A student account row must already exist because it is created
    during student registration.
    """

    if user_id is None:
        raise ValueError("User ID is required.")

    if student_id is None:
        raise ValueError("Student ID is required.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE student_accounts
            SET student_id = ?
            WHERE user_id = ?
            """,
            (
                student_id,
                user_id
            )
        )

        updated = cursor.rowcount > 0

        connection.commit()

        return updated

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def ensure_student_profile_for_user(
    user_id: int
) -> Optional[int]:
    """
    Return the student's profile ID for the authenticated user.

    If the student account exists but has no profile yet, this function
    creates an empty student_profiles record and links it to the account.

    This is the central identity bridge for the student side of CareerIQ.
    """

    if user_id is None:
        raise ValueError("User ID is required.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # ----------------------------------------------------
        # CHECK STUDENT ACCOUNT
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                student_id
            FROM student_accounts
            WHERE user_id = ?
            LIMIT 1
            """,
            (user_id,)
        )

        account = cursor.fetchone()

        if account is None:
            raise ValueError(
                "No student account is linked to this user."
            )

        # ----------------------------------------------------
        # PROFILE ALREADY EXISTS
        # ----------------------------------------------------

        if account["student_id"] is not None:

            cursor.execute(
                """
                SELECT id
                FROM student_profiles
                WHERE id = ?
                LIMIT 1
                """,
                (account["student_id"],)
            )

            profile = cursor.fetchone()

            if profile is not None:
                return profile["id"]

            # The account points to a missing profile.
            # We repair the mapping below.
            student_id = None

        else:
            student_id = None

        # ----------------------------------------------------
        # CREATE EMPTY PROFILE
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT INTO student_profiles (
                name,
                resume_text,
                resume_file_name,
                resume_file_size
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                "",
                "",
                "",
                0
            )
        )

        student_id = cursor.lastrowid

        # ----------------------------------------------------
        # LINK PROFILE TO STUDENT ACCOUNT
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE student_accounts
            SET student_id = ?
            WHERE user_id = ?
            """,
            (
                student_id,
                user_id
            )
        )

        if cursor.rowcount == 0:
            raise ValueError(
                "Student account could not be linked."
            )

        connection.commit()

        return student_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ============================================================
# STUDENT PROFILE
# ============================================================

def save_student_profile(
    profile: StudentProfile,
    student_id: Optional[int] = None,
    user_id: Optional[int] = None
) -> int:
    """
    Save or update a complete student profile.

    Preferred usage:

        save_student_profile(profile, user_id=user_id)

    or, when the profile ID is already known:

        save_student_profile(profile, student_id=student_id)

    The database generates student_profiles.id. The authenticated
    user's student_accounts row is then linked to that profile.
    """

    if profile is None:
        raise ValueError("Student profile is required.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # ----------------------------------------------------
        # RESOLVE PROFILE ID FROM AUTHENTICATED USER
        # ----------------------------------------------------

        if user_id is not None:

            cursor.execute(
                """
                SELECT student_id
                FROM student_accounts
                WHERE user_id = ?
                LIMIT 1
                """,
                (user_id,)
            )

            account = cursor.fetchone()

            if account is None:
                raise ValueError(
                    "No student account is linked to this user."
                )

            linked_student_id = account["student_id"]

            if linked_student_id is not None:

                cursor.execute(
                    """
                    SELECT id
                    FROM student_profiles
                    WHERE id = ?
                    LIMIT 1
                    """,
                    (linked_student_id,)
                )

                existing_profile = cursor.fetchone()

                if existing_profile is not None:
                    student_id = linked_student_id

        # ----------------------------------------------------
        # CREATE NEW PROFILE WHEN NECESSARY
        # ----------------------------------------------------

        if student_id is None:

            cursor.execute(
                """
                INSERT INTO student_profiles (
                    name,
                    resume_text,
                    resume_file_name,
                    resume_file_size
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    profile.name,
                    profile.resume_text,
                    profile.resume_file_name,
                    profile.resume_file_size
                )
            )

            student_id = cursor.lastrowid

        else:

            cursor.execute(
                """
                SELECT id
                FROM student_profiles
                WHERE id = ?
                LIMIT 1
                """,
                (student_id,)
            )

            existing_student = cursor.fetchone()

            if existing_student:

                cursor.execute(
                    """
                    UPDATE student_profiles
                    SET
                        name = ?,
                        resume_text = ?,
                        resume_file_name = ?,
                        resume_file_size = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (
                        profile.name,
                        profile.resume_text,
                        profile.resume_file_name,
                        profile.resume_file_size,
                        student_id
                    )
                )

            else:

                cursor.execute(
                    """
                    INSERT INTO student_profiles (
                        name,
                        resume_text,
                        resume_file_name,
                        resume_file_size
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        profile.name,
                        profile.resume_text,
                        profile.resume_file_name,
                        profile.resume_file_size
                    )
                )

                student_id = cursor.lastrowid

        # ----------------------------------------------------
        # LINK PROFILE TO AUTHENTICATED USER
        # ----------------------------------------------------

        if user_id is not None:

            cursor.execute(
                """
                UPDATE student_accounts
                SET student_id = ?
                WHERE user_id = ?
                """,
                (
                    student_id,
                    user_id
                )
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    "Student account could not be linked to the profile."
                )

        # ----------------------------------------------------
        # REMOVE OLD RELATED DATA
        # ----------------------------------------------------

        cursor.execute(
            """
            DELETE FROM education
            WHERE student_id = ?
            """,
            (student_id,)
        )

        cursor.execute(
            """
            DELETE FROM skills
            WHERE student_id = ?
            """,
            (student_id,)
        )

        cursor.execute(
            """
            DELETE FROM projects
            WHERE student_id = ?
            """,
            (student_id,)
        )

        cursor.execute(
            """
            DELETE FROM experience
            WHERE student_id = ?
            """,
            (student_id,)
        )

        cursor.execute(
            """
            DELETE FROM certifications
            WHERE student_id = ?
            """,
            (student_id,)
        )

        # ----------------------------------------------------
        # SAVE EDUCATION
        # ----------------------------------------------------

        for education in profile.education or []:

            if education and str(education).strip():

                cursor.execute(
                    """
                    INSERT INTO education (
                        student_id,
                        education
                    )
                    VALUES (?, ?)
                    """,
                    (
                        student_id,
                        str(education).strip()
                    )
                )

        # ----------------------------------------------------
        # SAVE SKILLS
        # ----------------------------------------------------

        for skill in profile.skills or []:

            if skill and str(skill).strip():

                cursor.execute(
                    """
                    INSERT INTO skills (
                        student_id,
                        skill
                    )
                    VALUES (?, ?)
                    """,
                    (
                        student_id,
                        str(skill).strip()
                    )
                )

        # ----------------------------------------------------
        # SAVE PROJECTS
        # ----------------------------------------------------

        for project in profile.projects or []:

            if project and str(project).strip():

                cursor.execute(
                    """
                    INSERT INTO projects (
                        student_id,
                        project
                    )
                    VALUES (?, ?)
                    """,
                    (
                        student_id,
                        str(project).strip()
                    )
                )

        # ----------------------------------------------------
        # SAVE EXPERIENCE
        # ----------------------------------------------------

        for experience in profile.experience or []:

            if experience and str(experience).strip():

                cursor.execute(
                    """
                    INSERT INTO experience (
                        student_id,
                        experience
                    )
                    VALUES (?, ?)
                    """,
                    (
                        student_id,
                        str(experience).strip()
                    )
                )

        # ----------------------------------------------------
        # SAVE CERTIFICATIONS
        # ----------------------------------------------------

        for certification in profile.certifications or []:

            if certification and str(certification).strip():

                cursor.execute(
                    """
                    INSERT INTO certifications (
                        student_id,
                        certification
                    )
                    VALUES (?, ?)
                    """,
                    (
                        student_id,
                        str(certification).strip()
                    )
                )

        connection.commit()

        return student_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ============================================================
# GET STUDENT PROFILE
# ============================================================

def get_student_profile(
    student_id: Optional[int] = None,
    user_id: Optional[int] = None
) -> Optional[StudentProfile]:
    """
    Retrieve a complete student profile.

    Either student_id or user_id may be supplied.
    user_id is preferred from authenticated UI flows.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # ----------------------------------------------------
        # RESOLVE STUDENT ID FROM USER ID
        # ----------------------------------------------------

        if user_id is not None:

            cursor.execute(
                """
                SELECT student_id
                FROM student_accounts
                WHERE user_id = ?
                LIMIT 1
                """,
                (user_id,)
            )

            account = cursor.fetchone()

            if account is None:
                return None

            student_id = account["student_id"]

            if student_id is None:
                return None

        if student_id is None:
            return None

        # ----------------------------------------------------
        # STUDENT
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                name,
                resume_text,
                resume_file_name,
                resume_file_size
            FROM student_profiles
            WHERE id = ?
            """,
            (student_id,)
        )

        student = cursor.fetchone()

        if student is None:
            return None

        # ----------------------------------------------------
        # EDUCATION
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT education
            FROM education
            WHERE student_id = ?
            ORDER BY id
            """,
            (student_id,)
        )

        education = [
            row["education"]
            for row in cursor.fetchall()
        ]

        # ----------------------------------------------------
        # SKILLS
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT skill
            FROM skills
            WHERE student_id = ?
            ORDER BY id
            """,
            (student_id,)
        )

        skills = [
            row["skill"]
            for row in cursor.fetchall()
        ]

        # ----------------------------------------------------
        # PROJECTS
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT project
            FROM projects
            WHERE student_id = ?
            ORDER BY id
            """,
            (student_id,)
        )

        projects = [
            row["project"]
            for row in cursor.fetchall()
        ]

        # ----------------------------------------------------
        # EXPERIENCE
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT experience
            FROM experience
            WHERE student_id = ?
            ORDER BY id
            """,
            (student_id,)
        )

        experience = [
            row["experience"]
            for row in cursor.fetchall()
        ]

        # ----------------------------------------------------
        # CERTIFICATIONS
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT certification
            FROM certifications
            WHERE student_id = ?
            ORDER BY id
            """,
            (student_id,)
        )

        certifications = [
            row["certification"]
            for row in cursor.fetchall()
        ]

        # ----------------------------------------------------
        # CREATE PROFILE OBJECT
        # ----------------------------------------------------

        return StudentProfile(
            id=student["id"],
            name=student["name"] or "",
            education=education,
            skills=skills,
            projects=projects,
            experience=experience,
            certifications=certifications,
            resume_text=student["resume_text"] or "",
            resume_file_name=student["resume_file_name"] or "",
            resume_file_size=student["resume_file_size"] or 0
        )

    finally:
        connection.close()


# ============================================================
# DELETE STUDENT PROFILE
# ============================================================

def delete_student_profile(
    student_id: int
):
    """
    Delete a student's complete profile.

    student_accounts.student_id is set to NULL by the database
    foreign-key rule before/when the profile is removed.
    """

    if student_id is None:
        raise ValueError("Student ID is required.")

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM student_profiles
            WHERE id = ?
            """,
            (student_id,)
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ============================================================
# CHECK WHETHER PROFILE EXISTS
# ============================================================

def student_profile_exists(
    student_id: int
) -> bool:
    """
    Check whether a student profile exists.
    """

    if student_id is None:
        return False

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM student_profiles
            WHERE id = ?
            LIMIT 1
            """,
            (student_id,)
        )

        return cursor.fetchone() is not None

    finally:
        connection.close()


# ============================================================
# COMPANY
# ============================================================

def create_company(
    company: Company
) -> int:
    """
    Create a new company and return its database ID.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO companies (
                company_name,
                email,
                website,
                industry,
                location,
                description,
                logo_url
            )

            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                company.company_name,
                company.email,
                company.website,
                company.industry,
                company.location,
                company.description,
                company.logo_url
            )
        )

        company_id = cursor.lastrowid

        connection.commit()

        return company_id

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


# ============================================================
# GET COMPANY
# ============================================================

def get_company(
    company_id: int
) -> Optional[Company]:
    """
    Retrieve a company by ID.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                company_name,
                email,
                website,
                industry,
                location,
                description,
                logo_url

            FROM companies

            WHERE id = ?
            """,
            (company_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return Company(
            id=row["id"],
            company_name=row["company_name"] or "",
            email=row["email"] or "",
            website=row["website"] or "",
            industry=row["industry"] or "",
            location=row["location"] or "",
            description=row["description"] or "",
            logo_url=row["logo_url"] or ""
        )

    finally:

        connection.close()


# ============================================================
# GET ALL COMPANIES
# ============================================================

def get_all_companies() -> List[Company]:
    """
    Retrieve all companies.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                company_name,
                email,
                website,
                industry,
                location,
                description,
                logo_url

            FROM companies

            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        return [
            Company(
                id=row["id"],
                company_name=row["company_name"] or "",
                email=row["email"] or "",
                website=row["website"] or "",
                industry=row["industry"] or "",
                location=row["location"] or "",
                description=row["description"] or "",
                logo_url=row["logo_url"] or ""
            )
            for row in rows
        ]

    finally:

        connection.close()


# ============================================================
# UPDATE COMPANY
# ============================================================

def update_company(
    company: Company
) -> bool:
    """
    Update an existing company.
    """

    if company.id is None:
        raise ValueError(
            "Company ID is required for update."
        )

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE companies

            SET
                company_name = ?,
                email = ?,
                website = ?,
                industry = ?,
                location = ?,
                description = ?,
                logo_url = ?,
                updated_at = CURRENT_TIMESTAMP

            WHERE id = ?
            """,
            (
                company.company_name,
                company.email,
                company.website,
                company.industry,
                company.location,
                company.description,
                company.logo_url,
                company.id
            )
        )

        connection.commit()

        return cursor.rowcount > 0

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


# ============================================================
# DELETE COMPANY
# ============================================================

def delete_company(
    company_id: int
):
    """
    Delete a company.

    All jobs belonging to the company will also be deleted
    because of the database foreign-key cascade.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM companies
            WHERE id = ?
            """,
            (company_id,)
        )

        connection.commit()

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


# ============================================================
# CREATE JOB
# ============================================================

def create_job(
    job: Job
) -> int:
    """
    Create a job and save its required skills.
    """

    if job.company_id is None:
        raise ValueError(
            "Company ID is required to create a job."
        )

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # ----------------------------------------------------
        # CREATE JOB
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT INTO jobs (
                company_id,
                title,
                description,
                location,
                employment_type,
                experience_required,
                education_required,
                salary_min,
                salary_max,
                status
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job.company_id,
                job.title,
                job.description,
                job.location,
                job.employment_type,
                job.experience_required,
                job.education_required,
                job.salary_min,
                job.salary_max,
                job.status
            )
        )

        job_id = cursor.lastrowid

        # ----------------------------------------------------
        # SAVE REQUIRED SKILLS
        # ----------------------------------------------------

        for skill in job.skills:

            if skill and str(skill).strip():

                cursor.execute(
                    """
                    INSERT INTO job_skills (
                        job_id,
                        skill
                    )

                    VALUES (?, ?)
                    """,
                    (
                        job_id,
                        str(skill).strip()
                    )
                )

        connection.commit()

        return job_id

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


# ============================================================
# GET JOB
# ============================================================

def get_job(
    job_id: int
) -> Optional[Job]:
    """
    Retrieve a job including its required skills.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # ----------------------------------------------------
        # JOB
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                company_id,
                title,
                description,
                location,
                employment_type,
                experience_required,
                education_required,
                salary_min,
                salary_max,
                status

            FROM jobs

            WHERE id = ?
            """,
            (job_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        # ----------------------------------------------------
        # JOB SKILLS
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT skill
            FROM job_skills
            WHERE job_id = ?
            ORDER BY id
            """,
            (job_id,)
        )

        skills = [
            skill_row["skill"]
            for skill_row in cursor.fetchall()
        ]

        return Job(
            id=row["id"],
            company_id=row["company_id"],
            title=row["title"] or "",
            description=row["description"] or "",
            location=row["location"] or "",
            employment_type=row["employment_type"] or "",
            experience_required=(
                row["experience_required"] or 0.0
            ),
            education_required=(
                row["education_required"] or ""
            ),
            salary_min=row["salary_min"],
            salary_max=row["salary_max"],
            status=row["status"] or "active",
            skills=skills
        )

    finally:

        connection.close()


# ============================================================
# GET COMPANY JOBS
# ============================================================

def get_company_jobs(
    company_id: int,
    status: Optional[str] = None
) -> List[Job]:
    """
    Retrieve all jobs belonging to a company.

    If status is provided, only jobs with that status
    are returned.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        if status is None:

            cursor.execute(
                """
                SELECT
                    id,
                    company_id,
                    title,
                    description,
                    location,
                    employment_type,
                    experience_required,
                    education_required,
                    salary_min,
                    salary_max,
                    status

                FROM jobs

                WHERE company_id = ?

                ORDER BY id DESC
                """,
                (company_id,)
            )

        else:

            cursor.execute(
                """
                SELECT
                    id,
                    company_id,
                    title,
                    description,
                    location,
                    employment_type,
                    experience_required,
                    education_required,
                    salary_min,
                    salary_max,
                    status

                FROM jobs

                WHERE company_id = ?
                AND status = ?

                ORDER BY id DESC
                """,
                (
                    company_id,
                    status
                )
            )

        rows = cursor.fetchall()

        jobs = []

        for row in rows:

            cursor.execute(
                """
                SELECT skill
                FROM job_skills
                WHERE job_id = ?
                ORDER BY id
                """,
                (row["id"],)
            )

            skills = [
                skill_row["skill"]
                for skill_row in cursor.fetchall()
            ]

            jobs.append(
                Job(
                    id=row["id"],
                    company_id=row["company_id"],
                    title=row["title"] or "",
                    description=row["description"] or "",
                    location=row["location"] or "",
                    employment_type=(
                        row["employment_type"] or ""
                    ),
                    experience_required=(
                        row["experience_required"] or 0.0
                    ),
                    education_required=(
                        row["education_required"] or ""
                    ),
                    salary_min=row["salary_min"],
                    salary_max=row["salary_max"],
                    status=row["status"] or "active",
                    skills=skills
                )
            )

        return jobs

    finally:

        connection.close()


# ============================================================
# GET ALL ACTIVE JOBS
# ============================================================

def get_all_active_jobs() -> List[Job]:
    """
    Retrieve all active jobs from all companies.

    This function is used by the student Job Discovery page.
    It returns only jobs whose status is exactly ``active`` and
    includes the required skills for each job.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                company_id,
                title,
                description,
                location,
                employment_type,
                experience_required,
                education_required,
                salary_min,
                salary_max,
                status

            FROM jobs

            WHERE LOWER(status) = 'active'

            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        jobs = []

        for row in rows:

            cursor.execute(
                """
                SELECT skill
                FROM job_skills
                WHERE job_id = ?
                ORDER BY id
                """,
                (row["id"],)
            )

            skills = [
                skill_row["skill"]
                for skill_row in cursor.fetchall()
            ]

            jobs.append(
                Job(
                    id=row["id"],
                    company_id=row["company_id"],
                    title=row["title"] or "",
                    description=row["description"] or "",
                    location=row["location"] or "",
                    employment_type=(
                        row["employment_type"] or ""
                    ),
                    experience_required=(
                        row["experience_required"] or 0.0
                    ),
                    education_required=(
                        row["education_required"] or ""
                    ),
                    salary_min=row["salary_min"],
                    salary_max=row["salary_max"],
                    status=row["status"] or "active",
                    skills=skills
                )
            )

        return jobs

    finally:

        connection.close()


# ============================================================
# UPDATE JOB STATUS
# ============================================================

def update_job_status(
    job_id: int,
    status: str
) -> bool:
    """
    Update the status of a job.

    Examples:
        active
        closed
        draft
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE jobs

            SET
                status = ?,
                updated_at = CURRENT_TIMESTAMP

            WHERE id = ?
            """,
            (
                status,
                job_id
            )
        )

        connection.commit()

        return cursor.rowcount > 0

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


# ============================================================
# DELETE JOB
# ============================================================

def delete_job(
    job_id: int
):
    """
    Delete a job.

    Required skills and applications are also deleted
    because of database foreign-key cascades.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM jobs
            WHERE id = ?
            """,
            (job_id,)
        )

        connection.commit()

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


# ============================================================
# CREATE JOB APPLICATION
# ============================================================

def create_job_application(
    application: JobApplication
) -> int:
    """
    Create a job application for a student.
    """

    if application.job_id is None:
        raise ValueError(
            "Job ID is required."
        )

    if application.student_id is None:
        raise ValueError(
            "Student ID is required."
        )

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO job_applications (
                job_id,
                student_id,
                match_score,
                application_status
            )

            VALUES (?, ?, ?, ?)
            """,
            (
                application.job_id,
                application.student_id,
                application.match_score,
                application.application_status
            )
        )

        application_id = cursor.lastrowid

        connection.commit()

        return application_id

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


# ============================================================
# GET JOB APPLICATIONS
# ============================================================

def get_job_applications(
    job_id: int
) -> List[JobApplication]:
    """
    Retrieve all applications for a job.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                job_id,
                student_id,
                match_score,
                application_status

            FROM job_applications

            WHERE job_id = ?

            ORDER BY
                match_score DESC,
                id DESC
            """,
            (job_id,)
        )

        rows = cursor.fetchall()

        return [
            JobApplication(
                id=row["id"],
                job_id=row["job_id"],
                student_id=row["student_id"],
                match_score=row["match_score"],
                application_status=(
                    row["application_status"]
                    or "applied"
                )
            )
            for row in rows
        ]

    finally:

        connection.close()


# ============================================================
# UPDATE APPLICATION STATUS
# ============================================================

def update_application_status(
    application_id: int,
    status: str
) -> bool:
    """
    Update the status of a job application.

    Examples:
        applied
        shortlisted
        rejected
        hired
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE job_applications

            SET
                application_status = ?,
                updated_at = CURRENT_TIMESTAMP

            WHERE id = ?
            """,
            (
                status,
                application_id
            )
        )

        connection.commit()

        return cursor.rowcount > 0

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
    print("      CareerIQ Repository Test")
    print("==========================================")
    print()

    print(
        "Student profile test requires an explicit authenticated "
        "user ID or student profile ID."
    )

    companies = get_all_companies()

    print(
        "Companies:",
        len(companies)
    )

    print()
    print(
        "Repository test completed."
    )
    print()
