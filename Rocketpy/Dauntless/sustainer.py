from rocketpy import Rocket

rocket = Rocket(
    radius=11.4 / 200,
    mass=3.703,  # rocket's mass without the motor in kg
    inertia=( 
        1.364, # (1/4) * mass * radius^2 + (1/12) * mass * length^2
        1.364, # (1/4) * mass * radius^2 + (1/12) * mass * length^2
        0.00602 # (1/2) * mass * radius^2
    ),  # in relation to the rocket's center of mass without motor
    power_off_drag="drag.csv",
    power_on_drag="drag.csv",
    center_of_mass_without_motor=0.92,
    coordinate_system_orientation="tail_to_nose",
)

nose_cone = rocket.add_nose(length=0.572, kind="von karman", position=2.1)

fin_set = rocket.add_trapezoidal_fins(
    n=3,
    root_chord=0.305,
    tip_chord=0.0508,
    span=0.102,
    cant_angle=0,
    sweep_length=0.254,
    airfoil=("airfoil.csv", "radians"),
    position=0,)

parachute_nosecone = rocket.add_parachute(
    name="main",
    cd_s=1.358, # reference area * drag coefficient
    trigger="apogee",  # ejection altitude in meters
    sampling_rate=105,
    lag=0,
)

parachute_body = rocket.add_parachute(
    name="main",
    cd_s=1.358, # reference area * drag coefficient
    trigger="apogee",  # ejection altitude in meters
    sampling_rate=105,
    lag=0,
)

from rocketpy.motors import SolidMotor

motor = SolidMotor(
    thrust_source="thrust.csv",
    dry_mass=2.932,
    burn_time=3.27,
    dry_inertia=(0.2722, 0.2722, 0.0037551),
    grain_number=6,
    grain_density=1080,
    grain_outer_radius=0.0375,
    grain_initial_inner_radius=0.015,
    grain_initial_height=0.1691,
    grain_separation=0,
    grains_center_of_mass_position=0.5125,
    center_of_dry_mass_position=0.5125,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

rocket.add_motor(motor, position=0.104)