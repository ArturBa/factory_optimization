from factoryclasses import Factory
from factoryclasses import SmallMachine
from factoryclasses import BigMachine

#CONSTANTS - WARTOSCI I FORMA ZAPISU DO UZGODNIENIA
material_cost = 1
big_spec = {'prep_time': 1, 'runtime': 2, 'product_value' : 40, 'mat_required': 4, 'base_salary': 5}
small_spec = {'prep_time': 1, 'runtime': 2, 'product_value' : 40, 'mat_required': 4, 'base_salary': 5}
requirements = { 'req_big': 20,'req_small' : 14, 'big_punish' : 2, 'small_punish' : 2}

min_material = big_spec['mat_required'] * requirements['req_big'] + small_spec['mat_required'] * requirements['req_small']

#RANDOMS
# material =  random <min_material, 5 * min_material>  ???
# machine count = random <1, 30> ???
# time = random <1, 16>
# bonus = random <0, 0.5>
# haste = random <0, 0.5>

#PROPONOWANA FORMA ZAPISU POPULACJI
# population = [({specs}, object, value ), ...] ???
# specs - wygenerowane randomy, wstępnie jako dictionary żeby było łatwiej ogarnąć co jest czym
# object - stworzony obiekt
# value - wartosc funkcji celu

# affinity jest niepotrzebne bo mamy wartość funkcji celu


def generate_population(size):
    # generate population of <size> with random specifications
    # return population
    pass

def select(population, x):
    # select <x> best cells
    selected = sorted(population, key=lambda population: population[2], reverse=True)[:x]
    return selected

def clone(selected):
    # clone cells, clones count proportional to cell's value
    # return clones
    pass

def hypermutate(clones):
    # hypermutate clones, mutation inversely proportional to value (worse value => bigger mutation)
    # return new_clones
    pass

def replace(population, clones):
    # replace cells with better clones
    # probability of replacement based on value
    pass

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

