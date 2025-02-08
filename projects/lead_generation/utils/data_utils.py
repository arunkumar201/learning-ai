def is_duplicate_venue(venue_name: str, seen_names: set) -> bool:
    return venue_name in seen_names


def is_complete_venue(venue: dict, required_keys: list) -> bool:
    return all(key in venue for key in required_keys)


def save_venues_to_xlsx(venues: list, filename: str):
    if not venues:
        print("No venues to save.")
        return

    if not filename.endswith(".xlsx"):
        filename += ".xlsx"
    import pandas as pd

    df = pd.DataFrame(venues)
    df.to_excel(filename, index=False)
    print(f"Saved {len(venues)} venues to '{filename}'.")
