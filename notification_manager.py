from datetime import datetime, timedelta

from config import DATE_FORMAT


class NotificationManager:

    def __init__(self, excel_manager):

        self.excel = excel_manager

        self.enabled = True

        self.days_warning = 3

    # =====================================================
    # CONFIGURACIÓN
    # =====================================================

    def enable(self):

        self.enabled = True

    def disable(self):

        self.enabled = False

    def is_enabled(self):

        return self.enabled

    # =====================================================
    # TAREAS
    # =====================================================

    @property
    def tasks(self):

        return self.excel.load_tasks()

    # =====================================================
    # VENCIDAS
    # =====================================================

    def overdue_tasks(self):

        return [

            t

            for t in self.tasks

            if t.esta_retrasada()

        ]

    # =====================================================
    # VENCEN HOY
    # =====================================================

    def due_today(self):

        hoy = datetime.now().strftime(

            DATE_FORMAT

        )

        return [

            t

            for t in self.tasks

            if t.fecha_prevista == hoy

        ]

    # =====================================================
    # PRÓXIMOS VENCIMIENTOS
    # =====================================================

    def upcoming_tasks(

        self,

        days=None

    ):

        if days is None:

            days = self.days_warning

        hoy = datetime.now().date()

        limite = hoy + timedelta(

            days=days

        )

        resultado = []

        for tarea in self.tasks:

            if not tarea.fecha_prevista:

                continue

            try:

                fecha = datetime.strptime(

                    tarea.fecha_prevista,

                    DATE_FORMAT

                ).date()

            except Exception:

                continue

            if hoy <= fecha <= limite:

                resultado.append(

                    tarea

                )

        return resultado

    # =====================================================
    # TAREAS CRÍTICAS
    # =====================================================

    def critical_tasks(self):

        return [

            t

            for t in self.tasks

            if t.prioridad == "Crítica"

        ]

    # =====================================================
    # PENDIENTES
    # =====================================================

    def pending_notifications(self):

        return {

            "vencidas":

                len(

                    self.overdue_tasks()

                ),

            "hoy":

                len(

                    self.due_today()

                ),

            "proximas":

                len(

                    self.upcoming_tasks()

                ),

            "criticas":

                len(

                    self.critical_tasks()

                )

        }



    # =====================================================
    # COLA DE NOTIFICACIONES
    # =====================================================

    def notification_queue(self):

        cola = []

        for tarea in self.overdue_tasks():

            cola.append({

                "tipo": "ERROR",

                "titulo": tarea.titulo,

                "mensaje": f"La tarea '{tarea.titulo}' está vencida.",

                "responsable": tarea.responsable,

                "fecha": tarea.fecha_prevista

            })

        for tarea in self.due_today():

            cola.append({

                "tipo": "WARNING",

                "titulo": tarea.titulo,

                "mensaje": f"La tarea '{tarea.titulo}' vence hoy.",

                "responsable": tarea.responsable,

                "fecha": tarea.fecha_prevista

            })

        for tarea in self.upcoming_tasks():

            cola.append({

                "tipo": "INFO",

                "titulo": tarea.titulo,

                "mensaje": f"La tarea '{tarea.titulo}' vencerá próximamente.",

                "responsable": tarea.responsable,

                "fecha": tarea.fecha_prevista

            })

        return cola

    # =====================================================
    # RESUMEN POR RESPONSABLE
    # =====================================================

    def owner_notifications(self):

        resultado = {}

        for aviso in self.notification_queue():

            responsable = aviso["responsable"] or "Sin asignar"

            resultado.setdefault(responsable, []).append(aviso)

        return resultado

    # =====================================================
    # RESUMEN DIARIO
    # =====================================================

    def daily_summary(self):

        return {

            "fecha": datetime.now().strftime("%d/%m/%Y"),

            "vencidas": len(self.overdue_tasks()),

            "vencen_hoy": len(self.due_today()),

            "proximas": len(self.upcoming_tasks()),

            "criticas": len(self.critical_tasks()),

            "total_avisos": len(self.notification_queue())

        }

    # =====================================================
    # MENSAJES PARA LA INTERFAZ
    # =====================================================

    def ui_messages(self):

        mensajes = []

        resumen = self.daily_summary()

        if resumen["vencidas"]:

            mensajes.append(

                f"⚠️ Hay {resumen['vencidas']} tareas vencidas."

            )

        if resumen["vencen_hoy"]:

            mensajes.append(

                f"📅 {resumen['vencen_hoy']} tareas vencen hoy."

            )

        if resumen["proximas"]:

            mensajes.append(

                f"⏳ {resumen['proximas']} tareas vencerán en los próximos días."

            )

        if resumen["criticas"]:

            mensajes.append(

                f"🚨 {resumen['criticas']} tareas tienen prioridad crítica."

            )

        return mensajes

    # =====================================================
    # CONFIGURACIÓN
    # =====================================================

    def set_warning_days(self, days):

        self.days_warning = max(1, int(days))

    # =====================================================
    # VALIDACIÓN
    # =====================================================

    def validate(self):

        try:

            self.pending_notifications()

            self.notification_queue()

            return True

        except Exception:

            return False

    # =====================================================
    # INFORMACIÓN
    # =====================================================

    def info(self):

        return {

            "manager": "NotificationManager",

            "enabled": self.enabled,

            "dias_aviso": self.days_warning,

            "estado": self.validate(),

            "resumen": self.daily_summary()

        }

    # =====================================================
    # MANTENIMIENTO
    # =====================================================

    def maintenance(self):

        return self.daily_summary()


