from datetime import datetime


class ClassTask:
    def __init__(self, tittle, description, date, color='#FFFFFF'):
        self.tittle = tittle
        self.description = description
        self.date_time = datetime.strptime(date, '%d/%m/%y %H:%M')
        self.color = color

    def print_tittle(self):
        print(self.tittle)

    def print_description(self):
        print(self.description)

    def print_date(self):
        print(
            datetime.strftime(self.date_time, '%d/%m/%y')
        )

    def print_time(self):
        print(
            datetime.strftime(self.date_time, '%H:%M')
        )

    def print_color(self):
        print(self.color)

Tarea1 = ClassTask('Reunion', 'Reunion con la Universidad', '1/12/21 22:30')

Tarea1.print_tittle()
Tarea1.print_description()
Tarea1.print_date()
Tarea1.print_time()
Tarea1.print_color()