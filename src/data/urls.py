
BASE_URL = "https://store.grupocoinp.com/shop/category/"

def pagination_definition(page: int = 1):
    if page > 1:
        return f"/page/{page}"
    else:
        return ""