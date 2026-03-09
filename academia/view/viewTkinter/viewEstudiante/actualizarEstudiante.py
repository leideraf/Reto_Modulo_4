import customtkinter as ctk
from tkinter import ttk, messagebox  # Importamos ttk para usar Treeview y messagebox para confirmación
from controllers.estudiante_controller import EstudianteController
from mysql.connector import IntegrityError
import re

class ActualizarEstudiante:
    def __init__(self, db=None, tema_actual="System"):
        self.db = db
        self.tema_actual = tema_actual
        self.root = ctk.CTk()
        self.root.title("Actualizar Estudiante")
        self.estudiante_controller = EstudianteController(db)

        # Configurar el tema de la ventana
        ctk.set_appearance_mode(tema_actual)

        # Obtener el ancho y alto de la pantalla
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        # Asignar tamaño de la ventana
        ancho_ventana = int(ancho_pantalla * 0.4)
        alto_ventana = int(alto_pantalla * 0.4)

        #calcular posicion para centrar
        posicion_x = int((ancho_pantalla - ancho_ventana) / 2)
        posicion_y = int((alto_pantalla - alto_ventana) / 2)

        #Establecer tamaño y posicon centrada
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

        # Configuración de restricciones de la ventana
        self.root.resizable(False, False)

        # Titulo de la ventana
        self.titulo = ctk.CTkLabel(self.root, text="Actualizar Estudiante", font=("Arial", 16))
        self.titulo.pack(pady=10)

        # Crear un frame para la tabla
        self.frame_tabla = ctk.CTkFrame(self.root)
        self.frame_tabla.pack(pady=10)

        # Crear la tabla (usando Treeview de tkinter)
        self.tabla = ttk.Treeview(self.frame_tabla, columns=("ID", "Nombre", "Apellido", "Correo", "Telefono"), show="headings")
        self.tabla.pack(expand=True, fill="both")

        # Configurar encabezados
        self.tabla.heading("ID", text="ID Estudiante")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Apellido", text="Apellido")
        self.tabla.heading("Correo", text="Correo")
        self.tabla.heading("Telefono", text="Teléfono")

        # Ajustar el ancho de las columnas
        self.tabla.column("ID", width=100)
        self.tabla.column("Nombre", width=150)
        self.tabla.column("Apellido", width=150)
        self.tabla.column("Correo", width=200)
        self.tabla.column("Telefono", width=120)

        # Crear un frame para los botones
        self.frame_botones = ctk.CTkFrame(self.root)
        self.frame_botones.pack(pady=10)

        # Botón para actualizar estudiante
        self.btn_actualizar = ctk.CTkButton(self.frame_botones, text="Actualizar Estudiante", command=self.actualizar_estudiante)
        self.btn_actualizar.pack(side="left", padx=5)

        # Botón para regresar al menú principal
        self.btn_regresar = ctk.CTkButton(self.frame_botones, text="Regresar", command=self.regresar_menu_principal)
        self.btn_regresar.pack(side="left", padx=5)

        # Cargar los datos de la tabla
        self.cargar_datos_tabla()

    def cargar_datos_tabla(self):
        try:
            estudiantes = self.estudiante_controller.listar_estudiantes()
            # Limpiar la tabla antes de cargar nuevos datos
            for row in self.tabla.get_children():
                self.tabla.delete(row)

            for estudiante in estudiantes:
                # Insertar filas en la tabla
                self.tabla.insert("", "end", values=(estudiante.id_estudiante, estudiante.nombre, estudiante.apellido, estudiante.correo, estudiante.telefono))

        except IntegrityError as e:
            print(f"Error al cargar los datos: {e}")
            # Aquí podrías mostrar un mensaje de error en la interfaz si lo deseas

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        # Crear una ventana de mensaje personalizada
        ventana_mensaje = ctk.CTkToplevel(self.root)
        ventana_mensaje.title(titulo)
        ventana_mensaje.geometry("300x150")
        ventana_mensaje.resizable(False, False)

        # Configurar el tema de la ventana
        ctk.set_appearance_mode(self.tema_actual)

        # Crear el mensaje
        label_mensaje = ctk.CTkLabel(ventana_mensaje, text=mensaje, font=("Arial", 14))
        label_mensaje.pack(pady=20)

        # Crear botón de aceptar
        btn_aceptar = ctk.CTkButton(ventana_mensaje, text="Aceptar", command=ventana_mensaje.destroy)
        btn_aceptar.pack(pady=10)

        # Hacer que la ventana sea modal
        ventana_mensaje.transient(self.root)
        ventana_mensaje.grab_set()
        self.root.wait_window(ventana_mensaje)

    def mostrar_confirmacion(self, titulo, mensaje):
        # Crear una ventana de confirmación personalizada
        ventana_confirmacion = ctk.CTkToplevel(self.root)
        ventana_confirmacion.title(titulo)
        ventana_confirmacion.geometry("350x150")
        ventana_confirmacion.resizable(False, False)

        # Configurar el tema de la ventana
        ctk.set_appearance_mode(self.tema_actual)

        # Variable para almacenar la respuesta
        respuesta = [False]

        # Crear el mensaje
        label_mensaje = ctk.CTkLabel(ventana_confirmacion, text=mensaje, font=("Arial", 14))
        label_mensaje.pack(pady=20)

        # Crear frame para los botones
        frame_botones = ctk.CTkFrame(ventana_confirmacion)
        frame_botones.pack(pady=10)

        # Crear botones de sí y no
        btn_si = ctk.CTkButton(frame_botones, text="Sí", command=lambda: [respuesta.__setitem__(0, True), ventana_confirmacion.destroy()])
        btn_si.pack(side="left", padx=5)

        btn_no = ctk.CTkButton(frame_botones, text="No", command=ventana_confirmacion.destroy)
        btn_no.pack(side="left", padx=5)

        # Hacer que la ventana sea modal
        ventana_confirmacion.transient(self.root)
        ventana_confirmacion.grab_set()
        self.root.wait_window(ventana_confirmacion)

        return respuesta[0]

    def actualizar_estudiante(self):
        # Obtener el item seleccionado
        seleccion = self.tabla.selection()
        if not seleccion:
            self.mostrar_mensaje("Advertencia", "Por favor seleccione un estudiante para actualizar", "warning")
            return

        # Obtener los datos del estudiante seleccionado
        item = self.tabla.item(seleccion[0])
        id_estudiante = item['values'][0]
        nombre_actual = item['values'][1]
        apellido_actual = item['values'][2]
        correo_actual = item['values'][3]
        telefono_actual = item['values'][4]

        # Crear ventana de actualización
        ventana_actualizacion = ctk.CTkToplevel(self.root)
        ventana_actualizacion.title("Actualizar Datos del Estudiante")
        ventana_actualizacion.geometry("400x450")
        ventana_actualizacion.resizable(False, False)

        # Configurar el tema de la ventana
        ctk.set_appearance_mode(self.tema_actual)

        # Crear campos de entrada con los valores actuales
        frame_campos = ctk.CTkFrame(ventana_actualizacion)
        frame_campos.pack(pady=20, padx=20, fill="both", expand=True)

        # Campo de nombre
        label_nombre = ctk.CTkLabel(frame_campos, text="Nombre:")
        label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_campos)
        self.entry_nombre.insert(0, nombre_actual)
        self.entry_nombre.pack(pady=5)

        # Campo de apellido
        label_apellido = ctk.CTkLabel(frame_campos, text="Apellido:")
        label_apellido.pack(pady=5)
        self.entry_apellido = ctk.CTkEntry(frame_campos)
        self.entry_apellido.insert(0, apellido_actual)
        self.entry_apellido.pack(pady=5)

        # Campo de correo
        label_correo = ctk.CTkLabel(frame_campos, text="Correo:")
        label_correo.pack(pady=5)
        self.entry_correo = ctk.CTkEntry(frame_campos)
        self.entry_correo.insert(0, correo_actual)
        self.entry_correo.pack(pady=5)

        # Campo de teléfono
        label_telefono = ctk.CTkLabel(frame_campos, text="Teléfono:")
        label_telefono.pack(pady=5)
        self.entry_telefono = ctk.CTkEntry(frame_campos)
        self.entry_telefono.insert(0, telefono_actual)
        self.entry_telefono.pack(pady=5)

        # Frame para los botones
        frame_botones = ctk.CTkFrame(ventana_actualizacion)
        frame_botones.pack(pady=20)

        # Botón de guardar
        btn_guardar = ctk.CTkButton(frame_botones, text="Guardar",
                                  command=lambda: self.guardar_actualizacion(id_estudiante, ventana_actualizacion))
        btn_guardar.pack(side="left", padx=5)

        # Botón de cancelar
        btn_cancelar = ctk.CTkButton(frame_botones, text="Cancelar",
                                   command=ventana_actualizacion.destroy)
        btn_cancelar.pack(side="left", padx=5)

        # Hacer que la ventana sea modal
        ventana_actualizacion.transient(self.root)
        ventana_actualizacion.grab_set()
        self.root.wait_window(ventana_actualizacion)

    def guardar_actualizacion(self, id_estudiante, ventana):
        # Obtener los nuevos valores
        nuevo_nombre = self.entry_nombre.get()
        nuevo_apellido = self.entry_apellido.get()
        nuevo_correo = self.entry_correo.get()
        nuevo_telefono = self.entry_telefono.get()

        # Validar campos
        if not nuevo_nombre or not nuevo_apellido or not nuevo_correo or not nuevo_telefono:
            self.mostrar_mensaje("Error", "Todos los campos son requeridos", "error")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", nuevo_correo):
            self.mostrar_mensaje("Error", "El formato del correo no es válido", "error")
            return

        # Mostrar confirmación
        confirmacion = self.mostrar_confirmacion(
            "Confirmar Actualización",
            "¿Está seguro que desea actualizar los datos del estudiante?"
        )

        if confirmacion:
            try:
                self.estudiante_controller.actualizar_estudiante(
                    id_estudiante, nuevo_nombre, nuevo_apellido, nuevo_correo, nuevo_telefono
                )
                self.mostrar_mensaje("Éxito", "Estudiante actualizado correctamente", "info")
                self.cargar_datos_tabla()  # Recargar la tabla
                ventana.destroy()  # Cerrar la ventana de actualización
            except Exception as e:
                self.mostrar_mensaje("Error", f"Error al actualizar el estudiante: {str(e)}", "error")

    def regresar_menu_principal(self):
        from view.viewTkinter.viewEstudiante.menuEstudiante import MenuEstudiante
        self.root.destroy()
        menu_principal = MenuEstudiante(db=self.db, tema_actual=self.tema_actual)
        menu_principal.root.mainloop()