from math import ceil


class Machine:
    def __init__(self):
        self.prep_time = 0
        self.runtime = 0
        self.product_value = 0
        self.mat_required = 0
        self.machine_count = 0
        self.base_salary = 0
        self.machine_count = 0

    def set_spec(self, prep_time, runtime, product_value, mat_required, base_salary):
        self.prep_time = prep_time
        self.runtime = runtime
        self.product_value = product_value
        self.mat_required = mat_required
        self.base_salary = base_salary

    def add(self, machine_count):
        self.machine_count = machine_count


class SmallMachine(Machine):
    def __str__(self):
        return ('Small machine specifications:\n' +
                f'Preparation time = {self.prep_time}\n' +
                f'Runtime = {self.runtime}\n' +
                f'Product value = {self.product_value}\n' +
                f'Material required = {self.mat_required}\n' +
                f'Machine count = {self.machine_count}\n' +
                f'Base salary = {self.base_salary}\n')


class BigMachine(Machine):
    def __str__(self):
        return ('Big machine specifications:\n' +
                f'Preparation time = {self.prep_time}\n' +
                f'Runtime = {self.runtime}\n' +
                f'Product value = {self.product_value}\n' +
                f'Material required = {self.mat_required}\n' +
                f'Machine count = {self.machine_count}\n' +
                f'Base salary = {self.base_salary}\n')


class Factory:
    def __init__(self, material, material_cost):
        self.material = material
        self.material_cost = material_cost
        self.req_small_parts = 0
        self.req_big_parts = 0
        self.small_punish_rate = 0
        self.big_punish_rate = 0
        self.big_machine = BigMachine()
        self.small_machine = SmallMachine()
        self.time = 0
        self.worker_bonus = 0
        self.haste = 0

    def __str__(self):
        return ('Factory specifications:\n' +
                f'Material quantity = {self.material}\n' +
                f'Material cost = {self.material_cost}\n' +
                f'Big machines = {self.big_machine.machine_count}\n' +
                f'Small machines = {self.small_machine.machine_count}\n'
                f'Working time = {self.time}\n' +
                f'Worker bonus = {self.worker_bonus}\n' +
                f'Haste = {self.haste}\n' +
                f'Required big parts = {self.req_big_parts}\n' +
                f'Required small parts = {self.req_small_parts}\n')

    def set_time(self, time):
        self.time = time

    def add_machines(self, big_machine_count, small_machine_count):
        self.big_machine.add(big_machine_count)
        self.small_machine.add(small_machine_count)

    def set_worker_bonus(self, bonus):
        self.worker_bonus = bonus

    def set_haste(self, haste):
        self.haste = haste

    def set_requirements(self, req_big, req_small, big_punish, small_punish):
        self.req_big_parts = req_big
        self.req_small_parts = req_small
        self.big_punish_rate = big_punish
        self.small_punish_rate = small_punish

    def run(self):
        punish = 0
        big_parts = 0
        small_parts = 0
        material_cost = self.material * self.material_cost
        # number of workers' shifts
        if self.time > 8:
            shifts = 2
        else:
            shifts = 1
        # real working time
        big_working_time = self.time - shifts * self.big_machine.prep_time
        small_working_time = self.time - shifts * self.small_machine.prep_time
        big_real_runtime = self.big_machine.runtime * (1 - self.haste)
        small_real_runtime = self.small_machine.runtime * (1 - self.haste)

        # created parts quantity:
        # 1. enough material for full work
        if (big_working_time // big_real_runtime * self.big_machine.machine_count * self.big_machine.mat_required
                + small_working_time // small_real_runtime * self.small_machine.machine_count *
                self.small_machine.mat_required <= self.material):
            big_parts = big_working_time // big_real_runtime * self.big_machine.machine_count
            small_parts = small_working_time // small_real_runtime * self.small_machine.machine_count
        # 2. not enough material for full work but enough for requirements
        elif (big_working_time // big_real_runtime * self.big_machine.machine_count * self.big_machine.mat_required
              + small_working_time // small_real_runtime * self.small_machine.machine_count
              * self.small_machine.mat_required > self.material and self.req_big_parts * self.big_machine.mat_required
              + self.req_small_parts * self.small_machine.mat_required < self.material):

            spare_material = self.material - ( self.req_big_parts * self.big_machine.mat_required
                                               + self.req_small_parts * self.small_machine.mat_required)

            spare_big_parts = 0
            spare_small_parts = 0

            # calculate time spend for creating required parts
            ## big done on 2 shifts
            if self.big_machine.prep_time + ceil(
                    self.req_big_parts / self.big_machine.machine_count) * big_real_runtime > 8:
                big_requirements_time = 2 * self.big_machine.prep_time + ceil(
                    self.req_big_parts / self.big_machine.machine_count) * big_real_runtime
            ## big done on 1 shift
            else:
                big_requirements_time = self.big_machine.prep_time + ceil(
                    self.req_big_parts / self.big_machine.machine_count) * big_real_runtime
            ## small done on 2 shifts
            if self.small_machine.prep_time + ceil(
                    self.req_small_parts / self.small_machine.machine_count) * small_real_runtime > 8:
                small_requirements_time = 2 * self.small_machine.prep_time + ceil(
                    self.req_small_parts / self.small_machine.machine_count) * small_real_runtime
            ## small done on 1 shift
            else:
                small_requirements_time = self.small_machine.prep_time + ceil(
                    self.req_small_parts / self.small_machine.machine_count) * small_real_runtime

            small_elapsed_time = small_requirements_time
            big_elapsed_time = big_requirements_time
            small_first_run = True
            big_first_run = True

            # calculate spare parts quantity
            while spare_material >= self.big_machine.mat_required or spare_material >= self.small_machine.mat_required:
                # small finished first
                if small_elapsed_time < big_elapsed_time:
                    # first run - fill last cycle
                    if small_first_run and self.req_small_parts % self.small_machine.machine_count != 0:
                        # enough material
                        if spare_material >= self.small_machine.mat_required * (self.small_machine.machine_count
                                            -self.req_small_parts % self.small_machine.machine_count):
                            spare_material -= self.small_machine.mat_required * (self.small_machine.machine_count
                                            - self.req_small_parts % self.small_machine.machine_count)
                            spare_small_parts += (self.small_machine.machine_count - self.req_small_parts
                                                  % self.small_machine.machine_count)
                            small_first_run = False

                        # not enough material
                        else:
                            spare_material -= self.small_machine.mat_required * (spare_material
                                                                                 // self.small_machine.mat_required)
                            spare_small_parts += spare_material // self.small_machine.mat_required
                            small_first_run = False

                    # regular cycle

                    elif small_first_run == False or self.req_small_parts % self.small_machine.machine_count == 0:
                        # not enough material for all machines
                        if spare_material // self.small_machine.mat_required < self.small_machine.machine_count:
                            spare_small_parts += spare_material // self.small_machine.mat_required
                            spare_material -= (spare_material // self.small_machine.mat_required) \
                                              * self.small_machine.mat_required
                            # workers' shift change
                            if small_elapsed_time < 8 and small_elapsed_time + small_real_runtime > 8:
                                small_elapsed_time += (small_real_runtime + self.small_machine.prep_time)
                            else:
                                small_elapsed_time += small_real_runtime

                        # enough material for all machines
                        else:
                            spare_small_parts += self.small_machine.machine_count
                            spare_material -= self.small_machine.machine_count * self.small_machine.mat_required
                            # Workers' shift change
                            if small_elapsed_time < 8 and small_elapsed_time + small_real_runtime > 8:
                                small_elapsed_time += (small_real_runtime + self.small_machine.prep_time)
                            else:
                                small_elapsed_time += small_real_runtime

                # big finished first
                else:
                    # first run - fill last cycle
                    if big_first_run and self.req_big_parts % self.big_machine.machine_count != 0:
                        if spare_material >= self.big_machine.mat_required * (self.big_machine.machine_count
                                            - self.req_big_parts % self.big_machine.machine_count):
                            spare_material -= self.big_machine.mat_required * (self.big_machine.machine_count
                                            - self.req_big_parts % self.big_machine.machine_count)
                            spare_big_parts += (self.big_machine.machine_count - self.req_big_parts
                                                % self.big_machine.machine_count)
                            big_first_run = False

                        else:
                            spare_material -= self.big_machine.mat_required * (spare_material // self.big_machine.mat_required)
                            spare_big_parts += spare_material // self.big_machine.mat_required
                            big_first_run = False

                    # regular cycle
                    elif big_first_run == False or self.req_big_parts % self.big_machine.machine_count == 0:
                        # not enough material for all machines
                        if spare_material // self.big_machine.mat_required < self.big_machine.machine_count:
                            spare_big_parts += spare_material // self.big_machine.mat_required
                            spare_material -= (spare_material // self.big_machine.mat_required) * self.big_machine.mat_required
                            # workers' shift change
                            if big_elapsed_time < 8 and big_elapsed_time + big_real_runtime > 8:
                                big_elapsed_time += (big_real_runtime + self.big_machine.prep_time)
                            else:
                                big_elapsed_time += big_real_runtime

                        # enough material for all machines
                        else:
                            spare_big_parts += self.big_machine.machine_count
                            spare_material -= self.big_machine.machine_count * self.big_machine.mat_required
                            # workers' shift change
                            if big_elapsed_time < 8 and big_elapsed_time + big_real_runtime > 8:
                                big_elapsed_time += (big_real_runtime + self.big_machine.prep_time)
                            else:
                                big_elapsed_time += big_real_runtime

            big_parts = self.req_big_parts + spare_big_parts
            small_parts = self.req_small_parts + spare_small_parts

        # 3. not enough material for requirements
        elif (self.req_big_parts * self.big_machine.mat_required
              + self.req_small_parts * self.small_machine.mat_required > self.material):
            print('Impossible requirements. Add more material or set lower requirements.')
            return
        else:
            print('Unexpected outcome.')
            return
        # punish
        if self.req_big_parts - big_parts > 0:
            punish += (self.req_big_parts - big_parts) * self.big_punish_rate

        if self.req_small_parts - small_parts > 0:
            punish += (self.req_small_parts - small_parts) * self.small_punish_rate

        # values and salary
        big_parts_value = big_parts * self.big_machine.product_value * (1 + self.worker_bonus) * (1 - 2 * self.haste)
        big_machine_salary = shifts * self.big_machine.machine_count * self.big_machine.base_salary * (
                1 + self.worker_bonus)

        small_parts_value = small_parts * self.small_machine.product_value * (1 + self.worker_bonus) * (
                1 - 2 * self.haste)
        small_machine_salary = shifts * self.small_machine.machine_count * self.small_machine.base_salary * (
                1 + self.worker_bonus)

        profit = big_parts_value + small_parts_value - big_machine_salary - small_machine_salary - material_cost - punish
        self.value = profit
        print(profit)
        return profit
