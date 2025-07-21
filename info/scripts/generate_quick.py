#!/usr/bin/env python3
"""
Quick documentation generator - simplified version
"""

import os
import sys
from pathlib import Path
import yaml

def load_project_metadata():
    """Load project metadata"""
    metadata_file = Path(__file__).parent.parent / 'metadata' / 'project_metadata.yaml'
    if metadata_file.exists():
        with open(metadata_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}

def load_hardware_content():
    """Load hardware README"""
    hardware_file = Path(__file__).parent.parent.parent / 'hardware' / 'README.md'
    if hardware_file.exists():
        with open(hardware_file, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def load_software_content():
    """Load software README"""
    software_file = Path(__file__).parent.parent.parent / 'software' / 'README.md'
    if software_file.exists():
        with open(software_file, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def escape_latex(text):
    """Escape LaTeX special characters"""
    replacements = {
        '\\': r'\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '^': r'\textasciicircum{}',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        'µ': r'\textmu{}',
        '°': r'\textdegree{}',
        '±': r'\textpm{}',
    }
    
    result = text
    for char, replacement in replacements.items():
        result = result.replace(char, replacement)
    
    return result

def convert_markdown_to_latex(markdown_text):
    """Convert markdown to LaTeX"""
    lines = markdown_text.split('\n')
    latex_lines = []
    
    for line in lines:
        # Skip image lines for now
        if line.strip().startswith('!['):
            continue
            
        # Headers
        if line.startswith('# '):
            latex_lines.append(f'\\section{{{escape_latex(line[2:].strip())}}}')
        elif line.startswith('## '):
            latex_lines.append(f'\\subsection{{{escape_latex(line[3:].strip())}}}')
        elif line.startswith('### '):
            latex_lines.append(f'\\subsubsection{{{escape_latex(line[4:].strip())}}}')
        elif line.startswith('#### '):
            latex_lines.append(f'\\paragraph{{{escape_latex(line[5:].strip())}}}')
        # Code blocks
        elif line.strip().startswith('```'):
            if 'c' in line or 'python' in line:
                latex_lines.append('\\begin{lstlisting}')
            else:
                latex_lines.append('\\end{lstlisting}')
        # Bold text
        elif '**' in line:
            line = line.replace('**', '\\textbf{', 1).replace('**', '}', 1)
            latex_lines.append(escape_latex(line))
        else:
            if line.strip():
                latex_lines.append(escape_latex(line))
            else:
                latex_lines.append('')
    
    return '\n'.join(latex_lines)

def create_latex_document():
    """Create complete LaTeX document"""
    metadata = load_project_metadata()
    hardware_content = load_hardware_content()
    software_content = load_software_content()
    
    # Basic template
    latex_doc = r'''
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{array}
\usepackage{float}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{fancyhdr}

\geometry{margin=2.5cm}

\title{Electronic Module Technical Datasheet}
\author{UNIT Electronics}
\date{\today}

\begin{document}

\maketitle

\tableofcontents
\newpage

'''

    # Add hardware section
    if hardware_content:
        latex_doc += "\\section{HARDWARE}\n\n"
        latex_doc += convert_markdown_to_latex(hardware_content)
        latex_doc += "\n\n"
    
    # Add software section
    if software_content:
        latex_doc += "\\section{SOFTWARE}\n\n" 
        latex_doc += convert_markdown_to_latex(software_content)
        latex_doc += "\n\n"
    
    latex_doc += "\\end{document}"
    
    return latex_doc

def main():
    """Main function"""
    print("Quick Documentation Generator")
    print("=============================")
    
    # Create output directory
    docs_dir = Path(__file__).parent.parent.parent / 'docs'
    docs_dir.mkdir(exist_ok=True)
    
    # Generate LaTeX
    latex_content = create_latex_document()
    
    # Save LaTeX file
    latex_file = docs_dir / 'datasheet_en.tex'
    with open(latex_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print(f"✓ LaTeX generated: {latex_file}")
    
    # Try to compile PDF
    os.chdir(docs_dir)
    result = os.system("pdflatex -interaction=nonstopmode datasheet_en.tex > /dev/null 2>&1")
    
    if result == 0:
        print("✓ PDF compiled successfully")
        # Get file size
        pdf_file = docs_dir / 'datasheet_en.pdf'
        if pdf_file.exists():
            size_mb = pdf_file.stat().st_size / (1024 * 1024)
            print(f"✓ PDF size: {size_mb:.1f} MB")
    else:
        print("❌ PDF compilation failed")
        print("LaTeX file created, but manual compilation needed")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
