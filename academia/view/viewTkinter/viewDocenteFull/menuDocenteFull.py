import customtkinter as ctk
import platform
from tkinter import ttk
from controllers.docente_controller import DocenteController
from mysql.connector import IntegrityError


class MenuDocenteFull():
    def __init__(self, db=None, tema_actual="System"):
        self.db = db
        self.tema_actual = tema_actual
        self.docente_controller = DocenteController(db)
        self.root = ctk.CTk()
        self.root.title("Menu Docente")
        self.root.attributes("-fullscreen", True)  # <- pantalla completa

        #Configurar el tema de la ventana
        ctk.set_appearance_mode(tema_actual)

        #Configuracion de cierra de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.regresar_menu_principal)

        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        #Asignar tamaño de la ventana
        self.root.geometry(f"{ancho_pantalla}x{alto_pantalla}")

        self.root.state("zoomed")

        #Titulo de la ventana
        self.titulo = ctk.CTkLabel(self.root, text="Menu Docente", font=("Arial", 16))
        self.titulo.pack(pady=20)

        # Crear un frame principal para la tabla y los botones
        self.frame_principal = ctk.CTkFrame(self.root)
        self.frame_principal.pack(pady=20, padx=40, fill="both", expand=True)

        # Crear un frame para la tabla
        self.frame_tabla = ctk.CTkFrame(self.frame_principal)
        self.frame_tabla.pack(side="left", fill="both", expand=True, padx=(0, 20))

        # Crear la tabla (usando Treeview de tkinter)
        self.tabla = ttk.Treeview(self.frame_tabla, columns=("ID", "Nombre", "Apellido", "Correo", "Telefono", "Especialidad"), show="headings")
        self.tabla.pack(expand=True, fill="both", padx=20)

        # Configurar encabezados
        self.tabla.heading("ID", text="ID Docente")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Apellido", text="Apellido")
        self.tabla.heading("Correo", text="Correo")
        self.tabla.heading("Telefono", text="Teléfono")
        self.tabla.heading("Especialidad", text="Especialidad")

        # Ajustar el ancho de las columnas
        self.tabla.column("ID", width=150)
        self.tabla.column("Nombre", width=250)
        self.tabla.column("Apellido", width=250)
        self.tabla.column("Correo", width=300)
        self.tabla.column("Telefono", width=200)
        self.tabla.column("Especialidad", width=250)

        # Crear un frame para los botones verticales
        self.frame_botones = ctk.CTkFrame(self.frame_principal, width=250)
        self.frame_botones.pack(side="right", fill="y", padx=(0, 20))
        self.frame_botones.pack_propagate(False)  # Evita que el frame se ajuste al contenido

        # Botón para registrar docente
        self.btn_registrar = ctk.CTkButton(self.frame_botones, text="Registrar Docente", command=self.registrar_docente, width=200)
        self.btn_registrar.pack(pady=10, padx=10, fill="x")

        # Botón para actualizar docente
        self.btn_actualizar = ctk.CTkButton(self.frame_botones, text="Actualizar Docente", command=self.actualizar_docente, width=200)
        self.btn_actualizar.pack(pady=10, padx=10, fill="x")

        # Botón para eliminar docente
        self.btn_eliminar = ctk.CTkButton(self.frame_botones, text="Eliminar Docente", command=self.eliminar_docente, width=200)
        self.btn_eliminar.pack(pady=10, padx=10, fill="x")

        # Botón para cambiar tema
        self.btn_tema = ctk.CTkButton(self.frame_botones, text="Cambiar Tema", command=self.cambiar_tema, width=200)
        self.btn_tema.pack(pady=10, padx=10, fill="x")

        # Cargar los datos de la tabla
        self.cargar_datos_tabla()

        # Agregar espacio vertical
        self.espacio_vertical = ctk.CTkLabel(self.root, text="")
        self.espacio_vertical.pack(pady=20)

        # Crear un frame para el botón de regresar
        self.frame_boton = ctk.CTkFrame(self.root)
        self.frame_boton.pack(pady=10, padx=40, fill="x")

        # Botón para regresar al menú principal
        self.btn_regresar = ctk.CTkButton(self.frame_boton, text="Regresar", command=self.regresar_menu_principal)
        self.btn_regresar.pack(side="left", padx=10)

    def cargar_datos_tabla(self):
        try:
            docentes = self.docente_controller.listar_docentes()
            # Limpiar la tabla antes de cargar nuevos datos
            for row in self.tabla.get_children():
                self.tabla.delete(row)

            for docente in docentes:
                # Insertar filas en la tabla
                self.tabla.insert("", "end", values=(
                    docente.id_docente,
                    docente.nombre,
                    docente.apellido,
                    docente.correo,
                    docente.telefono,
                    docente.especialidad
                ))

        except IntegrityError as e:
            print(f"Error al cargar los datos: {e}")
            # Aquí podrías mostrar un mensaje de error en la interfaz si lo deseas


    def regresar_menu_principal(self):
        from view.viewTkinter.menuPrincipal import MenuPrincipal
        self.root.destroy()
        menu_principal = MenuPrincipal(db=self.db, tema_actual=self.tema_actual)
        menu_principal.root.mainloop()

    def registrar_docente(self):
        from view.viewTkinter.viewDocenteFull.registrarDocente import RegistrarDocente
        self.root.destroy()
        registrar_docente = RegistrarDocente(db=self.db, tema_actual=self.tema_actual)
        registrar_docente.root.mainloop()

    def actualizar_docente(self):
        from view.viewTkinter.viewDocenteFull.actualizarDocente import ActualizarDocente
        self.root.destroy()
        actualizar_docente = ActualizarDocente(db=self.db, tema_actual=self.tema_actual)
        actualizar_docente.root.mainloop()

    def eliminar_docente(self):
        from view.viewTkinter.viewDocenteFull.eliminarDocente import EliminarDocente
        self.root.destroy()
        eliminar_docente = EliminarDocente(db=self.db, tema_actual=self.tema_actual)
        eliminar_docente.root.mainloop()

    def cambiar_tema(self):
        if self.tema_actual == "Light":
            ctk.set_appearance_mode("Dark")
            self.tema_actual = "Dark"
        else:
            ctk.set_appearance_mode("Light")
            self.tema_actual = "Light"
