import requests
from abc import ABC, abstractmethod

class MonedaBase(ABC):
    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def establecer_nombre(self, nombre):
        pass

    @abstractmethod
    def obtener_nombre(self):
        pass

class TipoMoneda(MonedaBase):
    def __init__(self, tipo, nombre_moneda):
        super().__init__(nombre_moneda)
        self.establecer_nombre(tipo)
        self.cotizaciones = []

    def establecer_nombre(self, tipo):
        self.tipo = tipo

    def obtener_nombre(self):
        return self.tipo

    def __str__(self):
        if self.cotizaciones:
            ultima_cotizacion = self.cotizaciones[-1]
            return f"La moneda es: {self.nombre} {self.obtener_nombre()} - Última cotización: {ultima_cotizacion}"
        else:
            return f"La moneda es: {self.nombre} {self.tipo} - Sin cotizaciones"

    def agregar_cotizacion(self, cotizacion):
        self.cotizaciones.append(cotizacion)

    def obtener_cotizaciones(self):
        return self.cotizaciones

class Cotizacion:
    def __init__(self, venta, compra, fecha):
        self.venta = venta or "No disponible"
        self.compra = compra or "No disponible"
        self.fecha = fecha or "Fecha no disponible"

    def obtener_compra(self):
        return self.compra

    def obtener_venta(self):
        return self.venta

    def obtener_fecha(self):
        return self.fecha

    def __str__(self):
        return f"Precio de compra: {self.obtener_compra()}, precio de venta: {self.obtener_venta()}, fecha de actualización: {self.obtener_fecha()}"

# Obtener datos de la API
response = requests.get("https://dolarapi.com/v1/dolares")
datos_api = response.json()

# Crear instancias de TipoMoneda para cada tipo de moneda en los datos de la API
monedas = {}

for cotizacion in datos_api:
    nombre_moneda = cotizacion.get("nombre", "moneda desconocida")
    tipo = cotizacion.get("casa", "tipo desconocido")
    venta = cotizacion.get("venta")
    compra = cotizacion.get("compra")
    fecha = cotizacion.get("fechaActualizacion")
    
    # Crear objeto Cotizacion
    cotizacion_obj = Cotizacion(venta, compra, fecha)
    
    # Crear o actualizar el objeto TipoMoneda correspondiente
    if tipo not in monedas:
        monedas[tipo] = TipoMoneda(tipo, nombre_moneda)
    monedas[tipo].agregar_cotizacion(cotizacion_obj)

# Mostrar resultados
for tipo, moneda in monedas.items():
    print(moneda)
    for cotizacion in moneda.obtener_cotizaciones():
        print(f"{moneda.nombre} {moneda.obtener_nombre()} - {cotizacion}")
