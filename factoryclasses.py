class Machine:
    def __init__(self):
        self.prep_time = 0
        self.runtime = 0
        self.product_value = 0
        self.mat_reqired = 0
        self.machine_count = 0
        self.base_salary = 0
        self.machine_count = 0

    def set_spec(self, prep_time, runtime, product_value, mat_reqired, base_salary):
        self.prep_time = prep_time
        self.runtime = runtime
        self.product_value = product_value
        self.mat_reqired = mat_reqired
        self.base_salary = base_salary

    def add(self, machine_count):
        self.machine_count = machine_count

class SmallMachine(Machine):
    def print_spec(self):
        print('Small machine specifications:\n' +
              f'Preparation time = {self.prep_time}\n' +
              f'Runtime = {self.runtime}\n' +
              f'Product value = {self.product_value}\n' +
              f'Material required = {self.mat_reqired}\n' +
              f'Machine count = {self.machine_count}\n' +
              f'Base salary = {self.base_salary}\n')

class BigMachine(Machine):
    def print_spec(self):
        print('Big machine specifications:\n' +
              f'Preparation time = {self.prep_time}\n' +
              f'Runtime = {self.runtime}\n' +
              f'Product value = {self.product_value}\n' +
              f'Material required = {self.mat_reqired}\n' +
              f'Machine count = {self.machine_count}\n' +
              f'Base salary = {self.base_salary}\n')

class Factory:
    def __init__(self, material, material_cost):
        self.material = material
        self.material_cost = material_cost
        self.req_small_parts = 0
        self.req_big_parts = 0
        self.big_machine = BigMachine()
        self.small_machine = SmallMachine()
        self.time = 0
        self.worker_bonus = 0


    def add_time(self, time):
        self.time = time

    def add_machines(self, big_machine_count, small_machine_count):
        self.big_machine.add(big_machine_count)
        self.small_machine.add(small_machine_count)

    def add_worker_bonus(self, bonus):
        self.worker_bonus = bonus

    def add_requirements(self, req_big, req_small):
        self.req_big_parts = req_big
        self.req_small_parts = req_small

    def print_spec(self):
        print('Factory specifications:\n'+
              f'Material quantity = {self.material}\n'+
              f'Material cost = {self.material_cost}\n'+
              f'Big machines = {self.big_machine.machine_count}\n'+
              f'Small machines = {self.small_machine.machine_count}\n'
              f'Working time = {self.time}\n'+
              f'Worker bonus = {self.worker_bonus}\n'+
              f'Required big parts = {self.req_big_parts}\n'+
              f'Required small parts = {self.req_small_parts}\n'
              )

    def run(self):
        #do uzupełnienia
        pass