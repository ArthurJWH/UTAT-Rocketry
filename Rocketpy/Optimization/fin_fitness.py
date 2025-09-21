from rocketpy import Rocket, Flight, TrapezoidalFins

def fin_fitness(parameters, **kwargs):

    valid = True

    flight = kwargs.get("flight", None)
    if flight is None:
        raise ValueError("Flight instance must be provided in kwargs with key 'flight'")
    env = flight.env
    info = {
        "rail_length": flight.rail_length,
        "inclination": flight.inclination,
        "heading": flight.heading,
    }
    rocket_dict = flight.rocket.to_dict()
    rocket_dict["aerodynamic_surfaces"] = [
        (component, pos)
        for component, pos in rocket_dict["aerodynamic_surfaces"]
        if not isinstance(component, TrapezoidalFins)
    ]

    new_rocket = Rocket.from_dict(rocket_dict)

    fin_dict = {
        "n": parameters[0],
        "root_chord": parameters[1],
        "tip_chord": parameters[2],
        "span": parameters[3],
        "cant_angle": parameters[4],
        "position": parameters[5],
        "sweep_length": parameters[6],
    }

    position = fin_dict.get("position", 0)
    position = position
    new_rocket.add_trapezoidal_fins(
        n=fin_dict["n"],
        root_chord=fin_dict["root_chord"],
        tip_chord=fin_dict["tip_chord"],
        span=fin_dict["span"],
        cant_angle=fin_dict["cant_angle"],
        sweep_length=fin_dict["sweep_length"],
        position=position,
    )
    new_flight = Flight(
        rocket=new_rocket,
        environment=env,
        rail_length=info["rail_length"],
        inclination=info["inclination"],
        heading=info["heading"],
    )

    fitness = 0
    optimize = kwargs.get("optimize", ())
    for opt in optimize:
        fitness += opt(new_flight)

    return fitness, valid