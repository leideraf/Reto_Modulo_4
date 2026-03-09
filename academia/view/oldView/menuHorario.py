from controllers.horario_controller import HorarioController
from mysql.connector import IntegrityError

def menu_principal_horario(db):
    horario_controller = HorarioController(db)

    while True:
        print("Bienvenido al sistema de gestión de horarios")
        print("1. Registrar horario")
        print("2. Listar horarios")
        print("3. Obtener horario por ID")
        print("4. Actualizar horario")
        print("5. Eliminar horario")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_horario(horario_controller)
        elif opcion == "2":
            listar_horarios(horario_controller)
        elif opcion == "3":
            obtener_horario_por_id(horario_controller)
        elif opcion == "4":
            actualizar_horario(horario_controller)
        elif opcion == "5":
            eliminar_horario(horario_controller)
        elif opcion == "6":
            print("Gracias por usar el sistema de gestión de horarios")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

def registrar_horario(horario_controller):
    print("============Registrar Horario=============")
    dia_semana = input("Ingrese el día de la semana: ")
    hora_inicio = input("Ingrese la hora de inicio: ")
    hora_fin = input("Ingrese la hora de fin: ")
    curso_id = input("Ingrese el ID del curso: ")

    try:
        horario_controller.registrar_horario(dia_semana, hora_inicio, hora_fin, curso_id)
        print("Horario registrado correctamente")
    except IntegrityError as e:
        print(f"Error al registrar el horario: {str(e)}")

def listar_horarios(horario_controller):
    print("============Listar Horarios=============")
    horarios = horario_controller.listar_horarios()
    if horarios:
        for horario in horarios:
            print(f"ID: {horario.id_horario}")
            print(f"Día de la semana: {horario.dia_semana}")
            print(f"Hora de inicio: {horario.hora_inicio}")
            print(f"Hora de fin: {horario.hora_fin}")
            print(f"ID del curso: {horario.curso_id}")
            print(f"Nombre del curso: {horario.curso_nombre}")
    else:
        print("No se encontraron horarios registrados.")

def obtener_horario_por_id(horario_controller):
    print("============Obtener Horario por ID=============")
    id_horario = input("Ingrese el ID del horario: ")
    try:
        horario = horario_controller.obtener_horario_por_id(id_horario)
        if horario:
            print(f"ID: {horario.id_horario}")
            print(f"Día de la semana: {horario.dia_semana}")
            print(f"Hora de inicio: {horario.hora_inicio}")
            print(f"Hora de fin: {horario.hora_fin}")
            print(f"ID del curso: {horario.curso_id}")
            print(f"Nombre del curso: {horario.curso_nombre}")
    except Exception as e:
        print(f"Error al obtener el horario: {str(e)}")

def actualizar_horario(horario_controller):
    print("============Actualizar Horario=============")
    id_horario = input("Ingrese el ID del horario: ")
    dia_semana = input("Ingrese el nuevo día de la semana: ")
    hora_inicio = input("Ingrese la nueva hora de inicio: ")
    hora_fin = input("Ingrese la nueva hora de fin: ")
    curso_id = input("Ingrese el nuevo ID del curso: ")

    try:
        horario_controller.actualizar_horario(id_horario, dia_semana, hora_inicio, hora_fin, curso_id)
        print("Horario actualizado correctamente")
    except Exception as e:
        print(f"Error al actualizar el horario: {str(e)}")

def eliminar_horario(horario_controller):
    print("============Eliminar Horario=============")
    id_horario = input("Ingrese el ID del horario: ")
    try:
        horario_controller.eliminar_horario(id_horario)
        print("Horario eliminado correctamente")
    except Exception as e:
        print(f"Error al eliminar el horario: {str(e)}")