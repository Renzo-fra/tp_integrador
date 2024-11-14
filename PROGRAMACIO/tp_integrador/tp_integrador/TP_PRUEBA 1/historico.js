// Añade un evento 'submit' al formulario con ID 'datosHistorico' que se ejecuta al enviarse el formulario
document.getElementById("datosHistorico").addEventListener('submit', function(event) {
    event.preventDefault();  // Evita que el formulario se envíe de manera tradicional (evita el refresco de la página)

    // Obtiene los valores de los campos del formulario
    const dolar = document.getElementById('dolar').value;  // Tipo de dólar seleccionado
    const fechainicio = document.getElementById('fechainicio').value;  // Fecha de inicio
    const fechafin = document.getElementById('fechafin').value;  // Fecha de fin
    const valores = document.getElementById('valores').value;  // Número de puntos de datos solicitados

    // Construye la URL para hacer la solicitud al endpoint de la API con los parámetros especificados
    const peticion = `http://127.0.0.1:5000/api/historico/${dolar}/${fechainicio}/${fechafin}/${valores}`;

    // Realiza una solicitud fetch a la URL construida
    fetch(peticion)
        .then(response => {
            if (!response.ok) {  // Verifica si la respuesta fue exitosa
                throw new Error(`Error en la respuesta: ${response.status}`);  // Lanza un error si no fue exitosa
            }
            return response.json();  // Convierte la respuesta a JSON
        })
        .then(data => {
            console.log("Datos recibidos:", data);  // Muestra en consola los datos recibidos desde la API
            crearGrafico(data);  // Llama a la función crearGrafico con los datos obtenidos
        })
        .catch(error => console.error('Error al obtener los datos:', error));  // Muestra en consola si ocurre un error
});

// Función para crear el gráfico de cotización histórica
function crearGrafico(data) {
    // Si ya existe un gráfico, lo destruye antes de crear uno nuevo
    if (window.chart) {
        window.chart.destroy();
    }

    // Extrae las etiquetas (fechas) y valores (cotizaciones) de los datos recibidos
    const labels = data.map(item => item.fecha);  // Obtiene las fechas
    const valores = data.map(item => item.valor);  // Obtiene los valores de cotización

    // Selecciona el contexto del canvas con ID 'graficoHistorico' donde se renderizará el gráfico
    const ctx = document.getElementById('graficoHistorico').getContext('2d');
    window.chart = new Chart(ctx, {  // Crea una instancia de Chart.js para generar el gráfico
        type: 'line',  // Define el tipo de gráfico (línea)
        data: {
            labels: labels,  // Asigna las fechas como etiquetas del eje X
            datasets: [{
                label: 'Cotización Histórica',  // Etiqueta del gráfico
                data: valores,  // Datos de cotización para el gráfico
                borderColor: 'rgba(75, 192, 192, 1)',  // Color de la línea del gráfico
                borderWidth: 2,  // Grosor de la línea
                fill: false  // No se rellena el área bajo la línea
            }]
        },
        options: {
            responsive: true,  // Hace el gráfico adaptable al tamaño del contenedor
            scales: {
                x: { title: { display: true, text: 'Fecha' } },  // Título del eje X
                y: { title: { display: true, text: 'Valor en ARS' } }  // Título del eje Y
            }
        }
    });
}
