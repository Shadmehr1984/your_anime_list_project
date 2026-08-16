from src.report_maker.ReportMaker import ReportMaker
from src.report_extractor.ReportExtractor import ReportExtractor
from src.logger.logger import Logger

#initial logger
logger = Logger(__name__)

#extract report
query = """
SELECT studio_name, product_numbers
FROM studio
ORDER BY product_numbers DESC
LIMIT 10
"""

data = ReportExtractor.extract(query)

logger.log("report extracted")

#fix data
fixed_data = []

rank = 1

for item in data:
    fixed_data.append((rank, item[0], item[1]))
    rank += 1

data = fixed_data

#make report
report_first_half = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Your Anime List · Top 10 Studios</title>

    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Bangers&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet" />
    <!-- Font Awesome 6 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />

    <style>
        /* ============================================================
           WHITE & TURQUOISE THEME · Light & Clean
           ============================================================ */
        :root {
            --bg-primary: #f2f9fc;
            --bg-glass: rgba(255, 255, 255, 0.75);
            --accent: #00bcd4;
            --accent-dark: #00838f;
            --accent-dim: rgba(0, 188, 212, 0.12);
            --text-main: #1a2a3a;
            --text-secondary: #546e7a;
            --shadow: 0 8px 40px rgba(0, 188, 212, 0.08);
            --radius: 20px;
            --transition: 0.3s ease;
        }

        /* ---------- Reset & Base ---------- */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-primary);
            color: var(--text-main);
            min-height: 100vh;
            padding: 30px 20px;
            background-image:
                radial-gradient(circle at 10% 20%, rgba(0, 188, 212, 0.04) 0%, transparent 50%),
                radial-gradient(circle at 90% 80%, rgba(0, 131, 143, 0.03) 0%, transparent 50%);
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            max-width: 1100px;
            width: 100%;
        }

        /* ---------- Glass Card (Light) ---------- */
        .glass {
            background: var(--bg-glass);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--accent-dim);
            border-radius: var(--radius);
            padding: 28px 30px;
            box-shadow: var(--shadow);
        }

        /* ---------- Header ---------- */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 35px;
            flex-wrap: wrap;
            gap: 15px;
        }

        .logo {
            font-family: 'Bangers', cursive;
            font-size: 34px;
            color: var(--accent-dark);
            letter-spacing: 2px;
            text-shadow: 0 0 20px rgba(0, 188, 212, 0.10);
        }

        .logo i {
            margin-right: 10px;
            color: var(--accent);
        }

        .header-date {
            color: var(--text-secondary);
            font-size: 14px;
            font-weight: 500;
        }

        .header-date i {
            margin-right: 6px;
            color: var(--accent);
        }

        /* ---------- Page Title ---------- */
        .page-title {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 6px;
            color: var(--text-main);
        }

        .page-title i {
            color: var(--accent);
            margin-right: 10px;
        }

        .page-subtitle {
            color: var(--text-secondary);
            font-size: 16px;
            margin-bottom: 30px;
            font-weight: 400;
        }

        /* ---------- Table Styles ---------- */
        .table-wrapper {
            overflow-x: auto;
        }

        .studio-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 15px;
        }

        .studio-table thead th {
            text-align: left;
            padding: 14px 16px;
            font-weight: 700;
            color: var(--accent-dark);
            border-bottom: 2px solid var(--accent-dim);
            font-size: 14px;
            letter-spacing: 0.03em;
            text-transform: uppercase;
        }

        .studio-table tbody td {
            padding: 14px 16px;
            border-bottom: 1px solid rgba(0, 188, 212, 0.04);
            color: var(--text-main);
            transition: background var(--transition);
        }

        .studio-table tbody tr:last-child td {
            border-bottom: none;
        }

        .studio-table tbody tr:hover td {
            background: rgba(0, 188, 212, 0.03);
        }

        .studio-table .rank-col {
            font-weight: 700;
            color: var(--text-secondary);
            width: 60px;
            font-family: 'JetBrains Mono', monospace;
        }

        .studio-table .studio-name {
            font-weight: 600;
            color: var(--text-main);
        }

        .studio-table .products-col {
            font-weight: 700;
            color: var(--accent-dark);
            text-align: right;
            font-family: 'JetBrains Mono', monospace;
            font-size: 16px;
        }

        /* ---------- Footer ---------- */
        .footer {
            text-align: center;
            color: var(--text-secondary);
            font-size: 14px;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid var(--accent-dim);
        }

        .footer i {
            color: var(--accent);
            margin: 0 4px;
        }

        /* ---------- Responsive ---------- */
        @media (max-width: 640px) {
            .header {
                flex-direction: column;
                align-items: flex-start;
            }
            .logo { font-size: 28px; }
            .page-title { font-size: 22px; }
            .glass { padding: 20px 16px; }
            .studio-table thead th,
            .studio-table tbody td {
                padding: 10px 12px;
                font-size: 14px;
            }
            .studio-table .products-col {
                font-size: 14px;
            }
        }

        @media (max-width: 400px) {
            .logo { font-size: 24px; }
            .page-title { font-size: 19px; }
            .studio-table thead th,
            .studio-table tbody td {
                padding: 8px 10px;
                font-size: 13px;
            }
        }
    </style>
</head>
<body>

    <div class="container">

        <!-- ============================================================
        HEADER
        ============================================================ -->
        <header class="header">
            <div class="logo">
                <i class="fas fa-film"></i>
                Your Anime List
            </div>
            <div class="header-date">
                <i class="fas fa-calendar-alt"></i>
                <span id="currentDate"></span>
            </div>
        </header>

        <!-- ============================================================
        MAIN CONTENT
        ============================================================ -->
        <main>

            <!-- Page Title -->
            <h1 class="page-title">
                <i class="fas fa-building"></i>
                Top 10 Active Studios
            </h1>
            <p class="page-subtitle">
                Studios with the highest number of products
            </p>

            <!-- Table -->
            <div class="glass">
                <div class="table-wrapper">
                    <table class="studio-table">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Studio Name</th>
                                <th style="text-align: right;">Products</th>
                            </tr>
                        </thead>
                        <tbody>
"""

report_item_template = """
<tr>
                                <td class="rank-col">%s</td>
                                <td class="studio-name">%s</td>
                                <td class="products-col">%s</td>
                            </tr>
"""

report_second_half = """

                        </tbody>
                    </table>
                </div>
            </div>

        </main>

        <!-- ============================================================
        FOOTER
        ============================================================ -->
        <footer class="footer">
            <i class="fas fa-crown"></i>
            Your Anime List &nbsp;&nbsp; Reports
            <i class="fas fa-crown"></i>
        </footer>

    </div>

    <!-- ============================================================
    SCRIPT: Display today's date
    ============================================================ -->
    <script>
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        document.getElementById('currentDate').textContent = year + '/' + month + '/' + day;
    </script>

</body>
</html>
"""


report_name = "active_studios_report.html"

report_maker = ReportMaker(report_name)

report_maker.set_report_first_half(report_first_half)
report_maker.set_report_second_half(report_second_half)

report_maker.set_item_template(report_item_template)

for item in data:
    report_maker.add_item(item)

report_maker.make()

logger.log("report created")