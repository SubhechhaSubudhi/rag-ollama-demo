#!/usr/bin/env python3
"""
Markdown to PDF Presentation Converter

Converts RAG_Presentation.md to a clean PDF presentation.

Requirements:
    pip install markdown pillow weasyprint

Or use pandoc (recommended):
    pip install pypandoc
    # Then: pandoc RAG_Presentation.md -o RAG_Presentation.pdf

This script provides both options.
"""

import subprocess
import sys
from pathlib import Path


def check_dependencies():
    """Check what tools are available"""
    tools = {}
    
    # Check for pandoc
    try:
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True)
        tools['pandoc'] = result.returncode == 0
    except FileNotFoundError:
        tools['pandoc'] = False
    
    # Check for weasyprint
    try:
        import weasyprint
        tools['weasyprint'] = True
    except ImportError:
        tools['weasyprint'] = False
    
    # Check for markdown2
    try:
        import markdown
        tools['markdown'] = True
    except ImportError:
        tools['markdown'] = False
    
    return tools


def convert_with_pandoc(input_file: str, output_file: str) -> bool:
    """Convert using pandoc (recommended)"""
    try:
        # Try with beamer (for presentations)
        cmd = [
            'pandoc',
            input_file,
            '-o', output_file,
            '--standalone',
            '--toc',
            '-V', 'theme:Warsaw',
            '-V', 'colortheme:whale',
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Created: {output_file}")
            return True
        else:
            print(f"Pandoc beamer failed: {result.stderr}")
            # Try basic PDF
            cmd_basic = [
                'pandoc',
                input_file,
                '-o', output_file,
                '--standalone',
            ]
            result = subprocess.run(cmd_basic, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Created (basic): {output_file}")
                return True
            return False
    except Exception as e:
        print(f"Pandoc error: {e}")
        return False


def convert_with_weasyprint(input_file: str, output_file: str) -> bool:
    """Convert using WeasyPrint"""
    try:
        import markdown
        from weasyprint import HTML
        
        # Read markdown
        with open(input_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert to HTML
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 14px;
            line-height: 1.6;
            padding: 40px;
            max-width: 800px;
            margin: 0 auto;
        }}
        h1 {{ font-size: 32px; color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ font-size: 24px; color: #34495e; margin-top: 30px; }}
        h3 {{ font-size: 18px; color: #7f8c8d; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: monospace; }}
        pre {{ background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background: #3498db; color: white; }}
        tr:nth-child(even) {{ background: #f9f9f9; }}
        ul, ol {{ margin: 10px 0; padding-left: 25px; }}
        li {{ margin: 5px 0; }}
        blockquote {{ border-left: 4px solid #3498db; margin: 20px 0; padding-left: 15px; color: #7f8c8d; }}
    </style>
</head>
<body>
{markdown.markdown(md_content)}
</body>
</html>"""
        
        # Convert to PDF
        HTML(string=html_content).write_pdf(output_file)
        print(f"✅ Created: {output_file}")
        return True
    except Exception as e:
        print(f"WeasyPrint error: {e}")
        return False


def convert_markdown_simple(input_file: str, output_file: str) -> bool:
    """Simple HTML to PDF conversion"""
    try:
        import markdown
        
        with open(input_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        html = markdown.markdown(md_content)
        
        html_doc = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>RAG Presentation</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 40px; max-width: 800px; margin: 0 auto; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; }}
        h2 {{ color: #34495e; }}
        code {{ background: #f4f4f4; padding: 2px 5px; }}
        pre {{ background: #2c3e50; color: white; padding: 10px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; }}
        th {{ background: #3498db; color: white; }}
    </style>
</head>
<body>
{html}
</body>
</html>"""
        
        # Try using weasyprint if available
        try:
            from weasyprint import HTML
            HTML(string=html_doc).write_pdf(output_file)
            print(f"✅ Created: {output_file}")
            return True
        except ImportError:
            # Save as HTML instead
            html_output = output_file.replace('.pdf', '.html')
            with open(html_output, 'w', encoding='utf-8') as f:
                f.write(html_doc)
            print(f"⚠️ PDF not available, saved as HTML: {html_output}")
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    input_file = "RAG_Presentation.md"
    output_file = "RAG_Presentation.pdf"
    
    print("=" * 50)
    print("Markdown to PDF Converter")
    print("=" * 50)
    
    # Check available tools
    tools = check_dependencies()
    
    print(f"\nAvailable tools:")
    print(f"  Pandoc: {'✅' if tools['pandoc'] else '❌'}")
    print(f"  WeasyPrint: {'✅' if tools['weasyprint'] else '❌'}")
    print(f"  Markdown: {'✅' if tools['markdown'] else '❌'}")
    
    if not Path(input_file).exists():
        print(f"\n❌ Input file not found: {input_file}")
        return
    
    print(f"\nConverting {input_file}...")
    
    # Try methods in order of preference
    if tools.get('pandoc'):
        print("\n→ Trying pandoc...")
        if convert_with_pandoc(input_file, output_file):
            return
    
    if tools.get('weasyprint') and tools.get('markdown'):
        print("\n→ Trying WeasyPrint...")
        if convert_with_weasyprint(input_file, output_file):
            return
    
    if tools.get('markdown'):
        print("\n→ Trying simple conversion...")
        convert_markdown_simple(input_file, output_file)
        return
    
    # Installation instructions
    print("\n" + "=" * 50)
    print("Installation Instructions")
    print("=" * 50)
    print("""
To convert Markdown to PDF, install one of:

Option 1: Pandoc (Recommended)
    pip install pypandoc
    # Also need LaTeX: https://www.latex-project.org/get/

Option 2: WeasyPrint
    pip install markdown weasyprint

Option 3: Basic HTML (no PDF)
    pip install markdown
    # Will create HTML file instead
""")


if __name__ == "__main__":
    main()
