from dataclasses import dataclass

@dataclass
class Brand:
    name: str
    url_name: str


@dataclass
class Product:
    name: str
    description: str | None
    price: float
    image: str

brands: list[Brand] = [
    Brand("Chint", "chint-103"),
    Brand("Steck", "steck-166"),
    Brand("Prasek", "prasek-124"),
    Brand("Narita", "narita-217"),
    Brand("General Eléctric", "g-e-144"),
    Brand("Camsco", "camsco-104"),
    Brand("Autonics", "autonics-102"),
    Brand("Mennekes", "mennekes-139"),
    Brand("BTicino", "bticino-145"),
]
