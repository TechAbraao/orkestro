""" Collection of functions responsible for caching strategies and keys """

def cache_key(include):
    key = "menus:all"
    if include:
        key += ":" + ":".join(sorted(include))
    return key

def get_cache_key_by_slug(slug: str, include_categories=True, include_products=False):
    key = f"menu:{slug}"
    if include_categories:
        key += ":categories"
    if include_products:
        key += ":products"
    return key