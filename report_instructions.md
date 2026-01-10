# LaTeX Report Compilation Instructions

## Requirements
- LaTeX distribution (MiKTeX for Windows, TeX Live for Linux/Mac)
- PDF viewer

## Compilation

### Using pdflatex (recommended)
```bash
pdflatex report.tex
pdflatex report.tex  # Run twice for proper references
```

### Using online compiler
- Upload `report.tex` to Overleaf.com
- Compile online

## Before Compiling

1. **Replace placeholders marked with [CHANGE] and [END CHANGE]**
   - Student names
   - Date
   - Image paths
   - Any sections marked for customization

2. **Add your images**
   - Place images in a folder (e.g., `images/`)
   - Update image paths in the report
   - Supported formats: PNG, JPG, PDF

3. **Review and customize**
   - Add quantitative results where marked
   - Add any additional explanations
   - Customize code snippets if needed

## Image Placeholders to Replace

- `[CHANGE] path/to/python_q1_result.png [END CHANGE]` - Python Q1 results
- `[CHANGE] path/to/esp32_q1_result.png [END CHANGE]` - ESP32 Q1 results  
- `[CHANGE] path/to/upsampling_result.jpg [END CHANGE]` - Upsampling result
- `[CHANGE] path/to/downsampling_result.jpg [END CHANGE]` - Downsampling result
- `[CHANGE] path/to/comparison_q3.png [END CHANGE]` - Q3 comparison

## Notes

- The report uses simple sentences as requested
- All sections marked with [CHANGE] need customization
- Code listings are formatted for readability
- Figures use the `[H]` placement to keep them in order

