# Report Structure

This directory contains the modular LaTeX report for the Embedded Digital Image Processing project.

## Structure

```
report/
├── Main.tex                 # Main document file
├── packages.tex             # LaTeX package definitions
├── titlepage.tex            # Title page
├── references.tex           # Bibliography
├── contents/                # Main content sections
│   ├── Abstract.tex
│   ├── Introduction.tex
│   ├── Question1.tex
│   ├── Question2.tex
│   ├── Question3.tex
│   └── Conclusion.tex
├── appendix/                # Code listings
│   ├── AppendixA.tex        # Question 1 code
│   ├── AppendixB.tex        # Question 2 code snippets
│   └── AppendixC.tex        # Question 3 code
└── images/                  # Image files (placeholders)
```

## Compilation

To compile the report:

```bash
cd report
pdflatex Main.tex
pdflatex Main.tex  # Run twice for references
```

Or use your preferred LaTeX editor/IDE.

## Notes

- All code listings use relative paths from the `report/` directory
- Image placeholders are marked with `[PLACEHOLDER]` - replace with actual images
- Sections marked with `[CHANGE] ... [END CHANGE]` need user input
- The report follows academic format with Abstract, Contents, Figures, Tables, Introduction, Questions, Conclusion, Appendix, and References

## Image Paths

Place your images in the `report/images/` directory and update the paths in:
- `contents/Question1.tex`
- `contents/Question2.tex`
- `contents/Question3.tex`

