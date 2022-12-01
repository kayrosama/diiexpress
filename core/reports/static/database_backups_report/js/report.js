var input_daterange;
var current_date;
var select_user;
var tblReport;
var columns = [];
var report = {
    list: function (all) {
        var parameters = {
            'action': 'search_report',
            'user': select_user.val(),
            'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
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
            order: [[0, 'asc']],
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
                {data: "id"},
                {data: "user.username"},
                {data: "date_joined"},
                {data: "hour"},
                {data: "remote_addr"},
                {data: "http_user_agent"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
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
    initTable: function () {
        tblReport = $('#tblReport').DataTable({
            autoWidth: false,
            destroy: true,
        });
        tblReport.settings()[0].aoColumns.forEach(function (value, index, array) {
   columns.push(value.sWidthOrig);
});
    }
};

$(function () {

    select_user = $('select[name="user"]');
    current_date = new moment().format('YYYY-MM-DD');
    input_daterange = $('input[name="date_range"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    select_user
        .on('change', function () {
            report.list(false);
        });

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            },
            autoApply: true,
        })
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