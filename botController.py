import logging
from datetime import datetime, timedelta

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler
)

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

# Pasos crear tarea
CT_TITLE, CT_DESCRIPTION, CT_DATE = range(3)

# Pasos eliminar tarea
DE_NAME = range(1)

# Pasos editar tarea
ED_FIND, ED_TITLE, ED_DESCRIPTION, ED_DATE = range(4)


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


##########################################

def create_steps(update, context):
    global title, description, date_user
    title = ''
    description = ''
    date_user = ''

    update.message.reply_text(f"Ingresa el nombre de la tarea a crear. Esta debe tener 4 o más caracteres"
                              f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")
    return CT_TITLE


def create_step_title(update, context):
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
        return CT_DESCRIPTION


def create_step_description(update, context):
    global description
    description = update.message.text

    if description == '/Cancel':
        update.message.reply_text(f"Has cancelado la acción!!")
        return ConversationHandler.END

    else:
        verification = verify_description(description)

        if verification != '':
            update.message.reply_text(verification)
            return None

        update.message.reply_text(f"Ingresa la fecha de la tarea a crear, \nel formato debe ser en DD/MM/YYYY hh:mm")
        return CT_DATE


def create_step_date(update, context):
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

        update.message.reply_text(f"La tarea ha sido creada con éxito")
        return ConversationHandler.END


############################################


def visualize(update, context):
    text = visualize_tasks()

    if len(text) > 0:
        update.message.reply_text(text)
        start(update, context)

    else:
        update.message.reply_text("No hay tareas agregadas. ¡Empieza a crear!")


############################################


def edit_steps(update, context):
    update.message.reply_text(f"Ingresa el nombre de la tarea a editar. Esta debe tener 4 o más caracteres"
                              f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")
    return ED_FIND


def edit_step_find(update, context):
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
            return ED_TITLE


def edit_step_change_title(update, context):
    global title, new_title, description
    new_title = update.message.text

    if new_title == '/Cancel' or new_title == '/cancel':
        update.message.reply_text(f"Has cancelado la acción!!")
        return ConversationHandler.END

    else:

        if new_title == 'No' or new_title == 'no':

            update.message.reply_text(f"El título de la tarea se mantiene como '{title}'\n"
                                      f">Si quieres cancelar el proceso, presiona este comando /Cancel")

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

                update.message.reply_text(f"Se ha editado el título de la tarea con éxito a '{new_title}'.")

        update.message.reply_text(f"La descripción actual de la tarea es:\n{description}.\n"
                                  f"Si deseas cambiarla, escribe una nueva, sino, escribe 'no'.\n"
                                  f">Si quieres cancelar el proceso, presiona este comando /Cancel")
        return ED_DESCRIPTION


def edit_step_change_description(update, context):
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
                update.message.reply_text(f"Se ha editado la descripción de la tarea con éxito a:\n'{description}'\n")

        update.message.reply_text(f"La fecha/hora actual de la tarea es '{date_user}'\n"
                                  f"Si deseas cambiarla, escribe una nueva, sino, escribe 'no'.\n"
                                  f">Si quieres cancelar el proceso, presiona este comando /Cancel")
        return ED_DATE


def edit_step_change_date(update, context):
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
                update.message.reply_text(f"Se ha editado la fecha/hora de la tarea con éxito a '{date_user}'\n")

        modify_task(title, new_title, description, date_user)
        update.message.reply_text(f"Se ha modificado con éxito la tarea.")
        return ConversationHandler.END


############################################


def remove_steps(update, context):
    global title
    title = ''

    update.message.reply_text(f"Ingresa el nombre de la tarea que deseas eliminar, esta debe ser mayor a 4 caracteres"
                              f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")
    return DE_NAME


def remove_step_title(update, context):
    global title
    title = update.message.text

    if title == '/Cancel':
        update.message.reply_text(f"Has cancelado la acción!!")
        return ConversationHandler.END

    else:
        if not isinstance(get_task(title), type(None)):
            remove_task(title)

        else:
            update.message.reply_text(f"El título de la tarea ingresada no existe. ¡intentalo de nuevo!"
                                      f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")
            return None

        update.message.reply_text(f"La tarea ha sido eliminada con éxito")
        return ConversationHandler.END


def alarm(context):
    global chat_id
    ahora = datetime.now()
    if len(list_tasks) > 0 and list_tasks[0].date_time <= ahora:
        context.bot.send_message(chat_id = chat_id, text = f"Tarea ha finalizado:\n{str(list_tasks[0])}")
        print("Fecha primera tarea es menor a la fecha actual. Tarea se elimina de la lista")
        del list_tasks[0]


def start(update, context):
    global chat_id
    chat_id = update.message.chat_id
    context.job_queue.run_repeating(alarm, interval = 60, context = update.message.chat_id)


############################################

def main():
    updater = Updater('2100146208:AAG2Je-LpR54dMBklwg6YXLHZwkDzfYdYQU', use_context = True)

    dp = updater.dispatcher

    ct_conv_hand = ConversationHandler(
        entry_points=[CommandHandler('Crear', create_steps)],
        states={
            CT_TITLE: [MessageHandler(Filters.text, create_step_title)],
            CT_DESCRIPTION: [MessageHandler(Filters.text, create_step_description)],
            CT_DATE: [MessageHandler(Filters.text, create_step_date)]
        },
        fallbacks=[CommandHandler('Cancel', create_steps)]
    )

    de_conv_hand = ConversationHandler(
        entry_points=[CommandHandler('Eliminar', remove_steps)],
        states={
            DE_NAME: [MessageHandler(Filters.text, remove_step_title)],
        },
        fallbacks=[CommandHandler('Cancel', remove_steps)]
    )

    ed_conv_hand = ConversationHandler(
        entry_points=[CommandHandler('Editar', edit_steps)],
        states={
            ED_FIND: [MessageHandler(Filters.text, edit_step_find)],
            ED_TITLE: [MessageHandler(Filters.text, edit_step_change_title)],
            ED_DESCRIPTION: [MessageHandler(Filters.text, edit_step_change_description)],
            ED_DATE: [MessageHandler(Filters.text, edit_step_change_date)]
        },
        fallbacks=[CommandHandler('Cancel', edit_steps)]
    )

    dp.add_handler(CommandHandler('Visualizar', visualize))
    dp.add_handler(CommandHandler('Start', start))
    dp.add_handler(ct_conv_hand)
    dp.add_handler(de_conv_hand)
    dp.add_handler(ed_conv_hand)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
