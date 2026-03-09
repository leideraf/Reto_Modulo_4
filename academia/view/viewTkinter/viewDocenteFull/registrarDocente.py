import customtkinter as ctk
from controllers.docente_controller import DocenteController
from mysql.connector import IntegrityError
import re

class RegistrarDocente:
    def __init__(self, db=None, tema_actual="System"):
        self.db = db
        self.tema_actual = tema_actual
        self.root = ctk.CTk()
        self.root.title("Registrar Docente")
        self.docente_controller = DocenteController(db)

        # Configurar el tema de la ventana
        ctk.set_appearance_mode(tema_actual)

        # Obtener el ancho y alto de la pantalla
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        # Asignar tamaño de la ventana
        ancho_ventana = int(ancho_pantalla * 0.3)
        alto_ventana = int(alto_pantalla * 0.70)
        # Calcular posición para centrar
        posicion_x = int((ancho_pantalla - ancho_ventana) / 2)
        posicion_y = int((alto_pantalla - alto_ventana) / 2)

        # Establecer tamaño y posición centrada
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

        # Configuración de restricciones de la ventana
        self.root.resizable(False, False)

        # Titulo de la ventana
        self.titulo = ctk.CTkLabel(self.root, text="Registrar Docente", font=("Arial", 16))
        self.titulo.pack(pady=10)

        # Crear un frame para los campos
        self.frame_campos = ctk.CTkFrame(self.root)
        self.frame_campos.pack(pady=10, padx=20, fill="both", expand=True)

        # Campo de nombre
        self.label_nombre = ctk.CTkLabel(self.frame_campos, text="Nombre:")
        self.label_nombre.pack(pady=5)
        self.campo_nombre = ctk.CTkEntry(self.frame_campos, placeholder_text="Nombre")
        self.campo_nombre.pack(pady=5)

        # Campo de apellido
        self.label_apellido = ctk.CTkLabel(self.frame_campos, text="Apellido:")
        self.label_apellido.pack(pady=5)
        self.campo_apellido = ctk.CTkEntry(self.frame_campos, placeholder_text="Apellido")
        self.campo_apellido.pack(pady=5)

        # Campo de correo
        self.label_correo = ctk.CTkLabel(self.frame_campos, text="Correo:")
        self.label_correo.pack(pady=5)
        self.campo_correo = ctk.CTkEntry(self.frame_campos, placeholder_text="Correo")
        self.campo_correo.pack(pady=5)

        # Campo de teléfono
        self.label_telefono = ctk.CTkLabel(self.frame_campos, text="Teléfono:")
        self.label_telefono.pack(pady=5)
        self.campo_telefono = ctk.CTkEntry(self.frame_campos, placeholder_text="Telefono")
        self.campo_telefono.pack(pady=5)

        # Campo de especialidad
        self.label_especialidad = ctk.CTkLabel(self.frame_campos, text="Especialidad:")
        self.label_especialidad.pack(pady=5)
        self.campo_especialidad = ctk.CTkEntry(self.frame_campos, placeholder_text="Especialidad")
        self.campo_especialidad.pack(pady=5)

        # Botón para registrar docente
        self.btn_registrar = ctk.CTkButton(self.frame_campos, text="Registrar", command=self.registrar_docente)
        self.btn_registrar.pack(side="left", padx=10, pady=20, expand=True)

        # Botón para regresar al menú principal
        self.btn_regresar = ctk.CTkButton(self.frame_campos, text="Regresar", command=self.regresar_menu_principal)
        self.btn_regresar.pack(side="left", padx=10, pady=20, expand=True)

    def regresar_menu_principal(self):
        from view.viewTkinter.viewDocenteFull.menuDocenteFull import MenuDocenteFull
        self.root.destroy()
        menu_docente = MenuDocenteFull(db=self.db, tema_actual=self.tema_actual)
        menu_docente.root.mainloop()

    def registrar_docente(self):
        nombre = self.campo_nombre.get()
        apellido = self.campo_apellido.get()
        correo = self.campo_correo.get()
        telefono = self.campo_telefono.get()
        especialidad = self.campo_especialidad.get()

        if not self.validar_campos():
            return

        try:
            self.docente_controller.registrar_docente(nombre, apellido, correo, telefono, especialidad)
            self.notificarcion(mensaje="Docente registrado correctamente")
            self.regresar_menu_principal()
        except IntegrityError as e:
            self.notificarcion(mensaje="Error al registrar docente: El correo ya está registrado")
            print(f"Error de integridad: {e.msg}")
        except Exception as e:
            self.notificarcion(mensaje="Error al registrar docente")
            print(f"Error inesperado: {e}")

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

    def validar_campos(self):
        if not self.campo_nombre.get():
            self.notificarcion(mensaje="El nombre es requerido")
            return False
        if not self.campo_apellido.get():
            self.notificarcion(mensaje="El apellido es requerido")
            return False
        if not self.campo_correo.get() or not re.match(r"[^@]+@[^@]+\.[^@]+", self.campo_correo.get()):
            self.notificarcion(mensaje="El correo es requerido y debe tener un formato válido")
            return False
        if not self.campo_telefono.get():
            self.notificarcion(mensaje="El telefono es requerido")
            return False
        if not self.campo_especialidad.get():
            self.notificarcion(mensaje="La especialidad es requerida")
            return False
        return True
