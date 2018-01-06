import pprint


class LoadBalancer():

    def day(self, day_name, load, set):
        return {
            'name': day_name,
            'load': load,
            # 'set': set
        }

    def add_week(self):
        new_week_number = len(self.weeks)
        print('\nAdding week {}'.format(new_week_number))
        self.weeks[new_week_number] = {
            'month': None,
            'days': {}
        }
        for idx, day_name in enumerate(self.day_names):
            self.weeks[new_week_number]['days'][idx] = self.day(day_name, [], False)

    def __init__(self):
        self.OVERLOADED_WEEK = 'Not enough hours in the week'
        self.errors = {}
        self.OVERLOADED_DAY = 'Not enough hours in the day'

        self.hours_per_day = 7.5
        self.day_names = ['mon', 'tues', 'wed', 'thurs', 'fri']

        self.weeks = {}
        self.add_week()
        self.add_week()
        self.add_week()
        self.add_week()
        self.current_week = 0

        self.__recalculate__()

    # load should be an array
    # def set_day_load(self, day_name, load, repeat=None):
    #     idx = self.day_names.index(day_name)
    #     self.weeks[self.current_week]['days'][idx]['load'] = load
    #
    #     print('set {} load to {}.'.format(
    #         self.weeks[self.current_week]['days'][idx]['name'],
    #         self.weeks[self.current_week]['days'][idx]['load'])
    #     )
    #     # self.__recalculate__()

    # load should be an array
    def add_day_load(self, week, day_name, load, repeat=False):
        if repeat:
            end_week = len(self.weeks)
        else:
            end_week = week + 1

        print('Adding {} hours to day {} in week range {} to {}'.format(load, day_name, week, end_week))

        for week_number in range(week, end_week):

            idx = self.day_names.index(day_name)
            self.weeks[week_number]['days'][idx]['load'].extend(load)

            print('set {} load to {}.'.format(
                self.weeks[week_number]['days'][idx]['name'],
                self.weeks[week_number]['days'][idx]['load'])
            )
        self.__recalculate__()

    def add_week_load(self, week, load):

        print('\nAdding new load of {} across the week {}'.format(load, week))

        for idx, day in enumerate(self.day_names):
            print('Load remaining to spread {}'.format(load))
            if load > 0:

                print('Summing {}'.format(self.weeks[week]['days'][idx]['load']))
                day_quota = sum(self.weeks[week]['days'][idx]['load'])
                if day_quota < self.hours_per_day:
                    available_time_in_day = self.hours_per_day - day_quota

                    print('day {} has {} hours available to fill'.format(day, available_time_in_day))

                    if load >= available_time_in_day:
                        self.add_day_load(week, day, [available_time_in_day])
                        load -= available_time_in_day
                    else:
                        self.add_day_load(week, day, [load])
                        load -= load

                else:
                    print('Day {} is already full'.format(day))
        if load > 0:
            self.error(None, self.OVERLOADED_WEEK + ' {}'.format(load))
            # self.add_week()
            print('Load of {} hours remaining to spread to week {}'.format(load, self.current_week + 1))
            self.add_week_load(week + 1, load)

            # self.__recalculate__()

    def __recalculate__(self):
        # week_balance = self.hours_per_day * len(self.day_names)
        week_balance = 0
        none_count = 0
        free_time = 0
        print('\nData for current week :', self.weeks[self.current_week]['days'], '\n')
        for idx, day in enumerate(self.day_names):

            print('Day {} load {}'.format(day, self.weeks[self.current_week]['days'][idx]['load']))

            if len(self.weeks[self.current_week]['days'][idx]['load']):
                day_quota = sum(self.weeks[self.current_week]['days'][idx]['load'])
                if day_quota > self.hours_per_day:
                    self.error(day, self.OVERLOADED_DAY)

                week_balance += day_quota

                print('day {} load is {} hours, weekly hours now {}'.format(
                    self.weeks[self.current_week]['days'][idx]['name'],
                    day_quota,
                    week_balance
                )
                )
            else:
                none_count += 1
                free_time += self.hours_per_day

        # if none_count:
        #     none_day_load = week_balance / none_count
        # else:
        #     none_day_load = 0

        print(
            'week_balance', week_balance,
            'none_count', none_count,
            # 'none_day_load', none_day_load,
            'free_time', free_time
        )

        for idx, day in enumerate(self.day_names):
            print(idx, day, self.weeks[self.current_week]['days'][idx]['load'])

            if not len(self.weeks[self.current_week]['days'][idx]['load']):
                self.weeks[self.current_week]['days'][idx]['load'] = []

    def pprint_loads(self):
        for week_number in range(0, len(self.weeks)):
            for idx, day in enumerate(self.day_names):
                print('Week {},\tday {},\tday {},\tload {}'.format(
                    week_number,
                    idx,
                    self.weeks[week_number]['days'][idx]['name'],
                    self.weeks[week_number]['days'][idx]['load']
                ))

    def error(self, day, msg):
        self.errors[self.current_week, day] = {
            'week': self.current_week,
            'day': day,
            msg: True
        }


if __name__ == '__main__':
    lb = LoadBalancer()

    print('\n\nbreak1\n\n')

    # Daily load can be flexible (default) - they can overflow into following days and weeks
    # flexible within week - can overflow into following days, but displace other work to remain within that week
    # non-flexible - will displace work from the day it is placed on, but overflow if more than a days work
    # strict - will displace work from day it is placed on, day will be extended in hours to fit work.

    # Loads can also be repeating, weekly. i.e. 1h every Tuesday

    lb.add_day_load(0, 'mon', [5, 5])
    lb.add_day_load(0, 'thurs', [5])
    lb.add_day_load(0, 'wed', [5], repeat=True)

    print('\n\nbreak2\n\n')

    lb.add_week_load(lb.current_week, 17.5)
    lb.add_week_load(lb.current_week, 12)
    lb.add_week_load(1, 10)
    lb.__recalculate__()

    print('\n\nbreak3\n\n')

    lb.pprint_loads()
    print(pprint.pformat(lb.errors))