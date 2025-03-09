from rocketpy import Flight

import DefiningEnvironment
import BuildingRocket

test_flight = Flight(
    rocket=BuildingRocket.rocket,
    environment=DefiningEnvironment.env,
    rail_length=4,  # metres
    inclination=90,  # degrees
    heading=0,  # degrees
)

test_flight.info()
# test_flight.export_kml("trajectory.kml")
