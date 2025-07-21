#!/usr/bin/env python3
"""
Validador de Documentación de Desarrollo
Valida que la documentación siga las mejores prácticas para proyectos en desarrollo
"""

import yaml
import os
import sys
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class DevelopmentDocumentValidator:
    """Validador para documentación de proyectos en desarrollo"""
    
    def __init__(self, standards_file='document_standards.yaml'):
        self.standards_file = standards_file
        self.load_standards()
    
    def load_standards(self):
        """Cargar configuración de estándares de desarrollo"""
        try:
            with open(self.standards_file, 'r', encoding='utf-8') as f:
                self.standards = yaml.safe_load(f)['document_standards']
            logger.info("Configuración de desarrollo cargada correctamente")
        except FileNotFoundError:
            logger.error(f"Archivo de configuración no encontrado: {self.standards_file}")
            sys.exit(1)
        except yaml.YAMLError as e:
            logger.error(f"Error al cargar configuración YAML: {e}")
            sys.exit(1)
    
    def validate_metadata(self, metadata_file):
        """Validar metadata del documento de desarrollo"""
        logger.info(f"Validando metadata: {metadata_file}")
        
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Archivo de metadata no encontrado: {metadata_file}")
            return False
        except yaml.YAMLError as e:
            logger.error(f"Error al cargar metadata: {e}")
            return False
        
        errors = []
        warnings = []
        
        # Verificar campos requeridos
        required = self.standards['required_metadata']
        for field in required:
            if field not in metadata:
                errors.append(f"Campo requerido faltante: {field}")
        
        # Verificar que la clasificación sea apropiada para desarrollo
        classification = metadata.get('classification', '')
        valid_classifications = self.standards['classifications']
        if classification not in valid_classifications.values():
            warnings.append(f"Clasificación '{classification}' no es estándar para desarrollo")
        
        # Verificar que no se declaren estándares de certificación no cumplidos
        if 'standards' in metadata:
            standards_list = metadata['standards']
            if isinstance(standards_list, str):
                standards_list = [standards_list]
            
            # Buscar menciones de certificaciones no válidas
            invalid_standards = ['ISO 9001', 'CE', 'FCC', 'UL', 'IEC 61010']
            for standard in standards_list:
                for invalid in invalid_standards:
                    if invalid in standard and 'preparation' not in standard.lower() and 'goal' not in standard.lower():
                        errors.append(f"No declare certificación no obtenida: {standard}")
        
        # Verificar que la organización sea consistente
        org = metadata.get('organization', '')
        expected_org = self.standards['company']['name']
        if org != expected_org:
            warnings.append(f"Organización '{org}' difiere del estándar '{expected_org}'")
        
        # Verificar formato de versión para desarrollo
        version = metadata.get('version', '')
        if version and not any(x in version for x in ['Rev.', 'V.', 'v.']):
            warnings.append(f"Formato de versión '{version}' no sigue el estándar")
        
        # Reportar resultados
        if errors:
            logger.error("Errores encontrados en metadata:")
            for error in errors:
                logger.error(f"  - {error}")
        
        if warnings:
            logger.warning("Advertencias en metadata:")
            for warning in warnings:
                logger.warning(f"  - {warning}")
        
        if not errors and not warnings:
            logger.info("Metadata validada correctamente para desarrollo")
        
        return len(errors) == 0
    
    def validate_content(self, content_file):
        """Validar contenido del documento"""
        logger.info(f"Validando contenido: {content_file}")
        
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            logger.error(f"Archivo de contenido no encontrado: {content_file}")
            return False
        
        errors = []
        warnings = []
        
        # Verificar secciones recomendadas para desarrollo
        recommended_sections = self.standards['recommended_sections']
        for section in recommended_sections:
            if section.split('.')[1].strip().upper() not in content.upper():
                warnings.append(f"Sección recomendada faltante: {section}")
        
        # Verificar que se mencione el estado de desarrollo
        development_keywords = ['prototype', 'development', 'preliminary', 'testing', 'evaluation']
        if not any(keyword in content.lower() for keyword in development_keywords):
            warnings.append("El documento debería indicar claramente que es para desarrollo/prototipo")
        
        # Verificar que no se hagan afirmaciones de certificación
        certification_claims = ['certified', 'complies with', 'meets standard', 'certified to']
        for claim in certification_claims:
            if claim in content.lower():
                errors.append(f"Evite afirmaciones de certificación no verificadas: '{claim}'")
        
        # Reportar resultados
        if errors:
            logger.error("Errores encontrados en contenido:")
            for error in errors:
                logger.error(f"  - {error}")
        
        if warnings:
            logger.warning("Advertencias en contenido:")
            for warning in warnings:
                logger.warning(f"  - {warning}")
        
        if not errors and not warnings:
            logger.info("Contenido validado correctamente")
        
        return len(errors) == 0
    
    def generate_development_report(self, language='en'):
        """Generar reporte de estado de desarrollo"""
        logger.info(f"Generando reporte de desarrollo en {language}")
        
        # Validar archivos del idioma
        metadata_file = f"{language}/metadata.yaml"
        content_file = f"{language}/content.md"
        
        metadata_valid = self.validate_metadata(metadata_file)
        content_valid = self.validate_content(content_file)
        
        # Generar resumen
        print("\n" + "="*60)
        print(f"REPORTE DE VALIDACIÓN DE DESARROLLO ({language.upper()})")
        print("="*60)
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Fase del proyecto: {self.standards['project_status']['phase']}")
        print(f"Estado del hardware: {self.standards['project_status']['hardware_status']}")
        print(f"Estado de certificación: {self.standards['project_status']['certification_status']}")
        print()
        
        print("VALIDACIÓN:")
        print(f"  Metadata: {'✅ VÁLIDA' if metadata_valid else '❌ ERRORES'}")
        print(f"  Contenido: {'✅ VÁLIDO' if content_valid else '❌ ERRORES'}")
        print()
        
        if metadata_valid and content_valid:
            print("🎉 Documentación lista para desarrollo")
        else:
            print("⚠️  Corrija los errores antes de proceder")
        
        print("="*60)
        
        return metadata_valid and content_valid

def main():
    """Función principal"""
    validator = DevelopmentDocumentValidator()
    
    # Validar ambos idiomas
    languages = ['en', 'es']
    all_valid = True
    
    for lang in languages:
        if os.path.exists(f"{lang}/metadata.yaml"):
            valid = validator.generate_development_report(lang)
            all_valid = all_valid and valid
            print()
    
    sys.exit(0 if all_valid else 1)

if __name__ == "__main__":
    main()

import yaml
import os
from pathlib import Path
from typing import Dict, List, Set

class DocumentStandardsValidator:
    def __init__(self, standards_file: str = "document_standards.yaml"):
        self.standards_file = Path(standards_file)
        self.standards = self.load_standards()
        
    def load_standards(self) -> Dict:
        """Carga los estándares de documentación"""
        try:
            with open(self.standards_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error cargando estándares: {e}")
            return {}
    
    def validate_metadata(self, metadata_file: str) -> Dict:
        """Valida que los metadatos cumplan con los estándares"""
        results = {
            'valid': True,
            'missing_fields': [],
            'recommendations': [],
            'errors': []
        }
        
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = yaml.safe_load(f)
        except Exception as e:
            results['valid'] = False
            results['errors'].append(f"Error leyendo metadata: {e}")
            return results
        
        # Verificar campos obligatorios
        required_fields = self.standards['document_standards']['required_metadata']
        for field in required_fields:
            if field not in metadata:
                results['missing_fields'].append(field)
                results['valid'] = False
        
        # Verificar formato de versión
        if 'version' in metadata:
            version = metadata['version']
            if not version.startswith('Rev.'):
                results['recommendations'].append(
                    f"La versión '{version}' debería seguir el formato 'Rev. X.Y'"
                )
        
        # Verificar número de parte
        if 'partnumber' in metadata:
            partnumber = metadata['partnumber']
            if not any(pattern.replace('XXXXX', '') in partnumber 
                      for pattern in self.standards['document_standards']['part_numbering'].values()):
                results['recommendations'].append(
                    f"El número de parte '{partnumber}' no sigue los patrones estándar"
                )
        
        return results
    
    def validate_content_structure(self, content_file: str) -> Dict:
        """Valida la estructura del contenido"""
        results = {
            'valid': True,
            'missing_sections': [],
            'structure_issues': [],
            'recommendations': []
        }
        
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            results['valid'] = False
            results['structure_issues'].append(f"Error leyendo contenido: {e}")
            return results
        
        # Verificar secciones obligatorias
        required_sections = self.standards['document_standards']['required_sections']
        for section in required_sections:
            if section not in content:
                results['missing_sections'].append(section)
        
        # Verificar que tenga al menos el 70% de las secciones obligatorias
        if len(results['missing_sections']) > len(required_sections) * 0.3:
            results['valid'] = False
        
        # Verificar numeración de secciones
        lines = content.split('\n')
        section_numbers = []
        for line in lines:
            if line.startswith('# ') and any(char.isdigit() for char in line):
                # Extraer número de sección
                number_part = line.split('.')[0].replace('#', '').strip()
                if number_part.isdigit():
                    section_numbers.append(int(number_part))
        
        # Verificar secuencia
        for i, num in enumerate(section_numbers):
            if i > 0 and num != section_numbers[i-1] + 1:
                results['structure_issues'].append(
                    f"Salto en numeración de secciones: de {section_numbers[i-1]} a {num}"
                )
        
        return results
    
    def generate_compliance_report(self, lang_dir: str) -> Dict:
        """Genera un reporte de cumplimiento completo"""
        report = {
            'language': lang_dir,
            'timestamp': str(Path().cwd()),
            'overall_compliance': True,
            'metadata_validation': {},
            'content_validation': {},
            'recommendations': [],
            'summary': {}
        }
        
        # Validar metadatos
        metadata_file = f"{lang_dir}/metadata.yaml"
        if os.path.exists(metadata_file):
            report['metadata_validation'] = self.validate_metadata(metadata_file)
            if not report['metadata_validation']['valid']:
                report['overall_compliance'] = False
        else:
            report['overall_compliance'] = False
            report['metadata_validation'] = {
                'valid': False,
                'errors': ['Archivo metadata.yaml no encontrado']
            }
        
        # Validar contenido
        content_file = f"{lang_dir}/content.md"
        if os.path.exists(content_file):
            report['content_validation'] = self.validate_content_structure(content_file)
            if not report['content_validation']['valid']:
                report['overall_compliance'] = False
        else:
            report['overall_compliance'] = False
            report['content_validation'] = {
                'valid': False,
                'errors': ['Archivo content.md no encontrado']
            }
        
        # Generar resumen
        total_issues = (
            len(report['metadata_validation'].get('missing_fields', [])) +
            len(report['metadata_validation'].get('errors', [])) +
            len(report['content_validation'].get('missing_sections', [])) +
            len(report['content_validation'].get('structure_issues', []))
        )
        
        total_recommendations = (
            len(report['metadata_validation'].get('recommendations', [])) +
            len(report['content_validation'].get('recommendations', []))
        )
        
        report['summary'] = {
            'compliance_level': 'COMPLIANT' if report['overall_compliance'] else 'NON-COMPLIANT',
            'total_issues': total_issues,
            'total_recommendations': total_recommendations,
            'score': max(0, 100 - (total_issues * 10) - (total_recommendations * 2))
        }
        
        return report
    
    def print_report(self, report: Dict):
        """Imprime un reporte de cumplimiento formateado"""
        print(f"\n{'='*60}")
        print(f"REPORTE DE CUMPLIMIENTO DE ESTÁNDARES - {report['language'].upper()}")
        print(f"{'='*60}")
        
        print(f"\n📊 RESUMEN GENERAL:")
        print(f"   Estado: {report['summary']['compliance_level']}")
        print(f"   Puntuación: {report['summary']['score']}/100")
        print(f"   Problemas críticos: {report['summary']['total_issues']}")
        print(f"   Recomendaciones: {report['summary']['total_recommendations']}")
        
        # Metadatos
        if report['metadata_validation']:
            print(f"\n📄 VALIDACIÓN DE METADATOS:")
            meta = report['metadata_validation']
            print(f"   Estado: {'✅ VÁLIDO' if meta['valid'] else '❌ INVÁLIDO'}")
            
            if meta.get('missing_fields'):
                print(f"   Campos faltantes: {', '.join(meta['missing_fields'])}")
            
            if meta.get('errors'):
                print(f"   Errores: {'; '.join(meta['errors'])}")
            
            if meta.get('recommendations'):
                print(f"   Recomendaciones: {'; '.join(meta['recommendations'])}")
        
        # Contenido
        if report['content_validation']:
            print(f"\n📝 VALIDACIÓN DE CONTENIDO:")
            content = report['content_validation']
            print(f"   Estado: {'✅ VÁLIDO' if content['valid'] else '❌ INVÁLIDO'}")
            
            if content.get('missing_sections'):
                print(f"   Secciones faltantes: {len(content['missing_sections'])}")
                for section in content['missing_sections'][:5]:  # Mostrar solo las primeras 5
                    print(f"     - {section}")
                if len(content['missing_sections']) > 5:
                    print(f"     ... y {len(content['missing_sections']) - 5} más")
            
            if content.get('structure_issues'):
                print(f"   Problemas de estructura: {'; '.join(content['structure_issues'])}")
        
        print(f"\n{'='*60}\n")

def main():
    """Función principal"""
    validator = DocumentStandardsValidator()
    
    # Buscar directorios de idiomas
    lang_dirs = []
    for item in Path('.').iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            if (item / "content.md").exists() and (item / "metadata.yaml").exists():
                lang_dirs.append(item.name)
    
    if not lang_dirs:
        print("❌ No se encontraron directorios de idiomas válidos")
        return
    
    print(f"🔍 Validando estándares para {len(lang_dirs)} idioma(s)...")
    
    overall_compliance = True
    for lang_dir in sorted(lang_dirs):
        report = validator.generate_compliance_report(lang_dir)
        validator.print_report(report)
        
        if not report['overall_compliance']:
            overall_compliance = False
    
    # Resumen final
    print(f"🎯 RESULTADO FINAL: {'✅ TODOS LOS DOCUMENTOS CUMPLEN' if overall_compliance else '❌ HAY DOCUMENTOS NO CONFORMES'}")

if __name__ == "__main__":
    main()
