import customtkinter as ctk
from tkinter import ttk
from controllers.horario_controller import HorarioController
from controllers.curso_controller import CursoController

class ActualizarHorario:
    def __init__(self, db=None, tema_actual="System"):
        self.db = db
        self.tema_actual = tema_actual
        self.root = ctk.CTk()
        self.root.title("Actualizar Horario")
        self.horario_controller = HorarioController(db)
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
        self.titulo = ctk.CTkLabel(self.root, text="Actualizar Horario", font=("Arial", 16))
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

        # Botón para actualizar horario
        self.btn_actualizar = ctk.CTkButton(self.frame_botones, text="Actualizar Horario", command=self.actualizar_horario)
        self.btn_actualizar.pack(side="left", padx=5)

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

    def actualizar_horario(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            self.mostrar_mensaje("Advertencia", "Por favor seleccione un horario para actualizar", "warning")
            return

        item = self.tabla.item(seleccion[0])
        id_horario = item['values'][0]
        dia_actual = item['values'][1]
        hora_inicio_actual = item['values'][2]
        hora_fin_actual = item['values'][3]
        curso_id_actual = item['values'][4]

        # Crear ventana de actualización
        ventana_actualizacion = ctk.CTkToplevel(self.root)
        ventana_actualizacion.title("Actualizar Datos del Horario")
        ventana_actualizacion.geometry("500x500")
        ventana_actualizacion.resizable(False, False)

        ctk.set_appearance_mode(self.tema_actual)

        frame_campos = ctk.CTkFrame(ventana_actualizacion)
        frame_campos.pack(pady=20, padx=20, fill="both", expand=True)

        # Campo para día de la semana
        label_dia = ctk.CTkLabel(frame_campos, text="Día de la semana:")
        label_dia.pack(pady=5)
        self.combo_dia = ctk.CTkComboBox(frame_campos, values=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
        self.combo_dia.set(dia_actual)
        self.combo_dia.pack(pady=5, fill="x")

        # Campo para hora de inicio
        label_hora_inicio = ctk.CTkLabel(frame_campos, text="Hora de inicio (HH:MM):")
        label_hora_inicio.pack(pady=5)
        self.entry_hora_inicio = ctk.CTkEntry(frame_campos)
        self.entry_hora_inicio.insert(0, str(hora_inicio_actual))
        self.entry_hora_inicio.pack(pady=5, fill="x")

        # Campo para hora de fin
        label_hora_fin = ctk.CTkLabel(frame_campos, text="Hora de fin (HH:MM):")
        label_hora_fin.pack(pady=5)
        self.entry_hora_fin = ctk.CTkEntry(frame_campos)
        self.entry_hora_fin.insert(0, str(hora_fin_actual))
        self.entry_hora_fin.pack(pady=5, fill="x")

        # Campo para curso
        label_curso = ctk.CTkLabel(frame_campos, text="Curso:")
        label_curso.pack(pady=5)
        self.combo_curso = ctk.CTkComboBox(frame_campos, values=["Cargando..."])
        self.combo_curso.pack(pady=5, fill="x")

        # Cargar cursos
        self.cargar_cursos_actualizar(curso_id_actual)

        frame_botones = ctk.CTkFrame(ventana_actualizacion)
        frame_botones.pack(pady=20)

        btn_guardar = ctk.CTkButton(frame_botones, text="Guardar",
                                  command=lambda: self.guardar_actualizacion(id_horario, ventana_actualizacion))
        btn_guardar.pack(side="left", padx=5)

        btn_cancelar = ctk.CTkButton(frame_botones, text="Cancelar",
                                   command=ventana_actualizacion.destroy)
        btn_cancelar.pack(side="left", padx=5)

        ventana_actualizacion.transient(self.root)
        ventana_actualizacion.grab_set()
        self.root.wait_window(ventana_actualizacion)

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

    def validar_hora(self, hora):
        try:
            partes = hora.split(":")
            if len(partes) != 2:
                return False
            horas = int(partes[0])
            minutos = int(partes[1])
            return 0 <= horas <= 23 and 0 <= minutos <= 59
        except:
            return False

    def guardar_actualizacion(self, id_horario, ventana):
        nuevo_dia = self.combo_dia.get()
        nueva_hora_inicio = self.entry_hora_inicio.get()
        nueva_hora_fin = self.entry_hora_fin.get()
        nuevo_curso = self.combo_curso.get()

        if not nuevo_dia or not nueva_hora_inicio or not nueva_hora_fin or nuevo_curso == "Cargando...":
            self.mostrar_mensaje("Error", "Todos los campos son requeridos", "error")
            return

        if not self.validar_hora(nueva_hora_inicio) or not self.validar_hora(nueva_hora_fin):
            self.mostrar_mensaje("Error", "Formato de hora inválido. Use HH:MM", "error")
            return

        # Extraer ID del curso
        nuevo_curso_id = int(nuevo_curso.split(" - ")[0])

        confirmacion = self.mostrar_confirmacion(
            "Confirmar Actualización",
            "¿Está seguro que desea actualizar los datos del horario?"
        )

        if confirmacion:
            try:
                self.horario_controller.actualizar_horario(
                    id_horario, nuevo_dia, nueva_hora_inicio, nueva_hora_fin, nuevo_curso_id
                )
                self.mostrar_mensaje("Éxito", "Horario actualizado correctamente", "info")
                self.cargar_datos_tabla()
                ventana.destroy()
            except Exception as e:
                self.mostrar_mensaje("Error", f"Error al actualizar el horario: {str(e)}", "error")

    def regresar_menu_principal(self):
        from view.viewTkinter.viewHorario.menuHorarioFull import MenuHorarioFull
        self.root.destroy()
        menu_horario = MenuHorarioFull(db=self.db, tema_actual=self.tema_actual)
        menu_horario.root.mainloop()
