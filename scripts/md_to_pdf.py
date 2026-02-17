#!/usr/bin/env python3
"""
Markdown to PDF Converter

This script converts Markdown (.md) files to PDF format.
Uses fpdf2 library (pure Python, no system dependencies required).

Usage:
    python scripts/md_to_pdf.py INTERIM_REPORT.md
    python scripts/md_to_pdf.py FINAL_REPORT.md
    python scripts/md_to_pdf.py --all  # Convert all .md files in root directory
"""

import argparse
import os
import re
import sys
from pathlib import Path

try:
    from fpdf import FPDF
    from fpdf.enums import XPos, YPos
except ImportError:
    print("Error: fpdf2 package not installed")
    print("Install with: pip install fpdf2")
    sys.exit(1)


def sanitize_text(text: str) -> str:
    """
    Replace Unicode characters that aren't supported by standard fonts.
    """
    if not text:
        return ""
        
    replacements = {
        '—': '-',  # em dash
        '–': '-',  # en dash
        ''': "'",  # right single quote
        ''': "'",  # left single quote
        '"': '"',  # left double quote
        '"': '"',  # right double quote
        '…': '...',  # ellipsis
        '•': '*',  # bullet
        '→': '->',  # arrow
        '←': '<-',  # arrow
        '▼': 'v',  # down arrow
        '▲': '^',  # up arrow
        '✓': '[x]',  # checkmark
        '✗': '[ ]',  # x mark
        '✅': '[DONE]',  # checkmark emoji
        '❌': '[X]',  # x emoji
        '⏰': '[TIME]',  # clock emoji
        '©': '(c)',  # copyright
        '®': '(R)',  # registered
        '™': '(TM)',  # trademark
        '°': ' deg',  # degree
        '±': '+/-',  # plus minus
        '×': 'x',  # multiplication
        '÷': '/',  # division
        '≈': '~',  # approximately
        '≠': '!=',  # not equal
        '≤': '<=',  # less than or equal
        '≥': '>=',  # greater than or equal
        '∞': 'inf',  # infinity
        '\u200b': '',  # zero-width space
        '\xa0': ' ',  # non-breaking space
        # Box drawing characters
        '┌': '+',
        '┐': '+',
        '└': '+',
        '┘': '+',
        '├': '+',
        '┤': '+',
        '┬': '+',
        '┴': '+',
        '┼': '+',
        '─': '-',
        '│': '|',
        '═': '=',
        '║': '|',
        '╔': '+',
        '╗': '+',
        '╚': '+',
        '╝': '+',
        '█': '#',
        '▓': '#',
        '▒': '=',
        '░': '-',
        '█': '#',
        '▌': '|',
        '▐': '|',
        '▀': '-',
        '▄': '_',
        '●': 'o',
        '○': 'o',
        '◆': '*',
        '◇': '*',
        '■': '#',
        '□': '[ ]',
        '▪': '*',
        '▫': '-',
        '★': '*',
        '☆': '*',
        'σ': 'sigma',
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Remove any remaining non-ASCII characters
    return text.encode('ascii', 'ignore').decode('ascii')


class MarkdownPDF(FPDF):
    """Custom PDF class with markdown support."""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(15, 15, 15)
        
    def header(self):
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'Stock Challenge Week 1 - Report', align='C')
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')
        
    def safe_cell(self, w, h, text, **kwargs):
        """Safely write a cell, handling width issues."""
        text = sanitize_text(str(text))
        if not text:
            return
        # Ensure minimum width
        if w <= 0:
            w = 180
        try:
            self.cell(w, h, text, **kwargs)
        except Exception as e:
            # Truncate text if too long
            while len(text) > 1:
                text = text[:-1]
                try:
                    self.cell(w, h, text + "...", **kwargs)
                    return
                except:
                    continue
                    
    def safe_multi_cell(self, w, h, text, **kwargs):
        """Safely write a multi_cell, handling width issues."""
        text = sanitize_text(str(text))
        if not text:
            return
        # Ensure minimum width
        if w <= 0:
            w = 180
        try:
            self.multi_cell(w, h, text, **kwargs)
        except Exception as e:
            # Try with shorter lines
            words = text.split()
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                if len(test_line) > 80:
                    if current_line:
                        try:
                            self.multi_cell(w, h, current_line, **kwargs)
                        except:
                            pass
                    current_line = word
                else:
                    current_line = test_line
            if current_line:
                try:
                    self.multi_cell(w, h, current_line, **kwargs)
                except:
                    pass


def convert_md_to_pdf(input_file: str, output_file: str = None) -> str:
    """
    Convert a Markdown file to PDF.
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    if not input_path.suffix.lower() == '.md':
        raise ValueError(f"Input file must be a .md file: {input_file}")
    
    if output_file is None:
        output_file = str(input_path.with_suffix('.pdf'))
    
    print(f"Converting: {input_file} -> {output_file}")
    
    # Read markdown content
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Create PDF
    pdf = MarkdownPDF()
    pdf.add_page()
    
    # Parse and write content
    lines = md_content.split('\n')
    in_code = False
    code_lines = []
    in_table = False
    table_headers = []
    table_rows = []
    
    for line_num, line in enumerate(lines):
        try:
            # Code blocks
            if line.strip().startswith('```'):
                if in_code:
                    # End code block
                    if code_lines:
                        pdf.set_fill_color(245, 245, 245)
                        pdf.set_font('Courier', '', 8)
                        for code_line in code_lines:
                            code_line = sanitize_text(code_line)[:85]
                            if pdf.get_y() > 265:
                                pdf.add_page()
                            pdf.cell(0, 5, code_line, new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
                        pdf.ln(3)
                    code_lines = []
                    in_code = False
                else:
                    in_code = True
                continue
                
            if in_code:
                code_lines.append(line)
                continue
            
            # Tables
            if '|' in line and not line.strip().startswith('|--'):
                cells = [c.strip() for c in line.split('|') if c.strip()]
                if cells:
                    if not in_table:
                        in_table = True
                        table_headers = cells
                    else:
                        table_rows.append(cells)
                continue
            elif line.strip().startswith('|--'):
                continue
            elif in_table:
                # Write table with dynamic column widths
                if table_headers:
                    num_cols = len(table_headers)
                    page_width = 180
                    
                    # Calculate max content length for each column
                    col_max_lens = [len(sanitize_text(str(h))) for h in table_headers]
                    for row in table_rows:
                        for i, c in enumerate(row):
                            if i < len(col_max_lens):
                                col_max_lens[i] = max(col_max_lens[i], len(sanitize_text(str(c))))
                    
                    # Calculate proportional widths
                    total_chars = sum(col_max_lens) or 1
                    col_widths = [max(20, min(60, int(page_width * (l / total_chars)))) for l in col_max_lens]
                    
                    # Adjust to fit page
                    total_width = sum(col_widths)
                    if total_width > page_width:
                        scale = page_width / total_width
                        col_widths = [max(15, int(w * scale)) for w in col_widths]
                    
                    pdf.set_font('Helvetica', 'B', 8)
                    pdf.set_fill_color(74, 105, 189)
                    pdf.set_text_color(255, 255, 255)
                    for i, h in enumerate(table_headers):
                        h = sanitize_text(str(h))[:25]
                        w = col_widths[i] if i < len(col_widths) else 25
                        pdf.cell(w, 7, h, border=1, fill=True, align='C')
                    pdf.ln()
                    
                    pdf.set_font('Helvetica', '', 8)
                    pdf.set_text_color(51, 51, 51)
                    for row_idx, row in enumerate(table_rows):
                        if row_idx % 2 == 0:
                            pdf.set_fill_color(249, 249, 249)
                        else:
                            pdf.set_fill_color(255, 255, 255)
                        for i, c in enumerate(row):
                            c = sanitize_text(str(c))[:25]
                            w = col_widths[i] if i < len(col_widths) else 25
                            pdf.cell(w, 6, c, border=1, fill=True)
                        pdf.ln()
                    pdf.ln(3)
                    
                in_table = False
                table_headers = []
                table_rows = []
            
            # Horizontal rules
            if re.match(r'^[-*_]{3,}$', line.strip()):
                pdf.ln(3)
                pdf.set_draw_color(200, 200, 200)
                pdf.line(15, pdf.get_y(), 195, pdf.get_y())
                pdf.ln(5)
                continue
            
            # Headers
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if header_match:
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                title = re.sub(r'\*\*(.+?)\*\*', r'\1', title)
                title = re.sub(r'\*(.+?)\*', r'\1', title)
                title = re.sub(r'`(.+?)`', r'\1', title)
                title = sanitize_text(title)
                
                pdf.ln(4)
                if level == 1:
                    pdf.set_font('Helvetica', 'B', 18)
                    pdf.set_text_color(26, 26, 46)
                elif level == 2:
                    pdf.set_font('Helvetica', 'B', 14)
                    pdf.set_text_color(44, 62, 80)
                elif level == 3:
                    pdf.set_font('Helvetica', 'B', 12)
                    pdf.set_text_color(52, 73, 94)
                else:
                    pdf.set_font('Helvetica', 'B', 10)
                    pdf.set_text_color(93, 109, 126)
                
                pdf.multi_cell(0, 7, title)
                
                if level <= 2:
                    pdf.set_draw_color(74, 105, 189)
                    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
                    
                pdf.ln(3)
                pdf.set_text_color(51, 51, 51)
                continue
            
            # Bullet points
            bullet_match = re.match(r'^(\s*)[-*+]\s+(.+)$', line)
            if bullet_match:
                indent_str = bullet_match.group(1)
                text = bullet_match.group(2)
                text = re.sub(r'^\[[ x]\]\s*', '', text)
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
                text = re.sub(r'\*(.+?)\*', r'\1', text)
                text = re.sub(r'`(.+?)`', r'\1', text)
                text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
                text = sanitize_text(text)
                
                # Calculate indent level (max 3)
                indent_level = min(len(indent_str) // 2, 3)
                indent_spaces = "  " * indent_level
                
                pdf.set_font('Helvetica', '', 10)
                pdf.set_text_color(51, 51, 51)
                pdf.multi_cell(0, 5, f"{indent_spaces}- {text}")
                continue
            
            # Numbered lists
            numbered_match = re.match(r'^(\s*)(\d+)\.\s+(.+)$', line)
            if numbered_match:
                indent_str = numbered_match.group(1)
                num = numbered_match.group(2)
                text = numbered_match.group(3)
                text = re.sub(r'^\[[ x]\]\s*', '', text)
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
                text = re.sub(r'\*(.+?)\*', r'\1', text)
                text = re.sub(r'`(.+?)`', r'\1', text)
                text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
                text = sanitize_text(text)
                
                # Calculate indent level (max 3)
                indent_level = min(len(indent_str) // 2, 3)
                indent_spaces = "  " * indent_level
                
                pdf.set_font('Helvetica', '', 10)
                pdf.set_text_color(51, 51, 51)
                pdf.multi_cell(0, 5, f"{indent_spaces}{num}. {text}")
                continue
            
            # Skip images
            if re.match(r'!\[.*\]\(.*\)', line):
                continue
            
            # Regular text
            text = line.strip()
            if text:
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
                text = re.sub(r'\*(.+?)\*', r'\1', text)
                text = re.sub(r'`(.+?)`', r'\1', text)
                text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
                text = sanitize_text(text)
                
                pdf.set_font('Helvetica', '', 10)
                pdf.set_text_color(51, 51, 51)
                pdf.multi_cell(0, 5, text)
                pdf.ln(1)
                
        except Exception as e:
            print(f"Warning: Error on line {line_num + 1}: {e}")
            continue
    
    # Handle remaining table
    if in_table and table_headers:
        try:
            num_cols = len(table_headers)
            page_width = 180
            
            # Calculate max content length for each column
            col_max_lens = [len(sanitize_text(str(h))) for h in table_headers]
            for row in table_rows:
                for i, c in enumerate(row):
                    if i < len(col_max_lens):
                        col_max_lens[i] = max(col_max_lens[i], len(sanitize_text(str(c))))
            
            # Calculate proportional widths
            total_chars = sum(col_max_lens) or 1
            col_widths = [max(20, min(60, int(page_width * (l / total_chars)))) for l in col_max_lens]
            
            # Adjust to fit page
            total_width = sum(col_widths)
            if total_width > page_width:
                scale = page_width / total_width
                col_widths = [max(15, int(w * scale)) for w in col_widths]
            
            pdf.set_font('Helvetica', 'B', 8)
            pdf.set_fill_color(74, 105, 189)
            pdf.set_text_color(255, 255, 255)
            for i, h in enumerate(table_headers):
                h = sanitize_text(str(h))[:25]
                w = col_widths[i] if i < len(col_widths) else 25
                pdf.cell(w, 7, h, border=1, fill=True, align='C')
            pdf.ln()
            
            pdf.set_font('Helvetica', '', 8)
            pdf.set_text_color(51, 51, 51)
            for row_idx, row in enumerate(table_rows):
                if row_idx % 2 == 0:
                    pdf.set_fill_color(249, 249, 249)
                else:
                    pdf.set_fill_color(255, 255, 255)
                for i, c in enumerate(row):
                    c = sanitize_text(str(c))[:25]
                    w = col_widths[i] if i < len(col_widths) else 25
                    pdf.cell(w, 6, c, border=1, fill=True)
                pdf.ln()
        except Exception as e:
            print(f"Warning: Error writing table: {e}")
    
    # Save PDF
    pdf.output(output_file)
    
    print(f"Successfully created: {output_file}")
    return output_file


def find_md_files(directory: str = ".") -> list:
    """Find all .md files in the specified directory."""
    md_files = []
    for file in Path(directory).glob("*.md"):
        if not file.name.startswith('.') and file.name not in ['README.md', 'CHANGELOG.md']:
            md_files.append(str(file))
    return sorted(md_files)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown files to PDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/md_to_pdf.py INTERIM_REPORT.md
    python scripts/md_to_pdf.py FINAL_REPORT.md -o reports/final.pdf
    python scripts/md_to_pdf.py --all
        """
    )
    
    parser.add_argument(
        'input_file',
        nargs='?',
        help='Input Markdown file to convert'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output PDF file path (default: same name with .pdf extension)'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Convert all .md files in the current directory'
    )
    
    parser.add_argument(
        '-d', '--directory',
        default='.',
        help='Directory to search for .md files (used with --all)'
    )
    
    args = parser.parse_args()
    
    if args.all:
        md_files = find_md_files(args.directory)
        
        if not md_files:
            print(f"No .md files found in {args.directory}")
            return
        
        print(f"Found {len(md_files)} Markdown file(s) to convert:")
        for f in md_files:
            print(f"  - {f}")
        print()
        
        success_count = 0
        for md_file in md_files:
            try:
                convert_md_to_pdf(md_file)
                success_count += 1
            except Exception as e:
                print(f"Error converting {md_file}: {e}")
        
        print(f"\nConversion complete: {success_count}/{len(md_files)} files converted successfully")
        
    elif args.input_file:
        try:
            convert_md_to_pdf(args.input_file, args.output)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
