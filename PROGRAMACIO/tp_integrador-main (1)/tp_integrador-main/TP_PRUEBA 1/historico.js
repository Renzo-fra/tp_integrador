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
/*
async function obtenerHistorico(moneda) {
    try {
        // Solicitar datos históricos específicos de la moneda
        const response = await fetch(`${apiHistoricoUrl}?moneda=${moneda}`);
        const datos = await response.json();

        const labels = [];
        const compraData = [];
        const ventaData = [];

        datos.forEach((cambio) => {
            labels.push(new Date(cambio.fecha).toLocaleDateString());
            compraData.push(cambio.compra);
            ventaData.push(cambio.venta);
        });

        crearGraficoHistorico(labels, compraData, ventaData);
    } catch (error) {
        console.error("Error al obtener datos del servidor:", error);
    }
}

function crearGraficoHistorico(labels, compraData, ventaData) {
    const ctx = document.getElementById('graficoHistorico').getContext('2d');

    // Destruir cualquier gráfico previo si existe
    if (window.miGrafico) {
        window.miGrafico.destroy();
    }

    // Crear un nuevo gráfico
    window.miGrafico = new Chart(ctx, {
        type: 'submit',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Compra',
                    date: compraData,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    fill: true
                },
                {
                    label: 'Venta',
                    date: ventaData,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'submit',
                    time: {
                        unit: 'day'
                    }
                },
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

// Detectar cambios en el selector de moneda y actualizar el gráfico
document.getElementById('selectorMoneda').addEventListener('change', (event) => {
    const monedaSeleccionada = event.target.value;
    obtenerHistorico(monedaSeleccionada);
});

// Cargar el gráfico con la moneda predeterminada al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    const monedaInicial = document.getElementById('selectorMoneda').value;
    obtenerHistorico(monedaInicial) ;
});*/