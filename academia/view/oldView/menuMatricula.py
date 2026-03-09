from controllers.matricula_controller import MatriculaController
from mysql.connector import IntegrityError

def menu_principal_matricula(db):
    matricula_controller = MatriculaController(db)

    while True:
        print("Bienvenido al sistema de gestión de matriculas")
        print("1. Registrar matricula")
        print("2. Listar matriculas")
        print("3. Obtener matricula por ID")
        print("4. Actualizar matricula")
        print("5. Eliminar matricula")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_matricula(matricula_controller)
        elif opcion == "2":
            listar_matriculas(matricula_controller)
        elif opcion == "3":
            obtener_matricula_por_id(matricula_controller)
        elif opcion == "4":
            actualizar_matricula(matricula_controller)
        elif opcion == "5":
            eliminar_matricula(matricula_controller)
        elif opcion == "6":
            print("Gracias por usar el sistema de gestión de matriculas")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")


def registrar_matricula(matricula_controller):
    print("============Registrar Matricula=============")
    estudiante_id = input("Ingrese el ID del estudiante: ")
    curso_id = input("Ingrese el ID del curso: ")
    fecha_matricula = input("Ingrese la fecha de la matricula: ")
    try:
        matricula_controller.registrar_matricula(estudiante_id, curso_id, fecha_matricula)
        print("Matricula registrada correctamente")
    except IntegrityError as e:
        print(f"Error al registrar la matricula: {str(e)}")

def listar_matriculas(matricula_controller):
    print("============Listar Matriculas=============")
    matriculas = matricula_controller.listar_matriculas()
    for matricula in matriculas:
        print(f"ID: {matricula.id_matricula}")
        print(f"Estudiante ID: {matricula.estudiante_id}")
        print(f"Curso ID: {matricula.curso_id}")
        print(f"Fecha de Matricula: {matricula.fecha_matricula}")

def obtener_matricula_por_id(matricula_controller):
    print("============Obtener Matricula por ID=============")
    id_matricula = input("Ingrese el ID de la matricula: ")
    matricula = matricula_controller.obtener_matricula_por_id(id_matricula)
    if matricula:
        print(f"ID: {matricula.id_matricula}")
        print(f"Estudiante ID: {matricula.estudiante_id}")
        print(f"Curso ID: {matricula.curso_id}")
        print(f"Fecha de Matricula: {matricula.fecha_matricula}")
    else:
        print("No se encontró ninguna matricula con ese ID.")

def actualizar_matricula(matricula_controller):
    print("============Actualizar Matricula=============")
    id_matricula = input("Ingrese el ID de la matricula a actualizar: ")
    estudiante_id = input("Ingrese el nuevo ID del estudiante: ")
    curso_id = input("Ingrese el nuevo ID del curso: ")
    fecha_matricula = input("Ingrese la nueva fecha de la matricula: ")
    try:
        matricula_controller.actualizar_matricula(id_matricula, estudiante_id, curso_id, fecha_matricula)
        print("Matricula actualizada correctamente")
    except IntegrityError as e:
        print(f"Error al actualizar la matricula: {str(e)}")

def eliminar_matricula(matricula_controller):
    print("============Eliminar Matricula=============")
    id_matricula = input("Ingrese el ID de la matricula a eliminar: ")
    try:
        matricula_controller.eliminar_matricula(id_matricula)
        print("Matricula eliminada correctamente")
    except IntegrityError as e:
        print(f"Error al eliminar la matricula: {str(e)}")