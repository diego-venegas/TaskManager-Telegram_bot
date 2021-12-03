from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler
)

from tasksController import *
from datetime import datetime

# Pasos crear tarea
CT_TITLE, CT_DESCRIPTION, CT_DATE = range(3)
title = ''
description = ''
date = ''

# Pasos eliminar tarea
DE_NAME = range(1)

# Pasos editar tarea
ED_NAME, ED_DESCRIPTION, ED_DATE = range(3)


def get_chat_id(update, context):
    chat_id = -1
    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]

    return chat_id


def cancel(update, context):
    update.message.reply_text(f"Has cancelado la acción!!")
    return ConversationHandler.END


##########################################

def create_steps(update, context):
    global title, description, date
    title = ''
    description = ''
    date = ''

    update.message.reply_text(f"Ingresa el nombre de la tarea a crear, esta debe ser mayor a 4 caracteres"
                              f"\n>Si quieres cancelar el proceso escibre /Cancel")
    return CT_TITLE


def create_step_title(update, context):
    global title
    title = update.message.text

    if title == '/Cancel':
        cancel(update, context)
        return ConversationHandler.END

    else:

        if len(title) < 4:
            update.message.reply_text(f"El nombre de la tarea debe ser mayor a 4 caracteres, intentalo denuevo!"
                                      f"\n>Si quieres cancelar el proceso escibre /Cancel")
            return None

        update.message.reply_text(f"Ingresa la descripción de la tarea a crear, sta debe ser mayor a 4 caracteres"
                                  f"\n>Si quieres cancelar el proceso escibre /Cancel")
        return CT_DESCRIPTION


def create_step_description(update, context):
    global description
    description = update.message.text

    if description == '/Cancel':
        cancel(update, context)
        return ConversationHandler.END

    else:

        if len(description) < 4:
            update.message.reply_text(f"La descripcióin de la tarea debe ser mayor a 4 caracteres, intentalo denuevo!"
                                      f"\n>Si quieres cancelar el proceso escibre /Cancel")
            return None

        update.message.reply_text(f"Ingresa la fecha de la tarea a crear, \nel formato es DIA/MES/AÑO HORA:MINUTO")
        return CT_DATE


def create_step_date(update, context):
    global title, description, date
    date = update.message.text

    if date == '/Cancel':
        cancel(update, context)
        return ConversationHandler.END

    else:

        try:
            datetime.strptime(date, '%d/%m/%y %H:%M')

        except ValueError:

            update.message.reply_text(f"El formato debe ser DIA/MES/AÑO HORA:MINUTO, intentalo denuevo!"
                                      f"\n>Si quieres cancelar el proceso escibre /Cancel")
            return None

        add_task(ClassTask(title, description, date))

        update.message.reply_text(f"La tarea a sido creada con exito")
        return ConversationHandler.END


############################################


def visualize(update, context):
    update.message.reply_text(visualize_tasks())


############################################


def main():
    updater = Updater('2100146208:AAG2Je-LpR54dMBklwg6YXLHZwkDzfYdYQU', use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('Visualizar', visualize))

    ct_conv_hand = ConversationHandler(
        entry_points=[CommandHandler('Crear', create_steps)],
        states={
            CT_TITLE: [MessageHandler(Filters.text, create_step_title)],
            CT_DESCRIPTION: [MessageHandler(Filters.text, create_step_description)],
            CT_DATE: [MessageHandler(Filters.text, create_step_date)]
        },
        fallbacks=[CommandHandler('Cancel', cancel)]
    )

    dp.add_handler(ct_conv_hand)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()