#!/usr/bin/env python3
"""
Electronic Module Documentation Generator
=========================================

Updated generator that uses the new organized directory structure
with info/, docs/, hardware/, and software/ directories.

Author: DevLab Team
Date: 2025
"""

import os
import re
import yaml
import shutil
import subprocess
from datetime import datetime
import argparse
from pathlib import Path
from typing import Dict, List

# Import path configuration
from path_config import PathConfig

class LatexDocGenerator:
    def __init__(self, base_dir: str = None):
        """
        Initialize the LaTeX document generator
        
        Args:
            base_dir (str): Base directory of the project
        """
        # Initialize path configuration
        self.path_config = PathConfig(base_dir)
        self.paths = self.path_config.get_all_paths()
        
        print(f"📂 Base directory: {self.paths['root']}")
        
        # Ensure required directories exist
        self.path_config.ensure_directories()
        
        # Copy essential files
        self.copy_essential_files()
    
    def copy_essential_files(self):
        """Copy essential files to docs directory"""
        # Copy logo if it exists
        logo_sources = [
            self.paths['root'] / 'logo.png',
            self.paths['hardware_resources'] / 'logo.png',
            self.paths['info_templates'] / 'logo.png'
        ]
        
        for logo_src in logo_sources:
            if logo_src.exists():
                logo_dst = self.paths['output_docs'] / 'logo.png'
                shutil.copy2(logo_src, logo_dst)
                print(f"✓ Copied logo: {logo_src} -> {logo_dst}")
                break
        else:
            print("⚠ Warning: No logo.png found")
        
        # Copy hardware resources
        if self.paths['hardware_resources'].exists():
            for img_file in self.paths['hardware_resources'].glob('*.png'):
                dst_file = self.paths['output_docs'] / img_file.name
                shutil.copy2(img_file, dst_file)
                print(f"✓ Copied image: {img_file.name}")
    
    def load_metadata(self) -> Dict:
        """Load project metadata"""
        metadata = {}
        
        # Load project metadata
        if self.paths['metadata_project'].exists():
            with open(self.paths['metadata_project'], 'r', encoding='utf-8') as f:
                project_data = yaml.safe_load(f)
                if 'project_metadata' in project_data:
                    metadata.update(project_data['project_metadata'])
        
        # Load document standards
        if self.paths['metadata_standards'].exists():
            with open(self.paths['metadata_standards'], 'r', encoding='utf-8') as f:
                standards_data = yaml.safe_load(f)
                if 'document_standards' in standards_data:
                    metadata.update(standards_data['document_standards'])
        
        # Set default values
        metadata.setdefault('title', 'Electronic Module')
        metadata.setdefault('author', 'UNIT Electronics')
        metadata.setdefault('date', datetime.now().strftime('%B %Y'))
        
        return metadata
    
    def load_content(self, language: str = 'en') -> str:
        """
        Load content for specified language
        
        Args:
            language (str): Language code ('en' or 'es')
            
        Returns:
            str: Loaded content
        """
        content_sections = []
        
        # Load main content
        content_file = self.paths[f'content_{language}']
        if content_file.exists():
            with open(content_file, 'r', encoding='utf-8') as f:
                content_sections.append(f.read())
        
        # Load hardware documentation
        hardware_readme = self.paths['hardware'] / 'README.md'
        if hardware_readme.exists():
            with open(hardware_readme, 'r', encoding='utf-8') as f:
                hardware_content = f.read()
                content_sections.append(f"\n\n# HARDWARE\n\n{hardware_content}")
        
        # Load software documentation
        software_examples_dir = self.paths['software_examples']
        if software_examples_dir.exists():
            software_content = self.load_software_examples()
            if software_content:
                content_sections.append(f"\n\n# SOFTWARE\n\n{software_content}")
        
        return '\n'.join(content_sections)
    
    def load_software_examples(self) -> str:
        """Load software examples"""
        examples_content = []
        
        # C examples
        c_readme = self.paths['software_c'] / 'README.md'
        if c_readme.exists():
            with open(c_readme, 'r', encoding='utf-8') as f:
                examples_content.append(f"## C Programming Examples\n\n{f.read()}")
        
        # Add C code example
        c_main = self.paths['software_c'] / 'main' / 'main.c'
        if c_main.exists():
            with open(c_main, 'r', encoding='utf-8') as f:
                c_code = f.read()
                examples_content.append(f"\n### C Code Example\n\n```c\n{c_code}\n```")
        
        # Python examples
        python_readme = self.paths['software_python'] / 'README.md'
        if python_readme.exists():
            with open(python_readme, 'r', encoding='utf-8') as f:
                examples_content.append(f"\n## Python Programming Examples\n\n{f.read()}")
        
        # Add Python code example
        python_main = self.paths['software_python'] / 'main' / 'main.py'
        if python_main.exists():
            with open(python_main, 'r', encoding='utf-8') as f:
                python_code = f.read()
                examples_content.append(f"\n### Python Code Example\n\n```python\n{python_code}\n```")
        
        return '\n'.join(examples_content)
    
    def escape_latex_chars(self, text: str) -> str:
        """Escape special LaTeX characters"""
        # LaTeX special characters that need escaping
        latex_special_chars = {
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
        for char, escape in latex_special_chars.items():
            result = result.replace(char, escape)
        
        return result
    
    def convert_markdown_to_latex(self, markdown_content: str) -> str:
        """Convert Markdown content to LaTeX"""
        latex_content = markdown_content
        
        # Convert headers with forced numbering reset
        latex_content = re.sub(r'^# (.+)$', 
                              lambda m: f'\n\\setcounter{{section}}{{0}}\n\\section{{{self.escape_latex_chars(m.group(1))}}}\n', 
                              latex_content, flags=re.MULTILINE)
        
        latex_content = re.sub(r'^## (.+)$', 
                              lambda m: f'\\subsection{{{self.escape_latex_chars(m.group(1))}}}', 
                              latex_content, flags=re.MULTILINE)
        
        latex_content = re.sub(r'^### (.+)$', 
                              lambda m: f'\\subsubsection{{{self.escape_latex_chars(m.group(1))}}}', 
                              latex_content, flags=re.MULTILINE)
        
        # Convert code blocks to lstlisting
        def replace_code_block(match):
            language = match.group(1) if match.group(1) else 'text'
            code = match.group(2).strip()
            return f'\\begin{{lstlisting}}[language={language}]\n{code}\n\\end{{lstlisting}}'
        
        latex_content = re.sub(r'```(\w*)\n(.*?)\n```', replace_code_block, 
                              latex_content, flags=re.DOTALL)
        
        # Convert inline code
        latex_content = re.sub(r'`([^`]+)`', r'\\texttt{\\footnotesize \1}', latex_content)
        
        # Convert bold and italic
        latex_content = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', latex_content)
        latex_content = re.sub(r'\*(.+?)\*', r'\\textit{\1}', latex_content)
        
        # Convert tables
        latex_content = self.convert_tables_to_latex(latex_content)
        
        return latex_content
    
    def convert_tables_to_latex(self, content: str) -> str:
        """Convert Markdown tables to LaTeX"""
        lines = content.split('\n')
        result_lines = []
        in_table = False
        table_lines = []
        
        for line in lines:
            if '|' in line and line.strip().startswith('|'):
                if not in_table:
                    in_table = True
                    table_lines = []
                table_lines.append(line)
            else:
                if in_table:
                    # Process table
                    latex_table = self.process_table(table_lines)
                    result_lines.append(latex_table)
                    in_table = False
                    table_lines = []
                result_lines.append(line)
        
        # Handle table at end of content
        if in_table and table_lines:
            latex_table = self.process_table(table_lines)
            result_lines.append(latex_table)
        
        return '\n'.join(result_lines)
    
    def process_table(self, table_lines: List[str]) -> str:
        """Process a single table"""
        if len(table_lines) < 2:
            return '\n'.join(table_lines)
        
        # Parse header
        header_line = table_lines[0].strip()
        headers = [cell.strip() for cell in header_line.split('|')[1:-1]]
        
        # Skip separator line
        data_lines = table_lines[2:] if len(table_lines) > 2 else []
        
        # Create column specification
        col_spec = 'l' * len(headers)
        
        # Start table
        latex_table = [
            '\\begin{table}[H]',
            '\\centering',
            f'\\begin{{tabular}}{{{col_spec}}}',
            '\\toprule'
        ]
        
        # Add header
        header_latex = ' & '.join([self.escape_latex_chars(h) for h in headers])
        latex_table.append(f'{header_latex} \\\\')
        latex_table.append('\\midrule')
        
        # Add data rows
        for data_line in data_lines:
            if '|' in data_line:
                cells = [cell.strip() for cell in data_line.split('|')[1:-1]]
                if len(cells) == len(headers):
                    row_latex = ' & '.join([self.escape_latex_chars(cell) for cell in cells])
                    latex_table.append(f'{row_latex} \\\\')
        
        # End table
        latex_table.extend([
            '\\bottomrule',
            '\\end{tabular}',
            '\\end{table}',
            ''
        ])
        
        return '\n'.join(latex_table)
    
    def generate_latex_document(self, language: str = 'en', output_file: str = None) -> str:
        """Generate complete LaTeX document"""
        if output_file is None:
            output_file = self.paths['output_latex']
        
        # Load template
        if not self.paths['template_latex'].exists():
            raise FileNotFoundError(f"Template not found: {self.paths['template_latex']}")
        
        with open(self.paths['template_latex'], 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Load metadata and content
        metadata = self.load_metadata()
        content = self.load_content(language)
        
        # Convert content to LaTeX
        latex_content = self.convert_markdown_to_latex(content)
        
        # Replace template variables
        for key, value in metadata.items():
            placeholder = f'${{{key}}}$'
            if placeholder in template_content:
                template_content = template_content.replace(placeholder, str(value))
        
        # Insert content before \end{document}
        if '\\end{document}' in template_content:
            template_content = template_content.replace('\\end{document}', 
                                                      f'{latex_content}\n\n\\end{{document}}')
        else:
            template_content += f'\n\n{latex_content}\n\n\\end{{document}}'
        
        # Write output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        print(f"✓ LaTeX document generated: {output_file}")
        return str(output_file)
    
    def compile_pdf(self, latex_file: str, max_attempts: int = 3) -> bool:
        """Compile LaTeX to PDF"""
        latex_file = Path(latex_file)
        output_dir = latex_file.parent
        
        for attempt in range(max_attempts):
            print(f"📄 Compiling PDF (attempt {attempt + 1}/{max_attempts})...")
            
            try:
                result = subprocess.run([
                    'pdflatex', 
                    '-interaction=nonstopmode',
                    '-output-directory', str(output_dir),
                    str(latex_file)
                ], 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                errors='replace',
                cwd=str(output_dir))
                
                if result.returncode == 0:
                    pdf_file = latex_file.with_suffix('.pdf')
                    if pdf_file.exists():
                        file_size = pdf_file.stat().st_size
                        print(f"✓ PDF compiled successfully: {pdf_file} ({file_size} bytes)")
                        return True
                else:
                    print(f"⚠ LaTeX compilation warnings (attempt {attempt + 1})")
                    if "Emergency stop" in result.stdout or "Fatal error" in result.stdout:
                        print("❌ Fatal error in LaTeX compilation")
                        print(result.stdout[-500:])  # Show last 500 chars
                        return False
                    
            except FileNotFoundError:
                print("❌ pdflatex not found. Please install LaTeX distribution.")
                return False
            except UnicodeDecodeError as e:
                print(f"❌ Encoding error during compilation: {e}")
                return False
            except Exception as e:
                print(f"❌ Error during compilation: {e}")
                return False
        
        # Final check
        pdf_file = latex_file.with_suffix('.pdf')
        if pdf_file.exists():
            file_size = pdf_file.stat().st_size
            print(f"✓ PDF generated: {pdf_file} ({file_size} bytes)")
            return True
        
        print("❌ PDF compilation failed after all attempts")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Generate electronic module documentation')
    parser.add_argument('--language', '-l', default='en', choices=['en', 'es'],
                       help='Documentation language')
    parser.add_argument('--base-dir', '-d', 
                       help='Base directory of the project')
    
    args = parser.parse_args()
    
    print("Electronic Module Documentation Generator")
    print("=" * 60)
    
    try:
        # Initialize generator
        generator = LatexDocGenerator(args.base_dir)
        
        # Validate project structure
        if not generator.path_config.validate_structure():
            print("❌ Project structure validation failed")
            return 1
        
        # Generate LaTeX document
        latex_file = generator.generate_latex_document(args.language)
        
        # Compile PDF
        if generator.compile_pdf(latex_file):
            print("✅ Documentation generation completed successfully")
            return 0
        else:
            print("❌ PDF compilation failed")
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
