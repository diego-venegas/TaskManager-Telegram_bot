from datetime import datetime


class ClassTask:
    """
    La clase tarea tiene como objetivo definir
    y guardar una tarea que el usuario desee
    crear

    La clase posee los siguientes parametros:
        - Titulo
        - Descripción
        - Fecha y hora
        - Color

    La clase posee los siguientes métodos:

        /Visualizar Datos/
        - Imprimir Titulo
        - Imprimir Descripción
        - Imprimir Fecha
        - Imprimir Hora
        - Imprimir Color

        /Modificar Datos/
        - Modificar Titulo
        - Modificar Descripción
        - Modificar Fecha y Hora
        - Modificar Color

    """

    def __init__(self, title, description, date, color='#FFFFFF'):
        self.title = title
        # Inicializamos el titulo de la tarea
        self.description = description
        # Inicializamos la descripcion de la tarea
        self.date_time = datetime.strptime(date, '%d/%m/%y %H:%M')
        # Inicializamos la fecha y hora de la tarea
        self.color = color
        # Inicializamos el color de la tarea en formato #HEX

    # Retorna el titulo de la tarea
    def print_title(self):
        print(self.title)

    # Retorna la descripción de la tarea
    def print_description(self):
        print(self.description)

    # Retorna la fecha de la tarea con formato DIA/MES/AÑO
    def print_date(self):
        print(
            datetime.strftime(self.date_time, '%d/%m/%y')
        )

    # Retorna la hora y minuto de la tarea con formato HORA:MINUTO
    def print_time(self):
        print(
            datetime.strftime(self.date_time, '%H:%M')
        )

    # Retorna el color asignado de la tarea
    def print_color(self):
        print(self.color)

    # Modifica el titulo de la tarea
    def modify_title(self, title):
        self.title = title

    # Modifica la descripción de la tarea
    def modify_description(self, description):
        self.description = description

    # Modifica la fecha y hora de la tarea
    def modify_date_time(self, date):
        self.date_time = datetime.strptime(date, '%d/%m/%y %H:%M')

    # Modifica el color de la tarea
    def modify_color(self, color):
        self.color = color


'''
# Programa ejemplo uso de la clase Tarea
print('\nEjemplo uso de clase Tarea: \n')
Tarea1 = ClassTask('Reunion', 'Reunion con la Universidad', '1/12/21 22:30')

Tarea1.print_title()
Tarea1.print_description()
Tarea1.print_date()
Tarea1.print_time()
Tarea1.print_color()

print('\nModificaciones: \n')
Tarea1.modify_title('Reunion 2')
Tarea1.print_title()

Tarea1.modify_description('Reunion con la Universidad 2')
Tarea1.print_description()

Tarea1.modify_date_time('1/1/22 10:30')
Tarea1.print_date()
Tarea1.print_time()

Tarea1.modify_color('#000000')
Tarea1.print_color()

print('\n')
'''
