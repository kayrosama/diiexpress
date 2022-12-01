var product = {
    list: function () {
        var parameters = {
            'action': 'search',
        };
        $('#data').DataTable({
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
            columns: [
                {data: "id"},
                {data: "name"},
                {data: "code"},
                {data: "category.name"},
                {data: "type"},
                {data: "image"},
                {data: "price"},
                {data: "pvp"},
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-6],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var name = row.type.name;
                        switch (row.type.id) {
                            case "product":
                                return '<span class="badge badge-primary badge-pill">' + name + '</span>';
                            case "service_day":
                                return '<span class="badge badge-success badge-pill">' + name + '</span>';
                            case "service_hour":
                                return '<span class="badge badge-info badge-pill">' + name + '</span>';
                        }
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<img alt="" src="' + row.image + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                    }
                },
                {
                    targets: [-3, -4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.type.id === 'product') {
                            if (row.stock > 0) {
                                return '<span class="badge badge-success badge-pill">' + row.stock + '</span>';
                            }
                            return '<span class="badge badge-danger badge-pill">' + row.stock + '</span>';
                        }
                        return '<span class="badge badge-secondary badge-pill">Sin stock</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '';
                        buttons += '<a href="/erp/product/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/erp/product/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a> ';
                        return buttons;
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                if (data.type.id === 'product') {
                    if (data.stock === 0) {
                        $(tr).css({'background': '#e74c3c', 'color': 'white'});
                    } else if (data.stock >= 1 && data.stock <= 4) {
                        $(tr).css({'background': '#ec9b07', 'color': 'white'});
                    }
                }
            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};

$(function () {
    product.list();

    $('#data').addClass('table-sm');
})