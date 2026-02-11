import time
from time_acumulador import TimeAcumulador

acc = TimeAcumulador()

Persona_id = 1

#simulación
acc.update(Persona_id, True)
time.sleep(2)

acc.update(Persona_id, False)

print("Total:", acc.get_total_time(Persona_id))
print("Sesión", acc.get_sessions(Persona_id))