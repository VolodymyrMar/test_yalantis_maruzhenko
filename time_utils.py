from time import mktime
from datetime import datetime


INPUT_FORMAT = "%d/%m/%Y %H:%M:%S"
OUTPUT_FORMAT = "%d-%m-%Y"


def timestamp_to_output(time_: str):
    return datetime.fromtimestamp(int(time_)).strftime(INPUT_FORMAT)


def input_to_timestamp(ts_time):
    return mktime(datetime.strptime(ts_time, "%d-%m-%Y").timetuple())
