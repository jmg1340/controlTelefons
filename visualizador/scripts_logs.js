$(document).ready(function() {
    // Cargar y mostrar la fecha de modificación del fichero
    fetch('../logs.json')
        .then(response => {
            if (response.ok) {
                const lastModifiedHeader = response.headers.get('Last-Modified');
                if (lastModifiedHeader) {
                    const lastModified = new Date(lastModifiedHeader);
                    const formattedLastModified = `${lastModified.getDate().toString().padStart(2, '0')}/${(lastModified.getMonth() + 1).toString().padStart(2, '0')}/${lastModified.getFullYear()} ${lastModified.getHours().toString().padStart(2, '0')}:${lastModified.getMinutes().toString().padStart(2, '0')}:${lastModified.getSeconds().toString().padStart(2, '0')}`;
                    $('#lastModified').text(formattedLastModified);
                } else {
                    $('#lastModified').text('No disponible');
                }
            } else {
                 $('#lastModified').text('Error al cargar');
            }
            return response.json();
        })
        .then(data => {
            const tableBody = $('#logsTableBody');
            tableBody.empty();
            data.forEach(function(log) {
                const timestamp = new Date(log.timeStamp);
                const formattedTimestamp = `${timestamp.getDate().toString().padStart(2, '0')}/${(timestamp.getMonth() + 1).toString().padStart(2, '0')}/${timestamp.getFullYear()} ${timestamp.getHours().toString().padStart(2, '0')}:${timestamp.getMinutes().toString().padStart(2, '0')}`;
                const row = `<tr>
                    <td>${formattedTimestamp}</td>
                    <td>${log.estado}</td>
                    <td>${log.extension}</td>
                    <td>${log['ip actual']}</td>
                </tr>`;
                tableBody.append(row);
            });
        })
        .catch(error => {
            console.error('Error al cargar o procesar logs.json:', error);
            $('#lastModified').text('Error');
        });


    // Funcionalidad de búsqueda
    $('#searchInput').on('keyup', function() {
        const value = $(this).val().toLowerCase();
        $('#logsTableBody tr').filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});
