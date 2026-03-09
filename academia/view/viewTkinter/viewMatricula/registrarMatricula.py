import customtkinter as ctk
from controllers.matricula_controller import MatriculaController
from controllers.estudiante_controller import EstudianteController
from controllers.curso_controller import CursoController
from datetime import datetime

class RegistrarMatricula:
    def __init__(self, db=None, tema_actual="System"):
        self.db = db
        self.tema_actual = tema_actual
        self.root = ctk.CTk()
        self.root.title("Registrar Matrícula")
        self.matricula_controller = MatriculaController(db)
        self.estudiante_controller = EstudianteController(db)
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
        self.titulo = ctk.CTkLabel(self.root, text="Registrar Nueva Matrícula", font=("Arial", 16))
        self.titulo.pack(pady=20)

        # Frame principal para los campos
        self.frame_campos = ctk.CTkFrame(self.root)
        self.frame_campos.pack(pady=20, padx=40, fill="both", expand=True)

        # Campo para seleccionar estudiante
        self.label_estudiante = ctk.CTkLabel(self.frame_campos, text="Estudiante:")
        self.label_estudiante.pack(pady=5)
        self.combo_estudiante = ctk.CTkComboBox(self.frame_campos, values=["Cargando..."])
        self.combo_estudiante.pack(pady=5, padx=20, fill="x")

        # Campo para seleccionar curso
        self.label_curso = ctk.CTkLabel(self.frame_campos, text="Curso:")
        self.label_curso.pack(pady=5)
        self.combo_curso = ctk.CTkComboBox(self.frame_campos, values=["Cargando..."])
        self.combo_curso.pack(pady=5, padx=20, fill="x")

        # Campo para fecha de matrícula
        self.label_fecha = ctk.CTkLabel(self.frame_campos, text="Fecha de Matrícula (YYYY-MM-DD):")
        self.label_fecha.pack(pady=5)
        self.entry_fecha = ctk.CTkEntry(self.frame_campos)
        self.entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_fecha.pack(pady=5, padx=20, fill="x")

        # Frame para botones
        self.frame_botones = ctk.CTkFrame(self.root)
        self.frame_botones.pack(pady=20)

        # Botón para registrar
        self.btn_registrar = ctk.CTkButton(self.frame_botones, text="Registrar Matrícula", command=self.registrar_matricula)
        self.btn_registrar.pack(side="left", padx=10)

        # Botón para regresar
        self.btn_regresar = ctk.CTkButton(self.frame_botones, text="Regresar", command=self.regresar_menu_principal)
        self.btn_regresar.pack(side="left", padx=10)

        # Cargar datos
        self.cargar_estudiantes()
        self.cargar_cursos()

    def cargar_estudiantes(self):
        try:
            estudiantes = self.estudiante_controller.listar_estudiantes()
            estudiantes_lista = [f"{estudiante.id_estudiante} - {estudiante.nombre} {estudiante.apellido}" for estudiante in estudiantes]
            self.combo_estudiante.configure(values=estudiantes_lista)
            if estudiantes_lista:
                self.combo_estudiante.set(estudiantes_lista[0])
        except Exception as e:
            print(f"Error al cargar estudiantes: {e}")

    def cargar_cursos(self):
        try:
            cursos = self.curso_controller.listar_cursos()
            cursos_lista = [f"{curso.id_curso} - {curso.nombre}" for curso in cursos]
            self.combo_curso.configure(values=cursos_lista)
            if cursos_lista:
                self.combo_curso.set(cursos_lista[0])
        except Exception as e:
            print(f"Error al cargar cursos: {e}")

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        ventana_mensaje = ctk.CTkToplevel(self.root)
        ventana_mensaje.title(titulo)
        ventana_mensaje.geometry("300x150")
        ventana_mensaje.resizable(False, False)

        ctk.set_appearance_mode(self.tema_actual)

        label_mensaje = ctk.CTkLabel(ventana_mensaje, text=mensaje, font=("Arial", 14))
        label_mensaje.pack(pady=20)

        btn_aceptar = ctk.CTkButton(ventana_mensaje, text="Aceptar", command=ventana_mensaje.destroy)
        btn_aceptar.pack(pady=10)

        ventana_mensaje.transient(self.root)
        ventana_mensaje.grab_set()
        self.root.wait_window(ventana_mensaje)

    def registrar_matricula(self):
        estudiante_seleccionado = self.combo_estudiante.get()
        curso_seleccionado = self.combo_curso.get()
        fecha = self.entry_fecha.get()

        if estudiante_seleccionado == "Cargando..." or curso_seleccionado == "Cargando..." or not fecha:
            self.mostrar_mensaje("Error", "Todos los campos son requeridos", "error")
            return

        try:
            # Validar formato de fecha
            datetime.strptime(fecha, "%Y-%m-%d")
            
            # Extraer IDs
            estudiante_id = int(estudiante_seleccionado.split(" - ")[0])
            curso_id = int(curso_seleccionado.split(" - ")[0])

            # Verificar si ya existe la matrícula
            sql_verificar = "SELECT COUNT(*) FROM Matriculas WHERE estudiante_id = %s AND curso_id = %s"
            resultado = self.db.execute_select(sql_verificar, (estudiante_id, curso_id))
            
            if resultado[0][0] > 0:
                self.mostrar_mensaje("Error", "El estudiante ya está matriculado en este curso", "error")
                return

            # Registrar matrícula
            self.matricula_controller.registrar_matricula(estudiante_id, curso_id, fecha)
            self.mostrar_mensaje("Éxito", "Matrícula registrada correctamente", "info")
            
            # Limpiar campos
            self.entry_fecha.delete(0, "end")
            self.entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
            
        except ValueError:
            self.mostrar_mensaje("Error", "Formato de fecha inválido. Use YYYY-MM-DD", "error")
        except Exception as e:
            self.mostrar_mensaje("Error", f"Error al registrar la matrícula: {str(e)}", "error")

    def regresar_menu_principal(self):
        from view.viewTkinter.viewMatricula.menuMatriculaFull import MenuMatriculaFull
        self.root.destroy()
        menu_matricula = MenuMatriculaFull(db=self.db, tema_actual=self.tema_actual)
        menu_matricula.root.mainloop()
