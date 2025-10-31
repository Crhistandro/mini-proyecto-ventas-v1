import datetime
import random

# ==========================
# Requerimientos y HU
# ==========================
# HU1: Como asesor comercial quiero registrar mis ventas para conocer mi progreso.
# HU2: Como asesor quiero ver el total de ventas y monto acumulado para saber cuánto llevo.
# HU3: Como asesor quiero comparar mis ventas con la meta para saber cuánto me falta.
# HU4: Como asesor quiero calcular mis comisiones automáticamente.
# HU5: Como asesor quiero ver una proyección de cumplimiento de mi meta.

# ==========================
# Programación Orientada a Objetos
# ==========================
class Venta:
    def __init__(self, monto):
        self.monto = monto
        self.fecha = datetime.datetime.now()

class Asesor:
    def __init__(self, nombre, meta, porcentaje_comision=0.05):
        self.nombre = nombre
        self.meta = meta
        self.porcentaje_comision = porcentaje_comision
        self.ventas = []

    def registrar_venta(self, monto):
        venta = Venta(monto)
        self.ventas.append(venta)
        print(f"✅ Venta registrada: ${monto} en {venta.fecha.strftime('%Y-%m-%d %H:%M:%S')}")

    def total_ventas(self):
        return len(self.ventas)

    def monto_total(self):
        return sum(v.monto for v in self.ventas)

    def comision(self):
        return self.monto_total() * self.porcentaje_comision

    def comparar_meta(self):
        diferencia = self.meta - self.monto_total()
        if diferencia > 0:
            return f"Te faltan ${diferencia} para cumplir tu meta."
        else:
            return f"🎉 ¡Meta alcanzada o superada por ${abs(diferencia)}!"

    def proyeccion(self):
        if self.total_ventas() == 0:
            return "Aún no hay datos suficientes para proyectar."
        promedio = self.monto_total() / self.total_ventas()
        proyeccion = promedio * random.randint(5, 10)  # Simulación de proyección
        return f"Proyección estimada de ventas futuras: ${proyeccion:.2f}"

# ==========================
# Funciones y estructuras de control
# ==========================
def menu():
    print("\n--- Sistema de Ventas ---")
    print("1. Registrar venta")
    print("2. Ver total de ventas")
    print("3. Ver monto acumulado")
    print("4. Ver comisión")
    print("5. Comparar con meta")
    print("6. Ver proyección")
    print("7. Salir")

def ejecutar():
    nombre = input("Ingrese su nombre: ")
    meta = float(input("Ingrese su meta de ventas en $: "))
    asesor = Asesor(nombre, meta)

    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            monto = float(input("Ingrese el monto de la venta: "))
            asesor.registrar_venta(monto)
        elif opcion == "2":
            print(f"📊 Total de ventas: {asesor.total_ventas()}")
        elif opcion == "3":
            print(f"💰 Monto acumulado: ${asesor.monto_total()}")
        elif opcion == "4":
            print(f"💵 Comisión generada: ${asesor.comision():.2f}")
        elif opcion == "5":
            print(asesor.comparar_meta())
        elif opcion == "6":
            print(asesor.proyeccion())
        elif opcion == "7":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("❌ Opción no válida, intente de nuevo.")

# ==========================
# Mini proyecto en ejecución
# ==========================
if __name__ == "__main__":
    ejecutar()
