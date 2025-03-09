from rocketpy import Environment

""" Defining the Environment """

""" Location """
env = Environment(latitude=42.692624, longitude=-77.18899, elevation=2333)

""" Time """
import datetime

tomorrow = datetime.date.today() + datetime.timedelta(days=1)

env.set_date(
    (tomorrow.year, tomorrow.month, tomorrow.day, 12)
)  # Hour given in UTC time

""" Atmospheric Model """
env.set_atmospheric_model(
    type="Forecast", file="GFS"  # "custom_atmosphere", wind_v, wind_u
)

# env.info()
