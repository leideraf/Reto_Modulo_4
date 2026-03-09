import customtkinter as ctk
from tkinter import ttk
from controllers.matricula_controller import MatriculaController
from controllers.estudiante_controller import EstudianteController
from controllers.curso_controller import CursoController
from datetime import datetime

class ActualizarMatricula:
    def __init__(self, db=None, tema_actual="System"):
        self.db = db
        self.tema_actual = tema_actual
        self.root = ctk.CTk()
        self.root.title("Actualizar Matrícula")
        self.matricula_controller = MatriculaController(db)
        self.estudiante_controller = EstudianteController(db)
        self.curso_controller = CursoController(db)

        # Configurar el tema de la ventana
        ctk.set_appearance_mode(tema_actual)

        # Obtener el ancho y alto de la pantalla
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        # Asignar tamaño de la ventana
        ancho_ventana = int(ancho_pantalla * 0.8)
        alto_ventana = int(alto_pantalla * 0.6)

        #calcular posicion para centrar
        posicion_x = int((ancho_pantalla - ancho_ventana) / 2)
        posicion_y = int((alto_pantalla - alto_ventana) / 2)

        #Establecer tamaño y posicon centrada
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

        # Configuración de restricciones de la ventana
        self.root.resizable(False, False)

        # Titulo de la ventana
        self.titulo = ctk.CTkLabel(self.root, text="Actualizar Matrícula", font=("Arial", 16))
        self.titulo.pack(pady=10)

        # Crear un frame para la tabla
        self.frame_tabla = ctk.CTkFrame(self.root)
        self.frame_tabla.pack(pady=10, padx=20, fill="both", expand=True)

        # Crear la tabla (usando Treeview de tkinter)
        self.tabla = ttk.Treeview(self.frame_tabla, columns=("ID", "Estudiante_ID", "Estudiante_Nombre", "Curso_ID", "Curso_Nombre", "Fecha"), show="headings")
        self.tabla.pack(expand=True, fill="both", padx=10, pady=10)

        # Configurar encabezados
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Estudiante_ID", text="ID Est.")
        self.tabla.heading("Estudiante_Nombre", text="Estudiante")
        self.tabla.heading("Curso_ID", text="ID Curso")
        self.tabla.heading("Curso_Nombre", text="Curso")
        self.tabla.heading("Fecha", text="Fecha")

        # Ajustar el ancho de las columnas
        self.tabla.column("ID", width=80)
        self.tabla.column("Estudiante_ID", width=80)
        self.tabla.column("Estudiante_Nombre", width=200)
        self.tabla.column("Curso_ID", width=80)
        self.tabla.column("Curso_Nombre", width=200)
        self.tabla.column("Fecha", width=120)

        # Crear un frame para los botones
        self.frame_botones = ctk.CTkFrame(self.root)
        self.frame_botones.pack(pady=10)

        # Botón para actualizar matrícula
        self.btn_actualizar = ctk.CTkButton(self.frame_botones, text="Actualizar Matrícula", command=self.actualizar_matricula)
        self.btn_actualizar.pack(side="left", padx=5)

        # Botón para regresar
        self.btn_regresar = ctk.CTkButton(self.frame_botones, text="Regresar", command=self.regresar_menu_principal)
        self.btn_regresar.pack(side="left", padx=5)

        # Cargar los datos de la tabla
        self.cargar_datos_tabla()

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

    def mostrar_confirmacion(self, titulo, mensaje):
        ventana_confirmacion = ctk.CTkToplevel(self.root)
        ventana_confirmacion.title(titulo)
        ventana_confirmacion.geometry("350x150")
        ventana_confirmacion.resizable(False, False)

        ctk.set_appearance_mode(self.tema_actual)

        respuesta = [False]

        label_mensaje = ctk.CTkLabel(ventana_confirmacion, text=mensaje, font=("Arial", 14))
        label_mensaje.pack(pady=20)

        frame_botones = ctk.CTkFrame(ventana_confirmacion)
        frame_botones.pack(pady=10)

        btn_si = ctk.CTkButton(frame_botones, text="Sí", command=lambda: [respuesta.__setitem__(0, True), ventana_confirmacion.destroy()])
        btn_si.pack(side="left", padx=5)

        btn_no = ctk.CTkButton(frame_botones, text="No", command=ventana_confirmacion.destroy)
        btn_no.pack(side="left", padx=5)

        ventana_confirmacion.transient(self.root)
        ventana_confirmacion.grab_set()
        self.root.wait_window(ventana_confirmacion)

        return respuesta[0]

    def actualizar_matricula(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            self.mostrar_mensaje("Advertencia", "Por favor seleccione una matrícula para actualizar", "warning")
            return

        item = self.tabla.item(seleccion[0])
        id_matricula = item['values'][0]
        estudiante_id_actual = item['values'][1]
        curso_id_actual = item['values'][3]
        fecha_actual = item['values'][5]

        # Crear ventana de actualización
        ventana_actualizacion = ctk.CTkToplevel(self.root)
        ventana_actualizacion.title("Actualizar Datos de la Matrícula")
        ventana_actualizacion.geometry("500x400")
        ventana_actualizacion.resizable(False, False)

        ctk.set_appearance_mode(self.tema_actual)

        frame_campos = ctk.CTkFrame(ventana_actualizacion)
        frame_campos.pack(pady=20, padx=20, fill="both", expand=True)

        # Campo para seleccionar estudiante
        label_estudiante = ctk.CTkLabel(frame_campos, text="Estudiante:")
        label_estudiante.pack(pady=5)
        self.combo_estudiante = ctk.CTkComboBox(frame_campos, values=["Cargando..."])
        self.combo_estudiante.pack(pady=5, fill="x")

        # Campo para seleccionar curso
        label_curso = ctk.CTkLabel(frame_campos, text="Curso:")
        label_curso.pack(pady=5)
        self.combo_curso = ctk.CTkComboBox(frame_campos, values=["Cargando..."])
        self.combo_curso.pack(pady=5, fill="x")

        # Campo para fecha
        label_fecha = ctk.CTkLabel(frame_campos, text="Fecha de Matrícula (YYYY-MM-DD):")
        label_fecha.pack(pady=5)
        self.entry_fecha = ctk.CTkEntry(frame_campos)
        self.entry_fecha.insert(0, str(fecha_actual))
        self.entry_fecha.pack(pady=5, fill="x")

        # Cargar datos
        self.cargar_estudiantes_actualizar(estudiante_id_actual)
        self.cargar_cursos_actualizar(curso_id_actual)

        frame_botones = ctk.CTkFrame(ventana_actualizacion)
        frame_botones.pack(pady=20)

        btn_guardar = ctk.CTkButton(frame_botones, text="Guardar",
                                  command=lambda: self.guardar_actualizacion(id_matricula, ventana_actualizacion))
        btn_guardar.pack(side="left", padx=5)

        btn_cancelar = ctk.CTkButton(frame_botones, text="Cancelar",
                                   command=ventana_actualizacion.destroy)
        btn_cancelar.pack(side="left", padx=5)

        ventana_actualizacion.transient(self.root)
        ventana_actualizacion.grab_set()
        self.root.wait_window(ventana_actualizacion)

    def cargar_estudiantes_actualizar(self, estudiante_id_actual):
        try:
            estudiantes = self.estudiante_controller.listar_estudiantes()
            estudiantes_lista = [f"{estudiante.id_estudiante} - {estudiante.nombre} {estudiante.apellido}" for estudiante in estudiantes]
            self.combo_estudiante.configure(values=estudiantes_lista)
            
            # Seleccionar el estudiante actual
            for estudiante_str in estudiantes_lista:
                if estudiante_str.startswith(str(estudiante_id_actual)):
                    self.combo_estudiante.set(estudiante_str)
                    break
        except Exception as e:
            print(f"Error al cargar estudiantes: {e}")

    def cargar_cursos_actualizar(self, curso_id_actual):
        try:
            cursos = self.curso_controller.listar_cursos()
            cursos_lista = [f"{curso.id_curso} - {curso.nombre}" for curso in cursos]
            self.combo_curso.configure(values=cursos_lista)
            
            # Seleccionar el curso actual
            for curso_str in cursos_lista:
                if curso_str.startswith(str(curso_id_actual)):
                    self.combo_curso.set(curso_str)
                    break
        except Exception as e:
            print(f"Error al cargar cursos: {e}")

    def guardar_actualizacion(self, id_matricula, ventana):
        nuevo_estudiante = self.combo_estudiante.get()
        nuevo_curso = self.combo_curso.get()
        nueva_fecha = self.entry_fecha.get()

        if nuevo_estudiante == "Cargando..." or nuevo_curso == "Cargando..." or not nueva_fecha:
            self.mostrar_mensaje("Error", "Todos los campos son requeridos", "error")
            return

        try:
            # Validar formato de fecha
            datetime.strptime(nueva_fecha, "%Y-%m-%d")
            
            # Extraer IDs
            nuevo_estudiante_id = int(nuevo_estudiante.split(" - ")[0])
            nuevo_curso_id = int(nuevo_curso.split(" - ")[0])

            # Verificar si ya existe otra matrícula con la misma combinación
            sql_verificar = "SELECT COUNT(*) FROM Matriculas WHERE estudiante_id = %s AND curso_id = %s AND id_matricula != %s"
            resultado = self.db.execute_select(sql_verificar, (nuevo_estudiante_id, nuevo_curso_id, id_matricula))
            
            if resultado[0][0] > 0:
                self.mostrar_mensaje("Error", "Ya existe una matrícula para este estudiante en este curso", "error")
                return

            confirmacion = self.mostrar_confirmacion(
                "Confirmar Actualización",
                "¿Está seguro que desea actualizar los datos de la matrícula?"
            )

            if confirmacion:
                self.matricula_controller.actualizar_matricula(
                    id_matricula, nuevo_estudiante_id, nuevo_curso_id, nueva_fecha
                )
                self.mostrar_mensaje("Éxito", "Matrícula actualizada correctamente", "info")
                self.cargar_datos_tabla()
                ventana.destroy()
                
        except ValueError:
            self.mostrar_mensaje("Error", "Formato de fecha inválido. Use YYYY-MM-DD", "error")
        except Exception as e:
            self.mostrar_mensaje("Error", f"Error al actualizar la matrícula: {str(e)}", "error")

    def regresar_menu_principal(self):
        from view.viewTkinter.viewMatricula.menuMatriculaFull import MenuMatriculaFull
        self.root.destroy()
        menu_matricula = MenuMatriculaFull(db=self.db, tema_actual=self.tema_actual)
        menu_matricula.root.mainloop()
