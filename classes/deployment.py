class Deployment():

    def __init__(self):
        ''


class Job():

    def __init__(self):
        self.name = ''
        self.start = ''
        self.end = ''


class Schedule_Manager():

    def __init__(self):
        ''

    def schedule_run(self,start):
        'add to schedule table'

    def daily_recurrance(self,hours,minutes=['00']):
        'create daily recurrance cadence'
        assert(type(hours) is list)
        assert(type(minutes) is list)
        return [f'{hr}:{mn}' for hr in hours for mn in minutes]

    def weekly_recurrance(self,days='weekdays'):
        'create weekly recurrance cadence'
        cadence = {
            'weekdays':[1,2,3,4,5],
            'all':[0,1,2,3,4,5,6],
            'weekends':[6,0]
        }
        if type(days) is not list:
            days = cadence[days]
        assert(type(days) is list)
        
        return [f'{hr}:{mn}' for hr in hours for mn in minutes]


class Pipeline():

    def __init__(self):
        ''

