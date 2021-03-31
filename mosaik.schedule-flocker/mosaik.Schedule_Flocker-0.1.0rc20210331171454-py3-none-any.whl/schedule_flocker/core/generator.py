import random
from pprint import pformat
from typing import List

from mosaik_schedule_flocker.schedule_flocker.core.log_borg import \
    LogBorg
from mosaik_schedule_flocker.schedule_flocker.core.config import \
    ScheduleFlockGeneratorConfig
from mosaik_schedule_flocker.schedule_flocker.core.util import \
    get_activation_ends, get_filtered_activation_starts, \
    get_random_activation_starts
from mosaik_schedule_flocker.schedule_flocker.model.\
    fill_electricity_schedule_dict_module import fill_electricity_schedule_dict


class Generator(object):

    def generate_schedule_flock_by_objects(
            self,
            config: ScheduleFlockGeneratorConfig,
    ) -> List[List[int]]:
        # seed random at call time to have it in test and production code
        random.seed(42)

        schedule_flock = self.collect_schedule_flock(config)
        electricity_schedules = []
        for schedule in schedule_flock:
            electricity_schedules.append(fill_electricity_schedule_dict(
                unit_id=config.unit_id,
                unit_type=config.unit_type,
                schedule=schedule))

        return electricity_schedules

    @staticmethod
    def collect_schedule_flock(config):
        schedule_flock = []
        while len(schedule_flock) < config.limit_size_flock:
            activation_starts = get_random_activation_starts(
                limit_count_activation=config.limit_count_activation)
            LogBorg().logger.debug(
                f'activation_starts: {activation_starts}')

            activation_starts = get_filtered_activation_starts(
                activation_starts=activation_starts)
            LogBorg().logger.debug(f'activation_starts after filtration: '
                                   f'{activation_starts}')

            activation_ends = \
                get_activation_ends(activation_starts=activation_starts)
            LogBorg().logger.debug(f'activation_ends: {activation_ends}')

            # Create copy of mutable list
            schedule = list(config.predicted_schedule)

            deviations_production = []
            deviations_consumption = []
            for start, end in zip(activation_starts, activation_ends):
                LogBorg().logger.debug(f'start {start}, end {end}')

                if start == end:
                    time_step_range = [start]
                else:
                    time_step_range = range(start, end)

                for time_step in time_step_range:
                    LogBorg().logger.debug(f'time_step {time_step}')

                    # Select next power at random
                    power = random.randint(a=config.limit_power_consumption,
                                           b=config.limit_power_production)
                    LogBorg().logger.debug(f'power {power}')

                    # Clip power by predicted flexibility
                    power = max(power, config.schedule_min[time_step])
                    LogBorg().logger.debug(f'Maximum power clipped by '
                                           f'minimum schedule {power}')

                    power = min(power, config.schedule_max[time_step])
                    LogBorg().logger.debug(f'Minimum power clipped by '
                                           f'maximum schedule {power}')

                    # Record flexibility energy
                    power_predicted = config.predicted_schedule[time_step]
                    LogBorg().logger.debug(f'power_predicted '
                                           f'{power_predicted}')
                    power_deviation = power - power_predicted
                    LogBorg().logger.debug(f'power_deviation '
                                           f'{power_deviation}')
                    if power_deviation > 0:
                        deviations_production.append(power_deviation)
                    if power_deviation < 0:
                        deviations_consumption.append(power_deviation)

                    schedule[time_step] = power

            if sum(deviations_production) > config.limit_energy_production:
                LogBorg().logger.debug(f'{sum(deviations_production)} > '
                                       f'{config.limit_energy_production}')
                continue
            if sum(
                    deviations_consumption) < config.limit_energy_consumption:
                LogBorg().logger.debug(f'{sum(deviations_consumption)} < '
                                       f'{config.limit_energy_consumption}')
                continue

            schedule_flock.append(schedule)
            LogBorg().logger.debug('schedule_flock')
            LogBorg().logger.debug(pformat(object=schedule_flock, indent=1,
                                           width=120, depth=None))

        return schedule_flock
