from rocketpy.motors import GenericMotor

""" Defining the thrust curve"""


def thrust_curve_function(t):  # load .csv table of time and thrust
    return 10000 - 100 * t**2


generic_motor = GenericMotor(
    thrust_source="Rocketpy/Discovery/Curves/enginefilev4.csv",
    chamber_radius=0.1,
    chamber_height=1.2,
    chamber_position=1.0,
    dry_mass=10,
    propellant_initial_mass=21,
    center_of_dry_mass_position=1.75,
    dry_inertia=(0.125, 0.125, 0.002),
    nozzle_radius=11.5 / 200,
    burn_time=6,
    nozzle_position=0,
    interpolation_method="linear",
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

# generic_motor.exhaust_velocity
# generic_motor.mass_flow_rate
# generic_motor.info()
