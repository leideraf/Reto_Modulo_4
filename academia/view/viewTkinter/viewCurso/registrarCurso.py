import customtkinter as ctk
from tkinter import ttk
from controllers.curso_controller import CursoController
from controllers.docente_controller import DocenteController
from mysql.connector import IntegrityError

class RegistrarCurso:
    def __init__(self, db=None, tema_actual="System"):
        self.db = db
        self.tema_actual = tema_actual
        self.root = ctk.CTk()
        self.root.title("Registrar Curso")
        self.curso_controller = CursoController(db)
        self.docente_controller = DocenteController(db)

        # Configurar el tema de la ventana
        ctk.set_appearance_mode(tema_actual)

        # Obtener el ancho y alto de la pantalla
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        # Asignar tamaño de la ventana
        ancho_ventana = int(ancho_pantalla * 0.4)
        alto_ventana = int(alto_pantalla * 0.7)
        # Calcular posición para centrar
        posicion_x = int((ancho_pantalla - ancho_ventana) / 2)
        posicion_y = int((alto_pantalla - alto_ventana) / 2)

        # Establecer tamaño y posición centrada
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

        # Configuración de restricciones de la ventana
        self.root.resizable(False, False)

        # Titulo de la ventana
        self.titulo = ctk.CTkLabel(self.root, text="Registrar Curso", font=("Arial", 16))
        self.titulo.pack(pady=10)

        # Crear un frame para los campos
        self.frame_campos = ctk.CTkFrame(self.root)
        self.frame_campos.pack(pady=10, padx=20, fill="both", expand=True)

        # Campo de nombre
        self.label_nombre = ctk.CTkLabel(self.frame_campos, text="Nombre del Curso:")
        self.label_nombre.pack(pady=5)
        self.campo_nombre = ctk.CTkEntry(self.frame_campos, placeholder_text="Nombre del curso")
        self.campo_nombre.pack(pady=5)

        # Campo de descripción
        self.label_descripcion = ctk.CTkLabel(self.frame_campos, text="Descripción:")
        self.label_descripcion.pack(pady=5)
        self.campo_descripcion = ctk.CTkTextbox(self.frame_campos, height=80)
        self.campo_descripcion.pack(pady=5, fill="x")

        # Campo de duración
        self.label_duracion = ctk.CTkLabel(self.frame_campos, text="Duración (horas):")
        self.label_duracion.pack(pady=5)
        self.campo_duracion = ctk.CTkEntry(self.frame_campos, placeholder_text="Duración en horas")
        self.campo_duracion.pack(pady=5)

        # Campo de docente (ComboBox)
        self.label_docente = ctk.CTkLabel(self.frame_campos, text="Docente:")
        self.label_docente.pack(pady=5)
        self.combo_docente = ctk.CTkComboBox(self.frame_campos, values=["Seleccione un docente"])
        self.combo_docente.pack(pady=5)

        # Cargar docentes en el ComboBox
        self.cargar_docentes()

        # Frame para botones
        self.frame_botones = ctk.CTkFrame(self.frame_campos)
        self.frame_botones.pack(pady=20, fill="x")

        # Botón para registrar curso
        self.btn_registrar = ctk.CTkButton(self.frame_botones, text="Registrar", command=self.registrar_curso)
        self.btn_registrar.pack(side="left", padx=10, expand=True)

        # Botón para regresar
        self.btn_regresar = ctk.CTkButton(self.frame_botones, text="Regresar", command=self.regresar_menu_principal)
        self.btn_regresar.pack(side="left", padx=10, expand=True)

    def cargar_docentes(self):
        try:
            docentes = self.docente_controller.listar_docentes()
            docentes_lista = [f"{docente.id_docente} - {docente.nombre} {docente.apellido}" for docente in docentes]
            self.combo_docente.configure(values=docentes_lista)
        except Exception as e:
            print(f"Error al cargar docentes: {e}")

    def registrar_curso(self):
        nombre = self.campo_nombre.get()
        descripcion = self.campo_descripcion.get("1.0", "end-1c")
        duracion = self.campo_duracion.get()
        docente_seleccionado = self.combo_docente.get()

        if not self.validar_campos():
            return

        # Extraer ID del docente
        docente_id = docente_seleccionado.split(" - ")[0]

        try:
            self.curso_controller.registrar_curso(nombre, descripcion, int(duracion), int(docente_id))
            self.notificarcion(mensaje="Curso registrado correctamente")
            self.regresar_menu_principal()
        except IntegrityError as e:
            self.notificarcion(mensaje="Error al registrar curso")
            print(f"Error de integridad: {e.msg}")
        except Exception as e:
            self.notificarcion(mensaje="Error al registrar curso")
            print(f"Error inesperado: {e}")

    def validar_campos(self):
        if not self.campo_nombre.get():
            self.notificarcion(mensaje="El nombre del curso es requerido")
            return False
        if not self.campo_descripcion.get("1.0", "end-1c").strip():
            self.notificarcion(mensaje="La descripción es requerida")
            return False
        if not self.campo_duracion.get():
            self.notificarcion(mensaje="La duración es requerida")
            return False
        try:
            int(self.campo_duracion.get())
        except ValueError:
            self.notificarcion(mensaje="La duración debe ser un número")
            return False
        if self.combo_docente.get() == "Seleccione un docente":
            self.notificarcion(mensaje="Debe seleccionar un docente")
            return False
        return True

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
        from view.viewTkinter.viewCurso.menuCursoFull import MenuCursoFull
        self.root.destroy()
        menu_curso = MenuCursoFull(db=self.db, tema_actual=self.tema_actual)
        menu_curso.root.mainloop()
