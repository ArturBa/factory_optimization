from factoryclasses import Factory
from factoryclasses import Machine
from factoryclasses import SmallMachine
from factoryclasses import BigMachine


factory = Factory(170, 3)
factory.add_machines(3, 4)
factory.big_machine.set_spec(1, 2, 40, 4, 5)
factory.small_machine.set_spec(1, 1, 35, 3, 5)
factory.set_time(4)  #hours
factory.set_requirements(20,14,2,2)
factory.set_worker_bonus(0)  #[0-1]
factory.set_haste(0)  #[0-1]
print(factory.big_machine)
print(factory.small_machine)
print(factory)
factory.run()