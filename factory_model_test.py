from factoryclasses import Factory
from factoryclasses import SmallMachine
from factoryclasses import BigMachine


factory = Factory(material= 170, material_cost= 3)
factory.add_machines(big_machine_count= 3, small_machine_count= 4)
factory.big_machine.set_spec(prep_time= 1, runtime= 2, product_value= 40, mat_required= 4, base_salary= 5)
factory.small_machine.set_spec(prep_time= 1, runtime= 1, product_value= 35, mat_required= 3, base_salary= 5)
factory.time = 4  #hours
factory.set_requirements(req_big= 20,req_small= 14,big_punish= 2,small_punish= 2)
factory.worker_bonus = 0
factory.haste = 0 #[0-1]
print(factory.big_machine)
print(factory.small_machine)
print(factory)
factory.run()