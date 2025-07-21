#!/usr/bin/env python3
"""
Generador LaTeX Final - Versión corregida y optimizada
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

class LatexDocGenerator:
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.docs_dir = self.base_dir / "docs"
        self.images_dir = self.base_dir / "images"
        self.template_file = self.base_dir / "template.tex"
        
        # Crear directorios
        self.docs_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
        
        # Copiar archivos esenciales (logo, etc.)
        self.copy_essential_files()
    
    def copy_essential_files(self):
        """Copia archivos esenciales como logos"""
        essential_files = ['logo.png', 'logo.jpg', 'logo.jpeg']
        
        for filename in essential_files:
            source_path = self.images_dir / filename
            if source_path.exists():
                dest_path = self.docs_dir / filename
                shutil.copy2(source_path, dest_path)
                print(f"✅ Copied {filename} to docs/")
                break
    
    def find_language_dirs(self) -> List[str]:
        """Encuentra directorios de idiomas"""
        lang_dirs = []
        for item in self.base_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                if (item / "content.md").exists() and (item / "metadata.yaml").exists():
                    lang_dirs.append(item.name)
        return sorted(lang_dirs)
    
    def load_metadata(self, lang_dir: str) -> Dict:
        """Carga metadatos"""
        metadata_file = self.base_dir / lang_dir / "metadata.yaml"
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error cargando metadatos para {lang_dir}: {e}")
            return {}
    
    def process_markdown(self, content: str, lang_dir: str) -> str:
        """Procesa markdown a LaTeX"""
        
        # 1. Headers
        content = re.sub(r'^# (.+)$', r'\\section{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.+)$', r'\\subsection{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^#### (.+)$', r'\\paragraph{\1}', content, flags=re.MULTILINE)
        
        # 2. Imágenes ANTES de procesar otros elementos
        content = self.process_images(content, lang_dir)
        
        # 3. Tablas
        content = self.process_tables(content)
        
        # 4. Listas
        content = self.process_lists(content)
        
        # 5. Formato de texto
        content = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', content)
        content = re.sub(r'\*(.*?)\*(?!\*)', r'\\textit{\1}', content)
        content = re.sub(r'`([^`]+)`', r'\\texttt{\1}', content)
        
        # 6. Enlaces
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\\href{\2}{\1}', content)
        
        # 7. Escapar caracteres especiales AL FINAL
        content = self.escape_latex_chars(content)
        
        return content
    
    def process_images(self, content: str, lang_dir: str) -> str:
        """Procesa imágenes markdown"""
        def replace_image(match):
            alt_text = match.group(1)
            image_path = match.group(2)
            
            # Buscar imagen en docs/resources/ (ya copiadas por workflow) o docs/
            dest_filename = None
            
            # Opción 1: buscar en docs/resources/ (copiadas por workflow)
            if image_path.startswith('resources/'):
                clean_path = image_path.replace('resources/', '')
                docs_resource_path = self.docs_dir / "resources" / clean_path
                if docs_resource_path.exists():
                    dest_filename = f"resources/{clean_path}"
            
            # Opción 2: buscar por nombre parcial en docs/resources/
            if not dest_filename:
                clean_path = image_path.replace('resources/', '').replace('images/', '')
                docs_resources_dir = self.docs_dir / "resources"
                if docs_resources_dir.exists():
                    for img_file in docs_resources_dir.glob("*"):
                        if (clean_path.lower() in img_file.name.lower() or 
                            img_file.stem.lower() in clean_path.lower()):
                            dest_filename = f"resources/{img_file.name}"
                            break
            
            # Opción 3: buscar en docs/ directamente
            if not dest_filename:
                clean_path = image_path.replace('resources/', '').replace('images/', '')
                docs_image_path = self.docs_dir / clean_path
                if docs_image_path.exists():
                    dest_filename = clean_path
            
            # Opción 4: fallback - copiar desde images/ si workflow no lo hizo
            if not dest_filename:
                source_path = None
                
                # Buscar en images/resources/
                if image_path.startswith('resources/') or not image_path.startswith('images/'):
                    clean_path = image_path.replace('resources/', '')
                    resource_path = self.images_dir / "resources" / clean_path
                    
                    if resource_path.exists():
                        source_path = resource_path
                        dest_filename = f"{lang_dir}_{resource_path.name}"
                    else:
                        # Buscar por nombre parcial en resources
                        resources_dir = self.images_dir / "resources"
                        if resources_dir.exists():
                            for img_file in resources_dir.glob("*"):
                                if (clean_path.lower() in img_file.name.lower() or 
                                    img_file.stem.lower() in clean_path.lower()):
                                    source_path = img_file
                                    dest_filename = f"{lang_dir}_{img_file.name}"
                                    break
                
                # Copiar imagen si la encontramos
                if source_path and source_path.exists():
                    dest_path = self.docs_dir / dest_filename
                    shutil.copy2(source_path, dest_path)
            
            if dest_filename:
                # Determinar ancho basado en el tipo de imagen
                width = "0.8\\textwidth"
                name_lower = dest_filename.lower()
                
                if any(keyword in name_lower for keyword in ['pinout', 'pin_out', 'diagram']):
                    width = "0.9\\textwidth"
                elif any(keyword in name_lower for keyword in ['dimension', 'size', 'physical']):
                    width = "0.6\\textwidth"
                elif any(keyword in name_lower for keyword in ['schematic', 'circuit']):
                    width = "\\textwidth"
                elif any(keyword in name_lower for keyword in ['block', 'topology', 'top', 'btm']):
                    width = "0.7\\textwidth"
                
                return f'''
\\begin{{figure}}[H]
\\centering
\\includegraphics[width={width}]{{{dest_filename}}}
\\caption{{{alt_text}}}
\\label{{fig:{dest_filename.replace('.', '-').replace('_', '-').replace('/', '-')}}}
\\end{{figure}}

'''
            
            return f"[Imagen no encontrada: {image_path}]"
        
        return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, content)
    
    def process_tables(self, content: str) -> str:
        """Procesa tablas markdown con títulos"""
        lines = content.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Detectar tabla
            if '|' in line and i + 1 < len(lines) and '|' in lines[i + 1]:
                # Buscar título de tabla en las líneas anteriores
                table_title = None
                
                # Buscar hacia atrás hasta 3 líneas para encontrar título
                for j in range(max(0, i-3), i):
                    if lines[j].strip().startswith('**Table') or lines[j].strip().startswith('**Tabla'):
                        table_title = lines[j].strip()
                        # Remover el título de result si ya fue agregado
                        if len(result) >= (i - j):
                            result = result[:-(i - j)]
                        break
                
                table_lines = []
                j = i
                
                # Recoger líneas de tabla
                while j < len(lines) and ('|' in lines[j] or lines[j].strip() == ''):
                    if '|' in lines[j]:
                        table_lines.append(lines[j])
                    j += 1
                
                if len(table_lines) >= 3:
                    latex_table = self.convert_table(table_lines, table_title)
                    result.append(latex_table)
                    i = j
                else:
                    result.append(line)
                    i += 1
            else:
                result.append(line)
                i += 1
        
        return '\n'.join(result)
    
    def convert_table(self, table_lines: List[str], table_title: str = None) -> str:
        """Convierte tabla a LaTeX con título opcional"""
        if len(table_lines) < 3:
            return '\n'.join(table_lines)
        
        # Header
        header_parts = [cell.strip() for cell in table_lines[0].split('|') if cell.strip()]
        num_cols = len(header_parts)
        
        if num_cols == 0:
            return '\n'.join(table_lines)
        
        # Data rows (skip separator)
        data_rows = []
        for line in table_lines[2:]:
            parts = [cell.strip() for cell in line.split('|') if cell.strip()]
            if parts:
                # Ajustar columnas
                while len(parts) < num_cols:
                    parts.append('')
                data_rows.append(parts[:num_cols])
        
        if not data_rows:
            return '\n'.join(table_lines)
        
        # Determinar especificación de columnas
        if num_cols <= 3:
            col_spec = '|' + 'c|' * num_cols
        else:
            col_spec = '|' + 'l|' * num_cols
        
        # Procesar título si existe
        caption_text = "Technical Specifications"  # Default
        if table_title:
            # Extraer el texto del título, removiendo **Table X:** o **Tabla X:**
            import re
            title_match = re.search(r'\*\*(?:Table|Tabla)\s+\d+:\s*([^*]+)\*\*', table_title)
            if title_match:
                caption_text = title_match.group(1).strip()
        
        # Generar LaTeX
        latex = f'''
\\begin{{table}}[H]
\\centering
\\small
\\begin{{tabular}}{{{col_spec}}}
\\hline
'''
        
        # Header
        latex += ' & '.join(header_parts) + ' \\\\\n\\hline\n'
        
        # Data rows
        for row in data_rows:
            latex += ' & '.join(row) + ' \\\\\n'
        
        latex += f'''\\hline
\\end{{tabular}}
\\caption{{{caption_text}}}
\\end{{table}}

'''
        
        return latex
    
    def process_lists(self, content: str) -> str:
        """Procesa listas"""
        lines = content.split('\n')
        result = []
        in_list = False
        list_type = None
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith('- ') or stripped.startswith('* '):
                if not in_list:
                    result.append('\\begin{itemize}')
                    in_list = True
                    list_type = 'itemize'
                elif list_type != 'itemize':
                    result.append(f'\\end{{{list_type}}}')
                    result.append('\\begin{itemize}')
                    list_type = 'itemize'
                
                item = stripped[2:].strip()
                result.append(f'\\item {item}')
                
            elif re.match(r'^\s*\d+\.\s', line):
                if not in_list:
                    result.append('\\begin{enumerate}')
                    in_list = True
                    list_type = 'enumerate'
                elif list_type != 'enumerate':
                    result.append(f'\\end{{{list_type}}}')
                    result.append('\\begin{enumerate}')
                    list_type = 'enumerate'
                
                item = re.sub(r'^\s*\d+\.\s*', '', line)
                result.append(f'\\item {item}')
                
            else:
                if in_list:
                    result.append(f'\\end{{{list_type}}}')
                    in_list = False
                    list_type = None
                result.append(line)
        
        if in_list:
            result.append(f'\\end{{{list_type}}}')
        
        return '\n'.join(result)
    
    def escape_latex_chars(self, text: str) -> str:
        """Escapa caracteres especiales y emojis"""
        lines = text.split('\n')
        result = []
        in_latex_env = False
        
        # Replace emojis with text equivalents first
        emoji_replacements = {
            '⚙️': 'Technical Specifications',
            '🔌': 'Pinout',
            '📏': 'Dimensions', 
            '📃': 'Topology',
            '🚀': '',
            '✅': '',
            '❌': '',
            '📊': '',
            '🧪': '',
            '📄': '',
            '📚': '',
            '🎯': '',
            '⚡': '',
            '🔧': '',
            '📦': '',
            '🌐': '',
            '💡': '',
            '🔥': '',
            '⭐': '',
            '🎉': '',
        }
        
        for emoji, replacement in emoji_replacements.items():
            text = text.replace(emoji, replacement)
        
        # Handle special Unicode characters
        special_chars = {
            'Ω': r'$\Omega$',
            '°': r'\degree',
            '±': r'$\pm$',
            'µ': r'$\mu$',
            '≤': r'$\leq$',
            '≥': r'$\geq$',
            '×': r'$\times$',
            '÷': r'$\div$',
            '√': r'$\sqrt{}$',
            '∞': r'$\infty$',
            'α': r'$\alpha$',
            'β': r'$\beta$',
            'γ': r'$\gamma$',
            'δ': r'$\delta$',
            'ε': r'$\varepsilon$',
            'θ': r'$\theta$',
            'λ': r'$\lambda$',
            'π': r'$\pi$',
            'σ': r'$\sigma$',
            'τ': r'$\tau$',
            'φ': r'$\phi$',
            'ω': r'$\omega$',
            '≥': r'$\geq$',
            '×': r'$\times$',
            '÷': r'$\div$',
            '²': r'$^2$',
            '³': r'$^3$',
            '½': r'$\frac{1}{2}$',
            '¼': r'$\frac{1}{4}$',
            '¾': r'$\frac{3}{4}$',
        }
        
        for char, replacement in special_chars.items():
            text = text.replace(char, replacement)
        
        lines = text.split('\n')
        
        for line in lines:
            # Detectar entornos LaTeX
            if ('\\begin{' in line or '\\end{' in line or 
                line.strip().startswith('\\') or
                '\\includegraphics' in line):
                in_latex_env = True
                result.append(line)
                continue
            
            if in_latex_env and (line.strip() == '' or '&' in line):
                result.append(line)
                continue
            else:
                in_latex_env = False
            
            # Escapar caracteres especiales solo en texto normal
            escape_chars = {
                '%': '\\%',
                '$': '\\$',
                '#': '\\#',
                '^': '\\textasciicircum{}',
                '_': '\\_',
                '~': '\\textasciitilde{}',
            }
            
            # Don't escape & in table environments
            if not ('|' in line and line.count('|') >= 2):
                escape_chars['&'] = '\\&'
            
            for char, replacement in escape_chars.items():
                # Don't escape if already escaped or in math mode
                if char not in ['$']:  # Don't double-escape math mode
                    line = re.sub(f'(?<!\\\\){re.escape(char)}(?![^$]*\\$)', replacement, line)
            
            result.append(line)
        
        return '\n'.join(result)
    
    def process_template(self, template: str, metadata: Dict) -> str:
        """Procesa template con soporte completo para condicionales Pandoc"""
        
        # Función para procesar condicionales de forma recursiva
        def process_conditionals(text):
            # Patrón para encontrar condicionales completos (incluyendo else opcional)
            pattern = r'\$if\(([^)]+)\)\$(.*?)(?:\$else\$(.*?))?\$endif\$'
            
            def replace_conditional(match):
                var_name = match.group(1)
                if_content = match.group(2) or ""
                else_content = match.group(3) or ""
                
                # Decidir qué contenido usar
                if var_name in metadata and metadata[var_name]:
                    result = if_content
                else:
                    result = else_content
                
                # Procesar condicionales anidados en el resultado
                return process_conditionals(result)
            
            # Mientras haya condicionales, seguir procesando
            while re.search(pattern, text, re.DOTALL):
                text = re.sub(pattern, replace_conditional, text, flags=re.DOTALL)
            
            return text
        
        # Procesar condicionales
        template = process_conditionals(template)
        
        # Función para obtener valor anidado de un diccionario
        def get_nested_value(data, key_path):
            """Obtiene valor anidado usando notación de punto"""
            keys = key_path.split('.')
            value = data
            try:
                for key in keys:
                    if isinstance(value, dict) and key in value:
                        value = value[key]
                    else:
                        return None
                return value
            except:
                return None
        
        # Reemplazar variables anidadas primero (ej: hardware_license.type)
        nested_pattern = r'\$([a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_.]*)\$'
        def replace_nested(match):
            key_path = match.group(1)
            value = get_nested_value(metadata, key_path)
            return str(value) if value is not None else f"${key_path}$"
        
        template = re.sub(nested_pattern, replace_nested, template)
        
        # Reemplazar variables simples
        for key, value in metadata.items():
            if value is not None:
                template = template.replace(f'${key}$', str(value))
        
        # Limpiar variables no definidas (reemplazar con valores por defecto)
        default_values = {
            'title': 'Hardware Module Documentation',
            'partnumber': 'HW-XXXXX-001',
            'version': 'Rev. 1.0',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'author': 'Development Team',
            'organization': 'UNIT Electronics'
        }
        
        for var, default in default_values.items():
            template = template.replace(f'${var}$', default)
        
        return template
        default_values = {
            'title': 'Hardware Documentation',
            'subtitle': 'Technical Specifications',
            'author': 'Engineering Team',
            'date': '2025-07-21',
            'version': 'Rev. 1.0',
            'organization': 'DevLab Electronics',
            'partnumber': 'HW-001',
            'classification': 'Public Technical Document',
            'standards': 'IEEE Std 1149.1, IPC-2221'
        }
        
        for key, default_value in default_values.items():
            template = template.replace(f'${key}$', default_value)
        
        # Limpiar cualquier variable restante no procesada
        template = re.sub(r'\$[a-zA-Z_][a-zA-Z0-9_]*\$', '', template)
        
        return template
    
    def generate_document(self, lang_dir: str) -> str:
        """Genera documento completo"""
        # Cargar metadatos
        metadata = self.load_metadata(lang_dir)
        
        # Leer contenido
        content_file = self.base_dir / lang_dir / "content.md"
        with open(content_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convertir a LaTeX
        latex_content = self.process_markdown(markdown_content, lang_dir)
        metadata['body'] = latex_content
        
        # Procesar template
        with open(self.template_file, 'r', encoding='utf-8') as f:
            template = f.read()
        
        return self.process_template(template, metadata)
    
    def compile_pdf(self, tex_file: Path) -> bool:
        """Compila PDF"""
        try:
            original_dir = os.getcwd()
            os.chdir(self.docs_dir)
            
            # Crear paths relativos al directorio docs
            tex_filename = tex_file.name
            pdf_filename = tex_filename.replace('.tex', '.pdf')
            
            # Compilar 3 veces para referencias cruzadas
            for i in range(3):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', tex_filename],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace'
                )
                
                if "Fatal error" in result.stdout:
                    print(f"Error fatal: {result.stdout[-800:]}")
                    return False
            
            # Verificar PDF - usando path relativo al directorio docs
            pdf_path = Path(pdf_filename)
            if pdf_path.exists():
                size = pdf_path.stat().st_size
                if size > 1000:
                    # Limpiar archivos auxiliares opcionales
                    for ext in ['.aux', '.out', '.toc', '.lof', '.lot']:
                        aux_file = Path(tex_filename.replace('.tex', ext))
                        if aux_file.exists():
                            try:
                                aux_file.unlink()
                            except:
                                pass  # No es crítico si no se pueden eliminar
                    return True
                else:
                    print(f"❌ PDF demasiado pequeño: {size} bytes")
                    return False
            else:
                print(f"❌ PDF no generado")
                return False
            
        except Exception as e:
            print(f"Error compilación: {e}")
            return False
        finally:
            os.chdir(original_dir)
    
    def generate_all(self):
        """Genera todos los documentos"""
        langs = self.find_language_dirs()
        
        if not langs:
            print("No se encontraron idiomas válidos")
            return
        
        print(f"Procesando idiomas: {', '.join(langs)}")
        
        for lang in langs:
            print(f"\n📝 Procesando {lang}...")
            
            try:
                # Generar LaTeX
                latex_doc = self.generate_document(lang)
                tex_file = self.docs_dir / f"datasheet_{lang}.tex"
                
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(latex_doc)
                
                print(f"✅ LaTeX generado: {tex_file}")
                
                # Compilar PDF
                if self.compile_pdf(tex_file):
                    pdf_file = tex_file.with_suffix('.pdf')
                    size_kb = pdf_file.stat().st_size // 1024
                    print(f"✅ PDF generado: {pdf_file} ({size_kb} KB)")
                else:
                    print(f"❌ Error compilando PDF para {lang}")
                    
            except Exception as e:
                print(f"❌ Error procesando {lang}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generador de Documentación LaTeX")
    parser.add_argument('--lang', help='Idioma específico')
    parser.add_argument('--dir', default='.', help='Directorio base')
    
    args = parser.parse_args()
    
    generator = LatexDocGenerator(args.dir)
    
    if args.lang:
        print(f"🚀 Generando para {args.lang}...")
        try:
            latex_doc = generator.generate_document(args.lang)
            tex_file = generator.docs_dir / f"datasheet_{args.lang}.tex"
            
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_doc)
            
            print(f"✅ LaTeX generado: {tex_file}")
            
            if generator.compile_pdf(tex_file):
                pdf_file = tex_file.with_suffix('.pdf')
                size_kb = pdf_file.stat().st_size // 1024
                print(f"✅ PDF generado: {pdf_file} ({size_kb} KB)")
            else:
                print(f"❌ Error compilando PDF")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        generator.generate_all()

if __name__ == "__main__":
    main()
