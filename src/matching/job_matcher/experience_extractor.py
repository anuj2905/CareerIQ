import ast
import re
from datetime import datetime


# ==========================================
# 1. Clean dataset values
# ==========================================

def clean_list_data(data):
    """
    Convert dataset values into a Python list.

    Example:

    "['2020-01-01', '2022-05-01']"

    becomes:

    ['2020-01-01', '2022-05-01']
    """

    # Handle None / empty values
    if data is None:
        return []

    # Handle NaN values
    if isinstance(data, float):

        try:
            if data != data:
                return []

        except Exception:
            pass

    # Already a Python list
    if isinstance(data, list):
        return data

    data = str(data).strip()

    if not data:
        return []


    # Dataset stores list as string
    if data.startswith("[") and data.endswith("]"):

        try:

            parsed_data = ast.literal_eval(data)

            if isinstance(parsed_data, list):
                return parsed_data

        except (
            ValueError,
            SyntaxError
        ):
            return []


    # Single value
    return [data]


# ==========================================
# 2. Parse date
# ==========================================

def parse_date(date_value):
    """
    Convert different date formats into datetime.
    """

    if date_value is None:
        return None

    date_value = str(date_value).strip()

    if not date_value:
        return None


    # Current employment
    current_values = {
        "present",
        "current",
        "till date",
        "now",
        "ongoing"
    }

    if date_value.lower() in current_values:
        return datetime.now()


    date_formats = [

        "%Y-%m-%d",
        "%d-%m-%Y",
        "%m-%d-%Y",

        "%Y/%m/%d",
        "%d/%m/%Y",
        "%m/%d/%Y",

        "%Y-%m",
        "%m/%Y",

        "%b %Y",
        "%B %Y",

        "%Y"
    ]


    for date_format in date_formats:

        try:

            return datetime.strptime(
                date_value,
                date_format
            )

        except ValueError:
            continue


    return None


# ==========================================
# 3. Calculate user experience years
# ==========================================

def calculate_total_experience(
    start_dates,
    end_dates
):
    """
    Calculate total experience years from
    start_dates and end_dates.
    """

    start_list = clean_list_data(
        start_dates
    )

    end_list = clean_list_data(
        end_dates
    )


    if not start_list:
        return 0.0


    total_days = 0


    # Loop through each job
    for index, start_value in enumerate(
        start_list
    ):

        start_date = parse_date(
            start_value
        )

        if not start_date:
            continue


        # Get matching end date
        if index < len(end_list):

            end_date = parse_date(
                end_list[index]
            )

        else:

            # If end date is missing,
            # assume current employment
            end_date = datetime.now()


        if not end_date:
            end_date = datetime.now()


        # Ignore invalid dates
        if end_date < start_date:
            continue


        experience_days = (
            end_date - start_date
        ).days


        total_days += experience_days


    # Convert days to years
    total_years = (
        total_days / 365.25
    )


    return round(
        total_years,
        2
    )


# ==========================================
# 4. Extract required experience years
# ==========================================

def extract_required_experience(
    experience_requirement
):
    """
    Extract required experience years
    from job requirements.

    Examples:

    '3 years of experience'
        → 3

    'Minimum 5 years experience'
        → 5

    '2-4 years of experience'
        → 2

    'Freshers can apply'
        → 0
    """

    if experience_requirement is None:
        return 0.0


    text = str(
        experience_requirement
    ).lower()


    if not text.strip():
        return 0.0


    # No experience required
    no_experience_patterns = [

        "fresher",
        "freshers",
        "no experience required",
        "no prior experience",
        "entry level",
        "entry-level"
    ]


    for pattern in no_experience_patterns:

        if pattern in text:
            return 0.0


    # --------------------------------------
    # Experience range
    # Example: 2-5 years
    # --------------------------------------

    range_match = re.search(

        r"(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",

        text
    )


    if range_match:

        # Use minimum requirement
        return float(
            range_match.group(1)
        )


    # --------------------------------------
    # Single value
    # Example: 5 years
    # --------------------------------------

    year_match = re.search(

        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",

        text
    )


    if year_match:

        return float(
            year_match.group(1)
        )


    return 0.0


# ==========================================
# 5. Extract complete experience information
# ==========================================

def extract_experience_data(
    start_dates,
    end_dates,
    experience_requirement
):
    """
    Extract:

    user_years
    required_years
    """


    user_years = calculate_total_experience(
        start_dates,
        end_dates
    )


    required_years = extract_required_experience(
        experience_requirement
    )


    return {

        "user_years":
            user_years,

        "required_years":
            required_years
    }


# ==========================================
# 6. Test
# ==========================================

if __name__ == "__main__":

    start_dates = (
        "['2020-01-01', '2022-06-01']"
    )

    end_dates = (
        "['2022-05-01', '2024-01-01']"
    )

    experience_requirement = (
        "Minimum 5 years of experience"
    )


    result = extract_experience_data(

        start_dates=start_dates,

        end_dates=end_dates,

        experience_requirement=
        experience_requirement
    )


    print("User Experience Years:")
    print(result["user_years"])


    print("\nRequired Experience Years:")
    print(result["required_years"])