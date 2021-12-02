from taskClass import *
from datetime import datetime
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
    :param task: Objeto tarea
    :return: bool
    """

    if get_task(task.return_title()) is None:
        list_tasks.append(task)
        sort_tasks()
        return True
    else:
        print(f"Error, {task.return_title()} ya se encuentra creada")
        return False


def remove_task(title):
    """
    Elimina una tarea del listado, verificando
    si este se encuentra creado o no
    :param title: titulo de la tarea
    :return: bool
    """
    task_element = get_task(title)

    if task_element is not None:
        list_tasks.remove(task_element)
        sort_tasks()
        return True
    else:
        print(f"Error, {title} no se encuentra creada")
        return False


def modify_task(title, new_title, new_description, new_date):
    """
    Modifica una tarea del listado, verificando 
    si esta o no tarea.
    :param title: titulo de la tarea
    :param new_title: titulo nuevo.
    :param new_description: descripcion nueva.
    :param new_date: nueva fecha de la tarea.
    :return: bool
    """
    
    task_to_modify = get_task(title)
    
    if task_to_modify is not None:
        
        task_to_modify.modify_title(new_title)
        task_to_modify.modify_description(new_description)
        task_to_modify.modify_date_time(new_date)
        print(f"Tarea Modificada")
        return True
        
    else:
        print(f"Error, {title} no se encuentra creada")
        return False


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


def check_task(date_time):
    """
    Recibe una fecha y hora, verifica si coinciden 
    con las de la tarea más próxima y devuelve un string
    si lo hacen
    :param title: Fecha y hora de posible tarea a verificar
    :return: Si la fecha y hora coinciden, retorna un string con el
    contenido de la tarea, si no, no devuelve nada
    """
    date_total = datetime.strptime(date_time, '%d/%m/%y %H:%M')
    date = datetime.strftime(date_total, '%d/%m/%y')
    time = datetime.strftime(date_total, '%H:%M')
    text_return = ''

    if len(list_tasks) > 0:
        for task in list_tasks:
            if task.return_date() <= date:
                if task.return_time() <= time:
                    text_return += str(task)
                    list_tasks.remove(task)
                else:
                    break
            else:
                break

    if len(text_return) > 0:
        return text_return
    else:
        return None
