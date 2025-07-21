#!/bin/bash
# 
# Electronic Module Documentation Builder
# =====================================
# 
# This script builds the electronic module documentation using the new
# organized directory structure.
#
# Usage: ./build_docs.sh [language]
#   language: en (default) or es
#

set -e  # Exit on any error

# Default language
LANGUAGE=${1:-en}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get script directory (should be info/scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

print_status "Electronic Module Documentation Builder"
print_status "========================================"
print_status "Project root: $PROJECT_ROOT"
print_status "Language: $LANGUAGE"
print_status ""

# Check if we're in the correct directory structure
if [[ ! -d "$PROJECT_ROOT/info" ]]; then
    print_error "Invalid project structure. Missing 'info' directory."
    print_error "This script should be run from info/scripts/ directory."
    exit 1
fi

# Change to scripts directory
cd "$SCRIPT_DIR"

# Check Python dependencies
print_status "Checking Python dependencies..."
if ! python3 -c "import yaml" 2>/dev/null; then
    print_warning "PyYAML not found. Installing..."
    pip3 install PyYAML
fi

# Check LaTeX installation
print_status "Checking LaTeX installation..."
if ! command -v pdflatex &> /dev/null; then
    print_error "pdflatex not found. Please install a LaTeX distribution:"
    print_error "  Ubuntu/Debian: sudo apt-get install texlive-full"
    print_error "  macOS: brew install --cask mactex"
    print_error "  Windows: Install MiKTeX or TeX Live"
    exit 1
fi

# Validate project structure
print_status "Validating project structure..."
python3 path_config.py
if [[ $? -ne 0 ]]; then
    print_error "Project structure validation failed"
    exit 1
fi

# Generate documentation
print_status "Generating documentation..."
python3 generate_docs_fixed.py --language "$LANGUAGE" --base-dir "$PROJECT_ROOT"

if [[ $? -eq 0 ]]; then
    print_success "Documentation generated successfully!"
    
    # Show output files
    DOCS_DIR="$PROJECT_ROOT/docs"
    if [[ -f "$DOCS_DIR/datasheet_${LANGUAGE}.pdf" ]]; then
        PDF_SIZE=$(stat -c%s "$DOCS_DIR/datasheet_${LANGUAGE}.pdf" 2>/dev/null || stat -f%z "$DOCS_DIR/datasheet_${LANGUAGE}.pdf" 2>/dev/null || echo "unknown")
        print_success "PDF generated: $DOCS_DIR/datasheet_${LANGUAGE}.pdf ($PDF_SIZE bytes)"
    fi
    
    if [[ -f "$DOCS_DIR/datasheet_${LANGUAGE}.tex" ]]; then
        print_success "LaTeX source: $DOCS_DIR/datasheet_${LANGUAGE}.tex"
    fi
    
    print_status ""
    print_status "Documentation build completed successfully! 🎉"
else
    print_error "Documentation generation failed"
    exit 1
fi
