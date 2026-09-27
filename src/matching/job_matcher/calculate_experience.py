def calculate_experience_match(
    user_years,
    required_years
):
    """
    Calculate experience years match score.

    Rules:
    - If the job does not require experience, return 100%.
    - If the user has equal or more experience than required, return 100%.
    - Otherwise, calculate the proportional match.

    Returns:
        float: Score between 0.0 and 1.0
    """

    # Validate values
    if user_years is None or required_years is None:
        return 0.0

    try:
        user_years = float(user_years)
        required_years = float(required_years)
    except (ValueError, TypeError):
        return 0.0

    # Negative experience is invalid
    user_years = max(0.0, user_years)
    required_years = max(0.0, required_years)

    # No experience required
    if required_years == 0:
        return 1.0

    # User meets or exceeds the requirement
    if user_years >= required_years:
        return 1.0

    # User has less experience than required
    return round(user_years / required_years, 4)


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    test_cases = [
        (3, 5),
        (5, 5),
        (7, 5),
        (0, 2),
        (3, 0)
    ]

    for user_years, required_years in test_cases:

        score = calculate_experience_match(
            user_years,
            required_years
        )

        print(
            f"User: {user_years} years | "
            f"Required: {required_years} years | "
            f"Match: {score * 100:.2f}%"
        )