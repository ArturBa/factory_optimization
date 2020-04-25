from factoryclasses import Factory
from factoryclasses import SmallMachine
from factoryclasses import BigMachine

factory = Factory(material=600, material_cost= 1)
factory.add_machines(big_machine_count= 8, small_machine_count= 10)
factory.big_machine.set_spec(prep_time= 1, runtime= 2, product_value= 40, mat_required= 4, base_salary= 5)
factory.small_machine.set_spec(prep_time= 1, runtime= 1, product_value= 35, mat_required= 3, base_salary= 5)
factory.time = 14   # hours
factory.set_requirements(req_big= 20,req_small= 14,big_punish= 2,small_punish= 2)
factory.set_worker_bonus(0.1)  # <0 - 0.5>
factory.set_haste(0.1)  # <0 - 0.5>
print(factory.big_machine)
print(factory.small_machine)
print(factory)
factory.run()