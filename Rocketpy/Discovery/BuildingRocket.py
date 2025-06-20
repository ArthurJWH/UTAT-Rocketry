from rocketpy import Rocket
# from rocketpy import RailButtons, NoseCone, TrapezoidalFins, Tail, Parachute

""" Defining rocket primary parameters """
rocket = Rocket(
    radius=15.2 / 200,
    mass=48.622,  # rocket's mass without the motor in kg
    inertia=(
        6.321,
        6.321,
        0.034,
    ),  # in relation to the rocket's center of mass without motor
    power_off_drag="Rocketpy/Discovery/Curves/DragCurve.csv",
    power_on_drag="Rocketpy/Discovery/Curves/DragCurve.csv",
    center_of_mass_without_motor=2.22,
    coordinate_system_orientation="tail_to_nose",
)

''' Adding the motor '''
from Motors import BuildingGenericMotor

motor = BuildingGenericMotor.generic_motor

rocket.add_motor(motor, position = -1.255)

""" Adding the rail guide """
rail_buttons = rocket.set_rail_buttons(
    # rail_buttons,
    upper_button_position=0.0818,
    lower_button_position=-0.6182,
    angular_position=45,
)

""" Adding aerodynamic components """

""" Nose cone """
nose_cone = rocket.add_nose(length=0.559, kind="von karman", position=1.278)

""" Fins """
fin_set = rocket.add_trapezoidal_fins(
    n=4,
    root_chord=0.120,
    tip_chord=0.060,
    span=0.110,
    cant_angle=0.5,
    airfoil=("Rocketpy/Discovery/Airfoils/Airfoil.csv", "radians"),
    position=-1.04956
)

""" Tail """
tail = rocket.add_tail(
    top_radius=0.0635, bottom_radius=0.0435, length=0.060, position=-1.194656
)

""" Adding parachute """

main = rocket.add_parachute(
    name="main",
    cd_s=10.0,
    trigger=800,  # ejection altitude in meters
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

drogue = rocket.add_parachute(
    name="drogue",
    cd_s=1.0,
    trigger="apogee",  # ejection at apogee
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

# rocket.plots.static_margin()

# rocket.draw()
