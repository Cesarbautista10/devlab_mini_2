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
        # Detectar la raíz del proyecto automáticamente
        current_path = Path(base_dir).resolve()
        
        # Si estamos en software/build/, subir dos niveles para llegar a la raíz
        if current_path.name == "build" and current_path.parent.name == "software":
            self.base_dir = current_path.parent.parent
        # Si estamos en software/, subir un nivel
        elif current_path.name == "software":
            self.base_dir = current_path.parent
        # Si ya estamos en la raíz o en un directorio diferente, usar tal como está
        else:
            self.base_dir = current_path
            
        print(f"📂 Base directory set to: {self.base_dir}")
        
        self.docs_dir = self.base_dir / "docs"
        self.images_dir = self.base_dir / "images"
        self.hardware_resources_dir = self.base_dir / "hardware" / "resources"
        self.template_file = self.base_dir / "template.tex"
        
        # Crear directorios
        self.docs_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
        
        # NUEVO: Crear directorios adicionales para imágenes
        self.create_additional_image_dirs()
        
        # Copiar archivos esenciales (logo, etc.)
        self.copy_essential_files()
    
    def create_additional_image_dirs(self):
        """Crea directorios adicionales para imágenes si no existen"""
        additional_dirs = [
            self.base_dir / "assets",
            self.base_dir / "media",
            self.base_dir / "docs" / "assets",
            self.images_dir / "custom"
        ]
        
        for dir_path in additional_dirs:
            dir_path.mkdir(exist_ok=True, parents=True)
            
        print("📁 Directorios de imágenes adicionales creados/verificados:")
        print("   - assets/")
        print("   - media/") 
        print("   - docs/assets/")
        print("   - images/custom/")
    
    def copy_essential_files(self):
        """Copia archivos esenciales como logos"""
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
                        print(f"✅ Copied {filename} from hardware/resources/img/ to docs/")
                        return
        
        # Fallback a la ubicación antigua
        for filename in essential_files:
            source_path = self.images_dir / filename
            if source_path.exists():
                dest_path = self.docs_dir / filename
                shutil.copy2(source_path, dest_path)
                print(f"✅ Copied {filename} to docs/")
                break
    
    def find_language_dirs(self) -> List[str]:
        """Define idiomas predefinidos sin necesidad de directorios existentes"""
        # Siempre generar para estos idiomas usando READMEs
        return ['en', 'es']
    
    def load_metadata(self, lang_dir: str) -> Dict:
        """Genera metadatos automáticamente desde archivos de configuración"""
        # Generar metadatos automáticamente desde project_metadata.yaml y document_standards.yaml
        return self.load_base_metadata(lang_dir)
    
    def create_temp_lang_dir(self, lang: str) -> Path:
        """Crea un directorio temporal para el idioma especificado"""
        temp_lang_dir = self.base_dir / lang
        temp_lang_dir.mkdir(exist_ok=True)
        
        # Generar metadatos automáticamente en build/ para conservar
        build_metadata_file = self.base_dir / "software" / "build" / f"metadata_{lang}.yaml"
        
        # Siempre regenerar metadatos desde configuración
        default_metadata = self.load_base_metadata(lang)
        
        with open(build_metadata_file, 'w', encoding='utf-8') as f:
            yaml.dump(default_metadata, f, default_flow_style=False, allow_unicode=True)
        print(f"📝 Generated metadata for {lang} in software/build/metadata_{lang}.yaml")
        
        # También crear copia temporal para el proceso
        metadata_file = temp_lang_dir / "metadata.yaml"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            yaml.dump(default_metadata, f, default_flow_style=False, allow_unicode=True)
        
        return temp_lang_dir
    
    def load_base_metadata(self, lang: str) -> Dict:
        """Carga metadatos base desde múltiples fuentes o usa valores por defecto - VERSIÓN SIMPLIFICADA"""
        
        # Metadatos por defecto genéricos
        default_metadata = {
            'title': "ICP-10111 Barometric Pressure Sensor",
            'subtitle': "Technical Datasheet and Development Guide", 
            'author': "UNIT Electronics",
            'date': datetime.now().strftime("%B %Y"),
            'version': "1.0.0",
            'product_name': "ICP-10111 Barometric Pressure Sensor",
            'product_sku': "UE0094",
            'language': lang,
            'language_name': lang.upper(),
            'copyright': f"© {datetime.now().year} UNIT Electronics. All rights reserved.",
            'logo': "logo.png",
            'organization': "UNIT Electronics",
            'division': "Hardware Development",
            'contact': "support@unitelectronics.com",
            'website': "www.unitelectronics.com",
            'project_phase': "Production",
            'hardware_status': "Released"
        }
        
        # Intentar cargar desde project_metadata.yaml de forma segura
        project_metadata_file = self.base_dir / "project_metadata.yaml"
        if project_metadata_file.exists():
            try:
                with open(project_metadata_file, 'r', encoding='utf-8') as f:
                    project_meta = yaml.safe_load(f) or {}
                
                # Cargar solo los campos básicos de forma segura
                if isinstance(project_meta, dict):
                    # Si tiene wrapper 'project_metadata'
                    meta = project_meta.get('project_metadata', project_meta)
                    
                    # Mapeo directo y seguro
                    safe_mappings = {
                        'title': meta.get('title') or meta.get('product_title') or meta.get('name'),
                        'author': meta.get('author') or meta.get('company') or meta.get('organization'),
                        'product_sku': meta.get('product_sku') or meta.get('sku') or meta.get('part_number'),
                        'version': meta.get('version') or meta.get('product_version')
                    }
                    
                    # Aplicar solo valores no nulos
                    for key, value in safe_mappings.items():
                        if value:
                            default_metadata[key] = value
                
                print(f"📋 Loaded metadata from project_metadata.yaml")
                
            except Exception as e:
                print(f"⚠️  Could not load project_metadata.yaml: {e}")
        else:
            print(f"📋 Using default metadata (no project_metadata.yaml found)")
        
        return default_metadata
    
    def cleanup_temp_lang_dir(self, lang: str):
        """Elimina el directorio temporal del idioma especificado"""
        temp_lang_dir = self.base_dir / lang
        if temp_lang_dir.exists():
            # Solo eliminar si es un directorio temporal (verificar si tiene content.md generado)
            content_file = temp_lang_dir / "content.md"
            if content_file.exists():
                try:
                    shutil.rmtree(temp_lang_dir)
                    print(f"🗑️  Cleaned up temporary directory: {lang}/")
                except Exception as e:
                    print(f"⚠️  Could not clean up {lang}/: {e}")
    
    def generate_content_from_readmes(self, lang_dir: str) -> str:
        """Genera contenido automáticamente desde READMEs de hardware y software"""
        content_parts = []
        
        # Encabezado principal
        content_parts.append("# SCOPE AND PURPOSE")
        content_parts.append("")
        content_parts.append("## Document Scope")
        content_parts.append("")
        content_parts.append("This technical datasheet provides comprehensive specifications, electrical characteristics, mechanical dimensions, and application guidelines for the ICP-10111 Barometric Pressure Sensor module. This document is intended for design engineers, system integrators, and technical personnel involved in the development and integration of environmental sensing solutions.")
        content_parts.append("")
        
        # Hardware section desde hardware/README.md
        hardware_readme = self.base_dir / "hardware" / "README.md"
        if hardware_readme.exists():
            content_parts.append("# HARDWARE DOCUMENTATION")
            content_parts.append("")
            try:
                with open(hardware_readme, 'r', encoding='utf-8') as f:
                    hardware_content = f.read()
                    
                # Procesar contenido del hardware README
                # Remover el primer # ya que lo reemplazamos
                lines = hardware_content.split('\n')
                skip_first_header = False
                
                for line in lines:
                    if line.startswith('# ') and not skip_first_header:
                        skip_first_header = True
                        continue
                    
                    # Ajustar niveles de headers (SOLO niveles 1-3)
                    if line.startswith('## '):
                        line = line.replace('## ', '## ')
                    elif line.startswith('### '):
                        line = line.replace('### ', '### ')
                    elif line.startswith('#### '):
                        # CONVERTIR nivel 4 a texto bold
                        title = line.replace('#### ', '')
                        line = f"**{title}**"
                    elif line.startswith('##### '):
                        # CONVERTIR nivel 5 a texto bold
                        title = line.replace('##### ', '')
                        line = f"**{title}**"
                    
                    # Ajustar rutas de imágenes para apuntar a hardware/resources
                    if '![' in line and '](' in line:
                        # Reemplazar rutas relativas con rutas desde hardware/resources
                        line = re.sub(r'!\[([^\]]*)\]\(images/([^)]+)\)', 
                                    r'![\1](unit_\2)', line)
                        line = re.sub(r'!\[([^\]]*)\]\(([^/)][^)]+)\)', 
                                    r'![\1](\2)', line)
                    
                    content_parts.append(line)
                    
            except Exception as e:
                print(f"Warning: No se pudo leer hardware/README.md: {e}")
                content_parts.append("Hardware documentation not available.")
        
        content_parts.append("")
        content_parts.append("")
        
        # Software section - SE PROCESARÁ INDEPENDIENTEMENTE
        # No añadir nada aquí - se maneja en generate_software_documentation()
        
        return '\n'.join(content_parts)
    
    def process_markdown(self, content: str, lang_dir: str) -> str:
        """Procesa markdown a LaTeX con orden correcto"""
        
        # 1. Bloques de código PRIMERO (para proteger contenido)
        content = self.process_code_blocks(content)
        
        # 2. Headers
        content = re.sub(r'^# (.+)$', r'\\section{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.+)$', r'\\subsection{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^#### (.+)$', r'\\paragraph{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^##### (.+)$', r'\\subparagraph{\1}', content, flags=re.MULTILINE)
        
        # 3. Imágenes
        content = self.process_images(content, lang_dir)
        
        # 4. Tablas
        content = self.process_tables(content)
        
        # 5. Listas (después de código)
        content = self.process_lists(content)
        
        # 6. Formato de texto (muy cuidadoso con el código)
        content = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', content)
        content = re.sub(r'\*(.*?)\*(?!\*)', r'\\textit{\1}', content)
        # Procesar código en línea de manera muy conservadora
        content = re.sub(r'`([^`\n\\{}#%$_&]+)`', r'\\texttt{\1}', content)
        
        # 7. Enlaces
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\\href{\2}{\1}', content)
        
        # 8. Escapar caracteres especiales AL FINAL
        content = self.escape_latex_chars(content)
        
        return content
    
    def process_markdown_no_headers(self, content: str, lang_dir: str) -> str:
        """Procesa markdown a LaTeX SIN procesar headers (ya procesados previamente)"""
        
        # 1. Bloques de código PRIMERO (para proteger contenido) - SALTADO, ya procesado
        # content = self.process_code_blocks(content)
        
        # 2. Headers - SALTADO, ya procesados por process_software_headers()
        
        # 3. Imágenes - SALTADO, ya procesadas
        # content = self.process_images(content, lang_dir)
        
        # 4. Tablas - SALTADO, ya procesadas
        # content = self.process_tables(content)
        
        # 5. Listas - SALTADO, ya procesadas
        # content = self.process_lists(content)
        
        # 6. Formato de texto - SALTADO, ya procesado
        # content = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', content)
        # content = re.sub(r'\*(.*?)\*(?!\*)', r'\\textit{\1}', content)
        # content = re.sub(r'`([^`\n\\{}#%$_&]+)`', r'\\texttt{\1}', content)
        
        # 7. Enlaces - SALTADO, ya procesados
        # content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\\href{\2}{\1}', content)
        
        # 8. Escapar caracteres especiales - YA HECHO SELECTIVAMENTE
        # content = self.escape_latex_chars(content)
        
        # Solo devolver el contenido tal cual - ya está completamente procesado
        return content
    
    def process_software_headers(self, content: str) -> str:
        """Procesa headers específicamente para SOFTWARE DOCUMENTATION con jerarquía correcta"""
        # SOFTWARE DOCUMENTATION es \section{}, entonces:
        # # headers -> \subsection{}
        # ## headers -> \subsubsection{}  
        # ### headers -> \paragraph{}
        # #### headers -> \subparagraph{}
        
        first_header_skipped = False
        lines = content.split('\n')
        processed_lines = []
        
        for line in lines:
            # Saltar solo el primer header principal (título del README)
            if line.startswith('# ') and not first_header_skipped:
                first_header_skipped = True
                continue
            
            # Procesar headers con jerarquía correcta para SOFTWARE
            if line.startswith('#### '):
                section_title = line.replace('#### ', '')
                processed_lines.append(f"\\subparagraph{{{section_title}}}")
            elif line.startswith('### '):
                section_title = line.replace('### ', '')
                processed_lines.append(f"\\paragraph{{{section_title}}}")
            elif line.startswith('## '):
                section_title = line.replace('## ', '')
                processed_lines.append(f"\\subsubsection{{{section_title}}}")
            elif line.startswith('# '):
                section_title = line.replace('# ', '')
                processed_lines.append(f"\\subsection{{{section_title}}}")
            else:
                processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def adjust_software_header_levels(self, content: str, abstract_content: str = "") -> str:
        """Ajusta los niveles de headers del software README para la jerarquía correcta"""
        # Como ya añadimos \section{SOFTWARE DOCUMENTATION} externamente,
        # necesitamos eliminar el primer header principal y ajustar todos los niveles
        # para que empiecen desde ## (subsection)
        
        lines = content.split('\n')
        processed_lines = []
        first_header_found = False
        
        # Añadir Abstract si se proporciona
        if abstract_content:
            processed_lines.append("## Abstract")
            processed_lines.append("")
            processed_lines.append(abstract_content)
            processed_lines.append("")
        
        for line in lines:
            # Eliminar el primer header principal ya que será reemplazado por \section{}
            if line.startswith('# ') and not first_header_found:
                first_header_found = True
                continue  # Saltar esta línea
            
            # Ajustar todos los headers para que estén en el nivel correcto
            # ## permanece como ## (\subsection)
            # ### permanece como ### (\subsubsection)  
            # #### permanece como #### (\paragraph)
            processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def generate_software_documentation(self) -> str:
        """Genera la documentación de SOFTWARE con numeración forzada línea por línea"""
        software_readme = self.base_dir / "software" / "README.md"
        if not software_readme.exists():
            return ""
        
        print(f"📋 Processing software README with FORCED numbering: {software_readme}")
        
        try:
            with open(software_readme, 'r', encoding='utf-8') as f:
                software_content = f.read()
                print(f"📋 Software README loaded: {len(software_content)} characters")
            
            # Procesar SOFTWARE con numeración completamente forzada
            lines = software_content.split('\n')
            processed_lines = []
            
            # Saltar el título principal del README y el párrafo descriptivo inicial
            skip_first_header = True
            skip_initial_paragraph = True
            subsection_counter = 0  # Contador manual para subsecciones (empezar en 0 para que Overview sea 3.1)
            
            for line in lines:
                # Saltar el primer header (título principal)
                if line.startswith('# ') and skip_first_header:
                    skip_first_header = False
                    continue
                
                # Saltar el párrafo inicial descriptivo Y las líneas vacías hasta llegar al primer ##
                if skip_initial_paragraph:
                    if line.startswith('##'):
                        skip_initial_paragraph = False
                    else:
                        continue  # Saltar TODO hasta el primer ##
                
                # Procesar cada línea con numeración FORZADA (SOLO niveles 1-3)
                if line.startswith('## '):
                    # Convertir ## a \subsection{} con numeración forzada SECUENCIAL
                    subsection_counter += 1  # Incrementar ANTES de usar
                    title = line.replace('## ', '')
                    processed_lines.append(f"\\setcounter{{subsection}}{{{subsection_counter - 1}}}")
                    processed_lines.append(f"\\setcounter{{subsubsection}}{{0}}")  # Reset subsubsection
                    processed_lines.append(f"\\subsection{{{title}}}")
                elif line.startswith('### '):
                    # Convertir ### a \subsubsection{}
                    title = line.replace('### ', '')
                    processed_lines.append(f"\\subsubsection{{{title}}}")
                elif line.startswith('#### '):
                    # ELIMINAR: No procesar niveles 4 - convertir a texto normal en bold
                    title = line.replace('#### ', '')
                    processed_lines.append(f"\\textbf{{{title}}}")
                    processed_lines.append("")  # Añadir línea vacía después
                elif line.startswith('##### '):
                    # ELIMINAR: No procesar niveles 5 - convertir a texto normal en bold
                    title = line.replace('##### ', '')
                    processed_lines.append(f"\\textbf{{{title}}}")
                    processed_lines.append("")  # Añadir línea vacía después
                else:
                    # Solo agregar líneas no vacías para evitar espaciado extra
                    if line.strip():  # Solo líneas con contenido
                        processed_lines.append(line)
                    elif processed_lines and processed_lines[-1].strip():  # Mantener solo una línea vacía después de contenido
                        processed_lines.append('')
            
            # Unir las líneas procesadas
            software_processed = '\n'.join(processed_lines)
            
            # Procesar otros elementos (imágenes, tablas, listas, etc.)
            software_processed = self.process_images(software_processed, 'en')
            software_processed = self.process_tables(software_processed)
            software_processed = self.process_lists(software_processed)
            software_processed = self.process_code_blocks(software_processed)
            
            # Formateo de texto
            software_processed = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', software_processed)
            software_processed = re.sub(r'\*(.*?)\*(?!\*)', r'\\textit{\1}', software_processed)
            software_processed = re.sub(r'`([^`\n\\{}#%$_&]+)`', r'\\texttt{\1}', software_processed)
            
            # Enlaces
            software_processed = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\\href{\2}{\1}', software_processed)
            
            # Escapar caracteres especiales
            software_processed = self.escape_latex_chars(software_processed)
            
            # Crear la sección SOFTWARE con TRIPLE forzado de numeración
            software_latex = []
            software_latex.append("\\clearpage")
            software_latex.append("\\newpage")  # Doble salto de página
            software_latex.append("")
            software_latex.append("% ===== COMPLETE RESET: SOFTWARE DOCUMENTATION =====")
            software_latex.append("% TRIPLE FORCE: Reset ALL LaTeX counters including deep levels")
            software_latex.append("")
            software_latex.append("% Level 1 - Complete counter reset")
            software_latex.append("\\setcounter{section}{2}")
            software_latex.append("\\setcounter{subsection}{0}")
            software_latex.append("\\setcounter{subsubsection}{0}")
            software_latex.append("\\setcounter{paragraph}{0}")
            software_latex.append("\\setcounter{subparagraph}{0}")
            software_latex.append("\\setcounter{equation}{0}")
            software_latex.append("\\setcounter{figure}{0}")
            software_latex.append("\\setcounter{table}{0}")
            software_latex.append("\\setcounter{footnote}{0}")
            software_latex.append("\\setcounter{page}{1}\\addtocounter{page}{-1}")  # Reset page counter effect
            software_latex.append("")
            software_latex.append("% Level 2 - Force section numbering format")
            software_latex.append("\\renewcommand{\\thesection}{3}")
            software_latex.append("\\renewcommand{\\thesubsection}{3.\\arabic{subsection}}")
            software_latex.append("\\renewcommand{\\thesubsubsection}{3.\\arabic{subsection}.\\arabic{subsubsection}}")
            software_latex.append("\\renewcommand{\\theparagraph}{3.\\arabic{subsection}.\\arabic{subsubsection}.\\arabic{paragraph}}")
            software_latex.append("\\renewcommand{\\thesubparagraph}{3.\\arabic{subsection}.\\arabic{subsubsection}.\\arabic{paragraph}.\\arabic{subparagraph}}")
            software_latex.append("")
            software_latex.append("% Level 3 - Force clean section start")
            software_latex.append("\\section{SOFTWARE DOCUMENTATION}")
            software_latex.append("")
            software_latex.append(software_processed)
            
            result = '\n'.join(software_latex)
            
            # Limpiar cualquier carácter problemático
            result = result.replace('\\#', '').replace('\n\n\n\n', '\n\n').replace('\n\n\n', '\n\n')
            
            print(f"📋 Software documentation processed with FORCED numbering")
            return result
            
        except Exception as e:
            print(f"Warning: No se pudo procesar software/README.md: {e}")
            return ""
    
    def process_images(self, content: str, lang_dir: str) -> str:
        """Procesa imágenes markdown con búsqueda ampliada en múltiples ubicaciones"""
        def replace_image(match):
            alt_text = match.group(1)
            image_path = match.group(2)
            
            # Buscar imagen en varios lugares - BÚSQUEDA AMPLIADA
            dest_filename = None
            
            # NUEVA: Opción 0 - Buscar primero en ubicaciones adicionales
            additional_search_dirs = [
                self.base_dir / "assets",
                self.base_dir / "media", 
                self.base_dir / "imgs",
                self.base_dir / "pictures",
                self.base_dir / lang_dir / "images",
                self.base_dir / lang_dir / "assets",
                self.base_dir / "docs" / "assets",
                self.base_dir / "software" / "assets"
            ]
            
            # Limpiar path de prefijos para búsqueda
            clean_path = image_path.replace('resources/', '').replace('images/', '').replace('assets/', '').replace('media/', '')
            
            # Buscar en directorios adicionales primero
            for search_dir in additional_search_dirs:
                if search_dir.exists():
                    # Búsqueda exacta
                    target_path = search_dir / clean_path
                    if target_path.exists():
                        dest_filename = clean_path
                        dest_path = self.docs_dir / dest_filename
                        shutil.copy2(target_path, dest_path)
                        print(f"✅ Copied {clean_path} from {search_dir.relative_to(self.base_dir)}/")
                        break
                    
                    # Búsqueda por patrón en el directorio
                    for img_file in search_dir.glob("**/*"):
                        if img_file.is_file() and img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.svg']:
                            if clean_path.lower() in img_file.name.lower() or img_file.stem.lower() in clean_path.lower():
                                dest_filename = img_file.name
                                dest_path = self.docs_dir / dest_filename
                                shutil.copy2(img_file, dest_path)
                                print(f"✅ Copied {img_file.name} from {search_dir.relative_to(self.base_dir)}/")
                                break
                    
                    if dest_filename:
                        break
            
            # Opción 1: buscar en hardware/resources/ directamente (ubicación original)
            if not dest_filename and self.hardware_resources_dir.exists():
                hardware_image_path = self.hardware_resources_dir / clean_path
                
                if hardware_image_path.exists():
                    dest_filename = clean_path
                    dest_path = self.docs_dir / dest_filename
                    shutil.copy2(hardware_image_path, dest_path)
                    print(f"✅ Copied {clean_path} from hardware/resources/")
                else:
                    # Buscar por nombre parcial en hardware/resources
                    best_match = None
                    for img_file in self.hardware_resources_dir.glob("**/*"):
                        if img_file.is_file() and img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.svg']:
                            # Mejorar la lógica de coincidencia
                            clean_name = clean_path.lower().replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
                            file_name = img_file.stem.lower()
                            
                            # Coincidencias específicas y generales
                            if (clean_name in file_name or file_name in clean_name or
                                ('pinout' in clean_name and 'pinout' in file_name) or
                                ('dimension' in clean_name and 'dimension' in file_name) or
                                ('block' in clean_name and ('topology' in file_name or 'block' in file_name)) or
                                ('topology' in clean_name and 'topology' in file_name)):
                                best_match = img_file
                                break
                    
                    if best_match:
                        dest_filename = best_match.name
                        dest_path = self.docs_dir / dest_filename
                        shutil.copy2(best_match, dest_path)
                        print(f"✅ Copied {best_match.name} from hardware/resources/")
            
            # Opción 2: buscar en docs/resources/ (copiadas por workflow)
            if not dest_filename and image_path.startswith('resources/'):
                clean_path = image_path.replace('resources/', '')
                docs_resource_path = self.docs_dir / "resources" / clean_path
                if docs_resource_path.exists():
                    dest_filename = f"resources/{clean_path}"
            
            # Opción 3: buscar por nombre parcial en docs/resources/
            if not dest_filename:
                clean_path = image_path.replace('resources/', '').replace('images/', '')
                docs_resources_dir = self.docs_dir / "resources"
                if docs_resources_dir.exists():
                    for img_file in docs_resources_dir.glob("*"):
                        if (clean_path.lower() in img_file.name.lower() or 
                            img_file.stem.lower() in clean_path.lower()):
                            dest_filename = f"resources/{img_file.name}"
                            break
            
            # Opción 4: buscar en docs/ directamente
            if not dest_filename:
                clean_path = image_path.replace('resources/', '').replace('images/', '')
                docs_image_path = self.docs_dir / clean_path
                if docs_image_path.exists():
                    dest_filename = clean_path
            
            # Opción 5: fallback - copiar desde images/ si workflow no lo hizo
            if not dest_filename:
                source_path = None
                
                # Buscar en images/resources/ (ubicación antigua)
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
        
        # Determinar especificación de columnas - formato más simple y eficiente
        if num_cols <= 2:
            col_spec = '|p{6cm}|p{6cm}|'
        elif num_cols == 3:
            col_spec = '|p{4cm}|p{4cm}|p{4cm}|'
        elif num_cols == 4:
            col_spec = '|p{3cm}|p{3cm}|p{3cm}|p{3cm}|'
        elif num_cols == 5:
            col_spec = '|p{2.4cm}|p{2.4cm}|p{2.4cm}|p{2.4cm}|p{2.4cm}|'
        else:
            # Para muchas columnas, usar tabularx con distribución automática
            col_spec = '|' + 'X|' * num_cols
        
        # Procesar título si existe
        caption_text = "Technical Specifications"  # Default
        if table_title:
            # Extraer el texto del título, removiendo **Table X:** o **Tabla X:**
            import re
            title_match = re.search(r'\*\*(?:Table|Tabla)\s+\d+:\s*([^*]+)\*\*', table_title)
            if title_match:
                caption_text = title_match.group(1).strip()
        
        # Generar LaTeX con tabularx para mejor control de ancho
        if num_cols > 5:
            latex = f'''
\\begin{{table}}[H]
\\centering
\\small
\\begin{{tabularx}}{{\\textwidth}}{{{col_spec}}}
\\hline
'''
        else:
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
        
        # Cerrar tabla según el tipo usado
        if num_cols > 5:
            latex += f'''\\hline
\\end{{tabularx}}
\\caption{{{caption_text}}}
\\end{{table}}

'''
        else:
            latex += f'''\\hline
\\end{{tabular}}
\\caption{{{caption_text}}}
\\end{{table}}

'''
        
        return latex
    
    def process_lists(self, content: str) -> str:
        """Procesa listas markdown con soporte para listas anidadas e indentación"""
        lines = content.split('\n')
        result = []
        list_stack = []  # Stack para manejar listas anidadas
        in_verbatim = False
        
        def close_lists_to_level(target_level):
            """Cierra listas hasta el nivel especificado"""
            while len(list_stack) > target_level:
                list_info = list_stack.pop()
                result.append(f'\\end{{{list_info["type"]}}}')
        
        def get_indent_level(line):
            """Obtiene el nivel de indentación de una línea"""
            return (len(line) - len(line.lstrip())) // 4  # 4 espacios = 1 nivel
        
        def is_list_item(line):
            """Determina si una línea es un elemento de lista"""
            stripped = line.strip()
            return (stripped.startswith('- ') or stripped.startswith('* ') or 
                   re.match(r'^\s*\d+\.\s', line))
        
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Detectar bloques verbatim para evitar procesarlos
            if '\\begin{verbatim}' in line:
                in_verbatim = True
            elif '\\end{verbatim}' in line:
                in_verbatim = False
            
            # No procesar listas dentro de bloques verbatim
            if in_verbatim:
                result.append(line)
                i += 1
                continue
            
            # No procesar como lista si es una sección LaTeX o Markdown header
            if (stripped.startswith('\\section') or stripped.startswith('\\subsection') or 
                stripped.startswith('\\subsubsection') or stripped.startswith('#')):
                close_lists_to_level(0)
                result.append(line)
                i += 1
                continue
            
            # Detectar elementos de lista con viñetas
            if stripped.startswith('- ') or stripped.startswith('* '):
                indent_level = get_indent_level(line)
                
                # Si ya tenemos una lista del mismo tipo y nivel, continuar con ella
                if (list_stack and len(list_stack) > indent_level and 
                    list_stack[indent_level]["type"] == "itemize" and
                    list_stack[indent_level]["level"] == indent_level):
                    # Continuar con la lista existente
                    pass
                else:
                    # Ajustar el stack de listas al nivel actual
                    close_lists_to_level(indent_level)
                    
                    # Si necesitamos una nueva lista en este nivel
                    if len(list_stack) <= indent_level:
                        result.append('\\begin{itemize}')
                        list_stack.append({"type": "itemize", "level": indent_level})
                
                item = stripped[2:].strip()
                result.append(f'\\item {item}')
                
            # Detectar listas numeradas
            elif re.match(r'^\s*\d+\.\s', line):
                indent_level = get_indent_level(line)
                
                # Para listas numeradas consecutivas al mismo nivel, mantener la misma lista
                # Solo crear nueva lista si cambia el nivel o no hay lista activa
                if not list_stack or list_stack[-1]["level"] != indent_level or list_stack[-1]["type"] != "enumerate":
                    # Ajustar el stack de listas al nivel actual
                    close_lists_to_level(indent_level)
                    
                    # Si necesitamos una nueva lista en este nivel
                    if len(list_stack) <= indent_level:
                        result.append('\\begin{enumerate}')
                        list_stack.append({"type": "enumerate", "level": indent_level})
                
                item = re.sub(r'^\s*\d+\.\s*', '', line)
                result.append(f'\\item {item}')
                
                # Procesar sublistas inmediatamente después del item
                j = i + 1
                while j < len(lines) and lines[j].strip() == '':
                    j += 1  # Saltar líneas vacías
                
                # Verificar si hay sublistas
                sublist_items = []
                while j < len(lines):
                    next_line = lines[j]
                    next_stripped = next_line.strip()
                    next_indent = get_indent_level(next_line)
                    
                    # Si es una sublista con mayor indentación
                    if ((next_stripped.startswith('- ') or next_stripped.startswith('* ')) and 
                        next_indent > indent_level):
                        sublist_items.append(next_line)
                        j += 1
                    elif next_stripped == '':
                        j += 1  # Saltar líneas vacías
                    else:
                        break
                
                # Procesar sublistas encontradas
                if sublist_items:
                    result.append('\\begin{itemize}')
                    for subitem_line in sublist_items:
                        subitem = subitem_line.strip()[2:].strip()
                        result.append(f'\\item {subitem}')
                    result.append('\\end{itemize}')
                    i = j - 1  # Ajustar índice ya que procesamos varias líneas
                
            else:
                # Línea que no es de lista
                if stripped == '':
                    # Línea vacía: mantener si no estamos en una lista activa
                    if not list_stack:
                        result.append(line)
                else:
                    # Contenido diferente: cerrar todas las listas si no es continuación
                    if not is_list_item(line):
                        close_lists_to_level(0)
                    result.append(line)
            
            i += 1
        
        # Cerrar cualquier lista abierta al final
        close_lists_to_level(0)
        
        return '\n'.join(result)
    
    def process_code_blocks(self, content: str) -> str:
        """Procesa bloques de código markdown con manejo de líneas largas"""
        lines = content.split('\n')
        result = []
        in_code_block = False
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Detectar inicio de bloque de código (``` o ````)
            if line.strip().startswith('```'):
                if not in_code_block:
                    # Inicio de bloque - usar lstlisting simple y aislado
                    language = line.strip()[3:].strip().lower()  # Extraer lenguaje
                    if language in ['c', 'cpp', 'python', 'bash', 'yaml', 'javascript']:
                        lang_param = f'language={language}'
                    else:
                        lang_param = 'language=text'
                    result.append('')  # Línea vacía antes
                    result.append('\\vspace{0.3em}')
                    result.append(f'\\begin{{lstlisting}}[{lang_param}, basicstyle=\\footnotesize\\ttfamily, frame=single, breaklines=true]')
                    in_code_block = True
                else:
                    # Fin de bloque
                    result.append('\\end{lstlisting}')
                    result.append('\\vspace{0.3em}')
                    result.append('')  # Línea vacía después
                    in_code_block = False
            elif in_code_block:
                # Dentro del bloque - dividir líneas muy largas
                if len(line) > 80:
                    # Dividir líneas largas en espacios o caracteres apropiados
                    chunks = []
                    current_line = line
                    while len(current_line) > 80:
                        # Buscar punto de división apropiado
                        break_point = 80
                        for char in [' ', ',', ';', '(', ')', '{', '}', '[', ']']:
                            pos = current_line.rfind(char, 0, 80)
                            if pos > 60:  # No dividir muy cerca del inicio
                                break_point = pos + 1
                                break
                        
                        chunks.append(current_line[:break_point])
                        current_line = '    ' + current_line[break_point:].lstrip()  # Indentar continuación
                    
                    chunks.append(current_line)
                    result.extend(chunks)
                else:
                    result.append(line)
            else:
                # Fuera del bloque de código
                result.append(line)
            
            i += 1
        
        # Si queda un bloque abierto, cerrarlo
        if in_code_block:
            result.append('\\end{verbatim}\\end{quote}')
        
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
            '✅': 'OK',
            '❌': 'ERROR',
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
            '🛠️': 'Tools',
            '⚠️': 'CAUTION',
            '❗': 'WARNING',
            'ℹ️': 'INFO',
            '💻': '',
            '🔍': '',
            '📋': '',
            '🏭': '',
            '⏰': '',
            '🎛️': '',
            '🚫': 'NOT ALLOWED',
            '🔒': 'SECURE',
            '🔓': 'OPEN',
            '📡': 'COMMUNICATION',
            '🔋': 'POWER',
            '🌡️': 'TEMPERATURE',
            '💾': 'STORAGE',
            '⚙': 'SETTINGS',
        }
        
        for emoji, replacement in emoji_replacements.items():
            text = text.replace(emoji, replacement)
        
        # Handle special Unicode characters
        special_chars = {
            'Ω': r'$\Omega$',
            '°': r'$^{\circ}$',
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
            
            # Escapar caracteres especiales solo en texto normal (muy simplificado)
            if not (line.strip().startswith('\\begin{verbatim}') or 
                   line.strip().startswith('\\end{verbatim}') or
                   'verbatim' in line):
                
                # Solo escapar los caracteres más problemáticos
                escape_chars = {
                    '%': '\\%',
                    '#': '\\#',
                }
                
                # Don't escape & in table environments
                if not ('|' in line and line.count('|') >= 2):
                    escape_chars['&'] = '\\&'
                
                for char, replacement in escape_chars.items():
                    line = line.replace(char, replacement)
            
            result.append(line)
        
        return '\n'.join(result)
    
    def escape_latex_chars_selective(self, text: str) -> str:
        """Escapa caracteres especiales excepto # para headers markdown"""
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
            '✅': 'OK',
            '❌': 'ERROR',
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
            '🛠️': 'Tools',
            '⚠️': 'CAUTION',
            '❗': 'WARNING',
            'ℹ️': 'INFO',
            '💻': '',
            '🔍': '',
            '📋': '',
            '🏭': '',
            '⏰': '',
            '🎛️': '',
            '🚫': 'NOT ALLOWED',
            '🔒': 'SECURE',
            '🔓': 'OPEN',
            '📡': 'COMMUNICATION',
            '🔋': 'POWER',
            '🌡️': 'TEMPERATURE',
            '💾': 'STORAGE',
            '⚙': 'SETTINGS',
        }
        
        for emoji, replacement in emoji_replacements.items():
            text = text.replace(emoji, replacement)
        
        # Handle special Unicode characters
        special_chars = {
            'Ω': r'$\Omega$',
            '°': r'$^{\circ}$',
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
            
            # Escapar caracteres especiales solo en texto normal (NO incluir #)
            if not (line.strip().startswith('\\begin{verbatim}') or 
                   line.strip().startswith('\\end{verbatim}') or
                   'verbatim' in line):
                
                # Solo escapar caracteres problemáticos EXCEPTO #
                escape_chars = {
                    '%': '\\%',
                    # NO escapar # para permitir headers markdown
                }
                
                # Don't escape & in table environments
                if not ('|' in line and line.count('|') >= 2):
                    escape_chars['&'] = '\\&'
                
                for char, replacement in escape_chars.items():
                    line = line.replace(char, replacement)
            
            result.append(line)
        
        return '\n'.join(result)
    
    def process_template(self, template: str, metadata: Dict) -> str:
        """Procesa template con soporte para condicionales de Pandoc"""
        
        # Procesar condicionales if-else-endif de Pandoc
        def process_pandoc_conditionals(text):
            # Patrón para $if(variable)$content$else$alternative$endif$
            pattern = r'\$if\(([^)]+)\)\$(.*?)(?:\$else\$(.*?))?\$endif\$'
            
            def replace_conditional(match):
                var_name = match.group(1).strip()
                if_content = match.group(2) if match.group(2) else ""
                else_content = match.group(3) if match.group(3) else ""
                
                # Si la variable existe y tiene valor, usar if_content, sino else_content
                if var_name in metadata and metadata[var_name]:
                    return if_content
                else:
                    return else_content
            
            # Aplicar reemplazos múltiples hasta que no haya más cambios
            prev_text = ""
            while prev_text != text:
                prev_text = text
                text = re.sub(pattern, replace_conditional, text, flags=re.DOTALL)
            
            return text
        
        # Aplicar procesamiento de condicionales
        template = process_pandoc_conditionals(template)
        
        # Reemplazar variables simples con sintaxis de Pandoc $variable$
        for key, value in metadata.items():
            if value is not None:
                template = template.replace(f'${key}$', str(value))
        
        # Limpiar variables restantes que no se procesaron
        template = re.sub(r'\$[a-zA-Z_][a-zA-Z0-9_]*\$', '', template)
        
        return template
    
    def generate_hardware_documentation(self, lang_dir: str) -> str:
        """Genera SOLO la documentación de HARDWARE de forma independiente"""
        print(f"📋 Processing HARDWARE documentation independently for {lang_dir}")
        
        # Generar contenido de SCOPE y HARDWARE desde READMEs
        content_parts = []
        
        # Encabezado principal
        content_parts.append("# SCOPE AND PURPOSE")
        content_parts.append("")
        content_parts.append("## Document Scope")
        content_parts.append("")
        content_parts.append("This technical datasheet provides comprehensive specifications, electrical characteristics, mechanical dimensions, and application guidelines for the ICP-10111 Barometric Pressure Sensor module. This document is intended for design engineers, system integrators, and technical personnel involved in the development and integration of environmental sensing solutions.")
        content_parts.append("")
        
        # Hardware section desde hardware/README.md
        hardware_readme = self.base_dir / "hardware" / "README.md"
        if hardware_readme.exists():
            content_parts.append("# HARDWARE DOCUMENTATION")
            content_parts.append("")
            try:
                with open(hardware_readme, 'r', encoding='utf-8') as f:
                    hardware_content = f.read()
                    
                # Procesar contenido del hardware README
                lines = hardware_content.split('\n')
                skip_first_header = False
                
                for line in lines:
                    if line.startswith('# ') and not skip_first_header:
                        skip_first_header = True
                        continue
                    
                    # Ajustar rutas de imágenes
                    if '![' in line and '](' in line:
                        line = re.sub(r'!\[([^\]]*)\]\(images/([^)]+)\)', r'![\1](unit_\2)', line)
                        line = re.sub(r'!\[([^\]]*)\]\(([^/)][^)]+)\)', r'![\1](\2)', line)
                    
                    content_parts.append(line)
                    
            except Exception as e:
                print(f"Warning: No se pudo leer hardware/README.md: {e}")
                content_parts.append("Hardware documentation not available.")
        
        hardware_markdown = '\n'.join(content_parts)
        
        # Convertir a LaTeX
        hardware_latex = self.process_markdown(hardware_markdown, lang_dir)
        
        # Limpiar caracteres problemáticos
        hardware_latex = hardware_latex.replace('\\#', '').replace('\n\n\n\n', '\n\n').replace('\n\n\n', '\n\n')
        
        print(f"� HARDWARE documentation processed independently")
        return hardware_latex

    def generate_document(self, lang_dir: str) -> str:
        """Genera documento completo procesando HARDWARE y SOFTWARE por separado"""
        # Si el directorio no existe, crearlo temporalmente
        temp_dir_created = False
        lang_path = self.base_dir / lang_dir
        
        if not lang_path.exists():
            self.create_temp_lang_dir(lang_dir)
            temp_dir_created = True
            print(f"📁 Created temporary directory for {lang_dir}")
        
        # Cargar metadatos
        metadata = self.load_metadata(lang_dir)
        
        print(f"🔄 GENERATING DOCUMENT WITH SEPARATE PROCESSING")
        print(f"   Step 1: Processing HARDWARE independently")
        print(f"   Step 2: Processing SOFTWARE independently") 
        print(f"   Step 3: Merging both sections")
        
        # PASO 1: Generar HARDWARE de forma completamente independiente
        hardware_latex = self.generate_hardware_documentation(lang_dir)
        
        # PASO 2: Generar SOFTWARE de forma completamente independiente
        software_latex = self.generate_software_documentation()
        
        # PASO 3: Fusionar ambas secciones
        final_latex_content = hardware_latex
        
        if software_latex:
            # Añadir SOFTWARE con separación clara
            final_latex_content += "\n" + software_latex
            print(f"📋 HARDWARE and SOFTWARE sections merged successfully")
        else:
            print(f"⚠️  SOFTWARE section was empty, using only HARDWARE")
        
        # Guardar content.md para debugging si es directorio temporal
        if temp_dir_created:
            content_file = self.base_dir / lang_dir / "content.md"
            debug_content = "# Document generated from separate HARDWARE and SOFTWARE processing\n\n"
            debug_content += "This content.md is for debugging purposes only.\n"
            debug_content += "The actual LaTeX is generated by merging independent sections.\n"
            with open(content_file, 'w', encoding='utf-8') as f:
                f.write(debug_content)
            print(f"✅ Debug content saved to {content_file}")
        
        metadata['body'] = final_latex_content
        
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
                    
                # Limpiar directorio temporal si fue creado
                self.cleanup_temp_lang_dir(lang)
                    
            except Exception as e:
                print(f"❌ Error procesando {lang}: {e}")
                # Limpiar directorio temporal incluso si hay error
                self.cleanup_temp_lang_dir(lang)

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
            
            # Limpiar directorio temporal si fue creado
            generator.cleanup_temp_lang_dir(args.lang)
                
        except Exception as e:
            print(f"❌ Error: {e}")
            # Limpiar directorio temporal incluso si hay error
            generator.cleanup_temp_lang_dir(args.lang)
    else:
        generator.generate_all()

if __name__ == "__main__":
    main()
