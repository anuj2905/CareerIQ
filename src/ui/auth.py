import streamlit as st

from src.auth.auth_repository import (
    create_user,
    authenticate_user,
)


# ============================================================
# AUTH PAGE STYLING
# ============================================================

def style_auth_page():
    """
    Styling for Login / Sign Up page.
    """

    st.html(
        """
        <style>

        /* ==================================================
           GLOBAL AUTH BACKGROUND
           ================================================== */

        .stApp {
            background:
                radial-gradient(
                    circle at 10% 10%,
                    rgba(17, 169, 181, 0.10),
                    transparent 25%
                ),
                radial-gradient(
                    circle at 90% 10%,
                    rgba(139, 92, 246, 0.09),
                    transparent 25%
                ),
                linear-gradient(
                    180deg,
                    #faf9f2 0%,
                    #f7f6ef 100%
                );
        }


        /* ==================================================
           MAIN CONTAINER
           ================================================== */

        .block-container {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }


        /* ==================================================
           AUTH WRAPPER
           ================================================== */

        .auth-container {
            max-width: 560px;
            margin: 35px auto 0;
        }


        /* ==================================================
           BRAND
           ================================================== */

        .auth-brand {
            text-align: center;
            color: #073b5c;
            font-size: 19px;
            font-weight: 850;
            letter-spacing: -0.3px;
        }


        .auth-brand-subtitle {
            text-align: center;
            color: #627586;
            font-size: 11px;
            font-weight: 650;
            margin-top: 3px;
        }


        /* ==================================================
           AUTH CARD
           ================================================== */

        .auth-card {
            margin-top: 28px;

            padding: 34px 38px 30px;

            border: 1px solid rgba(7, 59, 92, 0.13);

            border-radius: 24px;

            background:
                radial-gradient(
                    circle at 90% 4%,
                    rgba(17, 169, 181, 0.12),
                    transparent 24%
                ),
                rgba(255, 255, 255, 0.86);

            box-shadow:
                0 18px 55px rgba(7, 59, 92, 0.08);
        }


        /* ==================================================
           ROLE BADGE
           ================================================== */

        .auth-role {
            display: inline-block;

            padding: 6px 12px;

            border-radius: 999px;

            color: #12657b;

            background: rgba(17, 169, 181, 0.10);

            border: 1px solid rgba(17, 169, 181, 0.18);

            font-size: 10px;

            font-weight: 850;

            letter-spacing: 0.5px;

            text-transform: uppercase;
        }


        /* ==================================================
           TITLE
           ================================================== */

        .auth-title {
            color: #073b5c;

            font-size: 36px;

            line-height: 1.08;

            font-weight: 880;

            letter-spacing: -1.2px;

            margin-top: 14px;
        }


        /* ==================================================
           SUBTITLE
           ================================================== */

        .auth-subtitle {
            color: #627586;

            font-size: 13px;

            line-height: 1.7;

            margin-top: 9px;
        }


        /* ==================================================
           GRADIENT LINE
           ================================================== */

        .auth-gradient-line {
            height: 3px;

            width: 100%;

            margin: 21px 0 25px;

            border-radius: 999px;

            background:
                linear-gradient(
                    90deg,
                    #11a9b5,
                    #8b5cf6,
                    #ff5a36
                );
        }


        /* ==================================================
           FORM SECTION
           ================================================== */

        .auth-form-title {
            max-width: 560px;

            margin: 18px auto 0;

            color: #073b5c;

            font-size: 21px;

            font-weight: 820;
        }


        .auth-form-subtitle {
            max-width: 560px;

            margin: 4px auto 20px;

            color: #627586;

            font-size: 12px;
        }


        /* ==================================================
           INPUTS
           ================================================== */

        div[data-baseweb="input"] > div {

            background: rgba(255, 255, 255, 0.95) !important;

            border-color:
                rgba(7, 59, 92, 0.14) !important;

            border-radius: 12px !important;
        }


        label {

            color: #36546a !important;

            font-weight: 700 !important;
        }


        /* ==================================================
           BUTTONS
           ================================================== */

        .stButton > button {

            min-height: 44px;

            border-radius: 12px;

            font-weight: 780;
        }


        /* ==================================================
           TABS
           ================================================== */

        [data-testid="stTabs"] button {

            color: #49657a;

            font-weight: 750;
        }


        /* ==================================================
           SECURITY NOTE
           ================================================== */

        .auth-security-note {

            margin-top: 22px;

            padding: 12px 14px;

            border-radius: 12px;

            background: #f4f8f8;

            border: 1px solid
                rgba(17, 169, 181, 0.13);

            color: #5f7483;

            font-size: 11px;

            line-height: 1.6;

            text-align: center;
        }

        </style>
        """
    )


# ============================================================
# LOGIN
# ============================================================

def login_form(role):
    """
    Login form for Student or Company.
    """

    email = st.text_input(
        "Email",
        placeholder="you@example.com",
        key=f"{role}_login_email",
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password",
        key=f"{role}_login_password",
    )

    if st.button(
        "🔐 Login",
        use_container_width=True,
        type="primary",
        key=f"{role}_login_button",
    ):

        email = email.strip().lower()

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not email or not password:

            st.error(
                "Please enter both email and password."
            )

            return

        # ----------------------------------------------------
        # AUTHENTICATE
        # ----------------------------------------------------

        user = authenticate_user(
            email=email,
            password=password,
            role=role,
        )

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        if user:

            st.session_state["logged_in"] = True

            st.session_state["user_id"] = user["id"]

            st.session_state["user_email"] = user["email"]

            st.session_state["user_role"] = user["role"]

            # ------------------------------------------------
            # ROUTING
            # ------------------------------------------------

            if role == "company":

                st.session_state["page"] = (
                    "company_selector"
                )

            else:

                st.session_state["page"] = (
                    "student"
                )

            st.success(
                "Login successful!"
            )

            st.rerun()

        # ----------------------------------------------------
        # INVALID LOGIN
        # ----------------------------------------------------

        else:

            st.error(
                "Invalid email, password, or account type."
            )


# ============================================================
# SIGN UP
# ============================================================

def signup_form(role):
    """
    Sign Up form for Student or Company.
    """

    email = st.text_input(
        "Email",
        placeholder="you@example.com",
        key=f"{role}_signup_email",
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Minimum 8 characters",
        key=f"{role}_signup_password",
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        placeholder="Re-enter your password",
        key=f"{role}_signup_confirm_password",
    )

    if st.button(
        "✨ Create Account",
        use_container_width=True,
        type="primary",
        key=f"{role}_signup_button",
    ):

        email = email.strip().lower()

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if (
            not email
            or not password
            or not confirm_password
        ):

            st.error(
                "Please fill in all fields."
            )

            return

        if len(password) < 8:

            st.error(
                "Password must contain at least 8 characters."
            )

            return

        if password != confirm_password:

            st.error(
                "Passwords do not match."
            )

            return

        # ----------------------------------------------------
        # CREATE ACCOUNT
        # ----------------------------------------------------

        try:

            user_id = create_user(
                email=email,
                password=password,
                role=role,
            )

        except ValueError as exc:

            st.error(str(exc))

            return

        except Exception:

            st.error(
                "Unable to create your account right now. "
                "Please try again."
            )

            return

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        if user_id:

            st.session_state["logged_in"] = True

            st.session_state["user_id"] = user_id

            st.session_state["user_email"] = email

            st.session_state["user_role"] = role

            st.success(
                "Account created successfully!"
            )

            # ------------------------------------------------
            # ROUTING
            # ------------------------------------------------

            if role == "company":

                st.session_state["page"] = (
                    "company_selector"
                )

            else:

                st.session_state["page"] = (
                    "student"
                )

            st.rerun()

        else:

            st.error(
                "An account with this email already exists."
            )


# ============================================================
# AUTH PAGE
# ============================================================

def auth_page(role):
    """
    Login / Sign Up page.

    role:
        student
        company
    """

    # --------------------------------------------------------
    # APPLY STYLING
    # --------------------------------------------------------

    style_auth_page()

    # --------------------------------------------------------
    # ROLE INFORMATION
    # --------------------------------------------------------

    if role == "student":

        icon = "🎓"

        role_name = "Student"

        subtitle = (
            "Build your profile, discover opportunities, "
            "and plan your career with AI."
        )

    elif role == "company":

        icon = "🏢"

        role_name = "Company"

        subtitle = (
            "Create opportunities and discover "
            "relevant talent with AI."
        )

    else:

        st.error(
            "Invalid account type."
        )

        return

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.html(
        f"""
        <div class="auth-container">

            <div class="auth-brand">
                🧠 CareerIQ
            </div>

            <div class="auth-brand-subtitle">
                AI Career Intelligence Platform
            </div>

            <div class="auth-card">

                <div class="auth-role">
                    {icon} {role_name} Account
                </div>

                <div class="auth-title">
                    Welcome to CareerIQ
                </div>

                <div class="auth-subtitle">
                    {subtitle}
                </div>

                <div class="auth-gradient-line"></div>

            </div>

        </div>
        """
    )

    # --------------------------------------------------------
    # LOGIN / SIGNUP TABS
    # --------------------------------------------------------

    login_tab, signup_tab = st.tabs(
        [
            "🔐 Login",
            "✨ Create Account",
        ]
    )

    # ========================================================
    # LOGIN TAB
    # ========================================================

    with login_tab:

        st.html(
            """
            <div class="auth-form-title">
                Welcome back
            </div>

            <div class="auth-form-subtitle">
                Sign in to continue to your CareerIQ workspace.
            </div>
            """
        )

        login_form(role)

    # ========================================================
    # SIGNUP TAB
    # ========================================================

    with signup_tab:

        st.html(
            """
            <div class="auth-form-title">
                Create your account
            </div>

            <div class="auth-form-subtitle">
                Start building your AI-powered career profile.
            </div>
            """
        )

        signup_form(role)

    # --------------------------------------------------------
    # BACK TO HOME
    # --------------------------------------------------------

    st.divider()

    if st.button(
        "← Back to Home",
        use_container_width=True,
        key=f"{role}_back_home",
    ):

        st.session_state["page"] = "home"

        st.rerun()

    # --------------------------------------------------------
    # SECURITY NOTE
    # --------------------------------------------------------

    st.html(
        """
        <div class="auth-security-note">
            🔒 Your password is securely hashed before being stored.
        </div>
        """
    )