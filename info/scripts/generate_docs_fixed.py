#!/usr/bin/env python3
"""
Electronic Module Documentation Generator - Fixed Version
========================================================

Based on the working generate_final.py but adapted for the new directory structure.

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
        
        self.base_dir = self.paths['root']
        self.docs_dir = self.paths['output_docs']
        self.images_dir = self.base_dir / "images"
        self.hardware_resources_dir = self.paths['hardware_resources']
        self.template_file = self.paths['template_latex']
        
        print(f"📂 Base directory: {self.base_dir}")
        
        # Ensure required directories exist
        self.path_config.ensure_directories()
        
        # Create additional image directories
        self.create_additional_image_dirs()
        
        # Copy essential files
        self.copy_essential_files()
    
    def create_additional_image_dirs(self):
        """Crea directorios adicionales para imágenes si no existen"""
        additional_dirs = [
            self.base_dir / "assets",
            self.base_dir / "media",
            self.docs_dir / "assets",
            self.images_dir / "custom"
        ]
        
        for dir_path in additional_dirs:
            dir_path.mkdir(exist_ok=True, parents=True)
    
    def copy_essential_files(self):
        """Copia archivos esenciales como logos e imágenes"""
        essential_files = ['logo.png', 'logo.jpg', 'logo.jpeg']
        
        # Buscar primero en hardware/resources/img/
        if self.hardware_resources_dir.exists():
            img_dir = self.hardware_resources_dir / "img"
            if img_dir.exists():
                for filename in essential_files:
                    source_path = img_dir / filename
                    if source_path.exists():
                        dest_path = self.docs_dir / filename
                        shutil.copy2(source_path, dest_path)
                        print(f"✓ Copied {filename} from hardware/resources/img/ to docs/")
                        break
        
        # Copiar todas las imágenes de hardware/resources/
        if self.hardware_resources_dir.exists():
            for img_file in self.hardware_resources_dir.glob('*.png'):
                dst_file = self.docs_dir / img_file.name
                shutil.copy2(img_file, dst_file)
                print(f"✓ Copied image: {img_file.name}")
            
            for img_file in self.hardware_resources_dir.glob('*.jpg'):
                dst_file = self.docs_dir / img_file.name
                shutil.copy2(img_file, dst_file)
                print(f"✓ Copied image: {img_file.name}")
    
    def load_base_metadata(self, lang_dir: str) -> Dict:
        """Carga metadatos base desde archivos de configuración"""
        metadata = {
            'title': 'Electronic Module',
            'subtitle': 'Technical Datasheet and Development Guide',
            'product_name': 'Electronic Module',
            'product_sku': 'UEXXXX',
            'version': '1.0.0',
            'author': 'UNIT Electronics',
            'division': 'Hardware Development & Prototyping',
            'contact': 'info@unitelectronics.com',
            'website': 'www.uelectronics.com',
            'copyright': '© 2025 UNIT Electronics. All rights reserved.',
            'date': datetime.now().strftime('%B %Y'),
            'logo': 'logo.png',
            'project_phase': 'Prototype Development',
            'hardware_status': 'Functional prototype completed'
        }
        
        # Cargar project_metadata.yaml si existe
        project_metadata_file = self.paths['metadata_project']
        if project_metadata_file.exists():
            try:
                with open(project_metadata_file, 'r', encoding='utf-8') as f:
                    project_data = yaml.safe_load(f)
                    if 'project_metadata' in project_data:
                        metadata.update(project_data['project_metadata'])
                        print(f"✓ Loaded project metadata from {project_metadata_file}")
            except Exception as e:
                print(f"⚠ Warning: Could not load project metadata: {e}")
        
        # Cargar document_standards.yaml si existe
        standards_file = self.paths['metadata_standards']
        if standards_file.exists():
            try:
                with open(standards_file, 'r', encoding='utf-8') as f:
                    standards_data = yaml.safe_load(f)
                    if 'document_standards' in standards_data:
                        metadata.update(standards_data['document_standards'])
                        print(f"✓ Loaded document standards from {standards_file}")
            except Exception as e:
                print(f"⚠ Warning: Could not load document standards: {e}")
        
        return metadata
    
    def load_content_from_files(self, language: str) -> str:
        """Carga contenido desde archivos de la nueva estructura"""
        content_sections = []
        
        # Cargar contenido principal del idioma
        content_file = self.paths[f'content_{language}']
        if content_file.exists():
            with open(content_file, 'r', encoding='utf-8') as f:
                main_content = f.read()
                content_sections.append(main_content)
                print(f"✓ Loaded main content from {content_file}")
        
        # Cargar documentación de hardware
        hardware_readme = self.paths['hardware'] / 'README.md'
        if hardware_readme.exists():
            with open(hardware_readme, 'r', encoding='utf-8') as f:
                hardware_content = f.read()
                content_sections.append(f"\n\n# HARDWARE\n\n{hardware_content}")
                print(f"✓ Loaded hardware content from {hardware_readme}")
        
        # Cargar documentación de software
        software_content = self.load_software_examples()
        if software_content:
            content_sections.append(f"\n\n# SOFTWARE\n\n{software_content}")
        
        return '\n'.join(content_sections)
    
    def load_software_examples(self) -> str:
        """Carga ejemplos de software y documentación principal"""
        examples_content = []
        
        # Cargar README principal de software (documentación completa)
        software_readme = self.paths['software'] / 'README.md'
        if software_readme.exists():
            with open(software_readme, 'r', encoding='utf-8') as f:
                software_main_content = f.read()
                # Remover el título principal para evitar duplicación
                if software_main_content.startswith('# Software Documentation'):
                    software_main_content = software_main_content.split('\n', 1)[1]
                examples_content.append(software_main_content)
                print(f"✓ Loaded main software documentation from {software_readme}")
        
        # Ejemplos en C
        c_readme = self.paths['software_c'] / 'README.md'
        if c_readme.exists():
            with open(c_readme, 'r', encoding='utf-8') as f:
                examples_content.append(f"\n\n## Additional C Programming Examples\n\n{f.read()}")
                print(f"✓ Loaded C examples from {c_readme}")
        
        # Agregar código C
        c_main = self.paths['software_c'] / 'main' / 'main.c'
        if c_main.exists():
            with open(c_main, 'r', encoding='utf-8') as f:
                c_code = f.read()
                examples_content.append(f"\n### C Code Example\n\n```c\n{c_code}\n```")
        
        # Ejemplos en Python (solo si existen y no están ya en el README principal)
        python_readme = self.paths['software_python'] / 'README.md'
        if python_readme.exists():
            with open(python_readme, 'r', encoding='utf-8') as f:
                examples_content.append(f"\n\n## Additional Python Programming Examples\n\n{f.read()}")
                print(f"✓ Loaded Python examples from {python_readme}")
        
        # Agregar código Python
        python_main = self.paths['software_python'] / 'main' / 'main.py'
        if python_main.exists():
            with open(python_main, 'r', encoding='utf-8') as f:
                python_code = f.read()
                examples_content.append(f"\n### Python Code Example\n\n```python\n{python_code}\n```")
        
        return '\n'.join(examples_content)
    
    def escape_latex_special_chars(self, text: str) -> str:
        """Escapa caracteres especiales de LaTeX"""
        # Mapeo de caracteres especiales
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
    
    def convert_markdown_to_latex(self, content: str) -> str:
        """Convierte contenido Markdown a LaTeX"""
        latex_content = content
        
        # Conversión de encabezados con reset forzado
        latex_content = re.sub(r'^# (.+)$', 
                              lambda m: f'\n\\setcounter{{section}}{{0}}\n\\section{{{self.escape_latex_special_chars(m.group(1))}}}\n', 
                              latex_content, flags=re.MULTILINE)
        
        latex_content = re.sub(r'^## (.+)$', 
                              lambda m: f'\\subsection{{{self.escape_latex_special_chars(m.group(1))}}}', 
                              latex_content, flags=re.MULTILINE)
        
        latex_content = re.sub(r'^### (.+)$', 
                              lambda m: f'\\subsubsection{{{self.escape_latex_special_chars(m.group(1))}}}', 
                              latex_content, flags=re.MULTILINE)
        
        # Convertir imágenes con rutas relativas
        def replace_image(match):
            alt_text = match.group(1)
            image_path = match.group(2)
            
            # Normalizar rutas relativas
            if image_path.startswith('resources/'):
                # Quitar el prefijo 'resources/' ya que las imágenes se copian al directorio docs
                image_name = image_path.replace('resources/', '')
            elif image_path.startswith('/resources/'):
                # Quitar el prefijo '/resources/' 
                image_name = image_path.replace('/resources/', '')
            else:
                # Usar la ruta tal como está
                image_name = image_path
            
            return f'\\begin{{figure}}[H]\n\\centering\n\\includegraphics[width=0.8\\textwidth]{{{image_name}}}\n\\caption{{{alt_text}}}\n\\end{{figure}}'
        
        # Convertir imágenes ![alt](path)
        latex_content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, latex_content)
        
        # Convertir bloques de código a lstlisting
        def replace_code_block(match):
            language = match.group(1) if match.group(1) else 'text'
            code = match.group(2).strip()
            return f'\\begin{{lstlisting}}[language={language}]\n{code}\n\\end{{lstlisting}}'
        
        latex_content = re.sub(r'```(\w*)\n(.*?)\n```', replace_code_block, 
                              latex_content, flags=re.DOTALL)
        
        # Convertir código inline
        latex_content = re.sub(r'`([^`]+)`', r'\\texttt{\\footnotesize \1}', latex_content)
        
        # Convertir negrita e itálica
        latex_content = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', latex_content)
        latex_content = re.sub(r'\*(.+?)\*', r'\\textit{\1}', latex_content)
        
        # Convertir tablas
        latex_content = self.convert_tables_to_latex(latex_content)
        
        return latex_content
    
    def convert_tables_to_latex(self, content: str) -> str:
        """Convierte tablas Markdown a LaTeX"""
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
                    # Procesar tabla
                    latex_table = self.process_table(table_lines)
                    result_lines.append(latex_table)
                    in_table = False
                    table_lines = []
                result_lines.append(line)
        
        # Manejar tabla al final del contenido
        if in_table and table_lines:
            latex_table = self.process_table(table_lines)
            result_lines.append(latex_table)
        
        return '\n'.join(result_lines)
    
    def process_table(self, table_lines: List[str]) -> str:
        """Procesa una tabla individual"""
        if len(table_lines) < 2:
            return '\n'.join(table_lines)
        
        # Parsear encabezado
        header_line = table_lines[0].strip()
        headers = [cell.strip() for cell in header_line.split('|')[1:-1]]
        
        # Omitir línea separadora
        data_lines = table_lines[2:] if len(table_lines) > 2 else []
        
        # Crear especificación de columnas
        col_spec = 'l' * len(headers)
        
        # Iniciar tabla
        latex_table = [
            '\\begin{table}[H]',
            '\\centering',
            f'\\begin{{tabular}}{{{col_spec}}}',
            '\\toprule'
        ]
        
        # Agregar encabezado
        header_latex = ' & '.join([self.escape_latex_special_chars(h) for h in headers])
        latex_table.append(f'{header_latex} \\\\')
        latex_table.append('\\midrule')
        
        # Agregar filas de datos
        for data_line in data_lines:
            if '|' in data_line:
                cells = [cell.strip() for cell in data_line.split('|')[1:-1]]
                if len(cells) == len(headers):
                    row_latex = ' & '.join([self.escape_latex_special_chars(cell) for cell in cells])
                    latex_table.append(f'{row_latex} \\\\')
        
        # Terminar tabla
        latex_table.extend([
            '\\bottomrule',
            '\\end{tabular}',
            '\\end{table}',
            ''
        ])
        
        return '\n'.join(latex_table)
    
    def replace_template_variables(self, template_content: str, metadata: Dict) -> str:
        """Reemplaza variables en el template"""
        result = template_content
        
        # Reemplazar variables con formato $variable$
        for key, value in metadata.items():
            placeholder = f'${key}$'
            if placeholder in result:
                result = result.replace(placeholder, str(value))
                print(f"✓ Replaced {placeholder} with {value}")
        
        # Reemplazar bloques condicionales $if(variable)$...$else$...$endif$
        def replace_conditional(match):
            var_name = match.group(1)
            if_content = match.group(2)
            else_content = match.group(3) if match.group(3) else ''
            
            if var_name in metadata and metadata[var_name]:
                return if_content.replace(f'${var_name}$', str(metadata[var_name]))
            else:
                return else_content
        
        # Patrón para $if(var)$content$else$content$endif$
        result = re.sub(r'\$if\(([^)]+)\)\$(.*?)\$else\$(.*?)\$endif\$', 
                       replace_conditional, result, flags=re.DOTALL)
        
        # Patrón para $if(var)$content$endif$ (sin else)
        def replace_simple_conditional(match):
            var_name = match.group(1)
            if_content = match.group(2)
            
            if var_name in metadata and metadata[var_name]:
                return if_content.replace(f'${var_name}$', str(metadata[var_name]))
            else:
                return ''
        
        result = re.sub(r'\$if\(([^)]+)\)\$(.*?)\$endif\$', 
                       replace_simple_conditional, result, flags=re.DOTALL)
        
        return result
    
    def generate_latex_document(self, language: str = 'en', output_file: str = None) -> str:
        """Genera documento LaTeX completo"""
        if output_file is None:
            output_file = self.docs_dir / f'datasheet_{language}.tex'
        
        # Cargar template
        if not self.template_file.exists():
            raise FileNotFoundError(f"Template not found: {self.template_file}")
        
        with open(self.template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Cargar metadata y contenido
        metadata = self.load_base_metadata(language)
        content = self.load_content_from_files(language)
        
        # Convertir contenido a LaTeX
        latex_content = self.convert_markdown_to_latex(content)
        
        # Reemplazar variables del template
        result = self.replace_template_variables(template_content, metadata)
        
        # Insertar contenido antes de \end{document}
        if '\\end{document}' in result:
            result = result.replace('\\end{document}', 
                                  f'{latex_content}\n\n\\end{{document}}')
        else:
            result += f'\n\n{latex_content}\n\n\\end{{document}}'
        
        # Escribir archivo de salida
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        
        print(f"✓ LaTeX document generated: {output_file}")
        return str(output_file)
    
    def compile_pdf(self, latex_file: str, max_attempts: int = 3) -> bool:
        """Compila LaTeX a PDF"""
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
        
        # Verificación final
        pdf_file = latex_file.with_suffix('.pdf')
        if pdf_file.exists():
            file_size = pdf_file.stat().st_size
            print(f"✓ PDF generated: {pdf_file} ({file_size} bytes)")
            return True
        
        print("❌ PDF compilation failed after all attempts")
        return False

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Generate electronic module documentation')
    parser.add_argument('--language', '-l', default='en', choices=['en', 'es'],
                       help='Documentation language')
    parser.add_argument('--base-dir', '-d', 
                       help='Base directory of the project')
    
    args = parser.parse_args()
    
    print("Electronic Module Documentation Generator - Fixed Version")
    print("=" * 60)
    
    try:
        # Inicializar generador
        generator = LatexDocGenerator(args.base_dir)
        
        # Validar estructura del proyecto
        if not generator.path_config.validate_structure():
            print("❌ Project structure validation failed")
            return 1
        
        # Generar documento LaTeX
        latex_file = generator.generate_latex_document(args.language)
        
        # Compilar PDF
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
