import numpy as np
import pandas as pd
from rocketpy import Rocket
from rocketpy import RailButtons, NoseCone, TrapezoidalFins, Tail, Parachute
# Engine.info()

# curve_drag = pd.read_csv("Rocketpy/Curves/DragCurve.csv", sep = ', ')
# print(curve_drag.time)

''' Defining rocket primary parameters '''
rocket = Rocket(
    radius = 127 / 2000,
    mass = 14.426,        # rocket's mass without the motor in kg
    inertia = (6.321, 6.321, 0.034),      # in relation to the rocket's center of mass without motor
    power_off_drag = "Curves/DragCurve.csv",
    power_on_drag = "Curves/DragCurve.csv",
    center_of_mass_without_motor = 0,
    coordinate_system_orientation = "tail_to_nose",
)

# ''' Defining the motor '''
# from Motors import BuildingLiquidMotor

# motor = BuildingLiquidMotor.liquid_motor

''' Defining the rail guide '''
# rail_buttons = RailButtons(
#     buttons_distance = 0.7,
#     angular_position = 45
# )

''' Defining the nose cone'''
# nose_cone = NoseCone(
#     length = 0.55829,
#     rocket_radius = rocket.radius,
#     kind = "von karman"
# )

''' Defining fins'''
# fin_set = TrapezoidalFins(
#     n = 4,
#     rocket_radius = rocket.radius,
#     root_chord = 0.120,
#     tip_chord = 0.060,
#     span = 0.110,
#     cant_angle = 0.5,
#     airfoil = ("Airfoils/Airfoil.csv","radians")
# )

# ''' Adding the motor '''
# rocket.add_motor(motor, position = -1.255)

''' Adding the rail guide '''
rail_buttons = rocket.set_rail_buttons(
    # rail_buttons,
    upper_button_position = 0.0818,
    lower_button_position = -0.6182,
    angular_position = 45
)

''' Adding aerodynamic components '''

''' Nose cone '''
nose_cone = rocket.add_nose(
    length = 0.55829,
    kind = "von karman",
    position = 1.278
)

''' Fins '''
fin_set = rocket.add_trapezoidal_fins(
    n = 4,
    root_chord = 0.120,
    tip_chord = 0.060,
    span = 0.110,
    cant_angle = 0.5,
    airfoil = ("Airfoils/Airfoil.csv","radians"),
    position=-1.04956
    # fin_set
)

''' Tail '''
tail = rocket.add_tail(
    top_radius = 0.0635, bottom_radius = 0.0435, length = 0.060, position = -1.194656
)

''' Adding parachute '''

main = rocket.add_parachute(
    name = "main",
    cd_s = 10.0,
    trigger = 800,        # ejection altitude in meters
    sampling_rate = 105,
    lag = 1.5,
    noise = (0, 8.3, 0.5),
)

drogue = rocket.add_parachute(
    name = "drogue",
    cd_s = 1.0,
    trigger = "apogee",  # ejection at apogee
    sampling_rate = 105,
    lag = 1.5,
    noise = (0, 8.3, 0.5),
)

# rocket.plots.static_margin()

# rocket.draw()
