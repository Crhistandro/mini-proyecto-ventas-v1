import datetime
import json
import os
import random
import matplotlib.pyplot as plt


# ==========================
# Clases
# ==========================
class Venta:
    def __init__(self, monto, fecha=None):
        self.monto = monto
        self.fecha = datetime.datetime.fromisoformat(fecha) if fecha else datetime.datetime.now()
        
    def to_dict(self):
        return {
            "monto": self.monto,
            "fecha": self.fecha.isoformat()
        }

class Asesor:
    def __init__(self, nombre, meta, porcentaje_comision=0.05, ventas=None):
        self.nombre = nombre
        self.meta = meta
        self.porcentaje_comision = porcentaje_comision
        self.ventas = ventas or []

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
        proyeccion = promedio * random.randint(5, 10)
        return f"Proyección estimada de ventas futuras: ${proyeccion:.2f}"
    
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "meta": self.meta,
            "porcentaje_comision": self.porcentaje_comision,
            "ventas": [v.to_dict() for v in self.ventas]
        }

    @classmethod
    def from_dict(cls, data):
        ventas_objs = [Venta(v["monto"], v["fecha"]) for v in data.get("ventas", [])]
        return cls(
            nombre=data["nombre"],
            meta=data["meta"],
            porcentaje_comision=data.get("porcentaje_comision", 0.05),
            ventas=ventas_objs
        )

# ==========================
# Gráfica
# ==========================
def generar_grafica(asesor, mostrar=True, guardar=True, ruta="reports/indicadores.png"):
    categorias = ["Meta", "Acumulado"]
    valores = [asesor.meta, asesor.monto_total()]

    plt.figure(figsize=(6,4))
    barras = plt.bar(categorias, valores, color=["blue", "green"])
    plt.title(f"Indicadores de {asesor.nombre}")
    plt.ylabel("Monto en $")

    for barra in barras:
        yval = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2, yval + 10, f"${yval:.2f}", ha="center")

    if guardar:
        if not os.path.exists("reports"):
            os.makedirs("reports")
        plt.savefig(ruta)
        print(f"💾 Gráfica guardada en {ruta}")

    if mostrar:
        plt.show()

    plt.close()

# ==========================
# Persistencia
# ==========================
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "asesores.json")
BACKUP_FILE = os.path.join(DATA_DIR, "asesores_backup.json")

def asegurar_carpeta_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def guardar_asesores(asesores):
    try:
        asegurar_carpeta_data()
        data = {cc: a.to_dict() for cc, a in asesores.items()}
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        with open(BACKUP_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("💾 Datos guardados y respaldo creado.")
    except Exception as e:
        print(f"⚠️ Error al guardar los datos: {e}")

def cargar_asesores():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        if os.path.getsize(DATA_FILE) == 0:
            print("⚠️ El archivo de asesores está vacío. Se iniciará con datos nuevos.")
            return {}
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {cc: Asesor.from_dict(a) for cc, a in data.items()}
    except (json.JSONDecodeError, KeyError):
        print("⚠️ Archivo dañado. Intentando cargar respaldo...")
        if os.path.exists(BACKUP_FILE) and os.path.getsize(BACKUP_FILE) > 0:
            with open(BACKUP_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {cc: Asesor.from_dict(a) for cc, a in data.items()}
        return {}

# ==========================
# Entradas seguras
# ==========================
def leer_float(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("❌ Entrada inválida. Por favor ingrese un número válido.")

def leer_opcion(mensaje, opciones_validas):
    while True:
        opcion = input(mensaje)
        if opcion in opciones_validas:
            return opcion
        else:
            print(f"❌ Opción no válida. Debe ser una de: {', '.join(opciones_validas)}")

# ==========================
# Menú principal
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
    print("8. Cambiar meta")
    print("9. Ver gráfica de indicadores")

def ejecutar():
    asesores = cargar_asesores()

    cc = input("Ingrese su número de cédula: ")
    if cc in asesores:
        asesor = asesores[cc]
        print(f"👋 Bienvenido de nuevo, {asesor.nombre}. Meta: ${asesor.meta}, Ventas: {asesor.total_ventas()}")
    else:
        nombre = input("Ingrese su nombre: ")
        meta = leer_float("Ingrese su meta de ventas en $: ")
        asesor = Asesor(nombre, meta)
        asesores[cc] = asesor
        guardar_asesores(asesores)

    while True:
        menu()
        opcion = leer_opcion("Seleccione una opción: ", ["1","2","3","4","5","6","7","8","9"])

        if opcion == "1":
            monto = leer_float("Ingrese el monto de la venta: ")
            asesor.registrar_venta(monto)
            guardar_asesores(asesores)
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
            guardar_asesores(asesores)
            break
        elif opcion == "8":
            nueva_meta = leer_float("Ingrese la nueva meta en $: ")
            asesor.meta = nueva_meta
            guardar_asesores(asesores)
            print(f"✅ Meta actualizada a ${nueva_meta}")
        elif opcion == "9":
            mostrar = input("¿Desea mostrar la gráfica en pantalla? (s/n): ").lower() == "s"
            guardar = input("¿Desea guardar la gráfica como imagen? (s/n): ").lower() == "s"
            generar_grafica(asesor, mostrar=mostrar, guardar=guardar)

# ==========================
# Ejecución
# ==========================
if __name__ == "__main__":
    ejecutar()
