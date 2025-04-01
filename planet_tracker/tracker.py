from skyfield.api import load, Topos
from datetime import datetime, timezone


def get_planet_position(planet_name, observer_lat, observer_lon):

    planets = load('de421.bsp')  # Load planetary ephemeris
    earth, planet = planets['earth'], planets[planet_name]

    ts = load.timescale()
    t = ts.now()

    observer = earth + Topos(latitude_degrees=observer_lat, longitude_degrees=observer_lon)
    astrometric = observer.at(t).observe(planet).apparent()

    ra, dec, distance = astrometric.radec()
    alt, az, _ = astrometric.altaz()

    return {
        "Right Ascension": ra.hours,
        "Declination": dec.degrees,
        "Altitude": alt.degrees,
        "Azimuth": az.degrees
    }


if __name__ == "__main__":
    planet_name = "Mars"  # Change this to the planet you want to track
    observer_lat = 40.7128  # Example: New York City latitude
    observer_lon = -74.0060  # Example: New York City longitude

    position = get_planet_position(planet_name, observer_lat, observer_lon)
    print(f"{planet_name} Position:")
    for key, value in position.items():
        print(f"{key}: {value}")
