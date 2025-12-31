import difflib


def find_similar_menu_slug(target_slug: str, all_slugs: list[str]) -> str | None:
    matches = difflib.get_close_matches(
        target_slug,
        all_slugs,
        n=1,
        cutoff=0.4
    )

    return matches[0] if matches else None
