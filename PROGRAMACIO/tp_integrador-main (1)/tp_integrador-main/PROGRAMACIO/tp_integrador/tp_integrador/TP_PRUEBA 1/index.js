// URL de la API desde la cual se obtienen las cotizaciones
const apiUrl = "http://127.0.0.1:5000/api/cotizaciones";

// Función asíncrona para obtener datos de cotizaciones desde la API
async function obtenerDatos() {
    try {
        // Realiza una solicitud fetch para obtener los datos de la API
        const response = await fetch(apiUrl);
        const datos = await response.json();  // Convierte la respuesta a JSON

        // Selecciona el contenedor donde se mostrará la lista de cotizaciones
        const listaContainer = document.querySelector('.lista');
        listaContainer.innerHTML = '';  // Limpia el contenido previo del contenedor

        // Itera sobre los datos recibidos y crea elementos HTML para mostrar cada cotización
        datos.forEach((cambio) => {
            const tipoItem = document.createElement('li');  // Crea un elemento <li> para el tipo de cambio
            tipoItem.classList.add('tipo');  // Agrega la clase 'tipo' al elemento

            const listCambio = document.createElement('ul');  // Crea un elemento <ul> para los detalles del cambio
            listCambio.classList.add('list_cambio');  // Agrega la clase 'list_cambio' al <ul>

            // Crea elementos <li> para mostrar el nombre, compra, venta y fecha de actualización
            const nombreItem = document.createElement('li');
            nombreItem.classList.add('Nombre');
            nombreItem.textContent = `Nombre: ${cambio.nombre}`;  // Texto que muestra el nombre del cambio

            const compraItem = document.createElement('li');
            compraItem.classList.add('Compra');
            compraItem.textContent = `Compra: $${cambio.compra}`;  // Muestra el valor de compra

            const ventaItem = document.createElement('li');
            ventaItem.classList.add('Venta');
            ventaItem.textContent = `Venta: $${cambio.venta}`;  // Muestra el valor de venta

            const fechaItem = document.createElement('li');
            fechaItem.classList.add('Fecha');
            fechaItem.textContent = `Fecha de actualización: ${new Date(cambio.fecha).toLocaleString()}`;  // Muestra la fecha de actualización en formato local

            // Agrega los elementos de información al <ul> y luego lo añade al <li> tipoItem
            listCambio.appendChild(nombreItem);
            listCambio.appendChild(compraItem);
            listCambio.appendChild(ventaItem);
            listCambio.appendChild(fechaItem);
            tipoItem.appendChild(listCambio);
            listaContainer.appendChild(tipoItem);  // Agrega cada tipo de cambio a la lista principal
        });
    } catch (error) {
        console.error("Error al obtener datos del servidor:", error);  // Muestra un error en consola si falla la solicitud
    }
}

// Ejecuta obtenerDatos cuando el DOM está completamente cargado
document.addEventListener('DOMContentLoaded', obtenerDatos);

// Configura el envío del formulario de contacto
document.getElementById("formularioContacto").addEventListener('submit', function(event) {
    event.preventDefault();  // Evita el envío tradicional del formulario

    // Crea un objeto de datos con los valores de los campos del formulario
    const data = {
        nombre: document.getElementById('nombre').value,
        apellido: document.getElementById('apellido').value,
        email: document.getElementById('email').value,
        mensaje: document.getElementById('mensaje').value
    };

    // Realiza una solicitud POST para enviar los datos del formulario a la API de contacto
    fetch('http://127.0.0.1:5000/api/contacto/', {
        method: 'POST',  // Especifica que el método es POST
        headers: {
            'Content-Type': 'application/json'  // Define el tipo de contenido como JSON
        },
        mode: "cors",  // Habilita CORS para permitir el intercambio de recursos entre orígenes
        body: JSON.stringify(data)  // Convierte los datos a formato JSON
    })
    .then(response => {
        if (!response.ok) {  // Verifica si la respuesta es correcta
            throw new Error(`HTTP error! Status: ${response.status}`);  // Lanza un error si la respuesta no es correcta
        }
        return response.json();  // Convierte la respuesta a JSON si es exitosa
    })
    .then(data => {
        console.log('Success:', data);  // Muestra un mensaje de éxito en la consola
        alert('Contacto enviado exitosamente.');  // Muestra un mensaje de éxito al usuario
        document.getElementById("formularioContacto").reset();  // Restaura el formulario a su estado inicial
    })
    .catch((error) => {
        console.error('Error:', error);  // Muestra un mensaje de error en la consola si la solicitud falla
        alert('Hubo un error al enviar el contacto.');  // Muestra un mensaje de error al usuario
    });
});
