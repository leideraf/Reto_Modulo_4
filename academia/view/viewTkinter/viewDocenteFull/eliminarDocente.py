import customtkinter as ctk
from tkinter import ttk
from controllers.docente_controller import DocenteController
from mysql.connector import IntegrityError

class EliminarDocente:
    def __init__(self, db=None, tema_actual="System"):
        self.db = db
        self.tema_actual = tema_actual
        self.root = ctk.CTk()
        self.root.title("Eliminar Docente")
        self.docente_controller = DocenteController(db)

        # Configurar el tema de la ventana
        ctk.set_appearance_mode(tema_actual)

        # Obtener el ancho y alto de la pantalla
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        # Asignar tamaño de la ventana
        ancho_ventana = int(ancho_pantalla * 0.6)
        alto_ventana = int(alto_pantalla * 0.5)

        #calcular posicion para centrar
        posicion_x = int((ancho_pantalla - ancho_ventana) / 2)
        posicion_y = int((alto_pantalla - alto_ventana) / 2)

        #Establecer tamaño y posicon centrada
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

        # Configuración de restricciones de la ventana
        self.root.resizable(False, False)

        # Titulo de la ventana
        self.titulo = ctk.CTkLabel(self.root, text="Eliminar Docente", font=("Arial", 16))
        self.titulo.pack(pady=10)

        # Crear un frame para la tabla
        self.frame_tabla = ctk.CTkFrame(self.root)
        self.frame_tabla.pack(pady=10, padx=20, fill="both", expand=True)

        # Crear la tabla (usando Treeview de tkinter)
        self.tabla = ttk.Treeview(self.frame_tabla, columns=("ID", "Nombre", "Apellido", "Correo", "Telefono", "Especialidad"), show="headings")
        self.tabla.pack(expand=True, fill="both", padx=10, pady=10)

        # Configurar encabezados
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Apellido", text="Apellido")
        self.tabla.heading("Correo", text="Correo")
        self.tabla.heading("Telefono", text="Teléfono")
        self.tabla.heading("Especialidad", text="Especialidad")

        # Ajustar el ancho de las columnas
        self.tabla.column("ID", width=80)
        self.tabla.column("Nombre", width=120)
        self.tabla.column("Apellido", width=120)
        self.tabla.column("Correo", width=200)
        self.tabla.column("Telefono", width=120)
        self.tabla.column("Especialidad", width=150)

        # Crear un frame para los botones
        self.frame_botones = ctk.CTkFrame(self.root)
        self.frame_botones.pack(pady=10)

        # Botón para eliminar docente
        self.btn_eliminar = ctk.CTkButton(self.frame_botones, text="Eliminar Docente", command=self.eliminar_docente)
        self.btn_eliminar.pack(side="left", padx=5)

        # Botón para regresar
        self.btn_regresar = ctk.CTkButton(self.frame_botones, text="Regresar", command=self.regresar_menu_principal)
        self.btn_regresar.pack(side="left", padx=5)

        # Cargar los datos de la tabla
        self.cargar_datos_tabla()

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

    def eliminar_docente(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            self.mostrar_mensaje("Advertencia", "Por favor seleccione un docente para eliminar", "warning")
            return

        item = self.tabla.item(seleccion[0])
        id_docente = item['values'][0]
        nombre = item['values'][1]
        apellido = item['values'][2]

        confirmacion = self.mostrar_confirmacion(
            "Confirmar Eliminación",
            f"¿Está seguro que desea eliminar al docente {nombre} {apellido}?"
        )

        if confirmacion:
            try:
                self.docente_controller.eliminar_docente(id_docente)
                self.mostrar_mensaje("Éxito", "Docente eliminado correctamente", "info")
                self.cargar_datos_tabla()
            except Exception as e:
                self.mostrar_mensaje("Error", f"Error al eliminar el docente: {str(e)}", "error")

    def regresar_menu_principal(self):
        from view.viewTkinter.viewDocenteFull.menuDocenteFull import MenuDocenteFull
        self.root.destroy()
        menu_docente = MenuDocenteFull(db=self.db, tema_actual=self.tema_actual)
        menu_docente.root.mainloop()
