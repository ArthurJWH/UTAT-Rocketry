from rocketpy import Flight

import DefiningEnvironment
import BuildingRocket

test_flight = Flight(
    rocket=BuildingRocket.rocket,
    environment=DefiningEnvironment.env,
    rail_length=5.2,  # metres
    inclination=85,  # degrees
    heading=0,  # degrees
)

test_flight.info()
# test_flight.export_kml("trajectory.kml")
