# Image Path Reference Guide

This guide explains how to use relative paths for images in the Electronic Module Template documentation system.

## Directory Structure

```
hardware/
├── README.md                 # Hardware documentation
└── resources/               # Image resources directory
    ├── img/                 # Additional images
    │   └── logo.png
    ├── unit_top_v_1_0_0_ue0094_icp10111_barometric_pressure_sensor.png
    ├── unit_pinout_v_0_0_1_ue0094_icp10111_barometric_pressure_sensor_en.jpg
    ├── unit_dimension_v_1_0_0_ue0094_icp10111_barometric_pressure_sensor.png
    └── unit_topology_v_1_0_0_ue0094_icp10111_barometric_pressure_sensor.png
```

## Correct Image Syntax in README Files

### ✅ Correct Usage (Relative Paths)

When referencing images from within `hardware/README.md`, use:

```markdown
![Electronic Module](resources/unit_top_v_1_0_0_ue0094_icp10111_barometric_pressure_sensor.png)
![Pinout Diagram](resources/unit_pinout_v_0_0_1_ue0094_icp10111_barometric_pressure_sensor_en.jpg)
![Physical Dimensions](resources/unit_dimension_v_1_0_0_ue0094_icp10111_barometric_pressure_sensor.png)
![Block Diagram](resources/unit_topology_v_1_0_0_ue0094_icp10111_barometric_pressure_sensor.png)
```

### ❌ Incorrect Usage (Absolute Paths)

Avoid these formats:

```markdown
# Wrong - absolute path
![Electronic Module](/resources/unit_top_v_1_0_0_ue0094_icp10111_barometric_pressure_sensor.png)

# Wrong - missing directory
![Electronic Module](unit_top_v_1_0_0_ue0094_icp10111_barometric_pressure_sensor.png)

# Wrong - incorrect directory
![Electronic Module](hardware/resources/unit_top_v_1_0_0_ue0094_icp10111_barometric_pressure_sensor.png)
```

## How the System Works

1. **Relative Path Processing**: The documentation generator recognizes `resources/` prefix in image paths
2. **Automatic Copy**: All images from `hardware/resources/` are automatically copied to `docs/` during generation
3. **LaTeX Conversion**: Image references are converted to proper LaTeX figure environments
4. **Path Normalization**: The system removes the `resources/` prefix when generating LaTeX since images are copied to the same directory

## Image Processing Flow

```
hardware/README.md                    docs/datasheet_en.tex
├── ![Alt](resources/image.png)  →   ├── \begin{figure}[H]
                                      ├── \centering
                                      ├── \includegraphics[width=0.8\textwidth]{image.png}
                                      ├── \caption{Alt}
                                      └── \end{figure}

hardware/resources/image.png     →    docs/image.png (copied automatically)
```

## Supported Image Formats

- **PNG**: `.png` (preferred for diagrams and screenshots)
- **JPG/JPEG**: `.jpg`, `.jpeg` (preferred for photographs)
- **SVG**: Not directly supported in LaTeX, convert to PNG first

## Best Practices

### Image Naming Convention
Use descriptive, consistent names:
```
unit_top_v_1_0_0_ue0094_module_name.png           # Top view
unit_pinout_v_0_0_1_ue0094_module_name_en.jpg     # Pinout (English)
unit_dimension_v_1_0_0_ue0094_module_name.png     # Dimensions
unit_topology_v_1_0_0_ue0094_module_name.png      # Block diagram
```

### Alt Text Guidelines
Use descriptive alt text for accessibility:
```markdown
![Electronic Module Top View](resources/unit_top.png)          # Good
![Top View](resources/unit_top.png)                           # Okay  
![Image](resources/unit_top.png)                              # Poor
```

### Image Size Recommendations
- **Maximum width**: 1920px (will be scaled to fit)
- **Recommended DPI**: 300 DPI for print quality
- **File size**: Keep under 1MB per image when possible

## Content Files Structure

### Hardware Documentation (`hardware/README.md`)
- Use `resources/image.png` paths
- Images are relative to the hardware directory

### Main Content (`info/content_en.md`, `info/content_es.md`)
- For referencing hardware images, use full relative paths from root
- Example: `hardware/resources/image.png`

### Software Documentation (`software/examples/*/README.md`)
- Use relative paths from the software directory
- Example: `../../../hardware/resources/image.png` (if needed)

## Troubleshooting

### Image Not Appearing
1. Check that the image file exists in `hardware/resources/`
2. Verify the path in README.md uses `resources/` prefix
3. Ensure the image file extension matches the reference
4. Check for typos in the filename

### LaTeX Compilation Errors
1. Verify image file format is supported (PNG, JPG)
2. Check that image files don't have spaces in names
3. Ensure image files aren't corrupted

### Large PDF File Size
1. Optimize images before adding to `resources/`
2. Use appropriate formats (PNG for diagrams, JPG for photos)
3. Compress images while maintaining quality

## Example Usage

Here's a complete example of proper image usage in `hardware/README.md`:

```markdown
# Electronic Module

## Product Overview

This electronic module provides professional template functionality.

![Electronic Module](resources/unit_top_v_1_0_0_ue0094_module.png)

## Pinout Configuration

![Pinout Diagram](resources/unit_pinout_v_0_0_1_ue0094_module_en.jpg)

### Pin Description

| Pin | Function | Description |
|-----|----------|-------------|
| 1   | VCC      | Power supply |
| 2   | GND      | Ground |

## Physical Dimensions

![Physical Dimensions](resources/unit_dimension_v_1_0_0_ue0094_module.png)

## Block Diagram

![Block Diagram](resources/unit_topology_v_1_0_0_ue0094_module.png)
```

This will generate professional documentation with properly formatted figures, captions, and high-quality images in the final PDF.

---

*Image Path Reference Guide - Electronic Module Template v1.0.0*
