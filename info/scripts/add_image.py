#!/usr/bin/env python3
"""
Utilidad para Añadir Imágenes al Proyecto
Permite agregar imágenes fácilmente en cualquier ubicación permitida
"""

import os
import shutil
import argparse
from pathlib import Path
from typing import List

class ImageManager:
    """Gestor de imágenes para el proyecto de documentación"""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.available_locations = {
            'assets': self.base_dir / "assets",
            'media': self.base_dir / "media", 
            'hardware': self.base_dir / "hardware" / "resources",
            'hardware-img': self.base_dir / "hardware" / "resources" / "img",
            'docs-assets': self.base_dir / "docs" / "assets",
            'images': self.base_dir / "images",
            'images-custom': self.base_dir / "images" / "custom",
            'en-images': self.base_dir / "en" / "images",
            'es-images': self.base_dir / "es" / "images"
        }
        
        # Crear directorios que no existan
        self.create_directories()
    
    def create_directories(self):
        """Crea todos los directorios de imágenes disponibles"""
        for name, path in self.available_locations.items():
            path.mkdir(parents=True, exist_ok=True)
        print("📁 Directorios de imágenes disponibles creados/verificados")
    
    def list_locations(self):
        """Lista todas las ubicaciones disponibles para imágenes"""
        print("\n🗂️  Ubicaciones disponibles para imágenes:")
        print("=" * 50)
        
        for name, path in self.available_locations.items():
            status = "✅" if path.exists() else "❌"
            rel_path = path.relative_to(self.base_dir)
            print(f"{status} {name:15} -> {rel_path}")
        
        print("\n💡 Puedes usar cualquiera de estas ubicaciones para tus imágenes")
        print("   El sistema de generación las encontrará automáticamente")
    
    def add_image(self, source_path: str, destination: str, custom_name: str = None):
        """
        Añade una imagen a la ubicación especificada
        
        Args:
            source_path: Ruta de la imagen a copiar
            destination: Nombre de la ubicación de destino
            custom_name: Nombre personalizado para el archivo (opcional)
        """
        source = Path(source_path)
        
        # Validar archivo fuente
        if not source.exists():
            print(f"❌ Error: El archivo {source_path} no existe")
            return False
        
        if not source.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']:
            print(f"❌ Error: {source.suffix} no es un formato de imagen válido")
            return False
        
        # Validar destino
        if destination not in self.available_locations:
            print(f"❌ Error: '{destination}' no es una ubicación válida")
            print(f"   Ubicaciones disponibles: {', '.join(self.available_locations.keys())}")
            return False
        
        dest_dir = self.available_locations[destination]
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Determinar nombre del archivo
        if custom_name:
            # Mantener la extensión original
            dest_name = custom_name
            if not dest_name.endswith(source.suffix):
                dest_name += source.suffix
        else:
            dest_name = source.name
        
        dest_path = dest_dir / dest_name
        
        try:
            shutil.copy2(source, dest_path)
            rel_dest = dest_path.relative_to(self.base_dir)
            print(f"✅ Imagen copiada exitosamente:")
            print(f"   Desde: {source}")
            print(f"   Hacia: {rel_dest}")
            
            # Mostrar cómo referenciar la imagen en markdown
            self.show_markdown_usage(dest_name, destination)
            return True
            
        except Exception as e:
            print(f"❌ Error al copiar imagen: {e}")
            return False
    
    def show_markdown_usage(self, filename: str, location: str):
        """Muestra cómo usar la imagen en markdown"""
        print(f"\n📝 Para usar esta imagen en tu documentación:")
        
        # Diferentes formas de referenciar según la ubicación
        if location in ['assets', 'media']:
            print(f"   ![Descripción]({filename})")
        elif location.startswith('hardware'):
            print(f"   ![Descripción](resources/{filename})")
        elif location.startswith('docs'):
            print(f"   ![Descripción](assets/{filename})")
        elif location.startswith('images'):
            print(f"   ![Descripción](images/{filename})")
        else:
            print(f"   ![Descripción]({filename})")
        
        print("   (Reemplaza 'Descripción' con una descripción apropiada de la imagen)")
    
    def list_images(self, location: str = None):
        """Lista las imágenes en una ubicación específica o en todas"""
        if location:
            if location not in self.available_locations:
                print(f"❌ Error: '{location}' no es una ubicación válida")
                return
            locations = {location: self.available_locations[location]}
        else:
            locations = self.available_locations
        
        print("\n🖼️  Imágenes encontradas:")
        print("=" * 50)
        
        total_images = 0
        for name, path in locations.items():
            if path.exists():
                images = list(path.glob("**/*"))
                images = [img for img in images if img.is_file() and 
                         img.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']]
                
                if images:
                    print(f"\n📁 {name} ({path.relative_to(self.base_dir)}):")
                    for img in sorted(images):
                        rel_path = img.relative_to(path)
                        size = img.stat().st_size / 1024  # KB
                        print(f"   • {rel_path} ({size:.1f} KB)")
                    total_images += len(images)
        
        if total_images == 0:
            print("   No se encontraron imágenes")
        else:
            print(f"\n📊 Total: {total_images} imágenes encontradas")

def main():
    parser = argparse.ArgumentParser(description='Gestionar imágenes del proyecto')
    parser.add_argument('--base-dir', default='.', help='Directorio base del proyecto')
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Comando para listar ubicaciones
    subparsers.add_parser('locations', help='Listar ubicaciones disponibles')
    
    # Comando para añadir imagen
    add_parser = subparsers.add_parser('add', help='Añadir una imagen')
    add_parser.add_argument('source', help='Ruta de la imagen a añadir')
    add_parser.add_argument('destination', help='Ubicación de destino')
    add_parser.add_argument('--name', help='Nombre personalizado para el archivo')
    
    # Comando para listar imágenes
    list_parser = subparsers.add_parser('list', help='Listar imágenes existentes')
    list_parser.add_argument('--location', help='Ubicación específica a listar')
    
    args = parser.parse_args()
    
    manager = ImageManager(args.base_dir)
    
    if args.command == 'locations':
        manager.list_locations()
    elif args.command == 'add':
        manager.add_image(args.source, args.destination, args.name)
    elif args.command == 'list':
        manager.list_images(args.location)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
