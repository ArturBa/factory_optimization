from math import ceil
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('factoryclasses.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def calc_max_parts(machine):
    return machine.working_time // machine.real_runtime * machine.machine_count


def calc_time_for_req(machine):
    # done on 2 shifts
    if machine.prep_time + ceil(machine.parts_required / machine.machine_count) * machine.real_runtime > 8:
        return 2 * machine.prep_time + ceil(machine.parts_required / machine.machine_count) * machine.real_runtime
    # done on 1 shift
    else:
        return machine.prep_time + ceil(machine.parts_required / machine.machine_count) * machine.real_runtime


def first_cycle(machine, spare_material):
    # enough material
    if spare_material >= machine.mat_required * (
            machine.machine_count - machine.parts_required % machine.machine_count):
        used_material = machine.mat_required * (machine.machine_count - machine.parts_required % machine.machine_count)
        machine.created_parts += (machine.machine_count - machine.parts_required % machine.machine_count)
        return used_material
    # not enough material
    else:
        used_material = machine.mat_required * (spare_material // machine.mat_required)
        machine.created_parts += spare_material // machine.mat_required
        return used_material


def regular_cycle(machine, spare_material, max_time):
    # not enough material for all machines
    if spare_material // machine.mat_required < machine.machine_count:
        # workers' shift change
        if machine.elapsed_time < 8 and machine.elapsed_time + machine.real_runtime > 8:
            if machine.elapsed_time + machine.real_runtime + machine.prep_time < max_time:
                machine.elapsed_time += machine.real_runtime + machine.prep_time
                machine.created_parts += spare_material // machine.mat_required
                used_material = (spare_material // machine.mat_required) * machine.mat_required
            else:
                machine.elapsed_time = max_time
                used_material = 0
        else:
            if machine.elapsed_time + machine.real_runtime < max_time:
                machine.elapsed_time += machine.real_runtime
                machine.created_parts += spare_material // machine.mat_required
                used_material = (spare_material // machine.mat_required) * machine.mat_required
            else:
                machine.elapsed_time = max_time
                used_material = 0
        return used_material
    # enough material for all machines
    else:
        # Workers' shift change
        if machine.elapsed_time < 8 and machine.elapsed_time + machine.real_runtime > 8:
            if machine.elapsed_time + machine.real_runtime + machine.prep_time < max_time:
                machine.elapsed_time += machine.real_runtime + machine.prep_time
                machine.created_parts += machine.machine_count
                used_material = machine.machine_count * machine.mat_required
            else:
                machine.elapsed_time = max_time
                used_material = 0
        else:
            if machine.elapsed_time + machine.real_runtime < max_time:
                machine.elapsed_time += machine.real_runtime
                machine.created_parts += machine.machine_count
                used_material = machine.machine_count * machine.mat_required
            else:
                machine.elapsed_time = max_time
                used_material = 0
        return used_material


def calc_value(machine, multi):
    if machine.created_parts < multi * machine.parts_required:
        value = machine.created_parts * machine.real_product_value
    else:
        value = multi * machine.parts_required * machine.real_product_value
        value += (machine.created_parts - (multi * machine.parts_required)) * 0.75 * machine.real_product_value
    return value


class Machine(ABC):
    def __init__(self):
        self.prep_time = 0
        self.runtime = 0
        self.base_product_value = 0
        self.mat_required = 0
        self.parts_required = 0
        self._machine_count = 0
        self.base_salary = 0
        self.machine_count = 0
        self.created_parts = 0
        self.elapsed_time = 0
        self.haste = 0
        self.worker_bonus = 0
        self.first_run = True

    @abstractmethod
    def set_spec(self, *, prep_time, runtime, product_value, mat_required, base_salary):
        self.prep_time = prep_time
        self.runtime = runtime
        self.base_product_value = product_value
        self.mat_required = mat_required
        self.base_salary = base_salary

    @property  # machine_count getter/setter
    def machine_count(self):
        return self._machine_count

    @machine_count.setter
    def machine_count(self, machine_count):
        self._machine_count = machine_count

    @property
    def real_runtime(self):
        return self.runtime * (1 - self.haste)

    @property
    def real_product_value(self):
        return self.base_product_value * (1 + (1 - self.worker_bonus) * self.worker_bonus) * (1 - 2 * self.haste)

    @property
    def real_salary(self):
        return self.base_salary * (1 + self.worker_bonus)


class SmallMachine(Machine):
    def __init__(self):
        super().__init__()

    def set_spec(self, *, prep_time, runtime, product_value, mat_required, base_salary):
        super().set_spec(prep_time=prep_time, runtime=runtime, product_value=product_value, mat_required=mat_required,
                         base_salary=base_salary)

    def __str__(self):
        return ('Small machine specifications:\n' +
                f'Machine count = {self.machine_count}\n' +
                f'Preparation time = {self.prep_time}\n' +
                f'Basic runtime = {self.runtime}\n' +
                f'Haste = {self.haste * 100}%\n' +
                f'Real runtime = {self.real_runtime}\n' +
                f'Basic product value = {self.base_product_value}\n' +
                f'Material required = {self.mat_required}\n' +
                f'Parts required = {self.parts_required}\n' +
                f'Base salary = {self.base_salary}\n' +
                f'Worker bonus = {self.worker_bonus * 100}%\n')


class BigMachine(Machine):
    def __init__(self):
        super().__init__()

    def set_spec(self, *, prep_time, runtime, product_value, mat_required, base_salary):
        super().set_spec(prep_time=prep_time, runtime=runtime, product_value=product_value, mat_required=mat_required,
                         base_salary=base_salary)

    def __str__(self):
        return ('Big machine specifications:\n' +
                f'Machine count = {self.machine_count}\n' +
                f'Preparation time = {self.prep_time}\n' +
                f'Basic runtime = {self.runtime}\n' +
                f'Haste = {self.haste * 100}%\n' +
                f'Real runtime = {self.real_runtime}\n' +
                f'Basic product value = {self.base_product_value}\n' +
                f'Material required = {self.mat_required}\n' +
                f'Parts required = {self.parts_required}\n' +
                f'Base salary = {self.base_salary}\n' +
                f'Worker bonus = {self.worker_bonus * 100}%\n')


class Factory:
    def __init__(self, *, material, material_cost):
        self.material = material
        self.material_cost = material_cost
        self.small_punish_rate = 0
        self.big_punish_rate = 0
        self.big_machine = BigMachine()
        self.small_machine = SmallMachine()
        self._time = 0
        self.worker_bonus = 0

    def __str__(self):
        return ('Factory specifications:\n' +
                f'Material quantity = {self.material}\n' +
                f'Material cost = {self.material_cost}\n' +
                f'Big machines = {self.big_machine.machine_count}\n' +
                f'Small machines = {self.small_machine.machine_count}\n'
                f'Working time = {self.time}\n')

    @property  # time getter/setter
    def time(self):
        return self._time

    @time.setter
    def time(self, time):
        self._time = time

    @property
    def shifts(self):
        if self.time > 8:
            return 2
        else:
            return 1

    def add_machines(self, *, big_machine_count, small_machine_count):
        self.big_machine.machine_count = big_machine_count
        self.small_machine.machine_count = small_machine_count

    def set_worker_bonus(self, bonus):
        if bonus >= 0 and bonus <= 0.5:
            self.big_machine.worker_bonus = bonus
            self.small_machine.worker_bonus = bonus
        else:
            logger.debug('Workers\' bonus not changed. Enter bonus value from 0 to 0.5')

    def set_haste(self, haste):
        if haste >= 0 and haste <= 0.5:
            self.big_machine.haste = haste
            self.small_machine.haste = haste
        else:
            logger.debug('Haste not changed. Enter haste value from 0 to 0.5')

    def set_requirements(self, *, req_big, req_small, big_punish, small_punish):
        self.big_machine.parts_required = req_big
        self.small_machine.parts_required = req_small
        self.big_punish_rate = big_punish
        self.small_punish_rate = small_punish

    def run(self):
        # reset initial values
        punish = 0
        self.big_machine.created_parts = 0
        self.small_machine.created_parts = 0
        self.small_machine.first_run = True
        self.big_machine.first_run = True

        requirements_material = (self.big_machine.parts_required * self.big_machine.mat_required
                                 + self.small_machine.parts_required * self.small_machine.mat_required)

        spare_material = self.material

        # machines working time
        if self.time - self.shifts * self.big_machine.prep_time > 0:
            self.big_machine.working_time = self.time - self.shifts * self.big_machine.prep_time
        else:
            self.big_machine.working_time = 0
        if self.time - self.shifts * self.small_machine.prep_time > 0:
            self.small_machine.working_time = self.time - self.shifts * self.small_machine.prep_time
        else:
            self.small_machine.working_time = 0

        # 1. enough material for requirements
        if self.material - requirements_material >= 0:
            # required parts:
            if calc_time_for_req(self.small_machine) < self.time:
                self.small_machine.elapsed_time = calc_time_for_req(self.small_machine)
                self.small_machine.created_parts = self.small_machine.parts_required
            else:
                self.small_machine.elapsed_time = self.time
                self.small_machine.created_parts = calc_max_parts(self.small_machine)
                self.small_machine.first_run = False

            spare_material -= self.small_machine.created_parts * self.small_machine.mat_required

            if calc_time_for_req(self.big_machine) < self.time:
                self.big_machine.elapsed_time = calc_time_for_req(self.big_machine)
                self.big_machine.created_parts = self.big_machine.parts_required
            else:
                self.big_machine.elapsed_time = self.time
                self.big_machine.created_parts = calc_max_parts(self.big_machine)
                self.big_machine.first_run = False
            spare_material -= self.big_machine.created_parts * self.big_machine.mat_required
            # additional parts
            while (spare_material >= self.big_machine.mat_required or spare_material >= self.small_machine.mat_required) \
                    and not (
                    self.big_machine.elapsed_time == self.time and self.small_machine.elapsed_time == self.time):
                # small machine finished first
                if self.small_machine.elapsed_time < self.big_machine.elapsed_time:
                    # first cycle - fill last required parts cycle with spare parts
                    if self.small_machine.first_run and self.small_machine.parts_required % self.small_machine.machine_count != 0:
                        spare_material -= first_cycle(self.small_machine, spare_material)
                        self.small_machine.first_run = False
                    # regular cycle
                    else:
                        spare_material -= regular_cycle(self.small_machine, spare_material, self.time)
                # big machine finished first
                else:
                    # first cycle - fill last required parts cycle with spare parts
                    if self.big_machine.first_run and self.big_machine.parts_required % self.big_machine.machine_count != 0:
                        spare_material -= first_cycle(self.big_machine, spare_material)
                        self.big_machine.first_run = False
                    # regular cycle
                    else:
                        spare_material -= regular_cycle(self.big_machine, spare_material, self.time)

        # 2. not enough material for requirements
        elif self.material - requirements_material < 0:
            logger.info('Impossible requirements. Add more material or set lower requirements.')
            return
        else:
            logger.info('Unexpected outcome.')
            return

        # calculate profit
        material_cost = self.material * self.material_cost
        # punish
        if self.big_machine.parts_required - self.big_machine.created_parts > 0:
            punish += (self.big_machine.parts_required - self.big_machine.created_parts) * self.big_punish_rate
        if self.small_machine.parts_required - self.small_machine.created_parts > 0:
            punish += (self.small_machine.parts_required - self.small_machine.created_parts) * self.small_punish_rate
        # values and salary
        big_parts_value = calc_value(self.big_machine, 2)
        big_machine_salary = self.shifts * 8 * self.big_machine.machine_count * self.big_machine.real_salary
        small_parts_value = calc_value(self.small_machine, 2)
        small_machine_salary = self.shifts * 8 * self.small_machine.machine_count * self.small_machine.real_salary
        profit = round(
            big_parts_value + small_parts_value - big_machine_salary - small_machine_salary - material_cost - punish, 2)
        logger.info(f'Daily profit = {profit} \n')
        return profit