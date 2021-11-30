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

if __name__ == '__main__':
    unittest.main()