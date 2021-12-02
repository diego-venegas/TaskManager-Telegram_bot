from taskClass import *

list_tasks = []


def sort_tarea():
    list_tasks.sort(
        key=lambda x: x.date_time
    )
    return None


def add_task(task):

    if get_task(task.title) is None:
        list_tasks.append(task)
        sort_tarea()
    else:
        print(f"Error, {task.return_title()} ya se encuentra creada")
    return None


def remove_task():
    return None


def modify_task():
    return None


def get_task(title):

    for task in list_tasks:

        if task.return_title() == title:

            return task

    return None


def print_task():
    return None


def check_task():
    return None
