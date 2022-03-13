# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from tabulate import tabulate
from typing import List, Dict

def list2html(title:str, tablo_veri:List[Dict], header:str='', aciklama:str='', footer:str='', pdf_sayfa:str="A4") -> str:
    tablo_html = tabulate(tablo_veri, headers='keys', tablefmt='html')

    css = """<style>
        th, td {
            text-align: center !important;
        }
    </style>"""

    javascript = """<script>
            $("table").addClass("table table-bordered table-sm table-hover table-striped");
            $("thead").addClass("thead-dark");
            $(document).ready(function() {
                $("table").DataTable({
                    dom: 'Bfrtip',
                    paging: false,
                    language: {
                        "emptyTable": "Tabloda veri yok",
                        "lengthMenu": "Sayfa başına _MENU_ kaydı görüntüle",
                        "zeroRecords": "Hiçbir eşleşen kayıt bulunamadı",
                        // "info": "_TOTAL_ girişten _START_ - _END_ arası gösteriliyor",
                        "info": "_TOTAL_ Kayıt Mevcut",
                        "infoEmpty": "Kayıt yok",
                        "infoFiltered": "(_MAX_ toplam kayıttan filtrelenmiştir)",
                        "search": "Ara:",
                        "paginate": {
                            "first":      "İlk",
                            "last":       "Son",
                            "next":       "İleri",
                            "previous":   "Geri"
                        },
                    },
                    columnDefs: [
                        {"className": "dt-center", "targets": "_all"}
                    ],
                    buttons: [
                        'csv',
                        {
                            extend: 'excelHtml5',
                            autoFilter: true
                        },
                        {
                            extend:'pdfHtml5',
                            download:'open',
                            orientation:'landscape',
                            pageSize:'A4',
                            customize: function(doc) {
                                doc.content[1].margin = [ 100, 0, 100, 0 ], // left, top, right, bottom
                                doc.defaultStyle.fontSize = 11
                            }
                        }
                    ]
                });
                $(":button").removeClass("dt-button");
                $(":button").addClass("btn btn-secondary")
            });
        </script>""".replace("pageSize:'A4'", f"pageSize:'{pdf_sayfa}'")

    return f"""<!doctype html>
<html lang="tr">
<head>
    <!-- Gerekli meta tagler -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">

    <!-- Bootstrap CSS - Font Awesome -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@forevolve/bootstrap-dark@2.1.0/dist/css/bootstrap-dark.min.css" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css">

    <!-- DataTables -->
    <link href="https://cdn.datatables.net/1.11.5/css/dataTables.bootstrap4.min.css" rel="stylesheet"/>
    <link href="https://cdn.datatables.net/buttons/2.2.2/css/buttons.dataTables.min.css" rel="stylesheet"/>

    <!-- CSS -->
    {css}

    <!-- Ajax -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>

    <title>{title}</title>
</head>
<body class="d-flex align-items-center min-vh-100">
    <div class="container">
        <div class="card">
            <div class="card-header">
                <i class="fa fa-info" aria-hidden="true"></i> | {header or title}
            </div>
            <div class="card-body">
                <h3 class="d-flex justify-content-around">{aciklama or title}</h3>
                <hr>
                <div class="table-responsive-sm">

{tablo_html}

                </div>
            </div>
            <div class="card-footer text-muted">
                <i class="fa fa-bed" aria-hidden="true"></i> | {footer or title}
            </div>
        </div>
    </div>

        <!-- jQuery ve Bootstrap Bundle (Popper içerir) -->
        <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js"></script>
        <!-- <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script> -->
        <script src="https://cdn.jsdelivr.net/npm/@forevolve/bootstrap-dark@2.1.0/dist/js/bootstrap.bundle.min.js"></script>

        <!-- DataTables -->
        <script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
        <script src="https://cdn.datatables.net/1.11.5/js/dataTables.bootstrap4.min.js"></script>
        <script src="https://cdn.datatables.net/buttons/2.2.2/js/dataTables.buttons.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.1.3/jszip.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/pdfmake.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/vfs_fonts.js"></script>
        <script src="https://cdn.datatables.net/buttons/2.2.2/js/buttons.html5.min.js"></script>
        <script src="https://cdn.datatables.net/buttons/2.2.2/js/buttons.print.min.js"></script>

        <!-- Tablo Düzenle -->
        {javascript}
</body>
</html>"""
