import logging
from datetime import datetime, timedelta

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler, CallbackContext
)

from taskClass import ClassTask
from tasksController import *

# Logging
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

# Parametros a usar
title = ''
new_title = ''
description = ''
date_user = ''
chat_id = 0

# Etapas
INIT, CREATE_TITLE, CREATE_DESCRIPTION, CREATE_DATE, DELETE, EDIT_SEARCH_TITLE, \
    EDIT_TITLE, EDIT_DESCRIPTION, EDIT_DATE = range(9)


# FUNCIONES DE VERIFICACION Y CHEQUEO #############################################

def verify_title(text):
    if len(text) < 4:
        return (f"El nombre de la tarea debe ser mayor a 4 caracteres. ¡Intentalo de nuevo!"
                f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")

    if not isinstance(get_task(text), type(None)):
        return (f"El nombre de la tarea ya existe. ¡Reintenta con otro nombre!"
                f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")
    return ''


def verify_description(text):
    if len(text) < 4:
        return (f"La descripción de la tarea debe tener 4 o más caracteres. ¡Intentalo de nuevo!"
                f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")
    return ''


def verify_date(text):
    try:
        datetime.strptime(text, '%d/%m/%Y %H:%M')
        date_time_now = datetime.now()
        date_time_user = datetime.strptime(text, '%d/%m/%Y %H:%M')

        if date_time_user <= date_time_now:
            return (f"La fecha debe ser mayor a la actual, intentalo denuevo!"
                    f"\n>Si quieres cancelar el proceso escibre /Cancel")

    except ValueError:
        return (f"El formato debe ser DD/MM/YYYY hh:mm. ¡Intentalo de nuevo!"
                f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")
    return ''


# FLUJO PARA CREAR TAREA ##########################################################

def create_steps(update: Update, context: CallbackContext) -> int:
    global title, description, date_user
    title = ''
    description = ''
    date_user = ''

    query = update.callback_query
    query.answer()

    query.edit_message_text(text = f"Ingresa el nombre de la tarea a crear. Esta debe tener 4 o más caracteres\n"
                                   f">Si quieres cancelar el proceso, presiona este comando /Cancel")
    return CREATE_TITLE


def create_step_title(update: Update, context: CallbackContext) -> int or None:
    global title
    title = update.message.text

    if title == '/Cancel' or title == '/cancel':
        update.message.reply_text(f"Has cancelado la acción!!")
        return ConversationHandler.END

    else:
        verification = verify_title(title)

        if verification != '':
            update.message.reply_text(verification)
            return None

        update.message.reply_text(f"Ingresa la descripción de la tarea a crear. Esta debe tener 4 o más caracteres"
                                  f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")
        return CREATE_DESCRIPTION


def create_step_description(update: Update, context: CallbackContext) -> int or None:
    global description
    description = update.message.text

    if description == '/Cancel' or description == '/cancel':
        update.message.reply_text(f"Has cancelado la acción!!")
        return ConversationHandler.END

    else:
        verification = verify_description(description)

        if verification != '':
            update.message.reply_text(verification)
            return None

        update.message.reply_text(f"Ingresa la fecha de la tarea a crear,\nel formato debe ser en DD/MM/YYYY hh:mm"
                                  f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")
        return CREATE_DATE


def create_step_date(update: Update, context: CallbackContext) -> int or None:
    global title, description, date_user
    date_user = update.message.text

    if date_user == '/Cancel' or date_user == '/cancel':
        update.message.reply_text(f"Has cancelado la acción!!")
        return ConversationHandler.END

    else:
        verification = verify_date(date_user)

        if verification != '':
            update.message.reply_text(verification)
            return None

        add_task(ClassTask(title, description, date_user))

        update.message.reply_text(f"La tarea ha sido creada con éxito.\n"
                                  f"Si desea realizar otra tarea, presione este comando: /Opciones")
        return ConversationHandler.END


# PASO PARA VISUALIZAR LISTA DE TAREAS ###########################################

def visualize(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    text = visualize_tasks()

    if len(text) > 0:
        query.edit_message_text(text = text)

    else:
        query.edit_message_text("No hay tareas agregadas en la lista. ¡Empieza a crear tareas!\n"
                                "Presiona este comando: /Opciones y selecciona la opción Crear")

    return ConversationHandler.END


# PASOS PARA EDITAR TAREA ########################################################

def edit_steps(update: Update, context: CallbackContext) -> int or None:
    query = update.callback_query
    query.answer()
    text = visualize_tasks()

    if len(text) > 0:
        query.edit_message_text(text = f"Ingresa el nombre de la tarea a editar. Esta debe tener 4 o más caracteres\n"
                                       f">Si quieres cancelar el proceso, presiona este comando /Cancel")
        return EDIT_SEARCH_TITLE

    else:
        query.edit_message_text("No hay tareas en la lista. No se puede editar. Se sugiere crear una tarea.\n"
                                "Para ello presione este comando /Opciones y elija la opción Crear.")


def edit_step_find(update: Update, context: CallbackContext) -> int or None:
    global title, description, date_user
    title = update.message.text

    if title == '/Cancel' or title == '/cancel':
        update.message.reply_text(f"Has cancelado la acción!!")
        return ConversationHandler.END

    else:
        task = get_task(title)

        if isinstance(task, type(None)):
            update.message.reply_text(
                    f"Tarea no encontrada. ¡Reintentalo de nuevo!"
                    f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")
            return None

        else:
            description = task.return_description()
            date_user = task.return_date() + ' ' + task.return_time()

            update.message.reply_text(f"El nombre actual de la tarea es '{title}'.\n"
                                      f"Si deseas cambiar el nombre, escribe el nuevo, sino, escribe no.\n"
                                      f">Si quieres cancelar el proceso, presiona este comando /Cancel")
            return EDIT_TITLE


def edit_step_change_title(update: Update, context: CallbackContext) -> int or None:
    global title, new_title, description
    new_title = update.message.text

    if new_title == '/Cancel' or new_title == '/cancel':
        update.message.reply_text(f"Has cancelado la acción!!")
        return ConversationHandler.END

    else:
        if new_title == 'No' or new_title == 'no':
            update.message.reply_text(f"El título de la tarea se mantiene como '{title}'")
            new_title = title

        else:
            verification = verify_title(new_title)

            if verification != '':
                update.message.reply_text(verification)
                return None

            if new_title == title:
                update.message.reply_text(f"WARNING: El nuevo título de tarea es igual al anterior, "
                                          f"por lo que se mantiene '{title}'.\n")

            else:
                update.message.reply_text(f"Se editará el título de la tarea al finalizar el proceso a '{new_title}'.")

        update.message.reply_text(f"La descripción actual de la tarea es:\n{description}.\n"
                                  f"Si deseas cambiarla, escribe una nueva, sino, escribe 'no'.\n"
                                  f">Si quieres cancelar el proceso, presiona este comando /Cancel")
        return EDIT_DESCRIPTION


def edit_step_change_description(update: Update, context: CallbackContext) -> int or None:
    global description, date_user
    new_description = update.message.text

    if new_description == '/Cancel' or new_description == '/cancel':
        update.message.reply_text(f"Has cancelado la acción!!")
        return ConversationHandler.END

    else:
        if new_description == 'No' or new_description == 'no':
            update.message.reply_text(f"La descripción de la tarea se mantiene como:\n'{description}'\n")

        else:
            verification = verify_description(new_description)

            if verification != '':
                update.message.reply_text(verification)
                return None

            if new_description == description:
                update.message.reply_text(f"La descripción ingresada es igual a la anterior, por lo que se "
                                          f"mantiene:\n'{description}'\n")
            else:
                description = new_description
                update.message.reply_text(f"Se editará la descripción de la tarea al finalizar el proceso a:\n'{description}'\n")

        update.message.reply_text(f"La fecha/hora actual de la tarea es '{date_user}'\n"
                                  f"Si deseas cambiarla, escribe una nueva, sino, escribe 'no'.\n"
                                  f">Si quieres cancelar el proceso, presiona este comando /Cancel")
        return EDIT_DATE


def edit_step_change_date(update: Update, context: CallbackContext) -> int or None:
    global title, new_title, description, date_user
    new_date = update.message.text

    if new_date == '/Cancel' or new_date == '/cancel':
        update.message.reply_text(f"Has cancelado la acción!!")
        return ConversationHandler.END

    else:
        if new_date == 'No' or new_date == 'no':
            update.message.reply_text(f"La fecha/hora de la tarea se mantiene como '{date_user}'\n")

        else:
            verification = verify_date(new_date)

            if verification != '':
                update.message.reply_text(verification)
                return None

            if new_date == date_user:
                update.message.reply_text(f"La fecha/hora ingresada es igual a la anterior, por lo que se "
                                          f"mantiene: '{date_user}'\n")
            else:
                date_user = new_date
                update.message.reply_text(f"Se editará la fecha/hora de la tarea al finalizar el proceso a '{date_user}'\n")

        modify_task(title, new_title, description, date_user)
        update.message.reply_text(f"Se ha modificado con éxito la tarea.\n"
                                  f"Si desea realizar otra tarea, presione este comando: /Opciones")
        return ConversationHandler.END


# PASOS PARA ELIMINAR TAREA ########################################################

def remove_steps(update: Update, context: CallbackContext) -> int:
    global title
    title = ''

    query = update.callback_query
    query.answer()
    text = visualize_tasks()

    if len(text) > 0:
        query.edit_message_text(text = f"Ingresa el nombre de la tarea que deseas eliminar. Esta debe tener 4 o más caracteres\n"
                                       f">Si quieres cancelar el proceso, presiona este comando /Cancel")
        return DELETE

    else:
        query.edit_message_text("No hay tareas en la lista. No se puede eliminar. Se sugiere crear una tarea.\n"
                                "Para ello presione este comando: /Opciones y elija la opción Crear.")


def remove_step_title(update: Update, context: CallbackContext):
    global title
    title = update.message.text

    if title == '/Cancel' or title == '/cancel':
        update.message.reply_text(f"Has cancelado la acción!!")
        return ConversationHandler.END

    else:

        if not isinstance(get_task(title), type(None)):
            remove_task(title)

        else:
            update.message.reply_text(f"El título de la tarea ingresada no existe. ¡intentalo de nuevo!"
                                      f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")
            return None

        update.message.reply_text(f"La tarea ha sido eliminada con éxito.\n"
                                  f"Si desea realizar otra tarea, presione este comando: /Opciones")
        return ConversationHandler.END


# PROGRAMACION DE TAREAS AUXILIARES EN SEGUNDO PLANO #################################

def alarm(context):
    global chat_id
    ahora = datetime.now()

    if len(list_tasks) > 0:

        for i in range(len(list_tasks)):

            if list_tasks[i].date_time <= ahora:
                context.bot.send_message(chat_id = chat_id, text = f"Tarea ha finalizado:\n{str(list_tasks[i])}")
                del list_tasks[i]


def notify_less_30min(context):
    global chat_id
    ahora = datetime.now()
    por_terminar = ''

    if len(list_tasks) > 0:
        for i in range(len(list_tasks)):
            if (list_tasks[i].date_time - ahora) <= timedelta(minutes = 30):
                por_terminar += str(list_tasks[i])

        if len(por_terminar) > 0:
            context.bot.send_message(chat_id = chat_id, text = f"Tareas por finalizar en menos de 30 minutos:\n{por_terminar}")


# CONTROL DE INICIO DE LA APLICACION DE TELEGRAM ########################################

def start(update: Update, context: CallbackContext):
    global chat_id
    chat_id = update.message.chat_id

    update.message.reply_text(f"¡¡¡ Bienvenido al bot controlador de tareas !!!\n\n"
                              f"Para ver las opciones disponibles, solo presiona este comando: /Opciones")

    context.job_queue.run_repeating(alarm, interval = 60, context = update.message.chat_id)
    context.job_queue.run_repeating(notify_less_30min, interval = 60 * 15, context = update.message.chat_id)


def options(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    keyboard = [
        [
            InlineKeyboardButton("Crear", callback_data = "CREAR"),
            InlineKeyboardButton("Visualizar", callback_data = "VISUALIZAR"),
        ],
        [
            InlineKeyboardButton("Editar", callback_data = "EDITAR"),
            InlineKeyboardButton("Eliminar", callback_data = "ELIMINAR"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Elige una de las siguientes opciones disponibles:", reply_markup = reply_markup)
    return INIT


# MANEJO PRINCIPAL DE LA APP DE TELEGRAM: CONFIGURACION, HANDLERS Y UPDATE ###############

def main():
    updater = Updater('2100146208:AAG2Je-LpR54dMBklwg6YXLHZwkDzfYdYQU', use_context = True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
            entry_points = [CommandHandler('Opciones', options)],
            states = {
                    INIT: [
                            CallbackQueryHandler(create_steps, pattern = '^CREAR$'),
                            CallbackQueryHandler(visualize, pattern = '^VISUALIZAR$'),
                            CallbackQueryHandler(remove_steps, pattern = '^ELIMINAR$'),
                            CallbackQueryHandler(edit_steps, pattern = '^EDITAR$')
                    ],
                    CREATE_TITLE: [MessageHandler(Filters.text, create_step_title)],
                    CREATE_DESCRIPTION: [MessageHandler(Filters.text, create_step_description)],
                    CREATE_DATE: [MessageHandler(Filters.text, create_step_date)],
                    DELETE: [MessageHandler(Filters.text, remove_step_title)],
                    EDIT_SEARCH_TITLE: [MessageHandler(Filters.text, edit_step_find)],
                    EDIT_TITLE: [MessageHandler(Filters.text, edit_step_change_title)],
                    EDIT_DESCRIPTION: [MessageHandler(Filters.text, edit_step_change_description)],
                    EDIT_DATE: [MessageHandler(Filters.text, edit_step_change_date)],
            },
            fallbacks = [CommandHandler('Opciones', options)],
    )

    dp.add_handler(CommandHandler('Start', start))
    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
