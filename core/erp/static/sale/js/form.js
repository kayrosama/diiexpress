var input_datejoined, input_search_products, input_search_services, input_date_attention, input_peso;
var tblProducts, tblSearchProducts, tblServices, tblSearchServices, tblPackages;
var select_client, select_type, select_tariff, select_employee;
var fvSale, fvPackage;
var container_tab;

document.addEventListener('DOMContentLoaded', function (e) {
    fvSale = FormValidation.formValidation(document.getElementById('frmSale'), {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                excluded: new FormValidation.plugins.Excluded(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                client: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un cliente'
                        },
                    }
                },
                employee: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un empleado'
                        },
                    }
                },
                type: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un tipo de venta'
                        },
                    }
                },
                date_joined: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    }
                },
                date_attention: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha de atención es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD HH:MM',
                            message: 'La fecha de atención no es válida'
                        }
                    }
                },
            },
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fvSale.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fvSale.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var parameters = new FormData(fvSale.form);
            if (parameters.get('type') === 'housekeeping') {
                if ($.isEmptyObject(sale.details.products) && $.isEmptyObject(sale.details.services)) {
                    message_error('Debe tener al menos un item en el detalle');
                    return false;
                }
            } else {
                if ($.isEmptyObject(sale.details.packages)) {
                    message_error('Debe tener al menos un item en el detalle');
                    return false;
                }
            }
            parameters.append('details', JSON.stringify(sale.details));
            submit_formdata_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                parameters,
                function () {
                    location.href = fvSale.form.getAttribute('data-url');
                },
            );
        });
});

document.addEventListener('DOMContentLoaded', function (e) {
    fvPackage = FormValidation.formValidation(document.getElementById('frmPackage'), {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                description: {
                    validators: {
                        notEmpty: {},
                    }
                },
                condition: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una condición'
                        },
                    }
                },
                size: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un tamaño'
                        },
                    }
                },
                tariff: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una tarifa'
                        },
                    }
                },
                peso: {
                    validators: {
                        notEmpty: {},
                        numeric: {
                            message: 'El valor no es un número',
                            thousandsSeparator: '',
                            decimalSeparator: '.'
                        }
                    }
                },
                amount: {
                    validators: {
                        notEmpty: {},
                        numeric: {
                            message: 'El valor no es un número',
                            thousandsSeparator: '',
                            decimalSeparator: '.'
                        }
                    }
                },
            },
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fvPackage.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fvPackage.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var parameters = {};
            $(fvPackage.form).serializeArray().forEach(function (item, index, array) {
                parameters[item.name] = item.value;
            });
            parameters['tariff'] = select_tariff.select2('data')[0].data;
            parameters['condition'] = {'id': $('select[name="condition"]').val(), 'name': $("#id_condition option:selected").text()};
            parameters['size'] = {'id': $('select[name="size"]').val(), 'name': $("#id_size option:selected").text()};
            sale.addPackage(parameters);
            $('#myModalPackage').modal('hide');
        });
});

var sale = {
    details: {
        subtotal: 0.00,
        total_iva: 0.00,
        iva: 0.00,
        total: 0.00,
        products: [],
        services: [],
        packages: [],
    },
    calculateInvoice: function () {
        var subtotal = 0.00;
        if (select_type.val() === 'housekeeping') {
            this.details.products.forEach(function (value, index, array) {
                value.cant = parseInt(value.cant);
                value.subtotal = value.cant * parseFloat(value.pvp);
                subtotal += value.subtotal;
            });
            this.details.services.forEach(function (value, index, array) {
                value.cant = parseInt(value.cant);
                value.subtotal = value.cant * parseFloat(value.pvp);
                subtotal += value.subtotal;
            });
        } else {
            this.details.packages.forEach(function (value, index, array) {
                value.amount = parseFloat(value.amount);
                subtotal += value.amount;
            });
        }
        sale.details.subtotal = subtotal;
        sale.details.total_iva = sale.details.subtotal * (sale.details.iva / 100);
        sale.details.total = sale.details.subtotal + sale.details.total_iva;
        sale.details.total = parseFloat(sale.details.total.toFixed(2));

        $('input[name="subtotal"]').val(sale.details.subtotal.toFixed(2));
        $('input[name="iva"]').val(sale.details.iva.toFixed(2));
        $('input[name="total_iva"]').val(sale.details.total_iva.toFixed(2));
        $('input[name="total"]').val(sale.details.total.toFixed(2));
    },
    listProducts: function () {
        this.calculateInvoice();
        tblProducts = $('#tblProducts').DataTable({
            autoWidth: false,
            destroy: true,
            data: this.details.products,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                {data: "id"},
                {data: "code"},
                {data: "short_name"},
                {data: "stock"},
                {data: "cant"},
                {data: "pvp"},
                {data: "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary badge-pill">' + row.stock + '</span>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control" autocomplete="off" name="cant" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1, -2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fas fa-times"></i></a>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                tr.find('input[name="cant"]')
                    .TouchSpin({
                        min: 1,
                        max: data.stock,
                        verticalbuttons: true
                    })
                    .on('keypress', function (e) {
                        return validate_form_text('numbers', e, null);
                    });
            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
    getProductsIds: function () {
        return this.details.products.map(value => value.id);
    },
    addProduct: function (item) {
        this.details.products.push(item);
        this.listProducts();
    },
    listServices: function () {
        this.calculateInvoice();
        tblServices = $('#tblServices').DataTable({
            autoWidth: false,
            destroy: true,
            data: this.details.services,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                {data: "id"},
                {data: "code"},
                {data: "full_name"},
                {data: "type.name"},
                {data: "cant"},
                {data: "pvp"},
                {data: "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control" autocomplete="off" name="cant" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1, -2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fas fa-times"></i></a>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                tr.find('input[name="cant"]')
                    .TouchSpin({
                        min: 1,
                        max: 100000,
                        verticalbuttons: true
                    })
                    .on('keypress', function (e) {
                        return validate_form_text('numbers', e, null);
                    });
            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
    addService: function (item) {
        this.details.services.push(item);
        this.listServices();
    },
    getServicesIds: function () {
        return this.details.services.map(value => value.id);
    },
    listPackages: function () {
        this.calculateInvoice();
        tblPackages = $('#tblPackages').DataTable({
            autoWidth: false,
            destroy: true,
            data: this.details.packages,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                {data: "id"},
                {data: "description"},
                {data: "tariff.full_name"},
                {data: "condition.name"},
                {data: "size.name"},
                {data: "peso"},
                {data: "amount"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2) + ' KG';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '<a rel="edit" class="btn btn-warning btn-flat btn-xs"><i class="fa fa-edit fa-1x"></i></a> ';
                        buttons += '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fa fa-times fa-1x"></i></a>';
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
    addPackage: function (item) {
        var id = parseInt(fvPackage.form.getAttribute('data-id'));
        if (id > -1) {
            this.details.packages[id] = item;
        } else {
            this.details.packages.push(item);
        }
        this.listPackages();
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
};

$(function () {
    input_date_attention = $('input[name="date_attention"]');
    input_datejoined = $('input[name="date_joined"]');
    select_employee = $('select[name="employee"]');
    select_client = $('select[name="client"]');
    select_type = $('select[name="type"]');
    select_tariff = $('select[name="tariff"]');
    input_search_products = $('input[name="input_search_products"]');
    input_search_services = $('input[name="input_search_services"]');
    input_peso = $('input[name="peso"]');
    container_tab = $('.nav-tabs a');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    /* Form */

    select_client.on('change', function () {
        fvSale.revalidateField('client');
    });

    select_type.on('change', function () {
        fvSale.revalidateField('type');
        var content_employee = $('.content-employee');
        content_employee.hide();
        var id = $(this).val();
        if (id === 'housekeeping') {
            content_employee.show();
            sale.setVisibleTab([{'index': 0, 'visible': true, 'active': true}, {'index': 1, 'visible': true}, {'index': 2, 'visible': false}]);
        } else {
            sale.setVisibleTab([{'index': 0, 'visible': false}, {'index': 1, 'visible': false}, {'index': 2, 'visible': true, 'active': true}]);
        }
        sale.calculateInvoice();
    });

    input_datejoined.datetimepicker({
        format: 'YYYY-MM-DD',
        useCurrent: false,
        locale: 'es',
        orientation: 'bottom',
        keepOpen: false
    });

    input_date_attention.datetimepicker({
        format: 'YYYY-MM-DD HH:mm',
        useCurrent: false,
        locale: 'es',
        orientation: 'bottom',
        keepOpen: false,
        icons: {
            time: "far fa-clock",
            date: "fas fa-calendar-alt",
        }
    });

    input_date_attention
        .on('change.datetimepicker', function (e) {
            fvSale.revalidateField('date_attention');
        });

    input_datejoined.on('change.datetimepicker', function (e) {
        fvSale.revalidateField('date_joined');
        input_date_attention.datetimepicker('minDate', e.date);
        input_date_attention.datetimepicker('date', e.date);
    });

    select_employee.on('change', function () {
        fvSale.revalidateField('employee');
    });

    /* Products */

    input_search_products.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_products',
                    'term': request.term,
                    'ids': JSON.stringify(sale.getProductsIds()),
                },
                dataType: "json",
                type: "POST",
                headers: {
                    'X-CSRFToken': csrftoken
                },
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).blur();
            ui.item.cant = 1;
            sale.addProduct(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearProducts').on('click', function () {
        input_search_products.val('').focus();
    });

    $('#tblProducts tbody')
        .off()
        .on('change', 'input[name="cant"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            sale.details.products[tr.row].cant = parseInt($(this).val());
            sale.calculateInvoice();
            $('td:last', tblProducts.row(tr.row).node()).html('$' + sale.details.products[tr.row].subtotal.toFixed(2));
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            sale.details.products.splice(tr.row, 1);
            tblProducts.row(tr.row).remove().draw();
            sale.calculateInvoice();
        });

    $('.btnSearchProducts').on('click', function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_products',
                    'term': input_search_products.val(),
                    'ids': JSON.stringify(sale.getProductsIds()),
                },
                dataSrc: ""
            },
            columns: [
                {data: "code"},
                {data: "full_name"},
                {data: "pvp"},
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary badge-pill">' + row.stock + '</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="add" class="btn btn-success btn-flat btn-xs"><i class="fas fa-plus"></i></a>';
                    }
                }
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
        $('#myModalSearchProducts').modal('show');
    });

    $('#tblSearchProducts tbody')
        .off()
        .on('click', 'a[rel="add"]', function () {
            var row = tblSearchProducts.row($(this).parents('tr')).data();
            row.cant = 1;
            sale.addProduct(row);
            tblSearchProducts.row($(this).parents('tr')).remove().draw();
        });

    $('.btnRemoveAllProducts').on('click', function () {
        if (sale.details.products.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            sale.details.products = [];
            sale.listProducts();
        });
    });

    /* Services */

    input_search_services.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_services',
                    'term': request.term,
                    'ids': JSON.stringify(sale.getServicesIds()),
                },
                dataType: "json",
                type: "POST",
                headers: {
                    'X-CSRFToken': csrftoken
                },
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).blur();
            ui.item.cant = 1;
            sale.addService(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearServices').on('click', function () {
        input_search_services.val('').focus();
    });

    $('#tblServices tbody')
        .off()
        .on('change', 'input[name="cant"]', function () {
            var tr = tblServices.cell($(this).closest('td, li')).index();
            sale.details.services[tr.row].cant = parseInt($(this).val());
            sale.calculateInvoice();
            $('td:last', tblServices.row(tr.row).node()).html('$' + sale.details.services[tr.row].subtotal.toFixed(2));
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblServices.cell($(this).closest('td, li')).index();
            sale.details.services.splice(tr.row, 1);
            tblServices.row(tr.row).remove().draw();
            sale.calculateInvoice();
        });

    $('.btnSearchServices').on('click', function () {
        tblSearchServices = $('#tblSearchServices').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_services',
                    'term': input_search_services.val(),
                    'ids': JSON.stringify(sale.getServicesIds()),
                },
                dataSrc: ""
            },
            columns: [
                {data: "code"},
                {data: "full_name"},
                {data: "type.name"},
                {data: "pvp"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="add" class="btn btn-success btn-flat btn-xs"><i class="fas fa-plus"></i></a>';
                    }
                }
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
        $('#myModalSearchServices').modal('show');
    });

    $('#tblSearchServices tbody')
        .off()
        .on('click', 'a[rel="add"]', function () {
            var row = tblSearchServices.row($(this).parents('tr')).data();
            row.cant = 1;
            sale.addService(row);
            tblSearchServices.row($(this).parents('tr')).remove().draw();
        });

    $('.btnRemoveAllServices').on('click', function () {
        if (sale.details.services.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            sale.details.services = [];
            sale.listServices();
        });
    });

    /* Packages */

    $('select[name="condition"]').on('change', function () {
        fvPackage.revalidateField('condition');
    });

    $('select[name="size"]').on('change', function () {
        fvPackage.revalidateField('size');
    });

    select_tariff.select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            url: pathname,
            data: function (params) {
                return {
                    term: params.term,
                    peso: $('input[name="peso"]').val(),
                    action: 'search_tariff'
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese un ciudad para buscar la tarifa',
        minimumInputLength: 1,
    })
        .on('select2:select', function (e) {
            $('input[name="amount"]').val(e.params.data.price);
            input_peso.trigger("touchspin.updatesettings", {
                min: parseFloat(e.params.data.minimum_weight),
                max: parseFloat(e.params.data.maximum_weight),
            });
            input_peso.prop('disabled', false);
            fvPackage.revalidateField('tariff');
        })
        .on('select2:clear', function (e) {
            $('input[name="amount"]').val('');
            input_peso.val('0.00').prop('disabled', true);
            fvPackage.revalidateField('tariff');
        });

    input_peso
        .TouchSpin({
            min: 0.00,
            max: 1000000,
            step: 0.01,
            decimals: 2,
            boostat: 5,
            verticalbuttons: true,
            maxboostedstep: 10,
            prefix: 'KG'
        })
        .on('change touchspin.on.min touchspin.on.max', function () {
            fvPackage.revalidateField('peso');
        })
        .on('keypress', function (e) {
            return validate_decimals($(this), e);
        });

    $('.btnAddPackage').on('click', function () {
        fvPackage.resetForm(true);
        $('input[name="peso"]').val('0.00');
        $('input[name="amount"]').val('0.00');
        $(fvPackage.form).attr('data-id', '-1');
        $('#myModalPackage .modal-title').html('<i class="fa fa-plus"></i> Nuevo registro de un paquete');
        $('#myModalPackage').modal('show');
    });

    $('#myModalPackage').on('hidden.bs.modal', function () {
        $(fvPackage.form).find('select').val('').trigger('change');
        fvPackage.resetForm(true);
    });

    $('#tblPackages tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblPackages.cell($(this).closest('td, li')).index();
            sale.details.packages.splice(tr.row, 1);
            tblPackages.row(tr.row).remove().draw();
            $('.tooltip').remove();
        })
        .on('click', 'a[rel="edit"]', function () {
            var tr = tblPackages.cell($(this).closest('td, li')).index();
            var row = tblPackages.row(tr.row).data();
            $(fvPackage.form).attr('data-id', tr.row);
            $(fvPackage.form).find('input[name="description"]').val(row.description);
            $(fvPackage.form).find('input[name="peso"]').val(row.peso);
            $(fvPackage.form).find('input[name="amount"]').val(row.subtotal);
            select_tariff.val(row.tariff.id).trigger('change');
            $('select[name="condition"]').val(row.condition.id).trigger('change');
            $('select[name="size"]').val(row.size.id).trigger('change');
            $('#myModalPackage .modal-title').html('<b><i class="fas fa-edit"></i> Edición de un paquete</b>');
            $('#myModalPackage').modal('show');
        });

    $('input[name="amount"]')
        .TouchSpin({
            min: 0.00,
            max: 1000000,
            step: 0.01,
            decimals: 2,
            boostat: 5,
            verticalbuttons: true,
            maxboostedstep: 10,
            prefix: '$'
        })
        .on('change touchspin.on.min touchspin.on.max', function () {
            fvPackage.revalidateField('subtotal');
        })
        .on('keypress', function (e) {
            return validate_decimals($(this), e);
        });

    $('.btnRemovePackages').on('click', function () {
        if (sale.details.packages.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            sale.details.packages = [];
            sale.listPackages();
        });
    });

    select_type.trigger('change');
});