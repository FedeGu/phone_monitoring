import time


class TimeAcumulador:
    def __init__(self):
        self.active_sessions = {}  #Persona_id -> star_time
        self.total_time = {}  #Persona_id -> total_seconds
        self.sessions = {}    #Persona_id -> list sessions

    def update(self, Persona_id, is_using_phone, timestamp=None):
        """
        Actualiza el estado de una persona.

        :param person_id: ID del tracker
        :param is_using_phone: bool
        :param timestamp: opcional, si no se pasa usa time.time()
        """
        if timestamp is None:
            timestamp = time.time()
        # Inicializar estructuras si no existen
        if Persona_id not in self.total_time:
            self.total_time[Persona_id] = 0.0
            self.sessions[Persona_id] = 0
        # Caso 1: comienza una sesión
        if is_using_phone and Persona_id not in self.active_sessions:
            self.active_sessions[Persona_id] = timestamp

        # Caso 2: termina una sesión
        if not is_using_phone and Persona_id in self.active_sessions:
            start_time = self.active_sessions.pop(Persona_id)
            duration = timestamp - start_time

            self.total_time[Persona_id] += duration
            self.sessions[Persona_id].append({
                "start": start_time,
                "end": timestamp,
                "duration_sec": duration
            })

    def get_total_time(self, Persona_id):
        return self.total_time.get(Persona_id, 0.0)
    
    def get_sessions(self, Persona_id):
        return self.sessions.get(Persona_id, [])
    
    def close_all(self, timestamp=None):
        """ Cierra todas las sesiones activas(fin del día)"""
        if timestamp is None:
            timestamp = time.time()

        for Persona_id in list(self.active_sessions.keys()):
            self.update(Persona_id, False, timestamp)