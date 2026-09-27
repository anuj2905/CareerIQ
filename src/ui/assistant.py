import streamlit as st

from src.rag.career_assistant import ask_career_assistant


# ============================================================
# SESSION STATE
# ============================================================

if "assistant_question" not in st.session_state:
    st.session_state["assistant_question"] = ""

if "assistant_answer" not in st.session_state:
    st.session_state["assistant_answer"] = ""

if "assistant_last_question" not in st.session_state:
    st.session_state["assistant_last_question"] = ""


# ============================================================
# PAGE STYLING
# ============================================================

def style_assistant_page():
    """CareerIQ light documentation-style UI using st.html()."""

    st.html(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 12% 18%, rgba(22,184,190,.13), transparent 25%),
                radial-gradient(circle at 88% 32%, rgba(235,92,157,.10), transparent 28%),
                linear-gradient(135deg, #f8f7ec 0%, #f5f8f4 48%, #fbf1ed 100%);
        }

        [data-testid="stHeader"] {
            background: rgba(248,247,236,.92);
            border-bottom: 1px solid rgba(10,67,94,.14);
        }

        [data-testid="stToolbar"] {
            visibility: hidden;
            height: 0;
        }

        [data-testid="stDecoration"] {
            display: none;
        }

        [data-testid="stAppViewContainer"] > .main {
            background-image:
                radial-gradient(rgba(14,128,144,.20) 1px, transparent 1px);
            background-size: 28px 28px;
        }

        .block-container {
            max-width: 1180px !important;
            padding-top: 2.1rem !important;
            padding-bottom: 3rem !important;
        }

        div[data-testid="stButton"] > button {
            border-radius: 12px !important;
            border: 1px solid rgba(11,74,99,.15) !important;
            background: rgba(255,255,255,.84) !important;
            color: #0a4562 !important;
            font-weight: 650 !important;
            min-height: 44px !important;
            box-shadow: 0 5px 18px rgba(12,60,76,.06) !important;
            transition: all .18s ease !important;
        }

        div[data-testid="stButton"] > button:hover {
            border-color: #10aeb1 !important;
            color: #07516b !important;
            transform: translateY(-1px);
            box-shadow: 0 8px 24px rgba(16,174,177,.14) !important;
        }

        div[data-testid="stButton"] > button[kind="primary"] {
            background: linear-gradient(135deg, #07516b, #10aeb1) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 10px 26px rgba(7,81,107,.22) !important;
        }

        div[data-testid="stTextArea"] textarea {
            border-radius: 16px !important;
            border: 1px solid rgba(8,76,98,.18) !important;
            background: rgba(255,255,255,.82) !important;
            color: #123c50 !important;
            box-shadow: 0 8px 28px rgba(15,63,76,.06) !important;
            padding: 16px !important;
        }

        div[data-testid="stTextArea"] textarea:focus {
            border-color: #10aeb1 !important;
            box-shadow: 0 0 0 2px rgba(16,174,177,.12) !important;
        }

        @media (max-width: 800px) {
            .block-container {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }
        }
        </style>
        """
    )


# ============================================================
# HERO
# ============================================================

def show_hero():
    st.html(
        """
        <div style="
            position:relative;
            overflow:hidden;
            padding:34px 38px 32px;
            border-radius:24px;
            margin-bottom:22px;
            background:
                radial-gradient(circle at 92% 20%, rgba(231,82,151,.16), transparent 27%),
                radial-gradient(circle at 8% 85%, rgba(16,174,177,.18), transparent 28%),
                rgba(255,255,255,.72);
            border:1px solid rgba(8,73,96,.13);
            box-shadow:0 18px 45px rgba(16,62,78,.09);
            backdrop-filter:blur(10px);
        ">
            <div style="
                display:inline-flex;
                padding:7px 13px;
                border-radius:999px;
                background:rgba(16,174,177,.11);
                border:1px solid rgba(16,174,177,.18);
                color:#087286;
                font-size:13px;
                font-weight:750;
                margin-bottom:13px;
            ">🤖 AI CAREER INTELLIGENCE</div>

            <div style="
                font-size:clamp(30px,4vw,46px);
                line-height:1.06;
                font-weight:850;
                letter-spacing:-1.4px;
                color:#073f5d;
                margin-bottom:12px;
            ">Your AI Career Assistant</div>

            <div style="
                max-width:760px;
                font-size:16px;
                line-height:1.7;
                color:#587080;
            ">
                Ask CareerIQ about careers, skills, learning paths,
                projects, interviews and job preparation. Your answers
                are personalized using your resume and career knowledge.
            </div>

            <div style="
                margin-top:22px;
                height:3px;
                max-width:920px;
                border-radius:99px;
                background:linear-gradient(90deg,#12afb2,#5977c9,#e85d9d,transparent);
            "></div>
        </div>
        """
    )


# ============================================================
# INFORMATION CARDS
# ============================================================

def show_info_cards():

    cards = [
        ("🎯", "Personalized",
         "Guidance based on your resume, skills and current career profile."),
        ("🧠", "Knowledge-Based",
         "Answers are grounded in CareerIQ's career intelligence and knowledge."),
        ("🚀", "Action-Oriented",
         "Practical next steps instead of generic career advice."),
    ]

    columns = st.columns(3, gap="medium")

    for column, (icon, title, description) in zip(columns, cards):
        with column:
            st.html(
                f"""
                <div style="
                    min-height:145px;
                    padding:21px 20px;
                    border-radius:19px;
                    background:rgba(255,255,255,.76);
                    border:1px solid rgba(8,73,96,.12);
                    box-shadow:0 10px 28px rgba(16,62,78,.055);
                    backdrop-filter:blur(8px);
                ">
                    <div style="
                        width:42px;height:42px;display:flex;
                        align-items:center;justify-content:center;
                        border-radius:13px;
                        background:linear-gradient(
                            135deg,rgba(16,174,177,.13),
                            rgba(232,93,157,.10)
                        );
                        font-size:21px;margin-bottom:13px;
                    ">{icon}</div>

                    <div style="
                        font-size:16px;font-weight:800;
                        color:#0a4662;margin-bottom:6px;
                    ">{title}</div>

                    <div style="
                        font-size:13px;line-height:1.55;color:#68808c;
                    ">{description}</div>
                </div>
                """
            )


# ============================================================
# PROFILE STATUS
# ============================================================

def show_profile_status(profile):

    if profile is None:
        st.html(
            """
            <div style="
                margin-top:22px;padding:16px 18px;border-radius:15px;
                background:rgba(255,248,229,.86);
                border:1px solid rgba(201,151,37,.25);
                color:#73570c;font-size:14px;line-height:1.55;
            ">
                📄 <b>No resume profile is available yet.</b>
                Upload and analyze your resume first so CareerIQ can
                personalize your answers.
            </div>
            """
        )
        return

    name = getattr(profile, "name", "") or ""

    label = (
        f"Career assistant personalized for <b>{name}</b>."
        if name
        else "Your resume profile is connected to CareerIQ."
    )

    st.html(
        f"""
        <div style="
            margin-top:22px;padding:14px 18px;border-radius:15px;
            background:rgba(232,250,242,.80);
            border:1px solid rgba(24,155,105,.20);
            color:#176747;font-size:14px;
        ">✅ {label}</div>
        """
    )


# ============================================================
# QUICK QUESTIONS
# ============================================================

def show_quick_questions():

    st.html(
        """
        <div style="
            margin-top:25px;margin-bottom:10px;
            font-size:15px;font-weight:800;color:#0a4662;
        ">💡 Try asking</div>
        """
    )

    col1, col2 = st.columns(2, gap="medium")

    with col1:

        if st.button("🎯  What should I learn next?", use_container_width=True):
            st.session_state["assistant_question"] = (
                "Based on my resume, what should I learn next?"
            )
            st.rerun()

        if st.button("💼  Which career roles suit me?", use_container_width=True):
            st.session_state["assistant_question"] = (
                "Based on my resume, which career roles "
                "would suit my current skills?"
            )
            st.rerun()

    with col2:

        if st.button("🧠  What skills am I missing?", use_container_width=True):
            st.session_state["assistant_question"] = (
                "Based on my resume, what important skills "
                "am I currently missing for an AI or ML career?"
            )
            st.rerun()

        if st.button("📚  Give me a learning roadmap", use_container_width=True):
            st.session_state["assistant_question"] = (
                "Create a practical learning roadmap for "
                "becoming a Machine Learning Engineer based "
                "on my current skills."
            )
            st.rerun()


# ============================================================
# ASK ASSISTANT
# ============================================================

def ask_assistant(question: str, profile):

    with st.spinner("🧠 CareerIQ is analyzing your question..."):

        try:
            return ask_career_assistant(
                question=question,
                profile=profile,
            )

        except Exception as error:

            st.error(
                "Something went wrong while generating your career answer."
            )
            st.exception(error)

            return None


# ============================================================
# ANSWER CARD
# ============================================================

def show_answer(answer):

    if not answer:
        return

    last_question = st.session_state.get(
        "assistant_last_question",
        "",
    )

    question_html = ""
    if last_question:
        question_html = f"""
            <div style="
                margin-top:6px;color:#738792;font-size:12px;
                line-height:1.45;
            ">{last_question}</div>
        """

    st.html(
        f"""
        <div style="
            margin-top:28px;border-radius:20px;overflow:hidden;
            background:rgba(255,255,255,.82);
            border:1px solid rgba(8,73,96,.13);
            box-shadow:0 15px 40px rgba(16,62,78,.08);
        ">
            <div style="
                padding:15px 19px;
                background:linear-gradient(
                    90deg,rgba(7,81,107,.07),
                    rgba(16,174,177,.08),
                    rgba(232,93,157,.06)
                );
                border-bottom:1px solid rgba(8,73,96,.10);
            ">
                <div style="
                    font-size:14px;font-weight:800;color:#0a4662;
                ">🤖 CareerIQ Answer</div>
                {question_html}
            </div>
        </div>
        """
    )

    # The answer is generated Markdown, so native Markdown rendering
    # is intentionally retained only for the model response itself.
    st.markdown(answer)

    if st.button("🗑️ Clear Answer"):
        st.session_state["assistant_answer"] = ""
        st.session_state["assistant_last_question"] = ""
        st.session_state["assistant_question"] = ""
        st.rerun()


# ============================================================
# MAIN ASSISTANT PAGE
# ============================================================

def assistant_page():
    """Main AI Career Assistant page."""

    style_assistant_page()

    show_hero()

    profile = st.session_state.get("profile")

    show_profile_status(profile)

    show_info_cards()

    st.html(
        """
        <div style="margin-top:31px;">
            <div style="
                font-size:23px;font-weight:850;
                letter-spacing:-.3px;color:#073f5d;
            ">💬 Ask CareerIQ</div>

            <div style="
                margin-top:6px;color:#6a7f8b;font-size:14px;
                line-height:1.55;
            ">
                Ask anything about your career, skills, learning path,
                projects, interviews or job preparation.
            </div>
        </div>
        """
    )

    show_quick_questions()

    question = st.text_area(
        "Your question",
        key="assistant_question",
        placeholder=(
            "Example: Based on my resume, what should "
            "I learn next to become an ML Engineer?"
        ),
        height=130,
        label_visibility="collapsed",
    )

    st.html(
        """
        <div style="
            margin-top:8px;margin-bottom:8px;
            font-size:12px;color:#81929b;
        ">
            💡 Tip: Mention your target role, current skills,
            project or career goal for a more focused answer.
        </div>
        """
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        ask_clicked = st.button(
            "🤖  Ask CareerIQ",
            use_container_width=True,
            type="primary",
        )

    if ask_clicked:

        clean_question = question.strip()

        if not clean_question:
            st.warning("Please enter a question first.")

        elif profile is None:
            st.warning(
                "Please upload and analyze your resume first "
                "so CareerIQ can personalize the answer."
            )

        else:

            answer = ask_assistant(
                question=clean_question,
                profile=profile,
            )

            if answer:
                st.session_state["assistant_answer"] = answer
                st.session_state["assistant_last_question"] = clean_question
                st.rerun()

    answer = st.session_state.get("assistant_answer")

    if answer:
        show_answer(answer)

    st.html(
        """
        <div style="
            margin-top:42px;padding-top:18px;
            border-top:1px solid rgba(8,73,96,.10);
            text-align:center;color:#8798a0;font-size:12px;
        ">
            CareerIQ • AI-powered career intelligence
        </div>
        """
    )
