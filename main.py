import sys, yaml

COLOUR_NONE = "\033[0m"
COLOUR_RED = "\033[0;31m"
COLOUR_GREEN = "\033[0;32m"
COLOUR_YELLOW = "\033[2;33m"
COLOUR_BLUE = "\033[0;34m"
COLOUR_MAGENTA = "\033[0;35m"
COLOUR_CYAN = "\033[0;36m"

def time(string):
    string = string.split(":")
    seconds = float(string[-1])
    if len(string) >= 2:
        seconds += float(string[-2]) * 60
    return seconds


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

