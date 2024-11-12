from rocketpy.motors import Fluid, CylindricalTank, MassFlowRateBasedTank, LiquidMotor

''' Defining oxidizer and fuel '''
oxidizer_liquid = Fluid(
    name = "Liquid N2O",
    density = 1220 # kg/m3
)

oxidizer_gas = Fluid(
    name = "Gas N2O",
    density = 1.9277 # kg/m3
)

fuel_liq  = Fluid(
    name = "Liquid ethanol",
    density = 789 # kg/m3
)

fuel_gas = Fluid(
    name = "Gas ethanol",
    density = 1.59 # kg/m3
)

''' Creating the tank '''
tanks_geometry = CylindricalTank(
    radius = 0.1, # meters
    height = 1.2, #meters
    spherical_caps = True
)


''' Defining flow rate of the oxidizer '''
from math import exp

def mass_flow_rate_function(t): # load .csv table of time and flow rate
    return 32 / 3 * exp(-0.25 * t)

oxidizer_tank = MassFlowRateBasedTank(
    name = "oxidizer tank",
    geometry = tanks_geometry,
    flux_time = 5, # seconds
    initial_liquid_mass = 32, # kg
    initial_gas_mass = 0.01, # kg
    liquid_mass_flow_rate_in = 0,
    liquid_mass_flow_rate_out = mass_flow_rate_function,
    gas_mass_flow_rate_in = 0,
    gas_mass_flow_rate_out = 0,
    liquid = oxidizer_liquid,
    gas = oxidizer_gas
)

''' Defining the flow rate of the fuel '''
def liquid_mass_flow_rate_function(t): # load .csv table of time and flow rate
    return 21 / 3 * exp(-0.25* t)

def gas_mass_flow_rate_function(t): # load .csv table of time and flow rate
    return 0.01 / 3 * exp(-0.25 * t)

fuel_tank = MassFlowRateBasedTank(
    name = "fuel tank",
    geometry = tanks_geometry,
    flux_time  =5, # seconds
    initial_liquid_mass = 21, #kg
    initial_gas_mass = 0.01, # kg
    liquid_mass_flow_rate_in = 0,
    liquid_mass_flow_rate_out = liquid_mass_flow_rate_function,
    gas_mass_flow_rate_in = 0,
    gas_mass_flow_rate_out = gas_mass_flow_rate_function,
    liquid = fuel_liq,
    gas = fuel_gas
)

''' Defining the thrust curve'''
def thrust_curve_function(t): # load .csv table of time and thrust
    return 10000 - 100 * t**2

''' Assembling liquid motor '''
liquid_motor = LiquidMotor(
    thrust_source = thrust_curve_function,
    dry_mass = 2, # kg
    dry_inertia = (0.125, 0.125, 0.002), # kg/m2
    nozzle_radius = 0.075,
    center_of_dry_mass_position = 1.75,
    nozzle_position = 0,
    burn_time = 5, # seconds
    coordinate_system_orientation = "nozzle_to_combustion_chamber"
)

''' Add tanks to the motor '''
liquid_motor.add_tank(
    tank = oxidizer_tank,
    position = 1.0, # meters
)

liquid_motor.add_tank(
    tank = fuel_tank,
    position = 2.5, # meters
)

# liquid_motor.info()
# liquid_motor.draw()
