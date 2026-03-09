import customtkinter as ctk
from tkinter import ttk
from controllers.curso_controller import CursoController
from mysql.connector import IntegrityError

class MenuCursoFull:
    def __init__(self, db=None, tema_actual="System"):
        self.db = db
        self.tema_actual = tema_actual
        self.root = ctk.CTk()
        self.root.title("Menu Curso")
        self.root.attributes("-fullscreen", True)  # <- pantalla completa
        self.curso_controller = CursoController(db)

        # Configurar el tema de la ventana
        ctk.set_appearance_mode(tema_actual)

        # Configuracion de cierra de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.regresar_menu_principal)

        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        # Asignar tamaño de la ventana
        self.root.geometry(f"{ancho_pantalla}x{alto_pantalla}")
        self.root.state("zoomed")

        # Titulo de la ventana
        self.titulo = ctk.CTkLabel(self.root, text="Menu Curso", font=("Arial", 16))
        self.titulo.pack(pady=20)

        # Crear un frame principal para la tabla y los botones
        self.frame_principal = ctk.CTkFrame(self.root)
        self.frame_principal.pack(pady=20, padx=40, fill="both", expand=True)

        # Crear un frame para la tabla
        self.frame_tabla = ctk.CTkFrame(self.frame_principal)
        self.frame_tabla.pack(side="left", fill="both", expand=True, padx=(0, 20))

        # Crear la tabla (usando Treeview de tkinter)
        self.tabla = ttk.Treeview(self.frame_tabla, columns=("ID", "Nombre", "Descripcion", "Duracion", "Docente_ID", "Docente_Nombre"), show="headings")
        self.tabla.pack(expand=True, fill="both", padx=20)

        # Configurar encabezados
        self.tabla.heading("ID", text="ID Curso")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Descripcion", text="Descripción")
        self.tabla.heading("Duracion", text="Duración (hrs)")
        self.tabla.heading("Docente_ID", text="ID Docente")
        self.tabla.heading("Docente_Nombre", text="Docente")

        # Ajustar el ancho de las columnas
        self.tabla.column("ID", width=100)
        self.tabla.column("Nombre", width=200)
        self.tabla.column("Descripcion", width=300)
        self.tabla.column("Duracion", width=120)
        self.tabla.column("Docente_ID", width=100)
        self.tabla.column("Docente_Nombre", width=200)

        # Crear un frame para los botones verticales
        self.frame_botones = ctk.CTkFrame(self.frame_principal, width=250)
        self.frame_botones.pack(side="right", fill="y", padx=(0, 20))
        self.frame_botones.pack_propagate(False)

        # Botón para registrar curso
        self.btn_registrar = ctk.CTkButton(self.frame_botones, text="Registrar Curso", command=self.registrar_curso, width=200)
        self.btn_registrar.pack(pady=10, padx=10, fill="x")

        # Botón para actualizar curso
        self.btn_actualizar = ctk.CTkButton(self.frame_botones, text="Actualizar Curso", command=self.actualizar_curso, width=200)
        self.btn_actualizar.pack(pady=10, padx=10, fill="x")

        # Botón para eliminar curso
        self.btn_eliminar = ctk.CTkButton(self.frame_botones, text="Eliminar Curso", command=self.eliminar_curso, width=200)
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
            cursos = self.curso_controller.listar_cursos()
            # Limpiar la tabla antes de cargar nuevos datos
            for row in self.tabla.get_children():
                self.tabla.delete(row)

            for curso in cursos:
                # Insertar filas en la tabla
                self.tabla.insert("", "end", values=(
                    curso.id_curso,
                    curso.nombre,
                    curso.descripcion,
                    curso.duracion_horas,
                    curso.docente_id,
                    curso.docente_nombre
                ))

        except IntegrityError as e:
            print(f"Error al cargar los datos: {e}")

    def registrar_curso(self):
        from view.viewTkinter.viewCurso.registrarCurso import RegistrarCurso
        self.root.destroy()
        registrar_curso = RegistrarCurso(db=self.db, tema_actual=self.tema_actual)
        registrar_curso.root.mainloop()

    def actualizar_curso(self):
        from view.viewTkinter.viewCurso.actualizarCurso import ActualizarCurso
        self.root.destroy()
        actualizar_curso = ActualizarCurso(db=self.db, tema_actual=self.tema_actual)
        actualizar_curso.root.mainloop()

    def eliminar_curso(self):
        from view.viewTkinter.viewCurso.eliminarCurso import EliminarCurso
        self.root.destroy()
        eliminar_curso = EliminarCurso(db=self.db, tema_actual=self.tema_actual)
        eliminar_curso.root.mainloop()

    def cambiar_tema(self):
        if self.tema_actual == "Light":
            ctk.set_appearance_mode("Dark")
            self.tema_actual = "Dark"
        else:
            ctk.set_appearance_mode("Light")
            self.tema_actual = "Light"

    def regresar_menu_principal(self):
        from view.viewTkinter.menuPrincipal import MenuPrincipal
        self.root.destroy()
        menu_principal = MenuPrincipal(db=self.db, tema_actual=self.tema_actual)
        menu_principal.root.mainloop()
