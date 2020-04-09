from factoryclasses import Factory
from factoryclasses import Machine
from factoryclasses import SmallMachine
from factoryclasses import BigMachine


factory = Factory(170, 3)
factory.add_machines(3, 4)
factory.big_machine.set_spec(prep_time= 1, runtime= 2, product_value= 40, mat_required= 4, base_salary= 5)
factory.small_machine.set_spec(prep_time= 1, runtime= 1, product_value= 35, mat_required= 3, base_salary= 5)
factory.time = 4  #hours
factory.set_requirements(req_big= 20,req_small= 14,big_punish= 2,small_punish= 2)
factory.worker_bonus = 0
factory.set_haste(0)  #[0-1]
print(factory.big_machine)
print(factory.small_machine)
print(factory)
factory.run()