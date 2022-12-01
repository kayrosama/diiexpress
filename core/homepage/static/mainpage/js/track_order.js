var pathname = window.location.pathname;

$(function () {
    $('#header').removeClass('fixed-top');

    $('.btnSearch').on('click', function () {
        $('#tblShippingRoute').DataTable({
            autoWidth: false,
            destroy: true,
            paging: false,
            info: false,
            searching: false,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                data: {
                    'action': 'search_shipping_route',
                    'number': $('input[name="number"]').val()
                },
                dataSrc: ""
            },
            columns: [
                {data: "date_joined"},
                {data: "status"},
                {data: "comment"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var name = row.status.name;
                        switch (row.status.id) {
                            case "received":
                                return '<span class="badge bg-primary badge-pill">' + name + '</span>';
                            case "on_route":
                                return '<span class="badge bg-warning badge-pill">' + name + '</span>';
                            case "delivered":
                                return '<span class="badge bg-success badge-pill">' + name + '</span>';
                        }
                    }
                },
            ],
            initComplete: function (settings, json) {
                if($.isEmptyObject(json)){
                    alert_sweetalert('info', 'Alerta', 'No se ha encontrado ningun registro con ese número de guía', function () {

                    }, 2000, null);
                }
            }
        });
    });

    $('input[name="number"]')
        .on('keypress', function (e) {
            return validate_form_text('numbers', e, null);
        })
        .on('keyup', function () {
            var value = $(this).val();
            $('.btnSearch').prop('disabled', value.length === 0);
        })
});