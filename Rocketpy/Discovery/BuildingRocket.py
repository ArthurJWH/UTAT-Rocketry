from rocketpy import Rocket
# from rocketpy import RailButtons, NoseCone, TrapezoidalFins, Tail, Parachute

""" Defining rocket primary parameters """
rocket = Rocket(
    radius=15.2 / 200,
    mass=33.973,  # rocket's mass without the motor in kg
    inertia=(
        6.321,
        6.321,
        0.034,
    ),  # in relation to the rocket's center of mass without motor
    power_off_drag="Drag_Curve_Unpowered.csv",
    power_on_drag="Drag_Curve_Powered.csv",
    center_of_mass_without_motor=2.34,
    coordinate_system_orientation="nose_to_tail",
)

''' Adding the motor '''
import BuildingGenericMotor

motor = BuildingGenericMotor.generic_motor

rocket.add_motor(motor, position = 4.105)

""" Adding the rail guide """
rail_buttons = rocket.set_rail_buttons(
    # rail_buttons,
    upper_button_position=4.3282,
    lower_button_position=3.7912,
    angular_position=45,
)

""" Adding aerodynamic components """

""" Nose cone """
nose_cone = rocket.add_nose(length=0.451, kind="ogive", position=0.04)

""" Fins """
fin_set = rocket.add_trapezoidal_fins(
    n=3,
    root_chord=0.298,
    tip_chord=0.139,
    span=0.152,
    cant_angle=0,
    sweep_length=0.14,
    airfoil=("Airfoil.csv", "radians"),
    position= 4.112)

""" Diameter Transition """
transition = rocket.add_tail(
    top_radius=15.2 / 200,     
    bottom_radius=16.5 / 200,  
    length=0.635 / 100,        
    position=3.517,            
)
""" Adding parachute """

main = rocket.add_parachute(
    name="main",
    cd_s=16.07,
    trigger=304.8,  # ejection altitude in meters
    sampling_rate=105,
    lag=1.5,
)

drogue = rocket.add_parachute(
    name="drogue",
    cd_s= 0.591,
    trigger="apogee",  # ejection at apogee
    sampling_rate=105,
    lag=1.5,
)

# rocket.plots.static_margin()

#rocket.draw()
#rocket.info()
