def normalize_lead(lead: str):
    lead = lead.strip()

    if lead.startswith("http"):
        return lead

    # Convert business name → Google search URL (simple version)
    query = lead.replace(" ", "+")
    return f"https://www.google.com/search?q={query}"