from telegram.ext import (
    Updater,
    CommandHandler
)
import telegram
import time
import tasksController


class Question:

    def __init__(self, text, list_answers, correct_answers):
        self.text = text
        self.list_answers = list_answers
        self.correct_answers = correct_answers


def add_typing(update, context):
    context.bot.send_chat_action(
        chat_id=get_chat_id(update, context),
        action=telegram.ChatAction.TYPING,
        timeout=1,
    )
    time.sleep(1)


def get_chat_id(update, context):
    chat_id = -1
    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]

    return chat_id


def create_commander(update, context):
    c_id = get_chat_id(update, context)
    add_typing(update, context)
    context.bot.send_message(chat_id=get_chat_id(update, context),
                             text=f"Hola estoy creando")

    print("ewq")


def edit_commander(update, context):
    c_id = get_chat_id(update, context)
    add_typing(update, context)
    context.bot.send_message(chat_id=get_chat_id(update, context),
                             text=f"Hola, estoy editando")


def remover_commander(update, context):
    c_id = get_chat_id(update, context)
    add_typing(update, context)
    context.bot.send_message(chat_id=get_chat_id(update, context),
                             text=f"Hola, estoy eliminando")


def visualize_commander(update, context):
    c_id = get_chat_id(update, context)
    add_typing(update, context)
    context.bot.send_message(chat_id=get_chat_id(update, context),
                             text=tasksController.visualize_tasks())


def main():

    updater = Updater('2100146208:AAG2Je-LpR54dMBklwg6YXLHZwkDzfYdYQU', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("Crear", create_commander))
    dp.add_handler(CommandHandler("Editar", edit_commander))
    dp.add_handler(CommandHandler("Eliminar", remover_commander))
    dp.add_handler(CommandHandler("Visualizar", visualize_commander))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    tasksController.add_task(tasksController.ClassTask('Reunion', 'Reunion con la Universidad', '1/12/21 22:30'))
    tasksController.add_task(tasksController.ClassTask('Reunion2', 'Reunion con la Universidad', '1/12/21 22:30'))
    main()
