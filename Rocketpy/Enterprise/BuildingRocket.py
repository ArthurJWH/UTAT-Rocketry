from rocketpy import Rocket

""" Defining rocket primary parameters """
rocket = Rocket(
    radius=15.7 / 200,
    mass=18.2,  # rocket's mass without the motor in kg
    inertia=(
        7.503,
        7.503,
        0.05608,
    ),  # in relation to the rocket's center of mass without motor
    power_off_drag="Rocketpy/Enterprise/Curves/enterprise_drag.csv",
    power_on_drag="Rocketpy/Enterprise/Curves/enterprise_drag.csv",
    center_of_mass_without_motor=1.34,
    coordinate_system_orientation="tail_to_nose",
)

''' Adding the motor '''
from Motors import BuildingSolidMotor

motor = BuildingSolidMotor.solid_motor

rocket.add_motor(motor, position = 0.012)

""" Adding the rail guide """
rail_buttons = rocket.set_rail_buttons(
    upper_button_position=0.61,
    lower_button_position=0.00,
    angular_position=180,
)

""" Adding aerodynamic components """

""" Nose cone """
nose_cone = rocket.add_nose(length=0.657, kind="von karman", position=2.22)

""" Fins """
fin_set = rocket.add_trapezoidal_fins(
    n=3,
    root_chord=0.41,
    tip_chord=0.05,
    span=0.165,
    cant_angle=0.0,
    # airfoil=("Rocketpy/Enterprise/Airfoils/Airfoil.csv", "radians"),
    position=0.45,
    sweep_length=0.354,
    # sweep_angle=57.9,
)

""" Tail """
tail = rocket.add_tail(
    top_radius=0.0785, bottom_radius=0.04635, length=0.0356, position=0.03
)

""" Adding parachute """

main = rocket.add_parachute(
    name="main",
    cd_s=2.200,
    trigger=305,  # ejection altitude in meters
    sampling_rate=105,
    lag=0,
    noise=(0, 8.3, 0.5),
)

drogue = rocket.add_parachute(
    name="drogue",
    cd_s=0.800,
    trigger="apogee",  # ejection at apogee
    sampling_rate=105,
    lag=0,
    noise=(0, 8.3, 0.5),
)

# rocket.plots.static_margin()

# rocket.draw()
