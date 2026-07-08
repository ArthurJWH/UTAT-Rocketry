from rocketpy import Environment

""" Defining the Environment """

""" Location """
env = Environment(latitude=47.9657667, longitude=-81.8736056, elevation=423)

""" Time """
import datetime

flight_day= datetime.date(2026, 8, 24)

env.set_date(
    (flight_day.year, flight_day.month, flight_day.day, 12)
)  # Hour given in UTC time

""" Atmospheric Model """
env.set_atmospheric_model(
    type="custom_atmosphere", wind_u = 3, wind_v = 4)  # "custom_atmosphere", wind_v, wind_u

# env.info()
