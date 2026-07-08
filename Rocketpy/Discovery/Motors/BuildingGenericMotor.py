from rocketpy.motors import GenericMotor

""" Defining the thrust curve"""


def thrust_curve_function(t):  # load .csv table of time and thrust
    return 10000 - 100 * t**2


generic_motor = GenericMotor(
    thrust_source="Rocketpy/Discovery/Curves/enginefilev4.csv",
    chamber_radius=0.259,
    chamber_height=0.198,
    chamber_position=0.099,
    dry_mass=9.375,
    propellant_initial_mass=0,
    dry_inertia=(0.125, 0.125, 0.002),
    nozzle_radius=0.043,
    burn_time=4.58,
    nozzle_position=1.095,
    interpolation_method="linear",
    coordinate_system_orientation="combustion_chamber_to_nozzle",
)

# generic_motor.exhaust_velocity
# generic_motor.mass_flow_rate
# generic_motor.info()
