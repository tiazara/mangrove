import os
import re
import html
import subprocess
import markdown
from pypdf import PdfReader

CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
if not os.path.exists(CHROME_PATH):
    CHROME_PATH = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
  }},
  svg: {{ fontCache: 'global' }}
}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" id="MathJax-script"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>

<style>
@page {{
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
}}

* {{
    box-sizing: border-box;
}}

body {{
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    line-height: 1.6;
    font-size: 10pt;
    background: #ffffff;
    margin: 0;
    padding: 0;
}}

.header-banner {{
    background: linear-gradient(135deg, #1e3a8a 0%, #0284c7 100%);
    color: #ffffff;
    padding: 16px 20px;
    border-radius: 10px;
    margin-bottom: 24px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}}

.header-banner .badge {{
    display: inline-block;
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.4);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 8pt;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
}}

.header-banner h1 {{
    font-size: 15pt;
    font-weight: 800;
    color: #ffffff;
    margin: 4px 0 0 0;
    line-height: 1.35;
    border-bottom: none;
    padding-bottom: 0;
}}

h1 {{
    font-size: 15pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 2px solid #3b82f6;
    padding-bottom: 6px;
    margin-top: 24px;
    margin-bottom: 14px;
    line-height: 1.35;
}}

h2 {{
    font-size: 12.5pt;
    font-weight: 700;
    color: #1e40af;
    margin-top: 22px;
    margin-bottom: 10px;
    border-left: 4px solid #2563eb;
    padding-left: 10px;
    page-break-after: avoid;
}}

h3 {{
    font-size: 11pt;
    font-weight: 700;
    color: #0f172a;
    margin-top: 16px;
    margin-bottom: 8px;
    page-break-after: avoid;
}}

h4 {{
    font-size: 10pt;
    font-weight: 600;
    color: #334155;
    margin-top: 12px;
    margin-bottom: 6px;
    page-break-after: avoid;
}}

p {{
    margin: 8px 0;
    text-align: justify;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 8.8pt;
    page-break-inside: avoid;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}

th {{
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
    text-align: left;
    padding: 8px 9px;
    border: 1px solid #cbd5e1;
    font-size: 8.8pt;
}}

td {{
    padding: 7px 9px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
}}

tr:nth-child(even) td {{
    background: #f8fafc;
}}

a {{
    color: #2563eb;
    text-decoration: none;
    word-break: break-all;
}}

a:hover {{
    text-decoration: underline;
}}

code {{
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 8.8pt;
    background: #f1f5f9;
    color: #0f172a;
    padding: 1.5px 5px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
}}

pre {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 10px 12px;
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 8.5pt;
    line-height: 1.45;
    overflow-x: auto;
    page-break-inside: avoid;
}}

pre code {{
    background: transparent;
    padding: 0;
    border: none;
}}

blockquote {{
    border-left: 4px solid #3b82f6;
    background: #eff6ff;
    padding: 8px 12px;
    margin: 10px 0;
    border-radius: 0 6px 6px 0;
    color: #1e40af;
}}

hr {{
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 18px 0;
}}

ul, ol {{
    padding-left: 20px;
    margin: 6px 0;
}}

li {{
    margin-bottom: 4px;
}}

.mermaid {{
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 16px 0;
    background: #f8fafc;
    padding: 16px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    page-break-inside: avoid;
    text-align: center;
}}

.mermaid svg {{
    max-width: 100% !important;
    height: auto !important;
}}

.footer-note {{
    margin-top: 28px;
    padding-top: 10px;
    border-top: 1px solid #e2e8f0;
    font-size: 8pt;
    color: #64748b;
    display: flex;
    justify-content: space-between;
}}
</style>
</head>
<body>

<div class="header-banner">
    <div class="badge">ASEC ARSEN UNAIR 2026 • IMPLEMENTATION PLAN</div>
    <h1>{heading_title}</h1>
</div>

<div class="content">
{body}
</div>

<div class="footer-note">
    <span>Airlangga Statistics Essay Competition (ASEC) 2026</span>
    <span>Dokumen Rencana Implementasi Riset & Penulisan</span>
</div>

<script>
mermaid.initialize({{
    startOnLoad: true,
    theme: 'neutral',
    flowchart: {{
        useMaxWidth: true,
        htmlLabels: false,
        curve: 'basis'
    }}
}});
</script>

</body>
</html>
"""

def clean_mermaid_code(raw_code):
    # Ensure all lines in flowchart with brackets are properly quoted
    lines = raw_code.strip().split('\n')
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

def convert_md_to_pdf(md_path, pdf_path):
    print(f"Processing: {os.path.basename(md_path)}...")
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Extract title from first H1 or H2
    title = os.path.splitext(os.path.basename(md_path))[0].replace('_', ' ')
    lines = md_text.split('\n')
    heading_title = title
    for line in lines:
        if line.startswith('# '):
            heading_title = line.replace('# ', '').strip()
            md_text = md_text.replace(line, '', 1).strip()
            break

    # Convert markdown to html
    html_body = markdown.markdown(
        md_text,
        extensions=['extra', 'tables', 'fenced_code', 'toc']
    )

    # Pre-process: convert <pre><code class="language-mermaid"> to <div class="mermaid"> directly in Python!
    def replace_mermaid(match):
        code = match.group(1)
        # Unescape HTML entities
        unescaped = html.unescape(code).strip()
        return f'<div class="mermaid">\n{unescaped}\n</div>'

    html_body = re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        replace_mermaid,
        html_body,
        flags=re.DOTALL
    )

    full_html = HTML_TEMPLATE.format(
        title=title,
        heading_title=heading_title,
        body=html_body
    )

    temp_html = md_path.replace('.md', '_temp.html')
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(full_html)

    abs_html = os.path.abspath(temp_html)
    abs_pdf = os.path.abspath(pdf_path)

    cmd = [
        CHROME_PATH,
        '--headless=new',
        '--disable-gpu',
        '--run-all-compositor-stages-before-draw',
        '--virtual-time-budget=7000',
        f'--print-to-pdf={abs_pdf}',
        '--no-pdf-header-footer',
        f'file:///{abs_html}'
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(temp_html):
        os.remove(temp_html)

    if os.path.exists(abs_pdf) and os.path.getsize(abs_pdf) > 0:
        # Check with pypdf
        reader = PdfReader(abs_pdf)
        pdf_text = '\n'.join([p.extract_text() for p in reader.pages])
        has_error = 'Syntax error in text' in pdf_text
        if has_error:
            print(f" [MERMAID ERROR] in {os.path.basename(pdf_path)}!")
        else:
            print(f" [SUCCESS] -> {os.path.basename(pdf_path)} ({len(reader.pages)} pages, {os.path.getsize(abs_pdf)} bytes)")
    else:
        print(f" [FAILED] for {md_path}. Stderr: {res.stderr}")

if __name__ == '__main__':
    target_dir = r'd:\Kuliah\Lomba\ASEC Arsen Unair 2026\Rencana_Topik'
    files = [
        'Topik_1_Ketahanan_Pangan_AGRO-VULNERA.md',
        'Topik_2_Kesehatan_Masyarakat_PULMO-SHIELD.md',
        'Topik_3_Sosial_Ekonomi_EQUITY-GRID.md',
        'Topik_4_Lingkungan_COAST-SHIELD.md',
        'Topik_5_Lingkungan_PEAT-PULSE.md'
    ]
    for f in files:
        md_file = os.path.join(target_dir, f)
        pdf_file = md_file.replace('.md', '.pdf')
        convert_md_to_pdf(md_file, pdf_file)
