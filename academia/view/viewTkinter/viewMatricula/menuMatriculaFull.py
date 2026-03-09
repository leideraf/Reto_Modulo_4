import customtkinter as ctk
from tkinter import ttk
from controllers.matricula_controller import MatriculaController
from mysql.connector import IntegrityError

class MenuMatriculaFull:
    def __init__(self, db=None, tema_actual="System"):
        self.db = db
        self.tema_actual = tema_actual
        self.root = ctk.CTk()
        self.root.title("Menu Matrícula")
        self.root.attributes("-fullscreen", True)  # <- pantalla completa
        self.matricula_controller = MatriculaController(db)

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
        self.titulo = ctk.CTkLabel(self.root, text="Menu Matrícula", font=("Arial", 16))
        self.titulo.pack(pady=20)

        # Crear un frame principal para la tabla y los botones
        self.frame_principal = ctk.CTkFrame(self.root)
        self.frame_principal.pack(pady=20, padx=40, fill="both", expand=True)

        # Crear un frame para la tabla
        self.frame_tabla = ctk.CTkFrame(self.frame_principal)
        self.frame_tabla.pack(side="left", fill="both", expand=True, padx=(0, 20))

        # Crear la tabla (usando Treeview de tkinter)
        self.tabla = ttk.Treeview(self.frame_tabla, columns=("ID", "Estudiante_ID", "Estudiante_Nombre", "Curso_ID", "Curso_Nombre", "Fecha"), show="headings")
        self.tabla.pack(expand=True, fill="both", padx=20)

        # Configurar encabezados
        self.tabla.heading("ID", text="ID Matrícula")
        self.tabla.heading("Estudiante_ID", text="ID Estudiante")
        self.tabla.heading("Estudiante_Nombre", text="Estudiante")
        self.tabla.heading("Curso_ID", text="ID Curso")
        self.tabla.heading("Curso_Nombre", text="Curso")
        self.tabla.heading("Fecha", text="Fecha Matrícula")

        # Ajustar el ancho de las columnas
        self.tabla.column("ID", width=100)
        self.tabla.column("Estudiante_ID", width=100)
        self.tabla.column("Estudiante_Nombre", width=200)
        self.tabla.column("Curso_ID", width=100)
        self.tabla.column("Curso_Nombre", width=200)
        self.tabla.column("Fecha", width=150)

        # Crear un frame para los botones verticales
        self.frame_botones = ctk.CTkFrame(self.frame_principal, width=250)
        self.frame_botones.pack(side="right", fill="y", padx=(0, 20))
        self.frame_botones.pack_propagate(False)

        # Botón para registrar matrícula
        self.btn_registrar = ctk.CTkButton(self.frame_botones, text="Registrar Matrícula", command=self.registrar_matricula, width=200)
        self.btn_registrar.pack(pady=10, padx=10, fill="x")

        # Botón para actualizar matrícula
        self.btn_actualizar = ctk.CTkButton(self.frame_botones, text="Actualizar Matrícula", command=self.actualizar_matricula, width=200)
        self.btn_actualizar.pack(pady=10, padx=10, fill="x")

        # Botón para eliminar matrícula
        self.btn_eliminar = ctk.CTkButton(self.frame_botones, text="Eliminar Matrícula", command=self.eliminar_matricula, width=200)
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
            # Obtener matrículas con información de estudiantes y cursos
            sql = """
                SELECT m.id_matricula, m.estudiante_id, 
                       CONCAT(e.nombre, ' ', e.apellido) as estudiante_nombre,
                       m.curso_id, c.nombre as curso_nombre, m.fecha_matricula
                FROM Matriculas m
                JOIN Estudiantes e ON m.estudiante_id = e.id_estudiante
                JOIN Cursos c ON m.curso_id = c.id_curso
                ORDER BY m.id_matricula
            """
            resultados = self.db.execute_select(sql)
            
            # Limpiar la tabla antes de cargar nuevos datos
            for row in self.tabla.get_children():
                self.tabla.delete(row)

            for resultado in resultados:
                # Insertar filas en la tabla
                self.tabla.insert("", "end", values=(
                    resultado[0],  # id_matricula
                    resultado[1],  # estudiante_id
                    resultado[2],  # estudiante_nombre
                    resultado[3],  # curso_id
                    resultado[4],  # curso_nombre
                    resultado[5]   # fecha_matricula
                ))

        except Exception as e:
            print(f"Error al cargar los datos: {e}")

    def registrar_matricula(self):
        from view.viewTkinter.viewMatricula.registrarMatricula import RegistrarMatricula
        self.root.destroy()
        registrar_matricula = RegistrarMatricula(db=self.db, tema_actual=self.tema_actual)
        registrar_matricula.root.mainloop()

    def actualizar_matricula(self):
        from view.viewTkinter.viewMatricula.actualizarMatricula import ActualizarMatricula
        self.root.destroy()
        actualizar_matricula = ActualizarMatricula(db=self.db, tema_actual=self.tema_actual)
        actualizar_matricula.root.mainloop()

    def eliminar_matricula(self):
        from view.viewTkinter.viewMatricula.eliminarMatricula import EliminarMatricula
        self.root.destroy()
        eliminar_matricula = EliminarMatricula(db=self.db, tema_actual=self.tema_actual)
        eliminar_matricula.root.mainloop()

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
