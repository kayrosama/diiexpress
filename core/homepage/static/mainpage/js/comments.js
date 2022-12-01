var pathname = window.location.pathname;

document.addEventListener('DOMContentLoaded', function (e) {
    const fv = FormValidation.formValidation(document.getElementById('frmComments'), {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap5: new FormValidation.plugins.Bootstrap5({
                    rowSelector: '.mb-3',
                }),
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
                        }
                    }
                },
                email: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 5
                        },
                        regexp: {
                            regexp: /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/i,
                            message: 'El email no es correcto'
                        },
                    }
                },
                mobile: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 10
                        },
                        digits: {},
                    }
                },
                comment: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2
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
            parameters.append('action', 'send_comment');
            submit_formdata_with_ajax('Notificación', '¿Estas seguro de enviar el siguiente comentario?', pathname,
                parameters,
                function (request) {
                    alert_sweetalert('success', 'Alerta', 'Gracias por tu comentario, todo esto nos ayuda a mejorar', function () {
                        location.reload();
                    }, 2000, null);
                }
            );
        });
});

$(function () {
    $('input[name="names"]').on('keypress', function (e) {
        return validate_form_text('letters', e, null);
    });

    $('input[name="mobile"]').on('keypress', function (e) {
        return validate_form_text('numbers', e, null);
    });
});
