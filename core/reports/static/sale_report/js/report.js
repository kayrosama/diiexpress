var input_date_range;
var select_type_sale;
var current_date;
var tblReport;
var columns = [];
var report = {
    initTable: function () {
        tblReport = $('#tblReport').DataTable({
            autoWidth: false,
            destroy: true,
        });
        tblReport.settings()[0].aoColumns.forEach(function (value, index, array) {
            columns.push(value.sWidthOrig);
        });
    },
    list: function (all) {
        var parameters = {
            'action': 'search_report',
            'type': select_type_sale.val(),
            'start_date': input_date_range.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_date_range.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }
        tblReport = $('#tblReport').DataTable({
            destroy: true,
            autoWidth: false,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: parameters,
                dataSrc: ''
            },
            order: [[0, 'desc']],
            paging: false,
            ordering: true,
            searching: false,
            dom: 'Bfrtip',
            buttons: [
                {
                    extend: 'excelHtml5',
                    text: ' <i class="fas fa-file-excel"></i> Descargar Excel',
                    titleAttr: 'Excel',
                    className: 'btn btn-success btn-flat btn-sm'
                },
                {
                    extend: 'pdfHtml5',
                    text: '<i class="fas fa-file-pdf"></i> Descargar Pdf',
                    titleAttr: 'PDF',
                    className: 'btn btn-danger btn-flat btn-sm',
                    title: '',
                    orientation: 'landscape',
                    pageSize: 'LEGAL',
                    download: 'open',
                    customize: function (doc) {
                        doc.styles = {
                            header: {
                                fontSize: 18,
                                bold: true,
                                alignment: 'center'
                            },
                            subheader: {
                                fontSize: 18,
                                bold: true
                            },
                            quote: {
                                italics: true
                            },
                            small: {
                                fontSize: 15
                            },
                            tableHeader: {
                                bold: true,
                                fontSize: 13,
                                color: 'white',
                                fillColor: '#0d46d4',
                                alignment: 'center'
                            }
                        };
                        doc.content.splice(0, 0, {
                            margin: [0, 0, 0, 12],
                            fit: [75, 75],
                            alignment: 'center',
                            image: company.image_in_base64
                        });
                        doc.content.splice(1, 0, {
                            text: company.name,
                            style: 'header',
                        });
                        doc.content.splice(2, 0, {
                            alignment: 'center',
                            text: '' + current_date,
                            style: 'subheader'
                        });
                        doc.content.splice(3, 0, {
                            alignment: 'center',
                            text: title,
                            style: 'subheader'
                        });
                        doc.content[4].table.widths = columns;
                        doc.content[4].margin = [0, 35, 0, 0];
                        doc.content[4].layout = {};
                        doc.defaultStyle.fontSize = 13;
                        doc['footer'] = (function (page, pages) {
                            return {
                                columns: [
                                    {
                                        alignment: 'left',
                                        text: ['Fecha de creación: ', {text: current_date.toString()}]
                                    },
                                    {
                                        alignment: 'right',
                                        text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                    }
                                ],
                                margin: 20
                            }
                        });
                    }
                }
            ],
            columns: [
                {data: "number"},
                {data: "date_joined"},
                {data: "client.names"},
                {data: "type.name"},
                {data: "employee_date_attention"},
                {data: "subtotal"},
                {data: "total_iva"},
                {data: "total"},
            ],
            columnDefs: [
                {
                    targets: [-5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [-1, -2, -3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if(data === '---'){
                            return '---';
                        }
                        return '$' + parseFloat(data).toFixed(2);
                    }
                }
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};

$(function () {

    current_date = new moment().format('YYYY-MM-DD');
    select_type_sale = $('select[name="type_sale"]');
    input_date_range = $('input[name="date_range"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    select_type_sale
        .on('change', function () {
            report.list(false);
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
            report.list(false);
        });

    $('.drp-buttons').hide();

    report.initTable();

    report.list(false);

    $('.btnSearchAll').on('click', function () {
        report.list(true);
    });
});