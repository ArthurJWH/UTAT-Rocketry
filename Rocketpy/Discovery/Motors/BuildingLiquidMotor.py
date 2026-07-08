from rocketpy.motors import Fluid, CylindricalTank, MassFlowRateBasedTank, LiquidMotor

""" Defining oxidizer and fuel """
oxidizer_liquid = Fluid(name="Liquid N2O", density=1220)  # kg/m3

oxidizer_gas = Fluid(name="Gas N2O", density=1.9277)  # kg/m3

fuel_liq = Fluid(name="Liquid ethanol", density=789)  # kg/m3

fuel_gas = Fluid(name="Nitrogen Gas", density=55)  # kg/m3

""" Creating the tank """
fuel_tank_geometry = CylindricalTank(
    radius=0.076, height=1.24, spherical_caps=False  # meters  # meters
)

oxidizer_tank_geometry = CylindricalTank(
    radius=0.076, height=0.64, spherical_caps=False  # meters
)

""" Defining flow rate of the oxidizer """
from math import exp

oxidizer_tank = MassFlowRateBasedTank(
    name="oxidizer tank",
    geometry=oxidizer_tank_geometry,
    flux_time=4.58,  # seconds
    initial_liquid_mass=7.01,  # kg
    initial_gas_mass=0.01,  # kg
    liquid_mass_flow_rate_in=0,
    liquid_mass_flow_rate_out= 7.01/4.58,
    gas_mass_flow_rate_in=0,
    gas_mass_flow_rate_out=0,
    liquid=oxidizer_liquid,
    gas=oxidizer_gas,
)

""" Defining the flow rate of the fuel """

fuel_tank = MassFlowRateBasedTank(
    name="fuel tank",
    geometry=fuel_tank_geometry,
    flux_time=4.58,  # seconds
    initial_liquid_mass= 2.42,  # kg
    initial_gas_mass= 1,  # kg
    liquid_mass_flow_rate_in=0,
    liquid_mass_flow_rate_out= 2.42/4.58,
    gas_mass_flow_rate_in=0,
    gas_mass_flow_rate_out=0,
    liquid=fuel_liq,
    gas=fuel_gas,
)

""" Defining the thrust curve"""


def thrust_curve_function(t):  # load .csv table of time and thrust
    return 10000 - 100 * t**2


""" Assembling liquid motor """
liquid_motor = LiquidMotor(
   thrust_source="enginefilev4.csv",
    dry_mass=20.088,
    dry_inertia=(0.125, 0.125, 0.002),
    center_of_dry_mass_position= 1.074,
    nozzle_radius=0.043,
    burn_time=4.58,
    nozzle_position=0,
    interpolation_method="linear",
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

""" Add tanks to the motor """
liquid_motor.add_tank(
    tank=oxidizer_tank,
    position=1.22,  # meters
)

liquid_motor.add_tank(
    tank=fuel_tank,
    position=2.45,  # meters
)

#liquid_motor.info()
#liquid_motor.draw()
