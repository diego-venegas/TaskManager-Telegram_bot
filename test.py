import unittest
from tasksController import *
from taskClass import *

class Tests(unittest.TestCase):
    def test_add_task(self):
        """
        Prueba add_task de taskController
        """
        lista_inicial=list_tasks
        Tarea1 = ClassTask('Reunion', 'Reunion con la Universidad', '1/12/21 22:30')
        add_task(Tarea1)
        self.assertEquals(len(lista_inicial)+1, len(list_tasks))
        self.assertNotEquals(get_task('Reunion'), 'Error')

    def test_remove_task(self):
        """
        Prueba remove_task de taskController
        """   
        Tarea = ClassTask('Reunion1', 'Reunion con la Universidad', '1/12/21 22:00')
        add_task(Tarea)
        lista_inicial=list_tasks
        remove_task('Reunion1')
        self.assertEquals(len(lista_inicial)-1, len(list_tasks))
        self.assertEquals(get_task('Reunion1'), 'Error')

    def test_modify_task(self):
        """
        Prueba modify_task de taskController
        """   
        Tarea = ClassTask('Reunion1', 'Reunion con la Universidad', '1/12/21 22:00')
        add_task(Tarea)
        lista_inicial=list_tasks
        modify_task('Reunion1', 'Reunion1', 'Destruir Universidad', '1/12/21 22:00')
        self.assertEquals(len(lista_inicial), len(list_tasks))
        self.assertNotEquals(get_task('Reunion1'), Tarea)
        modify_task('Reunion1', 'Reunion2', 'Destruir Universidad', '1/12/21 22:00')
        self.assertEquals(get_task('Reunion1'), 'Error')

if __name__ == '__main__':
    unittest.main()