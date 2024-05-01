import sys, yaml

COLOUR_NONE = "\033[0m"
COLOUR_RED = "\033[0;31m"
COLOUR_GREEN = "\033[0;32m"
COLOUR_YELLOW = "\033[2;33m"
COLOUR_BLUE = "\033[0;34m"
COLOUR_MAGENTA = "\033[0;35m"
COLOUR_CYAN = "\033[0;36m"

def time(string):
    arr = string.split(":")
    seconds = 0
    mult = 1
    for index in range(1, len(arr) + 1, 1):
        seconds += float(arr[-index]) * mult
        mult *= 60
    return seconds

def prog(value, minimum, maximum):
    if value < minimum:
        return 0
    elif value > maximum:
        return 1
    else:
        return (value - minimum) / (maximum - minimum)

def timeprog(value, min_time, max_time):
    value = time(value)
    min_time = time(min_time)
    max_time = time(max_time)
    return prog(value, min_time, max_time)

def negtimeprog(value, min_time, max_time):
    return 1 - timeprog(value, max_time, min_time)

def read_tasksheet(tasksheet_name):
    filepath = tasksheet_name
    file = open(filepath, "r")
    data = yaml.safe_load(file)
    return data

def inspect_tasksheet(tasksheet):

    total_weight = 0
    completed_weight = 0
    for task in tasksheet["tasks"]:
        completion, weight = inspect_task(task)
        total_weight += weight
        completed_weight += completion * weight

    return completed_weight / total_weight

def inspect_task(task):
    if "subtasks" in task.keys():
        added_completed_weight = 0
        added_total_weight = 0
        for subtask in task["subtasks"]:
            completion, total_weight = inspect_task(subtask)
            added_completed_weight += completion * total_weight
            added_total_weight += total_weight
        return added_completed_weight / added_total_weight, task["wght"]
    else:
        task_weight = task["wght"]
        if task["comp"] == True:
            completed_weight = task_weight
        elif type(task["comp"]) in [int, float]:
            completed_weight = task["comp"] * task_weight
        elif type(task["comp"]) == str:
            completed_weight = eval(task["comp"]) * task_weight
        elif task["comp"] == False:
            completed_weight = 0
        else:
            print("ERROR - invalid comp value")
            sys.exit(1)
        return completed_weight / task_weight, task_weight

COMMAND = sys.argv[1]
SHEET_NAME = sys.argv[2]

if COMMAND == "evaluate":
    tasksheet = read_tasksheet(SHEET_NAME)
    completion = inspect_tasksheet(tasksheet)
    print("Sheet " + COLOUR_MAGENTA + SHEET_NAME + COLOUR_NONE + " is " + str(round(completion * 100, 1)) + "% complete")

