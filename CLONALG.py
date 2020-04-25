from factoryclasses import Factory
from factoryclasses import SmallMachine
from factoryclasses import BigMachine
import random as rd
import pprint

#CONSTANTS - WARTOSCI DO UZGODNIENIA
material_cost = 1
big_spec = {'prep_time': 1, 'runtime': 2, 'product_value' : 40, 'mat_required': 4, 'base_salary': 5}
small_spec = {'prep_time': 1, 'runtime': 2, 'product_value' : 40, 'mat_required': 4, 'base_salary': 5}
requirements = { 'req_big': 20,'req_small' : 14, 'big_punish' : 2, 'small_punish' : 2}
iterations = 3
population_size = 10
clone_rate = 0.01
selection_rate = 0.2

#RANDOMS
min_material = big_spec['mat_required'] * requirements['req_big'] + small_spec['mat_required'] * requirements['req_small']
max_material = min_material * 5
max_machines = 30


#PROPONOWANA FORMA ZAPISU POPULACJI
# population = [{'specifications':{specs}, 'object': object, 'value':value }, ...]
# {'specifications':{specs}, 'object': object, 'value':value } - dalej określane jako cell
# specs - wygenerowane randomy,
# object - stworzony obiekt
# value - wartosc funkcji celu

def create_cell(specs):
    #create cell with given specifications
    cell = {}
    cell.update({'specifications': specs})
    factory = Factory(material=specs['material'], material_cost=material_cost)
    factory.add_machines(big_machine_count=specs['big_machines'], small_machine_count=specs['small_machines'])
    factory.big_machine.set_spec(prep_time=big_spec['prep_time'], runtime=big_spec['runtime'], product_value=big_spec['product_value'],
                                 mat_required=big_spec['mat_required'], base_salary=big_spec['base_salary'])
    factory.small_machine.set_spec(prep_time=big_spec['prep_time'], runtime=big_spec['runtime'], product_value=big_spec['product_value'],
                                 mat_required=big_spec['mat_required'], base_salary=big_spec['base_salary'])
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
        random.update({'material':rd.randrange(min_material, max_material )})
        random.update({'big_machines': rd.randrange(1, max_machines)})
        random.update({'small_machines': rd.randrange(1, max_machines)})
        random.update({'time': rd.randrange(1, 17)})
        random.update({'bonus': round(rd.uniform(0,0.5),2)})
        random.update({'haste': round(rd.uniform(0,0.5),2)})
        cell = create_cell(random)
        population.append(cell)
    return population


def select(population, x):
    # select <x> best cells
    selected = sorted(population, key=lambda population: population['value'], reverse=True)[:x]
    return selected

def clone(selected, clone_rate):
    # clone cells, clones count proportional to cell's value
    clones = []
    for cell in selected:
        if cell['value'] > 0:
            clone_number = int(clone_rate * cell['value'])
            clones += [cell for i in range(clone_number)]
    return clones


def get_mutation_factor(max_value, value):
    return (max_value-value)/max_value * 0.6 + 0.1


def mature_material_value(current_value, mutation_factor):
    print(f'Curr val: {current_value}')
    val_range = int((max_material-min_material)*mutation_factor)
    mutation_value = rd.randrange(-val_range, val_range)
    if current_value + mutation_value > max_material: 
        return max_material
    elif current_value + mutation_value < min_material:
        return min_material
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
        mature.update({'material': mature_material_value(clone['specifications']['material'], mutation_factor)})
        mature.update({'big_machines': rd.randrange(1, max_machines)})
        mature.update({'small_machines': rd.randrange(1, max_machines)})
        mature.update({'time': rd.randrange(1, 17)})
        mature.update({'bonus': round(rd.uniform(0,0.5),2)})
        mature.update({'haste': round(rd.uniform(0,0.5),2)})
        cell = create_cell(mature)
        matured.append(cell)
    
    # return matured cells
    return matured

def replace(population, matured):
    # replace cells with better clones
    # probability of replacement based on value
    new_population = population
    return new_population

# jakis print/log typu nr iteracji, najlepszy wynik, najgorszy wynik
# jak starczy czasu to można dać jakiś wykresik

#ALGORYTM
#generate_population
#while something:
    #select x
    #clone x
    #mutate clones
    #replace cells fith better clones (keep original population size)
    #print results

population = generate_population(population_size)
for i in range(iterations):
    selected = select(population, int(selection_rate*population_size))
    clones = clone(selected, clone_rate)
    matured = hypermutate(clones)
    population = replace(population, matured)
    best_value = sorted(population, key=lambda population: population['value'], reverse=True)[0]['value']
    worst_value = sorted(population, key=lambda population: population['value'], reverse=True)[population_size-1]['value']
    print(f'Iteration: {i+1}\t Best value: {best_value}\t Worst value: {worst_value}\n')
pprint.pprint(sorted(population, key=lambda population: population['value'], reverse=True)[0], sort_dicts=False)
