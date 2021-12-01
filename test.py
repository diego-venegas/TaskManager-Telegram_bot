import unittest
from tasksController import *
from taskClass import *

class Tests(unittest.TestCase):
    def test_add_task(self):
        """
        Prueba add_task de taskController
        add_task(ClassTask task) -> 
        add_task recibe un objeto de tipo ClassTask y lo agrega a la lista list_tasks,
        que los ordena desde el de fecha más lejana al de fecha más cercana
        """
        lista_inicial=list_tasks[:]                                                  #Copiar estado inicial de list_task
        Tarea1 = ClassTask('Reunion', 'Reunion con la Universidad', '1/12/21 22:30') #Crear objeto ClassTask
        add_task(Tarea1)                                                             #Agregar objeto a list_task
        self.assertEquals(len(lista_inicial)+1, len(list_tasks))                     #Verificar que list_task creció en 1
        self.assertNotEquals(get_task('Reunion'), 'Error')                           #Verificar que se agregó el objeto a list_task

    def test_remove_task(self):
        """
        Prueba remove_task de taskController
        remove_task(str nombreTask) -> 
        remove_task recibe el nombre de un objeto del tipo ClassTask como string y elimina dicho objeto 
        de la lista list_task. 
        """   
        Tarea = ClassTask('Reunion1', 'Reunion con la Universidad', '1/12/21 22:00') #Crear objeto ClassTask
        add_task(Tarea)                                                              #Agregar objeto a list_task
        lista_inicial=list_tasks[:]                                                  #Copiar estado actual de list_task
        remove_task('Reunion1')                                                      #Quitar objeto de nombre indicado de list_task
        self.assertEquals(len(lista_inicial)-1, len(list_tasks))                     #Verificar que list_task disminuyó en 1
        self.assertEquals(get_task('Reunion1'), 'Error')                             #Verificar que se quitó el objeto de list_task

    def test_modify_task(self):
        """
        Prueba modify_task de taskController
        modify_task(str actualName, str newName, str newDescription, str newDate) -> 
        modify_task recibe como argumentos el nombre actual de un objeto del tipo ClassTask, el nuevo nombre, la nueva descripcion y 
        la nueva fecha de este y modifica el objeto indicado por el nombre actual usando los nuevos parametros
        """   
        Tarea = ClassTask('Reunion1', 'Reunion con la Universidad', '1/12/21 22:00') #Crear objeto ClassTask
        add_task(Tarea)                                                              #Agregar objeto a list_task
        lista_inicial=list_tasks[:]                                                  #Copiar estado actual de list_task
        modify_task('Reunion1', 'Reunion1', 'Destruir Universidad', '1/12/21 22:00') #Modificar descripcion de objeto indicado
        self.assertEquals(len(lista_inicial), len(list_tasks))                       #Verificar que tamaño de list_task no cambia
        self.assertNotEquals(get_task('Reunion1'), Tarea)                            #Verificar que no se eliminó el objeto a modificar
        modify_task('Reunion1', 'Reunion2', 'Destruir Universidad', '1/12/21 22:00') #Modificar nombre de objeto indicado
        self.assertEquals(get_task('Reunion1'), 'Error')                             #Verificar que no se encuentra un objeto con el nombre anterior
    
    def test_check_task(self):
        """
        Prueba check_task de taskController
        check_task(str dateTime) -> str || None
        check_task recibe una fecha y revisa si el ultimo objeto del tipo ClassTask dentro list_task tiene fecha igual a la dada. 
        Si encuentra un objeto con la misma fecha que la indicada, retorna un string formateado, de lo contrario no devuelve nada.
        """   
        Tarea = ClassTask('Reunion3', 'Reunion con la Universidad', '1/12/21 12:00') #Crear objeto ClassTask
        add_task(Tarea)                                                              #Agregar objeto a list_task
        task=check_task('1/12/21 12:00')                                             #Busca en list_task un objeto con fecha igual a la ingresada
        self.assertIsInstance(task, str)                                             #Verifica que la funcion retorne un string 
        self.assertEquals(get_task('Reunion3'), 'Error')                             #Verifica que se haya eliminado de list_task el objeto encontrado
        lista_inicial=list_tasks[:]                                                  #Copiar estado actual de list_task
        task1=check_task('1/12/21 11:00')                                            #Busca en list_task un objeto con fecha igual a la ingresada
        self.assertIsInstance(task1, None)                                           #Verifica que la funcion no retorne nada
        self.assertEquals(len(lista_inicial), len(list_tasks))                       #Verifica que tamaño de list_task no cambia
        
if __name__ == '__main__':
    unittest.main()
