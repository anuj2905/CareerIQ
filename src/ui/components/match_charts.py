import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# CAREERIQ MATCH CHART COMPONENTS
# ============================================================

def _normalize_score(score):
    """
    Convert a score into a safe 0-1 range.

    Supports:
        0.85  -> 0.85
        85    -> 0.85
    """

    try:
        score = float(score)
    except (TypeError, ValueError):
        score = 0.0

    # Support percentage values.
    if score > 1:
        score = score / 100

    return max(
        0.0,
        min(score, 1.0)
    )


def _score_percentage(score):
    """
    Convert normalized score to percentage.
    """

    return _normalize_score(score) * 100


def _score_status(score):
    """
    Return a simple descriptive status for the score.
    """

    percentage = _score_percentage(score)

    if percentage >= 85:
        return "Excellent Match"

    if percentage >= 70:
        return "Strong Match"

    if percentage >= 50:
        return "Moderate Match"

    return "Needs Improvement"


def _score_color(score):
    """
    Return a visual color based on match strength.
    """

    percentage = _score_percentage(score)

    if percentage >= 85:
        return "#11A9B5"

    if percentage >= 70:
        return "#6C63FF"

    if percentage >= 50:
        return "#F59E0B"

    return "#EF4444"


# ============================================================
# CIRCULAR MATCH CHART
# ============================================================

def create_match_circle(
    score,
    label,
    size=130,
    subtitle=None,
):
    """
    Create a professional circular match indicator.

    Parameters
    ----------
    score : float
        Score from 0-1 or 0-100.

    label : str
        Main label displayed below the circle.

    size : int
        Circle diameter in pixels.

    subtitle : str | None
        Optional secondary text.
    """

    normalized_score = _normalize_score(score)

    percentage = normalized_score * 100

    color = _score_color(
        normalized_score
    )

    inner_size = size * 0.76

    font_size = max(
        22,
        size * 0.18
    )

    status = _score_status(
        normalized_score
    )

    subtitle_html = ""

    if subtitle:

        subtitle_html = f"""
        <div style="
            margin-top:4px;
            color:#718096;
            font-size:11px;
            text-align:center;
        ">
            {subtitle}
        </div>
        """

    return f"""
    <div style="
        width:100%;
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        font-family:
            Inter,
            Arial,
            sans-serif;
        box-sizing:border-box;
    ">

        <!-- CIRCLE -->

        <div style="
            width:{size}px;
            height:{size}px;
            border-radius:50%;

            background:
                conic-gradient(
                    {color} {percentage}%,
                    #E8EDF2 {percentage}% 100%
                );

            display:flex;
            align-items:center;
            justify-content:center;

            box-shadow:
                0 10px 30px rgba(7,59,92,0.10);
        ">

            <div style="
                width:{inner_size}px;
                height:{inner_size}px;

                border-radius:50%;

                background:#FFFFFF;

                display:flex;
                flex-direction:column;
                align-items:center;
                justify-content:center;

                box-shadow:
                    inset 0 0 0 1px
                    rgba(7,59,92,0.06);
            ">

                <div style="
                    color:#073B5C;
                    font-size:{font_size}px;
                    font-weight:850;
                    line-height:1;
                    letter-spacing:-1px;
                ">
                    {percentage:.0f}%
                </div>

                <div style="
                    margin-top:6px;
                    color:#718096;
                    font-size:10px;
                    font-weight:650;
                ">
                    MATCH
                </div>

            </div>

        </div>


        <!-- LABEL -->

        <div style="
            margin-top:13px;

            color:#073B5C;

            font-size:15px;

            font-weight:800;

            text-align:center;
        ">
            {label}
        </div>


        <!-- STATUS -->

        <div style="
            margin-top:5px;

            color:{color};

            font-size:11px;

            font-weight:750;

            text-align:center;
        ">
            {status}
        </div>

        {subtitle_html}

    </div>
    """


# ============================================================
# MATCH BREAKDOWN CARD
# ============================================================

def _create_breakdown_card(
    score,
    icon,
    label,
    description,
):
    """
    Create a compact horizontal match breakdown card.
    """

    percentage = _score_percentage(score)

    color = _score_color(score)

    return f"""
    <div style="
        width:100%;

        padding:18px;

        border-radius:18px;

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.96),
                rgba(247,249,251,0.96)
            );

        border:
            1px solid rgba(7,59,92,0.10);

        box-shadow:
            0 8px 25px rgba(7,59,92,0.06);

        font-family:
            Inter,
            Arial,
            sans-serif;

        box-sizing:border-box;
    ">

        <!-- HEADER -->

        <div style="
            display:flex;
            align-items:center;
            justify-content:space-between;
        ">

            <div style="
                display:flex;
                align-items:center;
                gap:9px;
            ">

                <div style="
                    width:34px;
                    height:34px;

                    border-radius:10px;

                    display:flex;
                    align-items:center;
                    justify-content:center;

                    background:
                        rgba(17,169,181,0.09);

                    font-size:16px;
                ">
                    {icon}
                </div>

                <div>

                    <div style="
                        color:#073B5C;

                        font-size:13px;

                        font-weight:800;
                    ">
                        {label}
                    </div>

                    <div style="
                        color:#7A8997;

                        font-size:10px;

                        margin-top:2px;
                    ">
                        {description}
                    </div>

                </div>

            </div>


            <div style="
                color:{color};

                font-size:20px;

                font-weight:850;
            ">
                {percentage:.0f}%
            </div>

        </div>


        <!-- PROGRESS BAR -->

        <div style="
            width:100%;

            height:8px;

            margin-top:15px;

            border-radius:999px;

            background:#E8EDF2;

            overflow:hidden;
        ">

            <div style="
                width:{percentage}%;

                height:100%;

                border-radius:999px;

                background:
                    linear-gradient(
                        90deg,
                        {color},
                        #11A9B5
                    );
            ">
            </div>

        </div>

    </div>
    """


# ============================================================
# OVERALL MATCH HERO
# ============================================================

def _create_overall_match_html(
    score
):
    """
    Create the main Overall Match hero card.
    """

    normalized_score = _normalize_score(
        score
    )

    percentage = normalized_score * 100

    color = _score_color(
        normalized_score
    )

    status = _score_status(
        normalized_score
    )

    return f"""
    <div style="
        width:100%;

        min-height:300px;

        padding:30px;

        border-radius:24px;

        background:
            radial-gradient(
                circle at 88% 8%,
                rgba(17,169,181,0.16),
                transparent 28%
            ),

            radial-gradient(
                circle at 8% 92%,
                rgba(108,99,255,0.12),
                transparent 28%
            ),

            #FFFFFF;

        border:
            1px solid rgba(7,59,92,0.10);

        box-shadow:
            0 15px 45px rgba(7,59,92,0.08);

        font-family:
            Inter,
            Arial,
            sans-serif;

        box-sizing:border-box;

        display:flex;

        flex-direction:column;

        align-items:center;

        justify-content:center;
    ">

        <!-- LABEL -->

        <div style="
            color:#627586;

            font-size:12px;

            font-weight:750;

            letter-spacing:1px;

            text-transform:uppercase;
        ">
            AI-Powered Match Analysis
        </div>


        <!-- SCORE -->

        <div style="
            position:relative;

            width:190px;
            height:190px;

            margin-top:18px;

            border-radius:50%;

            background:
                conic-gradient(
                    {color} {percentage}%,
                    #E8EDF2 {percentage}% 100%
                );

            display:flex;

            align-items:center;

            justify-content:center;
        ">

            <div style="
                width:145px;
                height:145px;

                border-radius:50%;

                background:#FFFFFF;

                display:flex;

                flex-direction:column;

                align-items:center;

                justify-content:center;

                box-shadow:
                    0 4px 18px rgba(7,59,92,0.08);
            ">

                <div style="
                    color:#073B5C;

                    font-size:42px;

                    font-weight:900;

                    line-height:1;

                    letter-spacing:-2px;
                ">
                    {percentage:.0f}%
                </div>

                <div style="
                    margin-top:7px;

                    color:#718096;

                    font-size:10px;

                    font-weight:700;

                    letter-spacing:.7px;
                ">
                    OVERALL MATCH
                </div>

            </div>

        </div>


        <!-- STATUS -->

        <div style="
            margin-top:17px;

            padding:7px 15px;

            border-radius:999px;

            color:{color};

            background:rgba(17,169,181,0.08);

            border:
                1px solid rgba(17,169,181,0.13);

            font-size:12px;

            font-weight:800;
        ">
            {status}
        </div>

    </div>
    """


# ============================================================
# SHOW JOB MATCH DASHBOARD
# ============================================================

def show_job_match_dashboard(
    skill_score,
    education_score,
    experience_score,
    overall_score,
):
    """
    Display the complete CareerIQ job match dashboard.

    Existing function signature is preserved so current
    application code does not need to change.
    """

    # ========================================================
    # SECTION HEADER
    # ========================================================

    st.html(
        """
        <div style="
            margin-top:8px;
            margin-bottom:18px;
        ">

            <div style="
                color:#073B5C;
                font-size:25px;
                font-weight:850;
                letter-spacing:-0.6px;
            ">
                🏆 Job Match Analysis
            </div>

            <div style="
                margin-top:5px;
                color:#718096;
                font-size:12px;
            ">
                AI-generated compatibility analysis based on
                your profile and the job requirements.
            </div>

        </div>
        """
    )


    # ========================================================
    # OVERALL MATCH
    # ========================================================

    overall_html = _create_overall_match_html(
        overall_score
    )

    components.html(
        overall_html,
        height=330,
        scrolling=False,
    )


    # ========================================================
    # BREAKDOWN HEADER
    # ========================================================

    st.html(
        """
        <div style="
            margin-top:22px;
            margin-bottom:15px;
        ">

            <div style="
                color:#073B5C;
                font-size:20px;
                font-weight:820;
            ">
                📊 Match Breakdown
            </div>

            <div style="
                margin-top:4px;
                color:#718096;
                font-size:11px;
            ">
                See how each part of your profile contributes
                to the overall match.
            </div>

        </div>
        """
    )


    # ========================================================
    # SCORE CARDS
    # ========================================================

    col1, col2, col3 = st.columns(
        3,
        gap="medium",
    )


    # ========================================================
    # SKILLS
    # ========================================================

    with col1:

        skill_html = _create_breakdown_card(
            score=skill_score,
            icon="💻",
            label="Skills",
            description="Technical skill compatibility",
        )

        components.html(
            skill_html,
            height=145,
            scrolling=False,
        )


    # ========================================================
    # EDUCATION
    # ========================================================

    with col2:

        education_html = _create_breakdown_card(
            score=education_score,
            icon="🎓",
            label="Education",
            description="Education requirement match",
        )

        components.html(
            education_html,
            height=145,
            scrolling=False,
        )


    # ========================================================
    # EXPERIENCE
    # ========================================================

    with col3:

        experience_html = _create_breakdown_card(
            score=experience_score,
            icon="💼",
            label="Experience",
            description="Experience requirement match",
        )

        components.html(
            experience_html,
            height=145,
            scrolling=False,
        )


    # ========================================================
    # CIRCULAR COMPONENT
    # ========================================================

    st.html(
        """
        <div style="
            margin-top:25px;
            margin-bottom:10px;
            color:#073B5C;
            font-size:18px;
            font-weight:800;
        ">
            🎯 Detailed Scores
        </div>
        """
    )


    detail_col1, detail_col2, detail_col3 = st.columns(
        3,
        gap="large",
    )


    # ========================================================
    # SKILL CIRCLE
    # ========================================================

    with detail_col1:

        skill_circle = create_match_circle(
            score=skill_score,
            label="💻 Skills",
            size=120,
            subtitle="Technical compatibility",
        )

        components.html(
            skill_circle,
            height=190,
            scrolling=False,
        )


    # ========================================================
    # EDUCATION CIRCLE
    # ========================================================

    with detail_col2:

        education_circle = create_match_circle(
            score=education_score,
            label="🎓 Education",
            size=120,
            subtitle="Academic compatibility",
        )

        components.html(
            education_circle,
            height=190,
            scrolling=False,
        )


    # ========================================================
    # EXPERIENCE CIRCLE
    # ========================================================

    with detail_col3:

        experience_circle = create_match_circle(
            score=experience_score,
            label="💼 Experience",
            size=120,
            subtitle="Professional compatibility",
        )

        components.html(
            experience_circle,
            height=190,
            scrolling=False,
        )