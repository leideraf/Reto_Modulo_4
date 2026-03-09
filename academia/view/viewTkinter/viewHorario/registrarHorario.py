import customtkinter as ctk
from controllers.horario_controller import HorarioController
from controllers.curso_controller import CursoController
from mysql.connector import IntegrityError

class RegistrarHorario:
    def __init__(self, db=None, tema_actual="System"):
        self.db = db
        self.tema_actual = tema_actual
        self.root = ctk.CTk()
        self.root.title("Registrar Horario")
        self.horario_controller = HorarioController(db)
        self.curso_controller = CursoController(db)

        # Configurar el tema de la ventana
        ctk.set_appearance_mode(tema_actual)

        # Obtener el ancho y alto de la pantalla
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        # Asignar tamaño de la ventana
        ancho_ventana = int(ancho_pantalla * 0.4)
        alto_ventana = int(alto_pantalla * 0.6)

        #calcular posicion para centrar
        posicion_x = int((ancho_pantalla - ancho_ventana) / 2)
        posicion_y = int((alto_pantalla - alto_ventana) / 2)

        #Establecer tamaño y posicon centrada
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

        # Configuración de restricciones de la ventana
        self.root.resizable(False, False)

        # Titulo de la ventana
        self.titulo = ctk.CTkLabel(self.root, text="Registrar Horario", font=("Arial", 16))
        self.titulo.pack(pady=10)

        # Crear un frame para los campos
        self.frame_campos = ctk.CTkFrame(self.root)
        self.frame_campos.pack(pady=10, padx=20, fill="both", expand=True)

        # Campo de día de la semana
        self.label_dia = ctk.CTkLabel(self.frame_campos, text="Día de la Semana:")
        self.label_dia.pack(pady=5)
        self.combo_dia = ctk.CTkComboBox(self.frame_campos, values=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
        self.combo_dia.pack(pady=5)

        # Campo de hora de inicio
        self.label_hora_inicio = ctk.CTkLabel(self.frame_campos, text="Hora de Inicio (HH:MM):")
        self.label_hora_inicio.pack(pady=5)
        self.campo_hora_inicio = ctk.CTkEntry(self.frame_campos, placeholder_text="08:00")
        self.campo_hora_inicio.pack(pady=5)

        # Campo de hora de fin
        self.label_hora_fin = ctk.CTkLabel(self.frame_campos, text="Hora de Fin (HH:MM):")
        self.label_hora_fin.pack(pady=5)
        self.campo_hora_fin = ctk.CTkEntry(self.frame_campos, placeholder_text="10:00")
        self.campo_hora_fin.pack(pady=5)

        # Campo de curso (ComboBox)
        self.label_curso = ctk.CTkLabel(self.frame_campos, text="Curso:")
        self.label_curso.pack(pady=5)
        self.combo_curso = ctk.CTkComboBox(self.frame_campos, values=["Seleccione un curso"])
        self.combo_curso.pack(pady=5)

        # Cargar cursos en el ComboBox
        self.cargar_cursos()

        # Frame para botones
        self.frame_botones = ctk.CTkFrame(self.frame_campos)
        self.frame_botones.pack(pady=20, fill="x")

        # Botón para registrar horario
        self.btn_registrar = ctk.CTkButton(self.frame_botones, text="Registrar", command=self.registrar_horario)
        self.btn_registrar.pack(side="left", padx=10, expand=True)

        # Botón para regresar
        self.btn_regresar = ctk.CTkButton(self.frame_botones, text="Regresar", command=self.regresar_menu_principal)
        self.btn_regresar.pack(side="left", padx=10, expand=True)

    def cargar_cursos(self):
        try:
            cursos = self.curso_controller.listar_cursos()
            cursos_lista = [f"{curso.id_curso} - {curso.nombre}" for curso in cursos]
            self.combo_curso.configure(values=cursos_lista)
        except Exception as e:
            print(f"Error al cargar cursos: {e}")

    def registrar_horario(self):
        dia_semana = self.combo_dia.get()
        hora_inicio = self.campo_hora_inicio.get()
        hora_fin = self.campo_hora_fin.get()
        curso_seleccionado = self.combo_curso.get()

        if not self.validar_campos():
            return

        # Extraer ID del curso
        curso_id = curso_seleccionado.split(" - ")[0]

        try:
            self.horario_controller.registrar_horario(dia_semana, hora_inicio, hora_fin, int(curso_id))
            self.notificarcion(mensaje="Horario registrado correctamente")
            self.regresar_menu_principal()
        except IntegrityError as e:
            self.notificarcion(mensaje="Error al registrar horario")
            print(f"Error de integridad: {e.msg}")
        except Exception as e:
            self.notificarcion(mensaje="Error al registrar horario")
            print(f"Error inesperado: {e}")

    def validar_campos(self):
        if not self.combo_dia.get():
            self.notificarcion(mensaje="Debe seleccionar un día de la semana")
            return False
        if not self.campo_hora_inicio.get():
            self.notificarcion(mensaje="La hora de inicio es requerida")
            return False
        if not self.campo_hora_fin.get():
            self.notificarcion(mensaje="La hora de fin es requerida")
            return False
        if not self.validar_formato_hora(self.campo_hora_inicio.get()):
            self.notificarcion(mensaje="Formato de hora de inicio inválido (use HH:MM)")
            return False
        if not self.validar_formato_hora(self.campo_hora_fin.get()):
            self.notificarcion(mensaje="Formato de hora de fin inválido (use HH:MM)")
            return False
        if self.combo_curso.get() == "Seleccione un curso":
            self.notificarcion(mensaje="Debe seleccionar un curso")
            return False
        return True

    def validar_formato_hora(self, hora):
        try:
            partes = hora.split(":")
            if len(partes) != 2:
                return False
            horas = int(partes[0])
            minutos = int(partes[1])
            return 0 <= horas <= 23 and 0 <= minutos <= 59
        except ValueError:
            return False

    def notificarcion(self, mensaje=""):
        ventana_notificacion = ctk.CTk()
        ventana_notificacion.title("Notificacion")
        ventana_notificacion.geometry("300x100")
        ventana_notificacion.resizable(False, False)

        label_notificacion = ctk.CTkLabel(ventana_notificacion, text=mensaje, font=("Arial", 16))
        label_notificacion.pack(pady=10)

        btn_aceptar = ctk.CTkButton(ventana_notificacion, text="Aceptar", command=ventana_notificacion.destroy)
        btn_aceptar.pack(pady=10)

        ventana_notificacion.mainloop()

    def regresar_menu_principal(self):
        from view.viewTkinter.viewHorario.menuHorarioFull import MenuHorarioFull
        self.root.destroy()
        menu_horario = MenuHorarioFull(db=self.db, tema_actual=self.tema_actual)
        menu_horario.root.mainloop()
