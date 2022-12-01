var tblSale;
var input_date_range;
var container_tab;
var sale = {
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
        tblSale = $('#data').DataTable({
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
                {data: "employee_date_attention"},
                {data: "type.name"},
                {data: "subtotal"},
                {data: "iva"},
                {data: "total"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.type.id === 'housekeeping') {
                            return '<span class="badge badge-warning badge-pill">' + row.type.name + '</span>';
                        }
                        return '<span class="badge badge-success badge-pill">' + row.type.name + '</span>';
                    }
                },
                {
                    targets: [-2, -3, -4],
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
                        buttons += '<a class="btn btn-info btn-xs btn-flat" rel="detail"><i class="fas fa-folder-open"></i></a> ';
                        buttons += '<a href="' + pathname + 'print/invoice/' + row.id + '/" target="_blank" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-print"></i></a> ';
                        buttons += '<a href="' + pathname + 'delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a> ';
                        return buttons;
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
                var total = json.reduce((a, b) => a + (parseFloat(b.total) || 0), 0);
                $('.total').html('$' + total.toFixed(2));
            }
        });
    },
    setVisibleTab: function (parameters) {
        parameters.forEach(function (item) {
            var nav = $(container_tab[item.index]);
            var content = $('.tab-content');
            var href = nav.attr('href');
            nav.removeClass('active');
            content.find(href).removeClass('active');
            if (item.visible) {
                nav.closest('li').show();
                if (item.hasOwnProperty('active')) {
                    nav.tab('show');
                }
            } else {
                nav.closest('li').hide();
            }
        });
    },
}

$(function () {

    container_tab = $('.nav-tabs a');
    input_date_range = $('input[name="date_range"]');

    $('#data tbody')
        .off()
        .on('click', 'a[rel="detail"]', function () {
            $('.tooltip').remove();
            var tr = tblSale.cell($(this).closest('td, li')).index();
            var row = tblSale.row(tr.row).data();
            if (row.type.id === 'housekeeping') {
                $('#tblProducts').DataTable({
                    autoWidth: false,
                    destroy: true,
                    ajax: {
                        url: pathname,
                        type: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                        data: {
                            'action': 'search_detail_products',
                            'id': row.id
                        },
                        dataSrc: ""
                    },
                    columns: [
                        {data: "product.full_name"},
                        {data: "price"},
                        {data: "cant"},
                        {data: "subtotal"},
                    ],
                    columnDefs: [
                        {
                            targets: [-1, -3],
                            class: 'text-center',
                            render: function (data, type, row) {
                                return '$' + parseFloat(data).toFixed(2);
                            }
                        },
                        {
                            targets: [-2],
                            class: 'text-center',
                            render: function (data, type, row) {
                                return data;
                            }
                        }
                    ],
                    initComplete: function (settings, json) {
                        $(this).wrap('<div class="dataTables_scroll"><div/>');
                    }
                });
                $('#tblServices').DataTable({
                    autoWidth: false,
                    destroy: true,
                    ajax: {
                        url: pathname,
                        type: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                        data: {
                            'action': 'search_detail_services',
                            'id': row.id
                        },
                        dataSrc: ""
                    },
                    columns: [
                        {data: "product.full_name"},
                        {data: "product.type.name"},
                        {data: "price"},
                        {data: "cant"},
                        {data: "subtotal"},
                    ],
                    columnDefs: [
                        {
                            targets: [-1, -3],
                            class: 'text-center',
                            render: function (data, type, row) {
                                return '$' + parseFloat(data).toFixed(2);
                            }
                        },
                        {
                            targets: [-2],
                            class: 'text-center',
                            render: function (data, type, row) {
                                return data;
                            }
                        }
                    ],
                    initComplete: function (settings, json) {
                        $(this).wrap('<div class="dataTables_scroll"><div/>');
                    }
                });
                sale.setVisibleTab([{'index': 0, 'visible': true, 'active': true}, {'index': 1, 'visible': true}, {'index': 2, 'visible': false}]);
            } else {
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
                sale.setVisibleTab([{'index': 0, 'visible': false}, {'index': 1, 'visible': false}, {'index': 2, 'visible': true, 'active': true}]);
            }
            $('#myModalDetails').modal('show');
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
            sale.list(false);
        });

    $('.drp-buttons').hide();

    sale.list(false);

    $('.btnSearchAll').on('click', function () {
        sale.list(true);
    });
});

