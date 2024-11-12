// URL del servidor local Flask
const apiUrl = "http://127.0.0.1:5000/api/cotizaciones";

async function obtenerDatos() {
    try {
        const response = await fetch(apiUrl);
        const datos = await response.json();

        const listaContainer = document.querySelector('.lista');
        listaContainer.innerHTML = '';

        datos.forEach((cambio) => {
            const tipoItem = document.createElement('li');
            tipoItem.classList.add('tipo');

            const listCambio = document.createElement('ul');
            listCambio.classList.add('list_cambio');

            const nombreItem = document.createElement('li');
            nombreItem.classList.add('Nombre');
            nombreItem.textContent = `Nombre: ${cambio.nombre}`;

            const compraItem = document.createElement('li');
            compraItem.classList.add('Compra');
            compraItem.textContent = `Compra: $${cambio.compra}`;

            const ventaItem = document.createElement('li');
            ventaItem.classList.add('Venta');
            ventaItem.textContent = `Venta: $${cambio.venta}`;

            const fechaItem = document.createElement('li');
            fechaItem.classList.add('Fecha');
            fechaItem.textContent = `Fecha de actualización: ${new Date(cambio.fecha).toLocaleString()}`;

            listCambio.appendChild(nombreItem);
            listCambio.appendChild(compraItem);
            listCambio.appendChild(ventaItem);
            listCambio.appendChild(fechaItem);
            tipoItem.appendChild(listCambio);
            listaContainer.appendChild(tipoItem);
        });
    } catch (error) {
        console.error("Error al obtener datos del servidor:", error);
    }
}

document.addEventListener('DOMContentLoaded', obtenerDatos);
