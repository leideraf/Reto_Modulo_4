import customtkinter as ctk
from tkinter import ttk
from controllers.curso_controller import CursoController
from controllers.docente_controller import DocenteController
from mysql.connector import IntegrityError

class ActualizarCurso:
    def __init__(self, db=None, tema_actual="System"):
        self.db = db
        self.tema_actual = tema_actual
        self.root = ctk.CTk()
        self.root.title("Actualizar Curso")
        self.curso_controller = CursoController(db)
        self.docente_controller = DocenteController(db)

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
        self.titulo = ctk.CTkLabel(self.root, text="Actualizar Curso", font=("Arial", 16))
        self.titulo.pack(pady=10)

        # Crear un frame para la tabla
        self.frame_tabla = ctk.CTkFrame(self.root)
        self.frame_tabla.pack(pady=10, padx=20, fill="both", expand=True)

        # Crear la tabla (usando Treeview de tkinter)
        self.tabla = ttk.Treeview(self.frame_tabla, columns=("ID", "Nombre", "Descripcion", "Duracion", "Docente_ID", "Docente_Nombre"), show="headings")
        self.tabla.pack(expand=True, fill="both", padx=10, pady=10)

        # Configurar encabezados
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Descripcion", text="Descripción")
        self.tabla.heading("Duracion", text="Duración")
        self.tabla.heading("Docente_ID", text="ID Docente")
        self.tabla.heading("Docente_Nombre", text="Docente")

        # Ajustar el ancho de las columnas
        self.tabla.column("ID", width=80)
        self.tabla.column("Nombre", width=150)
        self.tabla.column("Descripcion", width=250)
        self.tabla.column("Duracion", width=100)
        self.tabla.column("Docente_ID", width=100)
        self.tabla.column("Docente_Nombre", width=200)

        # Crear un frame para los botones
        self.frame_botones = ctk.CTkFrame(self.root)
        self.frame_botones.pack(pady=10)

        # Botón para actualizar curso
        self.btn_actualizar = ctk.CTkButton(self.frame_botones, text="Actualizar Curso", command=self.actualizar_curso)
        self.btn_actualizar.pack(side="left", padx=5)

        # Botón para regresar
        self.btn_regresar = ctk.CTkButton(self.frame_botones, text="Regresar", command=self.regresar_menu_principal)
        self.btn_regresar.pack(side="left", padx=5)

        # Cargar los datos de la tabla
        self.cargar_datos_tabla()

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

    def actualizar_curso(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            self.mostrar_mensaje("Advertencia", "Por favor seleccione un curso para actualizar", "warning")
            return

        item = self.tabla.item(seleccion[0])
        id_curso = item['values'][0]
        nombre_actual = item['values'][1]
        descripcion_actual = item['values'][2]
        duracion_actual = item['values'][3]
        docente_id_actual = item['values'][4]

        # Crear ventana de actualización
        ventana_actualizacion = ctk.CTkToplevel(self.root)
        ventana_actualizacion.title("Actualizar Datos del Curso")
        ventana_actualizacion.geometry("500x600")
        ventana_actualizacion.resizable(False, False)

        ctk.set_appearance_mode(self.tema_actual)

        frame_campos = ctk.CTkFrame(ventana_actualizacion)
        frame_campos.pack(pady=20, padx=20, fill="both", expand=True)

        # Campos de entrada
        label_nombre = ctk.CTkLabel(frame_campos, text="Nombre:")
        label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_campos)
        self.entry_nombre.insert(0, nombre_actual)
        self.entry_nombre.pack(pady=5)

        label_descripcion = ctk.CTkLabel(frame_campos, text="Descripción:")
        label_descripcion.pack(pady=5)
        self.entry_descripcion = ctk.CTkTextbox(frame_campos, height=100)
        self.entry_descripcion.insert("1.0", descripcion_actual)
        self.entry_descripcion.pack(pady=5, fill="x")

        label_duracion = ctk.CTkLabel(frame_campos, text="Duración (horas):")
        label_duracion.pack(pady=5)
        self.entry_duracion = ctk.CTkEntry(frame_campos)
        self.entry_duracion.insert(0, str(duracion_actual))
        self.entry_duracion.pack(pady=5)

        label_docente = ctk.CTkLabel(frame_campos, text="Docente:")
        label_docente.pack(pady=5)
        self.combo_docente = ctk.CTkComboBox(frame_campos, values=["Cargando..."])
        self.combo_docente.pack(pady=5)

        # Cargar docentes
        self.cargar_docentes_actualizar(docente_id_actual)

        frame_botones = ctk.CTkFrame(ventana_actualizacion)
        frame_botones.pack(pady=20)

        btn_guardar = ctk.CTkButton(frame_botones, text="Guardar",
                                  command=lambda: self.guardar_actualizacion(id_curso, ventana_actualizacion))
        btn_guardar.pack(side="left", padx=5)

        btn_cancelar = ctk.CTkButton(frame_botones, text="Cancelar",
                                   command=ventana_actualizacion.destroy)
        btn_cancelar.pack(side="left", padx=5)

        ventana_actualizacion.transient(self.root)
        ventana_actualizacion.grab_set()
        self.root.wait_window(ventana_actualizacion)

    def cargar_docentes_actualizar(self, docente_id_actual):
        try:
            docentes = self.docente_controller.listar_docentes()
            docentes_lista = [f"{docente.id_docente} - {docente.nombre} {docente.apellido}" for docente in docentes]
            self.combo_docente.configure(values=docentes_lista)
            
            # Seleccionar el docente actual
            for docente_str in docentes_lista:
                if docente_str.startswith(str(docente_id_actual)):
                    self.combo_docente.set(docente_str)
                    break
        except Exception as e:
            print(f"Error al cargar docentes: {e}")

    def guardar_actualizacion(self, id_curso, ventana):
        nuevo_nombre = self.entry_nombre.get()
        nueva_descripcion = self.entry_descripcion.get("1.0", "end-1c")
        nueva_duracion = self.entry_duracion.get()
        nuevo_docente = self.combo_docente.get()

        if not nuevo_nombre or not nueva_descripcion.strip() or not nueva_duracion or nuevo_docente == "Cargando...":
            self.mostrar_mensaje("Error", "Todos los campos son requeridos", "error")
            return

        try:
            int(nueva_duracion)
        except ValueError:
            self.mostrar_mensaje("Error", "La duración debe ser un número", "error")
            return

        # Extraer ID del docente
        nuevo_docente_id = nuevo_docente.split(" - ")[0]

        confirmacion = self.mostrar_confirmacion(
            "Confirmar Actualización",
            "¿Está seguro que desea actualizar los datos del curso?"
        )

        if confirmacion:
            try:
                self.curso_controller.actualizar_curso(
                    id_curso, nuevo_nombre, nueva_descripcion, int(nueva_duracion), int(nuevo_docente_id)
                )
                self.mostrar_mensaje("Éxito", "Curso actualizado correctamente", "info")
                self.cargar_datos_tabla()
                ventana.destroy()
            except Exception as e:
                self.mostrar_mensaje("Error", f"Error al actualizar el curso: {str(e)}", "error")

    def regresar_menu_principal(self):
        from view.viewTkinter.viewCurso.menuCursoFull import MenuCursoFull
        self.root.destroy()
        menu_curso = MenuCursoFull(db=self.db, tema_actual=self.tema_actual)
        menu_curso.root.mainloop()
