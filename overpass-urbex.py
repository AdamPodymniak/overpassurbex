import overpy
from geopy import distance

def get_abandoned_buildings(latitude, longitude, radius):
    api = overpy.Overpass()

    bbox = calculate_bounding_box(latitude, longitude, radius)

    query = (
        f'[out:json];'
        f'(node[military=bunker]{bbox};'
        f'way[military=bunker]{bbox};'
        f'relation[military=bunker]{bbox};);'
        f'out center;'
    )

    result = api.query(query)

    abandoned_buildings = []
    for element in result.ways + result.nodes + result.relations:
        if element.tags.get("building") == "bunker":
            if isinstance(element, overpy.Way) or isinstance(element, overpy.Relation):
                lat = element.center_lat
                lon = element.center_lon
            else:
                lat = element.lat
                lon = element.lon
            abandoned_buildings.append((element.id, lat, lon))

    return abandoned_buildings

def calculate_bounding_box(latitude, longitude, radius):
    center = (latitude, longitude)
    destination = distance.distance(kilometers=radius).destination(center, 45)

    bbox = (
        min(latitude, destination.latitude),
        min(longitude, destination.longitude),
        max(latitude, destination.latitude),
        max(longitude, destination.longitude),
    )

    return bbox

input_latitude = float(input("Input latitude: "))
input_longitude = float(input("Input longitude: "))
input_radius = float(input("Input radius (km): "))

abandoned_buildings = get_abandoned_buildings(input_latitude, input_longitude, input_radius)

for building in abandoned_buildings:
    building_id, lat, lon = building
    print(f"LatLng: {lat}, {lon}")
