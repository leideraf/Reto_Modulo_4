from controllers.estudiante_controller import EstudianteController
from mysql.connector import IntegrityError

def menu_principal(db):

    estudiante_controller = EstudianteController(db)

    while True:
        print("Bienvenido al sistema de gestión de estudiantes")
        print("1. Registrar estudiante")
        print("2. Listar estudiantes")
        print("3. Obtener estudiante por ID")
        print("4. Actualizar estudiante")
        print("5. Eliminar estudiante")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_estudiante(estudiante_controller)
        elif opcion == "2":
            listar_estudiantes(estudiante_controller)
        elif opcion == "3":
            obtener_estudiante_por_id(estudiante_controller)
        elif opcion == "4":
            actualizar_estudiante(estudiante_controller)
        elif opcion == "5":
            eliminar_estudiante(estudiante_controller)
        elif opcion == "6":
            print("Gracias por usar el sistema de gestión de estudiantes")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

def registrar_estudiante(estudiante_controller):
    print ("============Registrar Estudiante=============")
    nombres = input("Ingrese los nombres del estudiante: ")
    apellidos = input("Ingrese los apellidos del estudiante: ")
    correo = input("Ingrese el correo electrónica del estudiante: ")
    telefono = input("Ingrese el teléfono del estudiante: ")

    try:
        estudiante_controller.registrar_estudiante(nombres, apellidos, correo, telefono)
        print("Estudiante registrado correctamente")
    except IntegrityError as e:
        print(f"Error de integridad: {e.msg}")
    except Exception as e:
        print(f"Error al registrar el estudiante: {str(e)}")

def listar_estudiantes(estudiante_controller):
    print ("============Listar Estudiantes=============")
    try:
        estudiantes = estudiante_controller.listar_estudiantes()
        if estudiantes:
            print("ID\tNombres\tApellidos\tCorreo\tTeléfono")
            for e in estudiantes:
                print(f"{e.id_estudiante} | {e.nombre} {e.apellido} | {e.correo} | {e.telefono}")
        else:
            print("No se encontraron estudiantes registrados.")
    except Exception as e:
        print(f"Error al listar los estudiantes: {str(e)}")

def obtener_estudiante_por_id(estudiante_controller):
    print("============Obtener Estudiante por ID=============")
    id_estudiante = input("Ingrese el ID del estudiante: ")
    try:
        estudiante = estudiante_controller.obtener_estudiante_por_id(id_estudiante)

        if estudiante:
            print(f"ID: {estudiante.id_estudiante}")
            print(f"Nombres: {estudiante.nombre}")
            print(f"Apellidos: {estudiante.apellido}")
            print(f"Correo: {estudiante.correo}")
            print(f"Teléfono: {estudiante.telefono}")
    except Exception as e:
        print(f"Error al obtener el estudiante: {str(e)}")


def actualizar_estudiante(estudiante_controller):
    print("============Actualizar Estudiante=============")
    id_estudiante = input("Ingrese el ID del estudiante: ")
    nombre = input("Ingrese el nuevo nombre del estudiante: ")
    apellido = input("Ingrese el nuevo apellido del estudiante: ")
    correo = input("Ingrese el nuevo correo electrónico del estudiante: ")
    telefono = input("Ingrese el nuevo teléfono del estudiante: ")

    try:
        estudiante_controller.actualizar_estudiante(id_estudiante, nombre, apellido, correo, telefono)
        print("Estudiante actualizado correctamente")
    except Exception as e:
        print(f"Error al actualizar el estudiante: {str(e)}")

def eliminar_estudiante(estudiante_controller):
    print("============Eliminar Estudiante=============")
    id_estudiante = input("Ingrese el ID del estudiante: ")
    try:
        estudiante_controller.eliminar_estudiante(id_estudiante)
        print("Estudiante eliminado correctamente")
    except Exception as e:
        print(f"Error al eliminar el estudiante: {str(e)}")
