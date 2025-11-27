# utils.py
def build_classification_url(country: str, classification: str):
    """
    Build:
        base_url = https://id.jobstreet.com
        route    = /jobs-in-accounting
        full_url = https://id.jobstreet.com/jobs-in-accounting
    """

    if not country or len(country) != 2:
        raise ValueError("Country code must be 2 letters, e.g., 'id', 'my', 'ph'.")

    if classification.startswith("/"):
        classification = classification[1:]

    if not classification.startswith("jobs-in-"):
        raise ValueError("Job classification must start with 'jobs-in-'.")

    base_url = f"https://{country}.jobstreet.com"
    route = f"/{classification}"
    full_url = base_url + route

    return base_url, route, full_url
