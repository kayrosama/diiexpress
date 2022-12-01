var fv;
var select_employee, select_event_type;
var input_datejoined;

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
                employee: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un empleado'
                        },
                    }
                },
                details: {
                    validators: {}
                },
                event_type: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un tipo de evento'
                        },
                    }
                },
                date_joined: {
                    validators: {
                        notEmpty: {},
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    employee: fv.form.querySelector('[name="employee"]').value,
                                    event_type: fv.form.querySelector('[name="event_type"]').value,
                                    start_date: input_datejoined.data('daterangepicker').startDate.format('YYYY-MM-DD'),
                                    end_date: input_datejoined.data('daterangepicker').endDate.format('YYYY-MM-DD'),
                                    start_time: input_datejoined.data('daterangepicker').startDate.format('HH:mm'),
                                    end_time: input_datejoined.data('daterangepicker').endDate.format('HH:mm'),
                                    action: 'validate_data'
                                };
                            },
                            message: 'El empleado, evento y fecha ya esta registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                valor: {
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
            parameters.append('start_date', input_datejoined.data('daterangepicker').startDate.format('YYYY-MM-DD'));
            parameters.append('end_date', input_datejoined.data('daterangepicker').endDate.format('YYYY-MM-DD'));
            parameters.append('start_time', input_datejoined.data('daterangepicker').startDate.format('HH:mm'));
            parameters.append('end_time', input_datejoined.data('daterangepicker').endDate.format('HH:mm'));
            submit_formdata_with_ajax('Alerta', '¿Estas seguro de realizar la siguiente acción?', pathname, parameters, function () {
                location.href = fv.form.getAttribute('data-url');
            });
        });
});

$(function () {

    select_employee = $('select[name="employee"]');
    select_event_type = $('select[name="event_type"]');
    input_datejoined = $('input[name="date_joined"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    select_employee.on('change', function () {
        fv.revalidateField('employee');
        fv.revalidateField('date_joined');
    });

    select_event_type.on('change', function () {
        fv.revalidateField('event_type');
        fv.revalidateField('date_joined');
    });

    input_datejoined
        .daterangepicker({
            language: 'auto',
            //startDate: new Date(),
            timePicker: true,
            timePicker24Hour: true,
            timePickerIncrement: 1,
            locale: {
                format: 'YYYY-MM-DD HH:mm',
            }
        })
        .on('apply.daterangepicker', function (ev, picker) {
            fv.revalidateField('date_joined');
        });

    $('.drp-buttons').hide();
});
