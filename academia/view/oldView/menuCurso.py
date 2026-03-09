from controllers.curso_controller import CursoController
from mysql.connector import IntegrityError

def menu_principal_curso(db):
    curso_controller = CursoController(db)

    while True:
        print("Bienvenido al sistema de gestión de cursos")
        print("1. Registrar curso")
        print("2. Listar cursos")
        print("3. Obtener curso por ID")
        print("4. Actualizar curso")
        print("5. Eliminar curso")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_curso(curso_controller)
        elif opcion == "2":
            listar_cursos(curso_controller)
        elif opcion == "3":
            obtener_curso_por_id(curso_controller)
        elif opcion == "4":
            actualizar_curso(curso_controller)
        elif opcion == "5":
            eliminar_curso(curso_controller)
        elif opcion == "6":
            print("Gracias por usar el sistema de gestión de cursos")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")


def registrar_curso(curso_controller):
    print("============Registrar Curso=============")
    nombre = input("Ingrese el nombre del curso: ")
    descripcion = input("Ingrese la descripción del curso: ")
    duracion_horas = input("Ingrese la duración del curso en horas: ")
    docente_id = input("Ingrese el ID del docente que imparte el curso: ")

    try:
        curso_controller.registrar_curso(nombre, descripcion, duracion_horas, docente_id)
        print("Curso registrado correctamente")
    except IntegrityError as e:
        print(f"Error al registrar el curso: {str(e)}")

def listar_cursos(curso_controller):
    print("============Listar Cursos=============")
    cursos = curso_controller.listar_cursos()
    if cursos:
        for curso in cursos:
            print(f"ID: {curso.id_curso}")
            print(f"Nombre: {curso.nombre}")
            print(f"Descripción: {curso.descripcion}")
            print(f"Duración: {curso.duracion_horas} horas")
            print(f"Docente ID: {curso.docente_id}")
            print(f"Docente Nombre: {curso.docente_nombre}")
    else:
        print("No hay cursos registrados.")

def obtener_curso_por_id(curso_controller):
    id_curso = input("Ingrese el ID del curso a obtener: ")
    curso = curso_controller.obtener_curso_por_id(id_curso)
    if curso:
        print(f"ID: {curso.id_curso}")
        print(f"Nombre: {curso.nombre}")
        print(f"Descripción: {curso.descripcion}")
        print(f"Duración: {curso.duracion_horas} horas")
        print(f"Docente ID: {curso.docente_id}")
        print(f"Docente Nombre: {curso.docente_nombre}")
    else:
        print("No se encontró ningún curso con ese ID.")

def actualizar_curso(curso_controller):
    id_curso = input("Ingrese el ID del curso a actualizar: ")
    nombre = input("Ingrese el nuevo nombre del curso: ")
    descripcion = input("Ingrese la nueva descripción del curso: ")
    duracion_horas = input("Ingrese la nueva duración del curso en horas: ")
    docente_id = input("Ingrese el nuevo ID del docente que imparte el curso: ")

    try:
        curso_controller.actualizar_curso(id_curso, nombre, descripcion, duracion_horas, docente_id)
        print("Curso actualizado correctamente")
    except Exception as e:
        print(f"Error al actualizar el curso: {str(e)}")

def eliminar_curso(curso_controller):
    id_curso = input("Ingrese el ID del curso a eliminar: ")
    try:
        curso_controller.eliminar_curso(id_curso)
        print("Curso eliminado correctamente")
    except Exception as e:
        print(f"Error al eliminar el curso: {str(e)}")