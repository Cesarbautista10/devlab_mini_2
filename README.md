# 📚 Automated Documentation System

This repository contains an automated system for generating professional LaTeX-based documentation from Markdown content with multi-language support.

## 🚀 Features

- **Multi-language Support**: English and Spanish documentation
- **Automated PDF Generation**: LaTeX compilation with professional formatting
- **Image Integration**: Automatic inclusion of hardware images from `images/resources/`
- **CI/CD Pipeline**: GitHub Actions for automated builds and deployments
- **GitHub Pages**: Web-based documentation hosting
- **Automatic Releases**: Tagged releases with PDF artifacts

## 📁 Project Structure

```
.
├── 📄 template.tex              # LaTeX template for professional formatting
├── 🐍 generate_final.py         # Main documentation generator
├── 🌐 docs/                     # Generated output directory
│   ├── index.html
│   ├── devlab_en.pdf
│   └── devlab_es.pdf
├── 🇺🇸 en/                      # English content
│   ├── content.md
│   └── metadata.yaml
├── 🇪🇸 es/                      # Spanish content
│   ├── content.md
│   └── metadata.yaml
├── 🖼️ images/resources/          # Hardware images and diagrams
└── ⚙️ .github/workflows/        # CI/CD automation
    ├── docs.yml                 # Main documentation workflow
    └── test.yml                 # Pull request testing
```

## 🔧 Local Development

### Prerequisites

```bash
# Ubuntu/Debian
sudo apt-get install texlive-full python3 python3-pip

# Python dependencies
pip install PyYAML
```

### Generate Documentation

```bash
# Generate English documentation
python generate_final.py --lang en

# Generate Spanish documentation
python generate_final.py --lang es

# Generate both languages
python generate_final.py --lang en
python generate_final.py --lang es
```

### Output Files

Generated PDFs will be available in the `docs/` directory:
- `docs/datasheet_en.pdf` - English documentation
- `docs/datasheet_es.pdf` - Spanish documentation

## 🤖 CI/CD Automation

### Main Workflow (docs.yml)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main`
- Manual workflow dispatch

**Jobs:**
1. **generate-docs**: Creates PDF documentation for both languages
2. **deploy-docs**: Deploys to GitHub Pages (main branch only)
3. **release**: Creates GitHub releases with PDF artifacts (main branch only)

**Artifacts:**
- PDF documentation files
- LaTeX source files
- Build summaries

### Test Workflow (test.yml)

**Triggers:**
- Pull requests to `main` or `develop`

**Purpose:**
- Validates PDF generation for both languages
- Ensures changes don't break the build process
- Provides test reports as artifacts

## 🌐 GitHub Pages

When changes are pushed to the `main` branch, documentation is automatically deployed to GitHub Pages with:

- **Landing Page**: Professional HTML interface
- **Download Links**: Direct access to PDF files
- **Build Information**: Commit details and timestamps
- **Multi-language Support**: Easy access to both English and Spanish versions

**URL**: `https://[username].github.io/[repository-name]/`

## 🏷️ Releases

Automatic releases are created on every push to `main` with:

- **Tag Format**: `docs-vYYYY.MM.DD-[run-number]`
- **Assets**: PDF files for both languages
- **Release Notes**: Automatic generation with build details
- **Change Log**: Recent commits related to documentation

## 📝 Content Management

### Adding Content

1. **Edit Markdown Files**:
   - `en/content.md` for English content
   - `es/content.md` for Spanish content

2. **Update Metadata**:
   - `en/metadata.yaml` for English metadata
   - `es/metadata.yaml` for Spanish metadata

3. **Add Images**:
   - Place images in `images/resources/`
   - Reference in Markdown: `![Description](unit_pinout.png)`

### Supported Content

- **Headers**: All markdown header levels
- **Lists**: Bulleted and numbered lists
- **Tables**: Automatic LaTeX table conversion
- **Images**: PNG, JPG with automatic sizing
- **Code Blocks**: Syntax highlighting
- **Special Characters**: UTF-8 support for international content

## ⚙️ Configuration

### Template Customization

Edit `template.tex` to modify:
- Document formatting and styling
- Color schemes and fonts
- Page layouts and margins
- Header/footer content

### Generator Settings

Modify `generate_final.py` for:
- Image processing rules
- Table conversion options
- Character escaping behavior
- Output file naming

### Workflow Configuration

Update `.github/workflows/docs.yml` for:
- Build triggers and conditions
- LaTeX package requirements
- Artifact retention policies
- Release automation rules

## 🐛 Troubleshooting

### Common Issues

1. **LaTeX Compilation Errors**:
   - Check `template.tex` syntax
   - Verify image file paths
   - Review special character escaping

2. **Missing Images**:
   - Ensure images exist in `images/resources/`
   - Check file extensions (PNG, JPG)
   - Verify markdown image references

3. **Build Failures**:
   - Review workflow logs in GitHub Actions
   - Check Python dependencies
   - Validate YAML syntax in metadata files

### Debug Commands

```bash
# Test LaTeX installation
pdflatex --version

# Validate YAML files
python -c "import yaml; yaml.safe_load(open('en/metadata.yaml'))"

# Check image files
ls -la images/resources/

# Manual generation with verbose output
python generate_final.py --lang en -v
```

## 📈 Monitoring

### Build Status

- **GitHub Actions**: View workflow status in the Actions tab
- **Artifacts**: Download generated files from workflow runs
- **Pages**: Monitor deployment status in repository settings

### Quality Metrics

- **PDF Size**: Validates generated files are not empty
- **Image Integration**: Ensures all referenced images are included
- **Multi-language**: Confirms both languages build successfully

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch
3. **Edit** content or configuration
4. **Test** locally with the generator
5. **Submit** a pull request

Pull requests automatically trigger test builds to validate changes before merging.

## 📄 License

This documentation system is available under the MIT License. See individual content licenses for documentation materials.

---

**Built with** ❤️ **using GitHub Actions, LaTeX, and Python**
