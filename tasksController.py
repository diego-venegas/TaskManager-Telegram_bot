from taskClass import *
list_tasks = []


def sort_tasks():
    """
    Ordena las tareas por sus fechas, desde la más proxima
    hasta las más lejana
    :return: None
    """

    list_tasks.sort(
        key=lambda x: x.date_time
    )
    return None


def add_task(task):
    """
    Agrega una nueva tarea al listado, verificando
    si este se encuentra creado o no
    :param task: Objecto tarea
    :return:  None
    """

    if get_task(task.return_title()) is None:
        list_tasks.append(task)
        sort_tasks()
    else:
        print(f"Error, {task.return_title()} ya se encuentra creada")
    return None


def remove_task(title):
    """
    Elimina una tarea del listado, verificando
    si este se encuentra creado o no
    :param title: Objecto tarea
    :return:  None
    """
    task_element = get_task(title)

    if task_element is not None:
        list_tasks.remove(task_element)
        sort_tasks()
    else:
        print(f"Error, {title} no se encuentra creada")
    return None


def modify_task():
    return None


def get_task(title):
    """
    Obtiene el objeto tarea, según su titulo
    :param title: Titulo de la tarea a buscar
    :return: Si la tarea existe la retorna
    """

    for task in list_tasks:

        if task.return_title() == title:
            return task

    return None


def print_task():
    return None


def check_task():
    return None
