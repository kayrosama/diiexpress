var tblShippingRoute;
var input_date_range;

var shipping_route = {
    list: function (all) {
        var parameters = {
            'action': 'search',
            'start_date': input_date_range.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_date_range.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }
        tblShippingRoute = $('#data').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: parameters,
                dataSrc: ""
            },
            order: [[0, "desc"], [5, "desc"]],
            columns: [
                {data: "number"},
                {data: "date_joined"},
                {data: "client.names"},
                {data: "client.dni"},
                {data: "subtotal"},
                {data: "iva"},
                {data: "total"},
                {data: "status"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var name = row.status.name;
                        switch (row.status.id) {
                            case "received":
                                return '<span class="badge badge-primary badge-pill">' + name + '</span>';
                            case "on_route":
                                return '<span class="badge badge-warning badge-pill">' + name + '</span>';
                            case "delivered":
                                return '<span class="badge badge-success badge-pill">' + name + '</span>';
                        }
                    }
                },
                {
                    targets: [-3, -4, -5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '';
                        buttons += '<a class="btn btn-secondary btn-xs btn-flat" rel="shipping_route"><i class="fa-solid fa-route"></i></a> ';
                        buttons += '<a class="btn btn-warning btn-xs btn-flat" href="/erp/shipping/route/add/' + row.id + '/"><i class="fas fa-folder-plus"></i></a> ';
                        buttons += '<a class="btn btn-info btn-xs btn-flat" rel="detail"><i class="fas fa-folder-open"></i></a> ';
                        buttons += '<a href="/erp/shipping/route/print/invoice/' + row.id + '/" target="_blank" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-print"></i></a> ';
                        buttons += '<a href="/erp/shipping/route/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a> ';
                        return buttons;
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
}

$(function () {

    input_date_range = $('input[name="date_range"]');

    $('#data tbody')
        .off()
        .on('click', 'a[rel="detail"]', function () {
            $('.tooltip').remove();
            var tr = tblShippingRoute.cell($(this).closest('td, li')).index();
            var row = tblShippingRoute.row(tr.row).data();
            $('#tblPackages').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_detail_packages',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "description"},
                    {data: "tariff.short_name"},
                    {data: "condition.name"},
                    {data: "size.name"},
                    {data: "peso"},
                    {data: "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [-1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return parseFloat(data).toFixed(2) + ' KG';
                        }
                    }
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('#myModalDetails').modal('show');
        })
        .on('click', 'a[rel="shipping_route"]', function () {
            $('.tooltip').remove();
            var tr = tblShippingRoute.cell($(this).closest('td, li')).index();
            var row = tblShippingRoute.row(tr.row).data();
            $('#tblShippingRoute').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_shipping_route',
                        'id': row.id
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
                                    return '<span class="badge badge-primary badge-pill">' + name + '</span>';
                                case "on_route":
                                    return '<span class="badge badge-warning badge-pill">' + name + '</span>';
                                case "delivered":
                                    return '<span class="badge badge-success badge-pill">' + name + '</span>';
                            }
                        }
                    },
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('#myModalShippingRoute').modal('show');
        });

    input_date_range
        .daterangepicker({
                language: 'auto',
                startDate: new Date(),
                locale: {
                    format: 'YYYY-MM-DD',
                },
                autoApply: true,
            }
        )
        .on('apply.daterangepicker', function (ev, picker) {
            shipping_route.list(false);
        });

    $('.drp-buttons').hide();

    shipping_route.list(false);

    $('.btnSearchAll').on('click', function () {
        shipping_route.list(true);
    });
});

