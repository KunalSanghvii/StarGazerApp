import numpy as np
from skyfield.api import load
from datetime import datetime, timedelta
from tracker import PlanetaryData

class PlanetClosestApproach:
    def find_closet_approach(self,start_date, end_date):
        start_time = self.ts.utc(start_date.year, start_date.month, start_date.day)
        end_time = self.ts.utc(end_date.year, end_date.month, end_date.day)

        time_range = [start_time + i * (end_time - start_time) / 365 for i in range(0, 365)]  # roughly 365 steps for a year

        # Initialize variables to track the closest approach
        closest_time = None
        min_distance = float('inf')

        # Calculate the distance at each time step
        earth = self.eph["earth"]
        target_planet = self.bodies[self.planet_name]

        for t in time_range:
            astrometric = earth.at(t).observe(target_planet).apparent()
            distance = astrometric.distance().km  # Distance in kilometers

            # If we find a closer distance, update the closest_time and min_distance
            if distance < min_distance:
                min_distance = distance
                closest_time = t

        # Convert the closest time to a human-readable format
        closest_time_dt = datetime.utcfromtimestamp(closest_time.utc_iso())
        return closest_time_dt, min_distance
