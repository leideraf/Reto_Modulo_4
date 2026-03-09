from controllers.docente_controller  import DocenteController
from mysql.connector import IntegrityError

def menu_principal_docente(db):
    docente_controller = DocenteController(db)

    while True:
        print("Bienvenido al sistema de gestión de docentes")
        print("1. Registrar docente")
        print("2. Listar docentes")
        print("3. Obtener docente por ID")
        print("4. Actualizar docente")
        print("5. Eliminar docente")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_docente(docente_controller)
        elif opcion == "2":
            listar_docentes(docente_controller)
        elif opcion == "3":
            obtener_docente_por_id(docente_controller)
        elif opcion == "4":
            actualizar_docente(docente_controller)
        elif opcion == "5":
            eliminar_docente(docente_controller)
        elif opcion == "6":
            print("Gracias por usar el sistema de gestión de docentes")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

def registrar_docente(docente_controller):
    print("============Registrar Docente=============")
    nombre = input("Ingrese el nombre del docente: ")
    apellido = input("Ingrese el apellido del docente: ")
    correo = input("Ingrese el correo del docente: ")
    telefono = input("Ingrese el teléfono del docente: ")
    especialidad = input("Ingrese la especialidad del docente: ")

    try:
        docente_controller.registrar_docente(nombre, apellido, correo, telefono, especialidad)
        print("Docente registrado correctamente")
    except IntegrityError as e:
        print(f"Error al registrar el docente: {str(e)}")

def listar_docentes(docente_controller):
    print("============Listar Docentes=============")
    docentes = docente_controller.listar_docentes()
    if docentes:
        for docente in docentes:
            print(f"ID: {docente.id_docente}")
            print(f"Nombres: {docente.nombre}")
            print(f"Apellidos: {docente.apellido}")
            print(f"Correo: {docente.correo}")
            print(f"Teléfono: {docente.telefono}")
            print(f"Especialidad: {docente.especialidad}")
    else:
        print("No se encontraron docentes registrados.")

def obtener_docente_por_id(docente_controller):
    print("============Obtener Docente por ID=============")
    id_docente = input("Ingrese el ID del docente: ")
    try:
        docente = docente_controller.obtener_docente_por_id(id_docente)

        if docente:
            print(f"ID: {docente.id_docente}")
            print(f"Nombres: {docente.nombre}")
            print(f"Apellidos: {docente.apellido}")
            print(f"Correo: {docente.correo}")
            print(f"Teléfono: {docente.telefono}")
            print(f"Especialidad: {docente.especialidad}")
    except Exception as e:
        print(f"Error al obtener el docente: {str(e)}")

def actualizar_docente(docente_controller):
    print("============Actualizar Docente=============")
    id_docente = input("Ingrese el ID del docente: ")
    nombre = input("Ingrese el nuevo nombre del docente: ")
    apellido = input("Ingrese el nuevo apellido del docente: ")
    correo = input("Ingrese el nuevo correo del docente: ")
    telefono = input("Ingrese el nuevo teléfono del docente: ")
    especialidad = input("Ingrese la nueva especialidad del docente: ")

    try:
        docente_controller.actualizar_docente(id_docente, nombre, apellido, correo, telefono, especialidad)
        print("Docente actualizado correctamente")
    except Exception as e:
        print(f"Error al actualizar el docente: {str(e)}")

def eliminar_docente(docente_controller):
    print("============Eliminar Docente=============")
    id_docente = input("Ingrese el ID del docente: ")
    try:
        docente_controller.eliminar_docente(id_docente)
        print("Docente eliminado correctamente")
    except Exception as e:
        print(f"Error al eliminar el docente: {str(e)}")