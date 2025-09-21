import random
import functools


def MDO(
    fitness: callable,
    parameters: list,
    pop_size: int = 100,
    generations: int = 10,
    seed=None,
    mutation_rate: float = 0.1,
    filename: str = None,
    append: bool = False,
    **kwargs,
):

    @functools.lru_cache(maxsize=None)
    def fitnessF(ind, **kwargs):
        return fitness(ind, **kwargs)

    def random_ind():
        ind = ()
        for param in parameters:
            if isinstance(param, tuple):
                ind += (random.uniform(param[0], param[1]),)
            elif isinstance(param, list):
                ind += (random.choice(param),)
        return ind

    def mutate(ind, mutation_rate=mutation_rate):
        new_ind = ()
        for i in range(len(ind)):
            if random.random() < mutation_rate:
                if isinstance(parameters[i], tuple):
                    new_ind += (random.uniform(parameters[i][0], parameters[i][1]),)
                elif isinstance(parameters[i], list):
                    new_ind += (random.choice(parameters[i]),)
            else:
                new_ind += (ind[i],)
        return new_ind

    def select_pair(pop):
        return random.choices(
            population=pop,
            weights=[fitnessF(individual, **kwargs)[0] for individual in pop],
            k=2,
        )

    def crossover(ind1, ind2):
        child1 = ()
        child2 = ()
        for i in range(len(ind1)):
            genes = (ind1[i], ind2[i])
            par1 = random.choices((0, 1), weights=(9, 1), k=1)[0]
            par2 = not par1
            child1 += (genes[par1],)
            child2 += (genes[par2],)
        child1 = mutate(child1)
        child2 = mutate(child2)
        return child1, child2
    
    pop = []
    if seed is not None:
        random.seed(seed)
    carry_over = 2

    if filename:
        try:
            with open(filename, "r") as f:
                for line in f:
                    if line.strip():
                        ind = eval(line.strip())
                        if fitnessF(ind, **kwargs)[1]:
                            pop.append(ind)
        except FileNotFoundError:
            pass
    while len(pop) < pop_size:
            new_ind = random_ind()
            if fitnessF(new_ind, **kwargs)[1]:
                pop.append(new_ind)
    
    pop.sort(key=lambda ind: fitnessF(ind, **kwargs)[0], reverse=True)
    print(f"Generation 1: Best score = {fitnessF(pop[0], **kwargs)[0]}; Parameters = {pop[0]}")
    
    for gen in range(2, generations + 1):

        next_gen = pop[0:carry_over]

        for _ in range(int(len(pop) / 2 - carry_over / 2)):
            parents = select_pair(pop)
            child1, child2 = crossover(
                parents[0], parents[1]
            )
            if fitnessF(child1, **kwargs)[1]:
                next_gen += [child1]
            if fitnessF(child2, **kwargs)[1]:
                next_gen += [child2]

        pop = next_gen

        while len(pop) < pop_size:
            new_ind = random_ind()
            if fitnessF(new_ind, **kwargs)[1]:
                pop.append(new_ind)

        pop.sort(key=lambda ind: fitnessF(ind, **kwargs)[0], reverse=True)
        print(f"Generation {gen}: Best score = {fitnessF(pop[0], **kwargs)[0]}; Parameters = {pop[0]}")

    best_inds = pop[0:10]
    if filename:
        with open(filename, "a" if append else "w") as f:
            for ind in best_inds:
                f.write(f"{ind}\n")

    return best_inds[0], fitnessF(best_inds[0], **kwargs)
