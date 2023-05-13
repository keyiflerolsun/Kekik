# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from tabulate import tabulate
from typing   import List, Dict

def list2html(title:str, tablo_veri:List[Dict], header:str="", aciklama:str="", footer:str="", pdf_sayfa:str="A4", sayfalama:bool=True) -> str:
    tablo_html = tabulate(tablo_veri, headers="keys", tablefmt="html")

    css = """<style>
        th, td {
            text-align: center !important;
        }
    </style>"""

    javascript = """<script>
            $("table").addClass("table table-dark table-sm table-bordered table-hover table-striped");
            $("thead").addClass("table-secondary");
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
                        "infoFiltered": "(Toplam _MAX_ kayıttan filtrelenmiştir)",
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
        </script>""".replace("pageSize:'A4'", f"pageSize:'{pdf_sayfa}'").replace("paging: false", f"paging: {str(sayfalama).lower()}")

    return f"""<!doctype html>
<html lang="tr" data-bs-theme="dark">

<head>
    <!-- ? Meta -->
    <meta charset="UTF-8">
    <meta http-equiv="Content-Language" content="tr">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>{title}</title>
    <meta name="keywords"    content="keyiflerolsun, Ömer Faruk Sancak, KekikAkademi, Kekik Akademi">
    <meta name="author"      content="keyiflerolsun">

    <!-- ? Bootstrap CSS - Font Awesome -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">

    <!-- ? DataTables -->
    <link href="https://cdn.datatables.net/1.13.4/css/dataTables.bootstrap5.min.css" rel="stylesheet"/>
    <link href="https://cdn.datatables.net/buttons/2.3.6/css/buttons.bootstrap5.min.css" rel="stylesheet"/>

    <!-- ? Statik CSS -->
    {css}
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

        <!-- ? jQuery ve Bootstrap Bundle (Popper içerir) -->
        <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.4/dist/jquery.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>

        <!-- ? DataTables -->
        <script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
        <script src="https://cdn.datatables.net/1.13.4/js/dataTables.bootstrap5.min.js"></script>
        <script src="https://cdn.datatables.net/buttons/2.3.6/js/dataTables.buttons.min.js"></script>
        <script src="https://cdn.datatables.net/buttons/2.3.6/js/buttons.html5.min.js"></script>
        <script src="https://cdn.datatables.net/buttons/2.3.6/js/buttons.print.min.js"></script>
        <script src="https://cdn.datatables.net/buttons/2.3.6/js/buttons.bootstrap5.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/pdfmake.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/vfs_fonts.js"></script>

        <!-- Tablo Düzenle -->
        {javascript}


<!-- ! Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.
* ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⠀⠀⡀⠀⠀⠀
* ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣷⣤⣾⡇⠀⠀⠀
* ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣈⡛⣿⡟⠁⢀⣀⠀
* ⠀⠀⠀⢰⡄⠀⠀⠀⠀⠀⢸⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⠿⠾⣷⣾⠿⠃⠀
* ⠀⠀⠀⠈⣿⣦⡀⠀⠀⠀⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀
* ⠀⠀⠀⠀⣿⣿⣿⣦⡀⠀⣿⣿⣿⣧⡀⠀⠀⠀⠀⢀⣤⣤⣤⣀⡀⠛⠀⠀⠀⠀
* ⠀⠀⠀⠀⠘⣿⣿⣿⣿⣶⣄⠙⠻⠿⣷⡀⠀⠀⢀⣿⣿⣿⣿⣿⡿⠶⠀⠀⠀⠀
* ⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣶⣦⣤⣤⣤⣤⣾⣿⣿⡏⠉⠀⣤⠄⠀⠀⠀⠀
* ⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠉⠀⠀⠀⠀⠀
* ⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀
* ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
* ⠀⣼⣷⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
* ⠀⢻⣿⣿⣿⣿⣿⠿⠟⠛⠛⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
* ⠀⠘⢿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
* ⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
! -->
</body>
</html>"""