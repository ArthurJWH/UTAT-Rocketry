from rocketpy.motors import SolidMotor

solid_motor = SolidMotor(
    thrust_source="Rocketpy/Enterprise/Curves/enterprise_thrust.csv",
    dry_mass=4.559,
    dry_inertia=(0.0996, 0.0996, 0.00307),
    nozzle_radius=0.0397,
    grain_number=1,
    grain_density=1807,
    grain_outer_radius=0.0397,
    grain_initial_inner_radius=0.0381,
    grain_initial_height=0.508,
    grain_separation=0,
    grains_center_of_mass_position=0.52,
    center_of_dry_mass_position=1.33,
    nozzle_position=2.22,
    # burn_time=2.764,
    throat_radius=0.0397,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

# solid_motor.info()