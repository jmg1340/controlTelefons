$(document).ready(function() {

    // Función para formatear el timestamp a "DD/MM/AAAA HH:MM"
    function formatTimestamp(isoTimestamp) {
        if (!isoTimestamp) {
            return 'N/A';
        }
        try {
            const date = new Date(isoTimestamp);
            const day = String(date.getDate()).padStart(2, '0');
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const year = date.getFullYear();
            const hours = String(date.getHours()).padStart(2, '0');
            const minutes = String(date.getMinutes()).padStart(2, '0');
            return `${day}/${month}/${year} ${hours}:${minutes}`;
        } catch (e) {
            return 'Fecha inválida';
        }
    }

    // Carga los datos del fichero JSON
    $.getJSON('../estado_telefonos.json', function(data) {
        const tablaBody = $('#tabla-telefonos');
        
        // Convierte el objeto de datos en un array para poder ordenarlo
        const telefonosArray = Object.keys(data).map(key => {
            return { extension: key, ...data[key] };
        });

        // Ordena el array: los desconectados (false) primero
        telefonosArray.sort((a, b) => {
            return a.estadoActual.conectado - b.estadoActual.conectado;
        });

        // Itera sobre el array ordenado para construir la tabla
        $.each(telefonosArray, function(i, telefono) {
            const extension = telefono.extension;
            const estado = telefono.estadoActual.conectado;
            const estadoClase = estado ? 'conectado' : 'desconectado';
            const estadoTexto = estado ? 'Conectado' : 'Desconectado';
            const ip = telefono.estadoActual.ip || 'N/A';

            // Construye la subtabla del historial
            let historialHtml = '<table class="table table-sm table-striped historial-table mb-0">';
            historialHtml += '<thead><tr><th>Fecha y Hora</th><th>Estado</th><th>IP</th></tr></thead>';
            historialHtml += '<tbody>';
            if (telefono.historial && telefono.historial.length > 0) {
                telefono.historial.slice().reverse().forEach(h => { // .slice().reverse() para mostrar el más reciente primero
                    historialHtml += `<tr>
                        <td>${formatTimestamp(h.timestamp)}</td>
                        <td>${h.conectado ? 'Conectado' : 'Desconectado'}</td>
                        <td>${h.ip || 'N/A'}</td>
                    </tr>`;
                });
            } else {
                historialHtml += '<tr><td colspan="3" class="text-center">Sin historial</td></tr>';
            }
            historialHtml += '</tbody></table>';

            // Construye la fila principal de la tabla
            const fila = `
                <tr>
                    <td><span class="estado-conexion ${estadoClase}"></span> ${estadoTexto}</td>
                    <td>${extension}</td>
                    <td>${ip}</td>
                    <td>${telefono.hostname || 'N/A'}</td>
                    <td>${telefono.model || 'N/A'}</td>
                    <td>${telefono.description || 'N/A'}</td>
                    <td>${historialHtml}</td>
                </tr>
            `;
            tablaBody.append(fila);
        });
    }).fail(function() {
        $('#tabla-telefonos').append('<tr><td colspan="5" class="text-center text-danger">No se pudo cargar el fichero estado_telefonos.json. Asegúrate de que existe y está en el directorio principal.</td></tr>');
    });

    // Funcionalidad del buscador
    $('#buscador').on('keyup', function() {
        const valor = $(this).val().toLowerCase();
        $('#tabla-telefonos tr').filter(function() {
            // $(this).text() obtiene todo el texto de la fila, incluyendo la subtabla
            $(this).toggle($(this).text().toLowerCase().indexOf(valor) > -1);
        });
    });
});
