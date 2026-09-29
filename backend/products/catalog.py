"""Sample product data and the beginner-friendly search function."""

PRODUCTS = [
    {"name": "Acer Aspire 5", "category": "laptop", "brand": "Acer", "price": 47999, "ram": "16GB", "storage": "512GB", "storage_type": "SSD", "color": "Silver"},
    {"name": "Lenovo IdeaPad Slim 3", "category": "laptop", "brand": "Lenovo", "price": 49999, "ram": "16GB", "storage": "512GB", "storage_type": "SSD", "color": "Grey"},
    {"name": "ASUS Vivobook 15", "category": "laptop", "brand": "ASUS", "price": 42990, "ram": "8GB", "storage": "512GB", "storage_type": "SSD", "color": "Blue"},
    {"name": "HP 15s", "category": "laptop", "brand": "HP", "price": 45990, "ram": "8GB", "storage": "512GB", "storage_type": "SSD", "color": "Natural Silver"},
    {"name": "Dell Inspiron 14", "category": "laptop", "brand": "Dell", "price": 58990, "ram": "16GB", "storage": "512GB", "storage_type": "SSD", "color": "Black"},
    {"name": "MSI Modern 14", "category": "laptop", "brand": "MSI", "price": 62990, "ram": "16GB", "storage": "512GB", "storage_type": "SSD", "color": "Black"},
    {"name": "Lenovo V15", "category": "laptop", "brand": "Lenovo", "price": 38990, "ram": "8GB", "storage": "256GB", "storage_type": "SSD", "color": "Black"},
    {"name": "ASUS TUF Gaming F15", "category": "laptop", "brand": "ASUS", "price": 69990, "ram": "16GB", "storage": "512GB", "storage_type": "SSD", "color": "Black"},
    {"name": "HP Pavilion x360", "category": "laptop", "brand": "HP", "price": 67990, "ram": "16GB", "storage": "512GB", "storage_type": "SSD", "color": "Silver"},
    {"name": "Acer Aspire Lite", "category": "laptop", "brand": "Acer", "price": 35990, "ram": "8GB", "storage": "512GB", "storage_type": "SSD", "color": "Steel Grey"},
    {"name": "Samsung Galaxy M55", "category": "mobile", "brand": "Samsung", "price": 19999, "ram": "8GB", "storage": "128GB", "color": "Blue"},
    {"name": "Motorola Edge 50 Fusion", "category": "mobile", "brand": "Motorola", "price": 22999, "ram": "8GB", "storage": "256GB", "color": "Pink"},
    {"name": "Redmi Note 13 Pro", "category": "mobile", "brand": "Redmi", "price": 18999, "ram": "8GB", "storage": "256GB", "color": "Black"},
    {"name": "OnePlus Nord CE 4 Lite", "category": "mobile", "brand": "OnePlus", "price": 17999, "ram": "8GB", "storage": "128GB", "color": "Silver"},
    {"name": "iQOO Z9", "category": "mobile", "brand": "iQOO", "price": 19999, "ram": "8GB", "storage": "128GB", "color": "Green"},
    {"name": "Samsung Galaxy A35", "category": "mobile", "brand": "Samsung", "price": 24999, "ram": "8GB", "storage": "128GB", "color": "Navy"},
    {"name": "Realme Narzo 70 Pro", "category": "mobile", "brand": "Realme", "price": 19999, "ram": "8GB", "storage": "128GB", "color": "Green"},
    {"name": "POCO X6", "category": "mobile", "brand": "POCO", "price": 21999, "ram": "8GB", "storage": "256GB", "color": "Black"},
    {"name": "Nothing Phone (2a)", "category": "mobile", "brand": "Nothing", "price": 23999, "ram": "8GB", "storage": "128GB", "color": "White"},
    {"name": "Motorola G64", "category": "mobile", "brand": "Motorola", "price": 14999, "ram": "8GB", "storage": "128GB", "color": "Blue"},
]


def search_products(
    category=None,
    brand=None,
    max_price=None,
    min_price=None,
    ram=None,
    storage=None,
    color=None,
):
    """Return products matching the filters that were provided."""
    matches = PRODUCTS

    if category:
        category = category.casefold().rstrip("s")
        matches = [item for item in matches if item["category"] == category]
    if brand:
        matches = [item for item in matches if item["brand"].casefold() == brand.casefold()]
    if max_price is not None:
        matches = [item for item in matches if item["price"] <= max_price]
    if min_price is not None:
        matches = [item for item in matches if item["price"] >= min_price]
    if ram:
        matches = [item for item in matches if item["ram"].casefold() == ram.casefold()]
    if storage:
        matches = [item for item in matches if item["storage"].casefold() == storage.casefold()]
    if color:
        matches = [item for item in matches if color.casefold() in item["color"].casefold()]

    return matches