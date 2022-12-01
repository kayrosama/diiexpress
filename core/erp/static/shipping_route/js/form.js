var select_status;
var tblShippingRoute;
var shipping_route = {
    listPackages: function () {
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
    },
    listShippingRoute: function () {
        tblShippingRoute = $('#tblShippingRoute').DataTable({
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
                },
                dataSrc: ""
            },
            columns: [
                {data: "date_joined"},
                {data: "status"},
                {data: "comment"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-3],
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
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if (row.hasOwnProperty('delete')) {
                            return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-times"></i></a>';
                        }
                        return '---';
                    }
                },
            ],
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
                shipping_route.loadStatesInSelect();
            }
        });
    },
    loadStatesInSelect: function () {
        $.ajax({
            url: pathname,
            data: {
                'action': 'load_states_in_select'
            },
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataType: 'json',
            success: function (request) {
                if (!request.hasOwnProperty('error')) {
                    select_status.html('');
                    if (!$.isEmptyObject(request)) {
                        select_status.select2({
                            data: request,
                            theme: 'bootstrap4',
                            language: "es"
                        });
                    }
                    select_status.prop('disabled', $.isEmptyObject(request));
                    return false;
                }
                message_error(request.error);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                message_error(errorThrown + ' ' + textStatus);
            },
            complete: function () {

            }
        });
    }
};

document.addEventListener('DOMContentLoaded', function (e) {
    const fv = FormValidation.formValidation(document.getElementById('frmForm'), {
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
                comment: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                status: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un estado'
                        },
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
            const iconPlugin = fv.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fv.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var parameters = new FormData(fv.form);
            submit_formdata_with_ajax('Notificación', '¿Estas seguro de registrar el siguiente estado de control de ruta de envío?', pathname,
                parameters,
                function (request) {
                    shipping_route.listShippingRoute();
                    $('input[name="comment"]').val('');
                }
            );
        });
});

$(function () {
    select_status = $('select[name="status"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    $('#tblShippingRoute tbody')
        .off()
        .on('click', 'a[rel="remove"]', function () {
            $('.tooltip').remove();
            var tr = tblShippingRoute.cell($(this).closest('td, li')).index();
            var row = tblShippingRoute.row(tr.row).data();
            submit_with_ajax('Alerta', '¿Estas seguro de eliminar el siguiente registro?', pathname, {
                'action': 'remove_status_shipping_route', 'id': row.id,
            }, function () {
                shipping_route.listShippingRoute();
            })
        });

    shipping_route.listPackages();
    shipping_route.listShippingRoute();
});