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