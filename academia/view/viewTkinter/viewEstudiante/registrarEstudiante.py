import customtkinter as ctk
from controllers.estudiante_controller import EstudianteController
from mysql.connector import IntegrityError
import re

class RegistrarEstudiante:

    def __init__(self, db=None, tema_actual="System"):
        self.db = db
        self.tema_actual = tema_actual
        self.root = ctk.CTk()
        self.root.title("Registrar Estudiante")
        self.estudiante_controller = EstudianteController(db)

        #Configuracion del tema
        ctk.set_appearance_mode(tema_actual)

        #Obtener el ancho y alto de la pantalla
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        #Asignar tamaño de la ventana
        ancho_ventana = int(ancho_pantalla * 0.3)
        alto_ventana = int(alto_pantalla * 0.45)

        #calcular posicion para centrar
        posicion_x = int((ancho_pantalla - ancho_ventana) / 2)
        posicion_y = int((alto_pantalla - alto_ventana) / 2)

        #Establecer tamaño y posicon centrada
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

        #Configuraracion de restricciones de la ventana
        self.root.resizable(False, False)

        #Titulo de la ventana
        self.titulo = ctk.CTkLabel(self.root, text="Registrar Estudiante", font=("Arial", 16))
        self.titulo.pack(pady=10)

        #Campo de nombre
        self.campo_nombre = ctk.CTkEntry(self.root, placeholder_text="Nombre")
        self.campo_nombre.pack(pady=10)

        #Campo de apellido
        self.campo_apellido = ctk.CTkEntry(self.root, placeholder_text="Apellido")
        self.campo_apellido.pack(pady=10)

        #Campo de correo
        self.campo_correo = ctk.CTkEntry(self.root, placeholder_text="Correo")
        self.campo_correo.pack(pady=10)

        #Campo de telefono
        self.campo_telefono = ctk.CTkEntry(self.root, placeholder_text="Telefono")
        self.campo_telefono.pack(pady=10)

        #Boton para registrar estudiante
        self.btn_registrar = ctk.CTkButton(self.root, text="Registrar", command=self.registrar_estudiante)
        self.btn_registrar.pack(pady=10)

        #Boton para regresar al menu principal
        self.btn_regresar = ctk.CTkButton(self.root, text="Regresar", command=self.regresar_menu_principal)
        self.btn_regresar.pack(pady=10)

    def regresar_menu_principal(self):
        from view.viewTkinter.viewEstudiante.menuEstudiante import MenuEstudiante
        self.root.destroy()
        menu_principal = MenuEstudiante(db=self.db, tema_actual=self.tema_actual)
        menu_principal.root.mainloop()

    def registrar_estudiante(self):
        from view.viewTkinter.menuPrincipal import MenuPrincipal
        nombre = self.campo_nombre.get()
        apellido = self.campo_apellido.get()
        correo = self.campo_correo.get()
        telefono = self.campo_telefono.get()

        if not self.validar_campos():
            return

        try:
            self.estudiante_controller.registrar_estudiante(nombre, apellido, correo, telefono)
            self.notificarcion(mensaje= "Estudiante registrado correctamente")
            self.regresar_menu_principal()
        except IntegrityError as e:
            self.notificarcion(mensaje= "Error al registrar estudiante")
            print(f"Error de integridad: {e.msg}")
        except Exception as e:
            self.notificarcion(mensaje= "Error al registrar estudiante")
            print(f"Error inesperado: {e}")

    def notificarcion(self, mensaje= ""):
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
            self.notificarcion(mensaje= "El nombre es requerido")
            return False
        if not self.campo_apellido.get():
            self.notificarcion(mensaje= "El apellido es requerido")
            return False
        if not self.campo_correo.get() or not re.match(r"[^@]+@[^@]+\.[^@]+", self.campo_correo.get()):
            self.notificarcion(mensaje= "El correo es requerido")
            return False
        if not self.campo_telefono.get():
            self.notificarcion(mensaje= "El telefono es requerido")
            return False
        return True