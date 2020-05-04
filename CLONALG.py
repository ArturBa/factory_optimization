from factoryclasses import Factory
import random as rd
import pprint
import matplotlib.pyplot as plt
import bisect
import math
from config import requirements, iterations, population_size, clone_rate, selection_rate, max_big_machines, \
    max_small_machines, max_bonus, max_haste, min_working_time, max_working_time, watchdog

# CONSTANTS - WARTOSCI DO UZGODNIENIA
material_cost = 4
big_spec = {'prep_time': 1.75, 'runtime': 1.5, 'product_value': 70, 'mat_required': 6, 'base_salary': 19}
small_spec = {'prep_time': 1.25, 'runtime': 1.25, 'product_value': 50, 'mat_required': 4, 'base_salary': 17}

# RANDOMS
min_material = big_spec['mat_required'] * requirements['req_big'] + \
               small_spec['mat_required'] * requirements['req_small']
max_material = min_material * 100


# PROPONOWANA FORMA ZAPISU POPULACJI
# population = [{'specifications':{specs}, 'object': object, 'value':value }, ...]
# {'specifications':{specs}, 'object': object, 'value':value } - dalej określane jako cell
# specs - wygenerowane randomy,
# object - stworzony obiekt
# value - wartosc funkcji celu

def calculate_avrg(population):
    value_sum = 0
    for cell in population:
        value_sum += cell['value']
    return round(value_sum / len(population), 2)


def create_cell(specs):
    # create cell with given specifications
    cell = {}
    cell.update({'specifications': specs})
    factory = Factory(material=specs['material'], material_cost=material_cost)
    factory.add_machines(big_machine_count=specs['big_machines'], small_machine_count=specs['small_machines'])
    factory.big_machine.set_spec(prep_time=big_spec['prep_time'], runtime=big_spec['runtime'],
                                 product_value=big_spec['product_value'],
                                 mat_required=big_spec['mat_required'], base_salary=big_spec['base_salary'])
    factory.small_machine.set_spec(prep_time=small_spec['prep_time'], runtime=small_spec['runtime'],
                                   product_value=small_spec['product_value'],
                                   mat_required=small_spec['mat_required'], base_salary=small_spec['base_salary'])
    factory.time = specs['time']
    factory.set_requirements(req_big=requirements['req_big'], req_small=requirements['req_small'],
                             big_punish=requirements['big_punish'], small_punish=requirements['small_punish'])
    factory.set_worker_bonus(specs['bonus'])
    factory.set_haste(specs['haste'])
    cell.update({'object': factory})
    cell.update({'value': cell['object'].run()})
    return cell


def generate_population(size):
    # generate population of <size> with random specifications
    population = []
    for i in range(size):
        random = {}
        random.update({'material': rd.randrange(min_material, max_material)})
        random.update({'big_machines': rd.randrange(1, max_big_machines)})
        random.update({'small_machines': rd.randrange(1, max_small_machines)})
        random.update({'time': rd.randrange(min_working_time, max_working_time + 1)})
        random.update({'bonus': round(rd.uniform(0, max_bonus), 2)})
        random.update({'haste': round(rd.uniform(0, max_haste), 2)})
        cell = create_cell(random)
        population.append(cell)
    return population


def select(population, x):
    # select <x> best cells
    selected = sorted(population, key=lambda population: population['value'], reverse=True)[:x]
    return selected


def clone(selected, clone_rate):
    # clone cells, clones count proportional to cell's value
    clone_number = clone_rate * population_size
    # offset = biggest absolute value
    offset = max(abs(selected[0]['value']), abs(selected[-1]['value']))+1
    val_sum = sum([sel['value'] + offset for sel in selected])
    clones = []
    while clone_number > 0:
        for cell in selected:
            factor = (cell['value'] + offset)/val_sum
            clones += [cell for i in range(math.ceil(factor * clone_number))]
            clone_number -= math.ceil(factor * clone_number)
    return clones


def get_mutation_factor(max_value, value):
    return abs((max_value - value) / max_value * 0.6 + 0.1)


def mature_material(current_value, mutation_factor):
    # get change range
    val_range = math.ceil((max_material - min_material) * mutation_factor)
    # get change value
    mutation_value = rd.randrange(-val_range, val_range)

    # check if value in range and return it
    if current_value + mutation_value > max_material:
        return max_material
    elif current_value + mutation_value < min_material:
        return min_material
    return current_value + mutation_value


def mature_big_machine_number(current_value, mutation_factor):
    # get change range
    val_range = math.ceil(max_big_machines * mutation_factor)
    # get change value
    mutation_value = rd.randrange(-val_range, val_range)
    if current_value + mutation_value > max_big_machines:
        return max_big_machines
    if current_value + mutation_value < 1:
        return 1
    return current_value + mutation_value


def mature_small_machine_number(current_value, mutation_factor):
    # get change range
    val_range = math.ceil(max_small_machines * mutation_factor)
    # get change value
    mutation_value = rd.randrange(-val_range, val_range)
    if current_value + mutation_value > max_small_machines:
        return max_small_machines
    if current_value + mutation_value < 1:
        return 1
    return current_value + mutation_value


def mature_time(current_value, mutation_factor):
    # get change range
    val_range = math.ceil((max_working_time - min_working_time) * mutation_factor)
    # get change value
    mutation_value = rd.randrange(-val_range, val_range)
    if current_value + mutation_value > max_working_time:
        return max_working_time
    elif current_value + mutation_value < min_working_time:
        return min_working_time
    return current_value + mutation_value


def mature_bonus(current_value, mutation_factor):
    # get change range
    val_range = max_bonus * mutation_factor
    # get change value
    mutation_value = round(rd.uniform(-val_range, val_range), 2)
    if current_value + mutation_value > max_bonus:
        return max_bonus
    if current_value + mutation_value < 0:
        return 0
    return current_value + mutation_value


def mature_haste(current_value, mutation_factor):
    # get change range
    val_range = max_haste * mutation_factor
    # get change value
    mutation_value = round(rd.uniform(-val_range, val_range), 2)
    if current_value + mutation_value > max_haste:
        return max_haste
    if current_value + mutation_value < 0:
        return 0
    return current_value + mutation_value


def hypermutate(clones):
    # hypermutate clones, mutation inversely proportional to value (worse value => bigger mutation)
    # get max value of clones
    values = [clone['value'] for clone in clones]
    max_value = max(values)

    # create matured cells from clones
    matured = []
    for clone in clones:
        mutation_factor = get_mutation_factor(max_value, clone['value'])
        mature = {}
        mature.update({'material': mature_material(clone['specifications']['material'], mutation_factor)})
        mature.update(
            {'big_machines': mature_big_machine_number(clone['specifications']['big_machines'], mutation_factor)})
        mature.update(
            {'small_machines': mature_small_machine_number(clone['specifications']['small_machines'], mutation_factor)})
        mature.update({'time': mature_time(clone['specifications']['time'], mutation_factor)})
        mature.update({'bonus': mature_bonus(clone['specifications']['bonus'], mutation_factor)})
        mature.update({'haste': mature_haste(clone['specifications']['haste'], mutation_factor)})
        cell = create_cell(mature)
        matured.append(cell)

    # return matured cells
    return matured


def cdf(how_many, b):
    # weights calculated on the basis of the parabola of the quadratic equation with the given parameter b: a*x^2 + b*x + c = 0
    # b should be within the range (1,2)
    assert 2 > b > 1
    result = []
    for i in range(1, how_many):
        result.append((1 - b) * (i / how_many) ** 2 + b * (i / how_many))
    return result


def choice(population):
    cdf_vals = cdf(len(population), 1.5)
    x = rd.random()
    idx = bisect.bisect(cdf_vals, x)
    return idx


def replace(population, matured):
    # replace cells with better clones
    # probability of replacement based on value
    new_population = population

    max_value = sorted(matured, key=lambda matured: matured['value'], reverse=True)[0]['value']

    considered_p = []
    for cell in population:
        if cell['value'] < max_value:
            considered_p.append(cell)

    if len(considered_p) < round(selection_rate * len(population)):
        how_many_changes = len(considered_p)
    else:
        how_many_changes = round(selection_rate * len(population))

    already_changed = []
    while len(already_changed) < how_many_changes:
        choosen = -1 if len(already_changed) == 0 else already_changed[0]
        while choosen in already_changed or choosen == -1:
            choosen = choice(sorted(considered_p, key=lambda considered_p: considered_p['value'],
                                    reverse=False))  # get index of cell that will be changed
        already_changed.append(choosen)

        considered_m = []
        for mature in matured:
            if mature['value'] > \
                    sorted(considered_p, key=lambda considered_p: considered_p['value'], reverse=False)[choosen][
                        'value']:
                considered_m.append(mature)

        index_to_change = new_population.index(
            sorted(considered_p, key=lambda considered_p: considered_p['value'], reverse=False)[choosen])
        new_population[index_to_change] = considered_m[rd.randint(0, len(considered_m) - 1)]

    return new_population


if __name__ == '__main__':
    population = generate_population(population_size)
    best = []
    worst = []
    avrg = []
    for i in range(iterations):
        selected = select(population, math.ceil(selection_rate * population_size))
        clones = clone(selected, clone_rate)
        matured = hypermutate(clones)
        population = replace(population, matured)
        best_value = sorted(population, key=lambda population: population['value'], reverse=True)[0]['value']
        best.append(best_value)
        worst_value = sorted(population, key=lambda population: population['value'], reverse=True)[-1]['value']
        worst.append(worst_value)
        avrg_value = calculate_avrg(population)
        avrg.append(avrg_value)
        print(f'Iteration: {i + 1}\tBest value: {best_value}\t'
              f'Worst value: {worst_value}\tAverage value: {avrg_value}')

        # Check progress using watchdog
        if i > watchdog:
            if best[-1] == best[-watchdog]:
                print(f'Max value {best[-1]}. No progress since {watchdog} iterations')
                break

    pprint.pprint(sorted(population, key=lambda population_value: population_value['value'], reverse=True)[0])
    plt.plot(range(len(best)), best, 'ro', range(len(worst)), worst, 'bo', range(len(avrg)), avrg, 'go')
    plt.yscale('symlog')
    plt.xlabel('Iteracja')
    plt.ylabel('Wartość funkcji celu')
    plt.title('Wykres wartości funkcji celu od iteracji podczas uczenia')
    plt.legend(['Wartość maksymalna', 'Wartość minimalna', 'Wartość średnia'])
    plt.show()
