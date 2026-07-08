from rocketpy import Rocket
# from rocketpy import RailButtons, NoseCone, TrapezoidalFins, Tail, Parachute

""" Defining rocket primary parameters """
rocket = Rocket(
    radius=15.2 / 200,
    mass=34.954,  # rocket's mass without the motor and propellant in kg
    inertia=( 
        56.7, # (1/4) * mass * radius^2 + (1/12) * mass * length^2
        56.7, # (1/4) * mass * radius^2 + (1/12) * mass * length^2
        0.101, # (1/2) * mass * radius^2
    ),  # in relation to the rocket's center of mass without motor
    power_off_drag="DragCurve.csv",
    power_on_drag="DragCurve.csv",
    center_of_mass_without_motor=2.22,
    coordinate_system_orientation="tail_to_nose",
)

""" Adding the motor """
from rocketpy.motors import LiquidMotor, Fluid, MassFlowRateBasedTank, CylindricalTank

oxidizer = Fluid(name="N2O", density=1220)
fuel = Fluid(name="ethanol", density=789)

shape_oxidizer_tank = CylindricalTank(radius=0.074, height=0.64)
shape_fuel_tank = CylindricalTank(radius=0.074, height=0.254)

oxidizer_tank = MassFlowRateBasedTank(
    name="oxidizer tank",
    liquid=oxidizer,
    geometry=shape_oxidizer_tank,
    flux_time=4,
    initial_liquid_mass=7.010,
    liquid_mass_flow_rate_in=0,
    liquid_mass_flow_rate_out=lambda t: 1.753 * t,
)

fuel_tank = MassFlowRateBasedTank(
    name="fuel tank",
    liquid=fuel,
    geometry=shape_fuel_tank,
    flux_time=4,
    initial_liquid_mass=2.420,
    liquid_mass_flow_rate_in=0,
    liquid_mass_flow_rate_out=lambda t: 0.605 * t,
)

motor = LiquidMotor(
    thrust_source="thrust.csv",
    dry_mass=9.780, # referring to "Engine Section" of Discovery's mass distribution spreadsheet
    center_of_dry_mass_position=0.1953, # UPDATE
    # dry_inertia=( , , ),
    nozzle_position=0,
    nozzle_radius=0.06,
    burn_time=4.56,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

motor.add_tank(tank=oxidizer_tank, position=0.8904)
motor.add_tank(tank=fuel_tank, position=1.8274)

""" Adding the rail guide 
rail_buttons = rocket.set_rail_buttons(
    upper_button_position=0.0818,
    lower_button_position=0.6182,
    angular_position=45,
) """

""" Adding aerodynamic components """

""" Nose cone """
nose_cone = rocket.add_nose(length=0.451, kind="ogive", position=4.41)

""" Fins """
fin_set = rocket.add_trapezoidal_fins(
    n=3,
    root_chord=0.298,
    tip_chord=0.139,
    span=0.152, # height of a single fin
    cant_angle=0,
    sweep_length=0.14,
    airfoil=("Airfoil.csv", "radians"),
    position=0.298,)

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
motor.info()
