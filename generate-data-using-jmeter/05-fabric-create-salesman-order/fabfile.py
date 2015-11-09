from datetime import datetime, timedelta
from fabric.api import local, task, lcd
import random

@task
def create_salesman_order():
    """
    Create Sales Order GT
    # 1. date between START and END.
    # 2. work from Monday to Saturday.
    # 3. create number_order_on_day.
    # 4. time between 08:00 and 17:00.
    """

    PATH_JMETER = '/home/coc/Applications/apache-jmeter/bin/jmeter'
    PATH_JMETER_SCRIPT_DIR = '/home/coc/lab/jmeter/create-salesman-order/'
    JMETER_SCRIPT = 'create-order-by-salesman.jmx'

    MIN_NUMBER_ORDER_PER_DAY = 0
    MAX_NUMBER_ORDER_PER_DAY = 3

    START_DATE_STR = '2015-05-13 00:00:00'
    END_DATE_STR = '2015-12-31 00:00:00'

    START_SECOND = 8*60*60
    END_SECOND = 17*60*60


    JMETER_COMMAND = '{} -n -t {}'.format(PATH_JMETER, JMETER_SCRIPT)

    START_DATE = datetime.strptime(START_DATE_STR, '%Y-%m-%d %H:%M:%S')
    END_DATE = datetime.strptime(END_DATE_STR, '%Y-%m-%d %H:%M:%S')

    day = START_DATE

    while day <= END_DATE:
        # don't work on Sunday
        if day.weekday() == 6:
            day = day + timedelta(days=1)
            continue

        number_order_on_day = random.randint(MIN_NUMBER_ORDER_PER_DAY, MAX_NUMBER_ORDER_PER_DAY)
        print('Number order on day:', number_order_on_day)

        time_shifts = sorted([random.randint(START_SECOND, END_SECOND)
                for _ in range(number_order_on_day)])

        for time_shift in time_shifts:
            t = day + timedelta(seconds=time_shift)

            local('sudo date -s "%s"' %(datetime.strftime(t, '%Y-%m-%d %H:%M:%S')))

            local('date --rfc-3339=seconds >> order_date.log')

            with lcd(PATH_JMETER_SCRIPT):
                local(JMETER_COMMAND)

        day = day + timedelta(days=1)

