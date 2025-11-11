from rocketpy import Rocket
# from rocketpy import RailButtons, NoseCone, TrapezoidalFins, Tail, Parachute

""" Defining rocket primary parameters """
rocket = Rocket(
    radius=15.2 / 200,
    mass=66.032,  # rocket's mass without the motor in kg
    inertia=(
        6.321,
        6.321,
        0.034,
    ),  # in relation to the rocket's center of mass without motor
    power_off_drag="DragCurve.csv",
    power_on_drag="DragCurve.csv",
    center_of_mass_without_motor=2.01,
    coordinate_system_orientation="tail_to_nose",
)

''' Adding the motor '''
import BuildingGenericMotor

motor = BuildingGenericMotor.generic_motor

rocket.add_motor(motor, position = 0)

""" Adding the rail guide """
rail_buttons = rocket.set_rail_buttons(
    # rail_buttons,
    upper_button_position=0.0818,
    lower_button_position=0.6182,
    angular_position=45,
)

""" Adding aerodynamic components """

""" Nose cone """
nose_cone = rocket.add_nose(length=0.461, kind="ogive", position=4.269)

""" Fins """
fin_set = rocket.add_trapezoidal_fins(
    n=3,
    root_chord=0.19,
    tip_chord=0.060,
    span=0.12,
    cant_angle=0,
    sweep_length=0.165,
    airfoil=("Airfoil.csv", "radians"),
    position= 0.205)

""" Tail """
'''boat_tail = rocket.add_tail(
    bottom_radius=0.0762,
    top_radius=0.1016,
    length=0.1524,
    position=0,
)'''

""" Adding parachute """

main = rocket.add_parachute(
    name="main",
    cd_s=10.0,
    trigger=800,  # ejection altitude in meters
    sampling_rate=105,
    lag=1.5,
)

drogue = rocket.add_parachute(
    name="drogue",
    cd_s=1.0,
    trigger="apogee",  # ejection at apogee
    sampling_rate=105,
    lag=1.5,
)

# rocket.plots.static_margin()

rocket.draw()
rocket.info()
