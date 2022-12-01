var fv;
var tblSocialNetworks;
var team = {
    items: [],
    listSocialNetworks: function () {
        tblSocialNetworks = $('#tblSocialNetworks').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: true,
            data: this.items,
            columns: [
                {data: "url"},
                {data: "icon"},
                {data: "url"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" name="icon" class="form-control" placeholder="Ingrese un icono" maxlength="50" value="' + row.icon + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" name="url" class="form-control" placeholder="Ingrese un enlace web" maxlength="50" value="' + row.url + '">';
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a class="btn btn-danger btn-xs btn-flat" rel="remove"><i class="fas fa-times"></i></a>';
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
    addSocialNetworks: function (item) {
        this.items.push(item);
        this.listSocialNetworks();
    }
};

document.addEventListener('DOMContentLoaded', function (e) {
    fv = FormValidation.formValidation(document.getElementById('frmForm'), {
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
                names: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                profession: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                description: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                image: {
                    notEmpty: {},
                    validators: {
                        file: {
                            extension: 'jpeg,jpg,png',
                            type: 'image/jpeg,image/png',
                            maxFiles: 1,
                            message: 'Introduce una imagen válida'
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
            if (team.items.length === 0) {
                message_error('Debe tener al menos un item en el detalle');
                return false;
            }
            var parameters = new FormData(fv.form);
            parameters.append('items', JSON.stringify(team.items));
            submit_formdata_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                parameters,
                function () {
                    location.href = fv.form.getAttribute('data-url');
                },
            );
        });
});

$(function () {
    $('.btnAddSocialNetworks').on('click', function () {
        team.addSocialNetworks({'url': '', 'icon': ''})
    });

    $('.btnRemoveSocialNetworks').on('click', function () {
        if (team.items.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            team.items = [];
            team.listSocialNetworks();
        }, function () {

        });
    });

    $('#tblSocialNetworks tbody')
        .off()
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblSocialNetworks.cell($(this).closest('td, li')).index();
            team.items.splice(tr.row, 1);
            tblSocialNetworks.row(tr.row).remove().draw();
        })
        .on('keyup', 'input[name="url"]', function () {
            var tr = tblSocialNetworks.cell($(this).closest('td, li')).index();
            team.items[tr.row].url = $(this).val();
        })
        .on('keyup', 'input[name="icon"]', function () {
            var tr = tblSocialNetworks.cell($(this).closest('td, li')).index();
            team.items[tr.row].icon = $(this).val();
        });
});
