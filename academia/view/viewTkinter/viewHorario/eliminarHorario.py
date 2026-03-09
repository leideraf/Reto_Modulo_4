import customtkinter as ctk
from tkinter import ttk
from controllers.horario_controller import HorarioController

class EliminarHorario:
    def __init__(self, db=None, tema_actual="System"):
        self.db = db
        self.tema_actual = tema_actual
        self.root = ctk.CTk()
        self.root.title("Eliminar Horario")
        self.horario_controller = HorarioController(db)

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
        self.titulo = ctk.CTkLabel(self.root, text="Eliminar Horario", font=("Arial", 16))
        self.titulo.pack(pady=10)

        # Crear un frame para la tabla
        self.frame_tabla = ctk.CTkFrame(self.root)
        self.frame_tabla.pack(pady=10, padx=20, fill="both", expand=True)

        # Crear la tabla (usando Treeview de tkinter)
        self.tabla = ttk.Treeview(self.frame_tabla, columns=("ID", "Dia", "Hora_Inicio", "Hora_Fin", "Curso_ID", "Curso_Nombre"), show="headings")
        self.tabla.pack(expand=True, fill="both", padx=10, pady=10)

        # Configurar encabezados
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Dia", text="Día")
        self.tabla.heading("Hora_Inicio", text="Hora Inicio")
        self.tabla.heading("Hora_Fin", text="Hora Fin")
        self.tabla.heading("Curso_ID", text="ID Curso")
        self.tabla.heading("Curso_Nombre", text="Curso")

        # Ajustar el ancho de las columnas
        self.tabla.column("ID", width=80)
        self.tabla.column("Dia", width=120)
        self.tabla.column("Hora_Inicio", width=120)
        self.tabla.column("Hora_Fin", width=120)
        self.tabla.column("Curso_ID", width=100)
        self.tabla.column("Curso_Nombre", width=200)

        # Crear un frame para los botones
        self.frame_botones = ctk.CTkFrame(self.root)
        self.frame_botones.pack(pady=10)

        # Botón para eliminar horario
        self.btn_eliminar = ctk.CTkButton(self.frame_botones, text="Eliminar Horario", command=self.eliminar_horario)
        self.btn_eliminar.pack(side="left", padx=5)

        # Botón para regresar
        self.btn_regresar = ctk.CTkButton(self.frame_botones, text="Regresar", command=self.regresar_menu_principal)
        self.btn_regresar.pack(side="left", padx=5)

        # Cargar los datos de la tabla
        self.cargar_datos_tabla()

    def cargar_datos_tabla(self):
        try:
            horarios = self.horario_controller.listar_horarios()
            # Limpiar la tabla antes de cargar nuevos datos
            for row in self.tabla.get_children():
                self.tabla.delete(row)

            for horario in horarios:
                # Insertar filas en la tabla
                self.tabla.insert("", "end", values=(
                    horario.id_horario,
                    horario.dia_semana,
                    horario.hora_inicio,
                    horario.hora_fin,
                    horario.curso_id,
                    horario.curso_nombre
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

    def eliminar_horario(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            self.mostrar_mensaje("Advertencia", "Por favor seleccione un horario para eliminar", "warning")
            return

        item = self.tabla.item(seleccion[0])
        id_horario = item['values'][0]
        dia = item['values'][1]
        curso_nombre = item['values'][5]

        confirmacion = self.mostrar_confirmacion(
            "Confirmar Eliminación",
            f"¿Está seguro que desea eliminar el horario del '{dia}' para '{curso_nombre}'?"
        )

        if confirmacion:
            try:
                self.horario_controller.eliminar_horario(id_horario)
                self.mostrar_mensaje("Éxito", "Horario eliminado correctamente", "info")
                self.cargar_datos_tabla()
            except Exception as e:
                self.mostrar_mensaje("Error", f"Error al eliminar el horario: {str(e)}", "error")

    def regresar_menu_principal(self):
        from view.viewTkinter.viewHorario.menuHorarioFull import MenuHorarioFull
        self.root.destroy()
        menu_horario = MenuHorarioFull(db=self.db, tema_actual=self.tema_actual)
        menu_horario.root.mainloop()
