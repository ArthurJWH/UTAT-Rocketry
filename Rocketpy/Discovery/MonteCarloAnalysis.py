from rocketpy.simulation import MonteCarlo
from rocketpy.stochastic import (
    StochasticEnvironment,
    StochasticGenericMotor,
    StochasticRocket,
    StochasticFlight,
    StochasticNoseCone,
    StochasticTail,
    StochasticTrapezoidalFins,
    StochasticParachute,
    StochasticRailButtons,
)

import DefiningEnvironment
from Motors import BuildingLiquidMotor, BuildingGenericMotor
import BuildingRocket
import Simulation

""" All stochastics values can be lists of possible values or have the form of:
(nominal value[optional], standard deviation, distribution type[optional])
type = “normal”, “binomial”, “chisquare”, “exponential”, “gamma”, “gumbel”, “laplace”, “logistic”, “poisson”, “uniform”, and “wald” """

stochastic_env = StochasticEnvironment(
    environment=DefiningEnvironment.env,
    longitude=0.01,
    latitude=0.01,
)

# stochastic_env.visualize_attributes()

# stochastic_motor = StochasticGenericMotor(
#     generic_motor = BuildingLiquidMotor.liquid_motor,
#     burn_start_time = (0, 0.1,"binomial"),
#     total_impulse = (6500, 100),
#     nozzle_radius = 0.5 / 1000,
#     nozzle_position = 0.001
# )
# stochastic_motor = BuildingLiquidMotor.liquid_motor
stochastic_motor = StochasticGenericMotor(
    generic_motor=BuildingGenericMotor.generic_motor,
    burn_start_time=(0, 0.1, "binomial"),
    total_impulse=(6500, 100),
    nozzle_radius=0.5 / 1000,
    nozzle_position=0.001,
)
# stochastic_motor.visualize_attributes()

stochastic_rocket = StochasticRocket(
    rocket=BuildingRocket.rocket,
    radius=0.0127 / 2000,
    mass=(15.426, 0.5, "normal"),
    inertia_11=(6.321, 0),
    inertia_22=0.01,
    inertia_33=0.01,
    center_of_mass_without_motor=0,
)

# stochastic_rocket.visualize_attributes()

stochastic_nose_cone = StochasticNoseCone(
    nosecone=BuildingRocket.nose_cone, length=0.001
)

stochastic_fin_set = StochasticTrapezoidalFins(
    trapezoidal_fins=BuildingRocket.fin_set,
    root_chord=0.0005,
    tip_chord=0.0005,
    span=0.0005,
)

stochastic_tail = StochasticTail(
    tail=BuildingRocket.tail, top_radius=0.001, bottom_radius=0.001, length=0.001
)

stochastic_rail_buttons = StochasticRailButtons(
    rail_buttons=BuildingRocket.rail_buttons, buttons_distance=0.001
)

stochastic_main = StochasticParachute(parachute=BuildingRocket.main, cd_s=0.1, lag=0.1)

stochastic_drogue = StochasticParachute(
    parachute=BuildingRocket.drogue, cd_s=0.07, lag=0.2
)

stochastic_rocket.add_motor(stochastic_motor, position=0.001)

stochastic_rocket.add_nose(stochastic_nose_cone, position=(1.134, 0.001))

stochastic_rocket.add_trapezoidal_fins(stochastic_fin_set, position=(0.001, "normal"))

stochastic_rocket.add_tail(stochastic_tail)

stochastic_rocket.set_rail_buttons(
    stochastic_rail_buttons, lower_button_position=(0.001, "normal")
)

stochastic_rocket.add_parachute(stochastic_main)

stochastic_rocket.add_parachute(stochastic_drogue)

# stochastic_rocket.visualize_attributes()

stochastic_flight = StochasticFlight(
    flight=Simulation.test_flight,
    inclination=(84.7, 1),  # mean= 84.7, std=1
    heading=(53, 2),  # mean= 53, std=2
)

# stochastic_flight.visualize_attributes()

test_dispersion = MonteCarlo(
    filename="Rocketpy/Discovery/Monte_Carlo_results/monte_carlos_analysis_output.txt",
    environment=stochastic_env,
    rocket=stochastic_rocket,
    flight=stochastic_flight,
)

test_dispersion.simulate(number_of_simulations=10, append=True)

test_dispersion.prints.all()

test_dispersion.plots.ellipses(xlim=(-200, 3500), ylim=(-200, 3500))

test_dispersion.plots.all()

test_dispersion.export_ellipses_to_kml(
    filename="Rocketpy/Discovery/Monte_Carlo_results/monte_carlo_class_example.kml",
    origin_lon=stochastic_env.longitude,
    origin_lat=stochastic_env.latitude,
    type="all",
)

# test_dispersion.import_outputs("Rocketpy/results.txt")
