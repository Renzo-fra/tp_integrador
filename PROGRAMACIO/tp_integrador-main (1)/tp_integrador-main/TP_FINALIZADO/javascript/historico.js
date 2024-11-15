document.getElementById("datosHistorico").addEventListener('submit', function(event) {
    event.preventDefault();

    // Capturar los valores del formulario
    const dolar = document.getElementById('dolar').value;
    const fechainicio = document.getElementById('fechainicio').value;
    const fechafin = document.getElementById('fechafin').value;
    const valores = document.getElementById('valores').value;

    // Construir la URL de la solicitud
    const peticion = `http://127.0.0.1:5000/api/historico/${dolar}/${fechainicio}/${fechafin}/${valores}`;

    fetch(peticion)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error en la respuesta: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Datos recibidos:", data);  // Verificar los datos en la consola
            crearGrafico(data);
        })
        .catch(error => console.error('Error al obtener los datos:', error));
});

// Función para crear el gráfico
function crearGrafico(data) {
    // Verificar si ya existe un gráfico anterior y destruirlo para evitar duplicados
    if (window.chart) {
        window.chart.destroy();
    }

    // Procesar los datos
    const labels = data.map(item => item.fecha);
    const valores = data.map(item => item.valor);

    const ctx = document.getElementById('graficoHistorico').getContext('2d');
    window.chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Cotización Histórica',
                data: valores,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Fecha' } },
                y: { title: { display: true, text: 'Valor en ARS' } }
            }
        }
    });
}
