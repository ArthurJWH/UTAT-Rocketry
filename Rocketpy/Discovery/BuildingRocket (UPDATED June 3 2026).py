from rocketpy import Rocket
# from rocketpy import RailButtons, NoseCone, TrapezoidalFins, Tail, Parachute

""" Defining rocket primary parameters """
rocket = Rocket(
    radius=15.2 / 200,
    mass=36.454,  # rocket's mass without the motor in kg
    inertia=( 
        43.919, # (1/4) * mass * radius^2 + (1/12) * mass * length^2
        43.919, # (1/4) * mass * radius^2 + (1/12) * mass * length^2
        0.1053, # (1/2) * mass * radius^2
    ),  # in relation to the rocket's center of mass without motor
    power_off_drag="DragCurve.csv",
    power_on_drag="DragCurve.csv",
    center_of_mass_without_motor=1.98,
    coordinate_system_orientation="tail_to_nose",
)

''' Adding the motor '''
import BuildingGenericMotor

motor = BuildingGenericMotor.generic_motor

rocket.add_motor(motor, position = 0)

""" Adding the rail guide """
rail_buttons = rocket.set_rail_buttons(
    upper_button_position=0.0818,
    lower_button_position=0.6182,
    angular_position=45,
)

""" Adding aerodynamic components """

""" Nose cone """
nose_cone = rocket.add_nose(length=0.451, kind="ogive", position=3.8)

""" Fins """
fin_set = rocket.add_trapezoidal_fins(
    n=3,
    root_chord=0.203,
    tip_chord=0.178,
    span=0.14,
    cant_angle=0,
    sweep_length=0.0509,
    airfoil=("Airfoil.csv", "radians"),
    position= 0.218,)

""" Adding parachute """

main = rocket.add_parachute(
    name="main",
    cd_s=16.074, # reference area * drag coefficient
    trigger=610,  # ejection altitude in meters
    sampling_rate=105,
)

drogue = rocket.add_parachute(
    name="drogue",
    cd_s=0.5905, # reference area * drag coefficient
    trigger="apogee",  # ejection altitude in meters
    sampling_rate=105,
    lag=2,
)

# rocket.plots.static_margin()

rocket.draw()
rocket.info()
