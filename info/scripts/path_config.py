#!/usr/bin/env python3
"""
Path Configuration Script
=========================

This script manages the extraction paths and routes for the electronic module
documentation generation system. It handles the new organized directory structure.

Author: DevLab Team
Date: 2025
"""

import os
import yaml
from pathlib import Path

class PathConfig:
    """Path configuration manager for the electronic module template"""
    
    def __init__(self, root_dir: str = None):
        """
        Initialize path configuration
        
        Args:
            root_dir (str): Root directory of the project
        """
        if root_dir is None:
            # Auto-detect root directory (3 levels up from this script)
            self.root_dir = Path(__file__).parent.parent.parent
        else:
            self.root_dir = Path(root_dir)
        
        self.paths = self._initialize_paths()
    
    def _initialize_paths(self) -> dict:
        """Initialize all project paths"""
        paths = {
            # Root directories
            'root': self.root_dir,
            'docs': self.root_dir / 'docs',
            'info': self.root_dir / 'info',
            'hardware': self.root_dir / 'hardware',
            'software': self.root_dir / 'software',
            
            # Info subdirectories
            'info_scripts': self.root_dir / 'info' / 'scripts',
            'info_metadata': self.root_dir / 'info' / 'metadata',
            'info_templates': self.root_dir / 'info' / 'templates',
            
            # Content directories (now in info/)
            'content_en': self.root_dir / 'info' / 'content_en.md',
            'content_es': self.root_dir / 'info' / 'content_es.md',
            
            # Hardware resources
            'hardware_resources': self.root_dir / 'hardware' / 'resources',
            'hardware_images': self.root_dir / 'hardware' / 'resources' / 'img',
            
            # Software examples
            'software_examples': self.root_dir / 'software' / 'examples',
            'software_c': self.root_dir / 'software' / 'examples' / 'c',
            'software_python': self.root_dir / 'software' / 'examples' / 'python',
            
            # Template files
            'template_latex': self.root_dir / 'info' / 'templates' / 'template.tex',
            'metadata_project': self.root_dir / 'info' / 'metadata' / 'project_metadata.yaml',
            'metadata_standards': self.root_dir / 'info' / 'metadata' / 'document_standards.yaml',
            
            # Generated outputs
            'output_docs': self.root_dir / 'docs',
            'output_latex': self.root_dir / 'docs' / 'datasheet_en.tex',
            'output_pdf': self.root_dir / 'docs' / 'datasheet_en.pdf',
        }
        
        return paths
    
    def get_path(self, key: str) -> Path:
        """
        Get a specific path
        
        Args:
            key (str): Path key
            
        Returns:
            Path: Requested path
        """
        if key not in self.paths:
            raise KeyError(f"Path key '{key}' not found")
        return self.paths[key]
    
    def get_all_paths(self) -> dict:
        """Get all configured paths"""
        return self.paths.copy()
    
    def ensure_directories(self):
        """Ensure all necessary directories exist"""
        directories_to_create = [
            'docs', 'info', 'hardware', 'software',
            'info_scripts', 'info_metadata', 'info_templates',
            'hardware_resources', 'software_examples',
            'output_docs'
        ]
        
        for dir_key in directories_to_create:
            if dir_key in self.paths:
                self.paths[dir_key].mkdir(parents=True, exist_ok=True)
                print(f"✓ Directory ensured: {self.paths[dir_key]}")
    
    def validate_structure(self) -> bool:
        """
        Validate the project structure
        
        Returns:
            bool: True if structure is valid
        """
        required_paths = [
            'info_metadata', 'info_templates', 'info_scripts',
            'hardware', 'software', 'docs'
        ]
        
        missing_paths = []
        for path_key in required_paths:
            if not self.paths[path_key].exists():
                missing_paths.append(path_key)
        
        if missing_paths:
            print("Missing required directories:")
            for path_key in missing_paths:
                print(f"  - {path_key}: {self.paths[path_key]}")
            return False
        
        print("✓ Project structure validation passed")
        return True
    
    def get_extraction_paths(self) -> dict:
        """Get paths for content extraction"""
        extraction_paths = {
            'content_sources': {
                'english': self.get_path('content_en'),
                'spanish': self.get_path('content_es'),
                'hardware': self.get_path('hardware') / 'README.md',
                'software_c': self.get_path('software_c') / 'README.md',
                'software_python': self.get_path('software_python') / 'README.md',
            },
            'metadata_sources': {
                'project': self.get_path('metadata_project'),
                'standards': self.get_path('metadata_standards'),
            },
            'template_sources': {
                'latex': self.get_path('template_latex'),
            },
            'output_targets': {
                'docs_dir': self.get_path('output_docs'),
                'latex_file': self.get_path('output_latex'),
                'pdf_file': self.get_path('output_pdf'),
            }
        }
        
        return extraction_paths
    
    def export_config(self, output_file: str = None):
        """
        Export path configuration to YAML file
        
        Args:
            output_file (str): Output file path
        """
        if output_file is None:
            output_file = self.get_path('info_metadata') / 'path_config.yaml'
        
        # Convert Path objects to strings for YAML serialization
        paths_str = {k: str(v) for k, v in self.paths.items()}
        
        config_data = {
            'project_name': 'Electronic Module Template',
            'version': '1.0.0',
            'paths': paths_str,
            'extraction_paths': {
                k: {k2: str(v2) for k2, v2 in v.items()} 
                for k, v in self.get_extraction_paths().items()
            }
        }
        
        with open(output_file, 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False, indent=2)
        
        print(f"✓ Path configuration exported to: {output_file}")

def main():
    """Main function for testing path configuration"""
    print("Electronic Module Template - Path Configuration")
    print("=" * 60)
    
    # Initialize path config
    config = PathConfig()
    
    # Ensure directories
    config.ensure_directories()
    
    # Validate structure
    if config.validate_structure():
        print("\n✓ Project structure is valid")
    else:
        print("\n✗ Project structure validation failed")
        return 1
    
    # Export configuration
    config.export_config()
    
    # Display extraction paths
    print("\nExtraction Paths:")
    extraction_paths = config.get_extraction_paths()
    for category, paths in extraction_paths.items():
        print(f"\n{category.upper()}:")
        for name, path in paths.items():
            print(f"  {name}: {path}")
    
    return 0

if __name__ == "__main__":
    exit(main())
