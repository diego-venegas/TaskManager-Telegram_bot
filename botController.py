import logging
from datetime import timedelta

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler, CallbackContext
)

from tasksController import *

# LOGGING ########################################################################
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

# PARAMETROS DE USO EN TAREAS ####################################################
title = ''
new_title = ''
description = ''
date_user = ''
chat_id = 0

# ETAPAS DEL HANDLER DE CONVERSACION #############################################
INIT, CREATE_TITLE, CREATE_DESCRIPTION, CREATE_DATE, DELETE, EDIT_SEARCH_TITLE, \
    EDIT_TITLE, EDIT_DESCRIPTION, EDIT_DATE = range(9)


# FUNCIONES DE VERIFICACION Y CHEQUEO ############################################

def verify_title(text):
    """
    Funcion que verifica si un titulo cumple con los requisitos establecidos para el mismo,
    correspondientes a un largo mayor o igual a 4 carateres y que no se encuentra ya creada.
    @param text: Titulo ingresado para ser verificado.
    @return: String con un posible mensaje de error o vacio.
    """
    if len(text) < 4:
        return (f"El nombre de la tarea debe ser mayor a 4 caracteres. ¡Intentalo de nuevo!"
                f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")

    if not isinstance(get_task(text), type(None)):
        return (f"El nombre de la tarea ya existe. ¡Reintenta con otro nombre!"
                f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")
    return ''


def verify_description(text):
    """
    Funcion que verifica si una descripcion cumple con los requisitos establecidos para la misma,
    correspondientes a un largo mayor o igual a 4 carateres.
    @param text: Descripcion ingresada para ser verificada.
    @return: String con un posible mensaje de error o vacio.
    """
    if len(text) < 4:
        return (f"La descripción de la tarea debe tener 4 o más caracteres. ¡Intentalo de nuevo!"
                f"\n>Si quieres cancelar el proceso, presiona este comando /Cancel")
    return ''


def verify_date(text):
    """
    Funcion que verifica si una fecha cumple con los requisitos establecidos para la misma,
    principalmente respectivas a su formato y si es una fecha valida mayor a la actual.
    @param text: Fecha ingresada para ser verificada.
    @return: String con un posible mensaje de error o vacio.
    """
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
    """
    Funcion que representa el primer paso en la creacion de una tarea en el bot.
    Establece las variables auxiliares a usar para su creacion como strings vacios,
    responde el callback y pregunta al usuario por el titulo de la tarea.
    @param update: Controlador de actualizacion del bot.
    @param context: Contexto del usuario dentro del bot.
    @return: Entero identificador del segundo paso en la creacion de una tarea
    """
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
    """
    Funcion que representa el segundo paso en la creacion de una tarea en el bot.
    Recibe el titulo escrito y enviado por el usuario, lo procesa y verifica que sea correcto.
    Si es correcto pregunta al usuario por la descripcion de la tarea. Si no lo es, continua
    preguntando por el ingreso de un titulo valido.
    El usuario siempre puede salir al presionar el comando Cancel.
    @param update: Controlador de actualizacion del bot.
    @param context: Contexto del usuario dentro del bot.
    @return: Entero identificador del tercer paso en la creacion de una tarea o nada reiniciando la funcion
    """
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
    """
    Funcion que representa el tercer paso en la creacion de una tarea en el bot.
    Recibe la descripcion escrita y enviada por el usuario, la procesa y verifica que sea correcta.
    Si es correcta pregunta al usuario por la fecha y hora a la que se realiza la tarea.
    Si no lo es, continua preguntando por el ingreso de una descripcion valida.
    El usuario siempre puede salir al presionar el comando Cancel.
    @param update: Controlador de actualizacion del bot.
    @param context: Contexto del usuario dentro del bot.
    @return: Entero identificador del cuarto paso en la creacion de una tarea o nada reiniciando la funcion.
    """
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
    """
    Funcion que representa el cuarto y ultimo paso en la creacion de una tarea en el bot.
    Recibe la fecha y hora escrita y enviada por el usuario, la procesa y verifica que sea correcta.
    Si es correcta la tarea es guardada en la lista de tareas, terminando el proceso de creacion.
    Si no lo es, continua preguntando por el ingreso de una fecha y hora valida.
    El usuario siempre puede salir al presionar el comando Cancel.
    @param update: Controlador de actualizacion del bot.
    @param context: Contexto del usuario dentro del bot.
    @return: Un entero que confirma la correcta creacion de la tarea o nada reinciando la funcion.
    """
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
    """
    Funcion que permite la visualizacion de la lista de tareas, al recibir como callback de que presiono
    el boton correspondiente para visualizar tareas.
    @param update: Controlador de actualizacion del bot.
    @param context: Contexto del usuario dentro del bot.
    @return: Entero identificador de exito en mostrar lista de tareas o en enviar mensaje al usuario.
    """
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
    """
    Funcion que permite iniciar un proceso de edicion de tarea, al recibir como callback que se presiono
    el boton correspondiente. Responde el callback, verifica si hay tareas en la lista central de tareas
    y envia un mensaje al usuario con el resultado.
    Si existen tareas pregunta al usuario por el nombre de la tarea que se debe editar y procede al primer
    paso en el proceso de edicion que corresponde a buscar dicho nombre. Si no hay tareas en la lista,
    se notifica al usuario y se termina el proceso.
    @param update: Controlador de actualizacion del bot.
    @param context: Contexto del usuario dentro del bot.
    @return: Entero identificador del primer paso en el proceso de edicion de tarea o de que termino la misma
    porque no hay tareas en lista.
    """
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
    """
    Funcion que corresponde al primer paso de editar una tarea. Recibe el texto ingresado del usuario
    correspondiente al nombre de la tarea que desea modificar y que se debe buscar. Se realiza
    verificacion de si la tarea existe, y si se encuentra solicita al usuario el nuevo nombre de la
    tarea. El usuario puede responder 'no' para saltar este paso y mantener el nombre actual.
    El usuario siempre puede salir al presionar el comando Cancel.
    @param update: Controlador de actualizacion del bot.
    @param context: Contexto del usuario dentro del bot.
    @return: Entero identificador del segundo paso en el proceso de edicion de tarea, identificador
    de salida o nada reiniciando la funcion.
    """
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
    """
    Funcion que corresponde al segundo paso de editar una tarea. Recibe el texto ingresado del usuario
    correspondiente a un 'no', 'cancel' o un string que es el nuevo nombre de la tarea. Se realiza
    verificacion de si este string es un titulo valido, y si lo es, es guardado temporalmente
    mientras aun se encuentra en edicion la tarea, para luego preguntar al usuario por si desea cambiar
    la descripcion de la tarea. El usuario puede responder 'no' para saltar este paso y mantener la
    descripcion actual.
    El usuario siempre puede salir al presionar el comando Cancel, pero esto anula todos los cambios
    realizados, por no completar el proceso.
    @param update: Controlador de actualizacion del bot.
    @param context: Contexto del usuario dentro del bot.
    @return: Entero identificador del tercer paso en el proceso de edicion de tarea, identificador
    de salida o nada reiniciando la funcion.
    """
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
    """
    Funcion que corresponde al tercer paso de editar una tarea. Recibe el texto ingresado del usuario
    correspondiente a un 'no', 'cancel' o un string que es la nueva descripcion de la tarea. Se realiza
    verificacion de si este string es una descripcion valida, y si lo es, es guardada temporalmente
    mientras aun se encuentra en edicion la tarea, para luego preguntar al usuario por si desea cambiar la
    fecha y hora de la tarea. El usuario puede responder 'no' para saltar este paso y mantener la
    fecha y hora actual.
    Si la verificacion falla se reinicia la funcion y se vuelve a preguntar.
    El usuario siempre puede salir al presionar el comando Cancel, pero esto anula todos los cambios
    realizados, por no completar el proceso.
    @param update: Controlador de actualizacion del bot.
    @param context: Contexto del usuario dentro del bot.
    @return: Entero identificador del cuarto paso en el proceso de edicion de tarea, identificador de
    salida o nada reiniciando la funcion.
    """
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
    """
    Funcion que corresponde al cuarto paso de editar una tarea. Recibe el texto ingresado del usuario
    correspondiente a un 'no', 'cancel' o un string que es la nueva fecha y hora de la tarea. Se realiza
    verificacion de si esta fecha es valida, y si lo es, es guardada temporalmente mientras aun se
    encuentra en edicion la tarea, para luego terminar el proceso de edición guardando los cambios en la
    tarea respectiva en la lista de tareas.
    Si la verificacion falla se reinicia la funcion y se vuelve a preguntar.
    El usuario siempre puede salir al presionar el comando Cancel, pero esto anula todos los cambios
    realizados, por no completar el proceso.
    @param update: Controlador de actualizacion del bot.
    @param context: Contexto del usuario dentro del bot.
    @return: Entero identificador de éxito en el proceso de edicion de tarea, identificador de salida
    o nada reiniciando la funcion.
    """
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

def remove_steps(update: Update, context: CallbackContext) -> int or None:
    """
    Funcion que permite iniciar un proceso de eliminacion de una tarea, al recibir como callback que se presiono
    el boton correspondiente. Responde el callback, verifica si hay tareas en la lista central de tareas
    y envia un mensaje al usuario con un mensaje o una solicitud segun corresponda.
    Si existen tareas pregunta al usuario por el nombre de la tarea que se desea eliminar y procede al siguiente
    paso en el proceso de eliminacion definitiva de la tarea segun su nombre. Si no hay tareas en la lista,
    se notifica al usuario y se termina el proceso.
    @param update: Controlador de actualizacion del bot.
    @param context: Contexto del usuario dentro del bot.
    @return: Entero identificador del paso eliminar tarea o de salida si no hay tareas en lista.
    """
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


def remove_step_title(update: Update, context: CallbackContext) -> int or None:
    """
    Funcion que corresponde al unico paso en el proceso de eliminar una tarea, que verifica si el nombre
    ingresado por el usuario de la tarea existe y si es asi, la elimina de la lista. Si no se encuentra la
    tarea se vuelve a preguntar al usuario.
    El usuario siempre puede salir al presionar el comando Cancel.
    @param update: Controlador de actualizacion del bot.
    @param context: Contexto del usuario dentro del bot.
    @return: Entero identificador de éxito en el proceso o de salida si usuario cancela.
    """
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


# PROGRAMACION DE TAREAS AUXILIARES EN SEGUNDO PLANO (CRONJOB) #################################

def alarm(context):
    """
    Funcion que establece un trabajo en segundo plano de manera cronológica (cron) para observar
    si hay tareas en la lista que ya han terminado cada minuto, avisando al usaurio si existe alguna que
    efectivamente haya terminado y eliminadola de la lista de tareas.
    @param context: Contexto del usuario dentro del bot.
    @return: Void
    """
    global chat_id
    ahora = datetime.now()

    if len(list_tasks) > 0:

        for i in range(len(list_tasks)):

            if list_tasks[i].date_time <= ahora:
                context.bot.send_message(chat_id = chat_id, text = f"Tarea ha finalizado:\n{str(list_tasks[i])}")
                del list_tasks[i]


def notify_less_30min(context):
    """
    Funcion que establece un trabajo en segundo plano de manera cronológica (cron) para retornar al
    usuario a modo de mensaje cada 15 min, y si existen tareas en lista, aquellas tareas que estén
    por terminar dentro de 30 minutos.
    @param context: Contexto del usuario dentro del bot.
    @return: Void
    """
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
    """
    Funcion relacioanda alc omando de inicio del bot, que es el primer comando en ser ejecutado una vez se
    accede al bot mismo. Esta funcion da la bienvenida al usuario y le presenta los comandos que peude usar,
    así como inicia tambien los trabajos en segundo plano para verificar plazos de tareas y entregar
    informacion en tiempo.
    @param update: Controlador de actualizacion del bot.
    @param context: Contexto del usuario dentro del bot.
    @return: Void
    """
    global chat_id
    chat_id = update.message.chat_id

    update.message.reply_text(f"¡¡¡ Bienvenido al bot controlador de tareas !!!\n\n"
                              f"Para ver las opciones disponibles, solo presiona este comando: /Opciones")

    context.job_queue.run_repeating(alarm, interval = 60, context = update.message.chat_id)
    context.job_queue.run_repeating(notify_less_30min, interval = 60 * 15, context = update.message.chat_id)


def options(update: Update, context: CallbackContext) -> int:
    """
    Funcion que genera botones en el chat para dar opciones al usuario, el cual al ser
    presionados generan un callback el cual es capturado por alguna de los estados
    dentro de un Handler de conversacion, el cual permite realizar el proceso
    correspondiente a dicho boton.
    @param update: Controlador de actualizacion del bot.
    @param context: Contexto del usuario dentro del bot.
    @return: Identificador de Paso inicial.
    """
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
    # Updater y dispacher del bot para manejo de control de estado en chat.
    updater = Updater('2100146208:AAG2Je-LpR54dMBklwg6YXLHZwkDzfYdYQU', use_context = True)

    dp = updater.dispatcher

    # Handler de conversacion global que maneja las posibles funcionalidades del bot
    # a través de botones, y que se activa al escribir en chat /Opciones.
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

    # Se agregan los handler de conversacion global y de inicio al dispacher
    dp.add_handler(CommandHandler('Start', start))
    dp.add_handler(conv_handler)

    # Se inicicializa el bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
