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


document.getElementById("formularioContacto").addEventListener('submit', function(event) {
    event.preventDefault(); // Evita que el formulario se envíe de manera tradicional

    const data = {
        nombre: document.getElementById('nombre').value,
        apellido: document.getElementById('apellido').value,
        email: document.getElementById('email').value,
        mensaje: document.getElementById('mensaje').value
    };

    fetch('http://127.0.0.1:5000/api/contacto/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        mode: "cors",
        body: JSON.stringify(data) // Convierte los datos a formato JSON
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("HTTP error! Status: ${response.status}");
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        alert('Contacto enviado exitosamente.');
        document.getElementById("formularioContacto").reset(); // Resetea el formulario después de enviar
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Hubo un error al enviar el contacto.');
    });
});



document.getElementById('envioCotizacionesMostrar').addEventListener('click', async function() {
    const email = document.getElementById('email1').value;
    if (email) {
        try {
            const response = await fetch('/api/contacto/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email1: email })
            });
            const result = await response.json();
            if (response.ok) {
                alert('Correo enviado exitosamente');
            } else {
                alert(result.error || 'Error al enviar el correo');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ocurrió un error al intentar enviar el correo');
        }
    } else {
        alert('Por favor ingresa un correo electrónico');
    }
});