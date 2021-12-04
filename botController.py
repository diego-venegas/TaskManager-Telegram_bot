from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler
)

from tasksController import *

title = ''
description = ''
date_user = ''
count = 0

# Pasos crear tarea
CT_TITLE, CT_DESCRIPTION, CT_DATE = range(3)

# Pasos eliminar tarea
DE_NAME = range(1)

# Pasos editar tarea
ED_NAME, ED_DESCRIPTION, ED_DATE = range(3)


def cancel(update, context):
    update.message.reply_text(f"Has cancelado la acción!!")
    text = visualize_tasks()
    if len(text) > 0:
        start(update, context)
    return ConversationHandler.END


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
        cancel(update, context)
        return ConversationHandler.END

    else:

        if len(title) < 4:
            update.message.reply_text(f"El nombre de la tarea debe ser mayor a 4 caracteres. ¡Intentalo de nuevo!"
                                      f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")
            return None

        if not isinstance(get_task(title), type(None)):
            update.message.reply_text(f"El nombre de la tarea ya existe. ¡Reintenta con otro nombre!"
                                      f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")
            return None

        update.message.reply_text(f"Ingresa la descripción de la tarea a crear. Esta debe tener 4 o más caracteres"
                                  f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")
        return CT_DESCRIPTION


def create_step_description(update, context):
    global description
    description = update.message.text

    if description == '/Cancel':
        cancel(update, context)
        return ConversationHandler.END

    else:

        if len(description) < 4:
            update.message.reply_text(f"La descripción de la tarea debe tener 4 o más caracteres. ¡Intentalo de nuevo!"
                                      f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")
            return None

        update.message.reply_text(f"Ingresa la fecha de la tarea a crear, \nel formato debe ser en DD/MM/YYYY hh:mm")
        return CT_DATE


def create_step_date(update, context):
    global title, description, date_user
    date_user = update.message.text

    if date_user == '/Cancel' or date_user == '/cancel':
        cancel(update, context)
        return ConversationHandler.END

    else:

        try:
            datetime.strptime(date_user, '%d/%m/%Y %H:%M')

        except ValueError:

            update.message.reply_text(f"El formato debe ser DD/MM/YYYY hh:mm. ¡Intentalo de nuevo!"
                                      f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")
            return None

        date_time_now = datetime.now()
        date_time_user = datetime.strptime(date_user, '%d/%m/%Y %H:%M')

        if date_time_user <= date_time_now:

            update.message.reply_text(f"La fecha debe ser mayor a la actual, intentalo denuevo!"
                                     f"\n>Si quieres cancelar el proceso escibre /Cancel")
            return None

        add_task(ClassTask(title, description, date_user))

        update.message.reply_text(f"La tarea ha sido creada con éxito")
        start(update, context)
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

############################################


def remove_steps(update, context):
    global title
    title = ''

    update.message.reply_text(f"Ingresa el nombre de la tarea que deseas eliminar, esta debe ser mayor a 4 caracteres"
                              f"\n>Si quieres cancelar el proceso escibre /Cancel")
    return DE_NAME


def remove_step_title(update, context):
    global title
    title = update.message.text

    if title == '/Cancel':
        cancel(update, context)
        return ConversationHandler.END

    else:

        if not isinstance(get_task(title), type(None)):

            remove_task(title)

        else:

            update.message.reply_text(f"El título de la tarea ingresada no existe. ¡intentalo de nuevo!"
                                      f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")
            return None

        update.message.reply_text(f"La tarea ha sido eliminada con éxito")
        start(update, context)
        return ConversationHandler.END


def alarm(context):
    global count
    count += 1
    print(f'Saludos realizados: {count}')
    ahora = datetime.now()
    if list_tasks[0].datetime <= ahora:
        print("Fecha primera tarea es menor a la fecha actual. Tarea se elimina de la lista")
        del list_tasks[0]


def start(update, context):
    context.job_queue.run_repeating(alarm, interval = 60, context = update.message.chat_id)


############################################

def main():
    updater = Updater('2100146208:AAG2Je-LpR54dMBklwg6YXLHZwkDzfYdYQU', use_context=True)

    dp = updater.dispatcher

    ct_conv_hand = ConversationHandler(
        entry_points=[CommandHandler('Crear', create_steps)],
        states={
            CT_TITLE: [MessageHandler(Filters.text, create_step_title)],
            CT_DESCRIPTION: [MessageHandler(Filters.text, create_step_description)],
            CT_DATE: [MessageHandler(Filters.text, create_step_date)]
        },
        fallbacks=[CommandHandler('Cancel', cancel)]
    )

    de_conv_hand = ConversationHandler(
        entry_points=[CommandHandler('Eliminar', remove_steps)],
        states={
            DE_NAME: [MessageHandler(Filters.text, remove_step_title)],
        },
        fallbacks=[CommandHandler('Cancel', cancel)]
    )

    dp.add_handler(CommandHandler('Visualizar', visualize))
    dp.add_handler(CommandHandler('Start', start))
    dp.add_handler(ct_conv_hand)
    dp.add_handler(de_conv_hand)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
