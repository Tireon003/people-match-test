import math
from fastapi_cache.decorator import cache


@cache(expire=120)
def calculate_distance(
        lat1: int | float,
        lon1: int | float,
        lat2: int | float,
        lon2: int | float,
) -> float:

    earth_radius = 6371

    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(
        math.radians,
        [lat1, lon1, lat2, lon2]
    )

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance_km = earth_radius * c

    return distance_km
