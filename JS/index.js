fetch("https://dolarapi.com/v1/dolares") //todos los tipos de dolares
    .then(response => response.json())
    .then(data => {
        for (i = 0; i < data.length; i++) {
            agregarCotizacion(data[i].nombre, data[i].venta, data[i].compra)
        }
    })


fetch("https://dolarapi.com/v1/cotizaciones") //cotizaciones que no son dolares
    .then(response => response.json())
    .then(data => {
        for (i = 1; i < data.length; i++) {
            agregarCotizacion(data[i].nombre, data[i].venta, data[i].compra)
        }
    })

function agregarCotizacion(nombre, venta, compra) {
    var x = document.getElementsByClassName("tipo")[0].cloneNode(true)

    x.querySelector(".Nombre").innerHTML = nombre
    x.querySelector(".Venta").innerHTML = "Venta: " + venta
    x.querySelector(".Compra").innerHTML = "Compra: " + compra
    document.getElementsByClassName("lista")[0].appendChild(x);  
}