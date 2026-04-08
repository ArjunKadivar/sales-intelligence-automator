def validate_output(data):
    required_keys = [
        "company_overview",
        "core_service",
        "target_customer",
        "b2b_qualified",
        "sales_questions"
    ]

    for key in required_keys:
        if key not in data:
            return False

    if len(data["sales_questions"]) != 3:
        return False

    return True