from abc import ABC, abstractmethod  # Importa la biblioteca ABC para crear clases abstractas

# Definimos la clase abstracta Moneda
class Moneda(ABC):
    # Método abstracto de inicialización para Moneda
    @abstractmethod
    def __init__(self, nombre):
        self.nombre = nombre  # Atributo que almacena el nombre de la moneda
    
    # Método abstracto para cargar el nombre de la moneda
    @abstractmethod
    def cargar_nombre(self, nombre):
        self.nombre = nombre  # Asigna un nuevo nombre a la moneda
    
    # Método abstracto para mostrar el nombre de la moneda
    @abstractmethod
    def mostrar_nombre(self):
        return self.nombre  # Retorna el nombre de la moneda

# Clase Tipo, que hereda de Moneda
class Tipo(Moneda):  
    def __init__(self, tipo, moneda):
        super().__init__(moneda)  # Inicializa la clase base con el nombre de la moneda
        self.cargar_nombre(tipo)  # Define el tipo de moneda (por ejemplo, "oficial" o "blue")
        self.cotizaciones = []  # Lista para almacenar las cotizaciones de la moneda

    # Método para cargar el tipo de la moneda
    def cargar_nombre(self, tipo):
        self.tipo = tipo  # Almacena el tipo de moneda
    
    # Método para mostrar el tipo de la moneda
    def mostrar_nombre(self):
        return self.tipo  # Retorna el tipo de moneda
    
    # Método para mostrar información de la moneda en formato de cadena
    def __str__(self):
        if self.cotizaciones:  # Verifica si hay cotizaciones
            # Si hay cotizaciones, muestra la última junto con el nombre y tipo de moneda
            return f"La moneda es: {super().mostrar_nombre()} {self.mostrar_nombre()} {self.cotizaciones[-1]}"
        else:
            # Si no hay cotizaciones, muestra solo el nombre y tipo de moneda
            return f"La moneda es: {self.nombre} {self.tipo} sin cotizaciones"

    # Método para agregar una cotización a la lista de cotizaciones
    def cargarcotizaciones(self, cotizacion):
        self.cotizaciones.append(cotizacion)  # Añade la nueva cotización a la lista

    # Método para mostrar todas las cotizaciones de la moneda
    def mostrarcotizacion(self):
        return self.cotizaciones  # Retorna la lista de cotizaciones
    
# Clase Cotizacion, que maneja los valores de venta, compra y fecha
class Cotizacion:
    # Inicializador que asigna venta, compra y fecha
    def __init__(self, venta, compra, fecha):
        self.cargarventa(venta)  # Asigna el valor de venta
        self.cargarcompra(compra)  # Asigna el valor de compra
        self.cargarfecha(fecha)  # Asigna la fecha de la cotización

    # Método para asignar el valor de compra
    def cargarcompra(self, compra):
        self.compra = compra
    
    # Método para asignar el valor de venta
    def cargarventa(self, venta):
        self.venta = venta

    # Método para asignar la fecha de la cotización
    def cargarfecha(self, fecha):
        self.fecha = fecha

    # Método para mostrar el valor de compra
    def mostrarcompra(self):
        return self.compra  # Retorna el valor de compra
    
    # Método para mostrar el valor de venta
    def mostrarventa(self):
        return self.venta  # Retorna el valor de venta

    # Método para mostrar la fecha de la cotización
    def mostrarfecha(self):
        return self.fecha  # Retorna la fecha de la cotización

    # Método para mostrar los detalles de la cotización en formato de cadena
    def __str__(self):
        return f"El precio de compra es: {self.mostrarcompra()}, el precio de venta es: {self.mostrarventa()} y la fecha de actualizacion es {self.mostrarfecha()}"

# Creación de una instancia de Tipo con el nombre "dolar" y el tipo "oficial"
moneda1 = Tipo("oficial", "dolar")

# Creación de una instancia de Cotizacion con valores de venta, compra y fecha
cotizacion1 = Cotizacion(900, 950, "20121009")

# Agrega la cotización a la lista de cotizaciones de moneda1
moneda1.cargarcotizaciones(cotizacion1)

# Imprime información de moneda1, incluyendo la última cotización si existe
print(moneda1)

# Imprime los detalles de cotizacion1
print(cotizacion1)

# Imprime la primera cotización en la lista de cotizaciones de moneda1
print(moneda1.cotizaciones[0])
