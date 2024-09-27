fetch("https://dolarapi.com/v1/dolares")
    .then(response => response.json())
    .then(data => {
        for (i = 0; i < data.length; i++) {
            agregarCotizacion(data[i].nombre, data[i].venta, data[i].compra)
        }
    })


fetch("https://dolarapi.com/v1/cotizaciones")
    .then(response => response.json())
    .then(data => {
        for (i = 1; i < data.length; i++) {
            agregarCotizacion(data[i].nombre, data[i].venta, data[i].compra)
        }
    })

function agregarCotizacion(nombre, venta, compra) {
    var x = document.getElementsByClassName("tipo")[0].cloneNode(true)

    x.querySelector(".Nombre").innerHTML = nombre
    x.querySelector(".Venta").innerHTML = venta
    x.querySelector(".Compra").innerHTML = compra
    document.getElementsByClassName("lista")[0].appendChild(x);  

}