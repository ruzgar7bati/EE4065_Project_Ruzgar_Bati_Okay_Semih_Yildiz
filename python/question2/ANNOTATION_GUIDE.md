# Annotation Guide for Digits 0, 4, 7

This guide explains how to annotate images for the simplified 3-digit detection task.

## Class Mapping

When annotating, use these class IDs:
- **Class 0** → Digit "0"
- **Class 1** → Digit "4"  
- **Class 2** → Digit "7"

## Using LabelImg

1. **Download LabelImg**: https://github.com/tzutalin/labelImg
2. **Set format to YOLO**: In LabelImg, go to View → Auto Save mode, and make sure format is set to YOLO
3. **Open image folder**: File → Open Dir → Select `images/train/` (or val/test)
4. **Annotate each digit**:
   - Draw bounding box around each digit
   - Select correct class:
     - For digit "0" → select class "0"
     - For digit "4" → select class "1" (this maps to "4" in our config)
     - For digit "7" → select class "2" (this maps to "7" in our config)
   - Save (Ctrl+S) - this creates a `.txt` file with same name as image

## Label File Format

Each `.txt` file should have one line per digit detected:
```
class_id center_x center_y width height
```

Example for an image with one "4" and one "7":
```
1 0.3 0.4 0.15 0.2
2 0.7 0.5 0.12 0.18
```

## Important Notes

- **One image can have multiple digits** - each digit gets its own line
- **Coordinates are normalized** (0.0 to 1.0)
- **File names must match**: `image001.jpg` → `image001.txt`
- **Save labels in corresponding folders**: 
  - Labels for `images/train/` go in `labels/train/`
  - Labels for `images/val/` go in `labels/val/`
  - Labels for `images/test/` go in `labels/test/`

## Quick Checklist

- [ ] Images of digits 0, 4, 7 in `images/train/`, `images/val/`, `images/test/`
- [ ] Each image has a corresponding `.txt` file in `labels/train/`, `labels/val/`, `labels/test/`
- [ ] Class IDs are correct: 0="0", 1="4", 2="7"
- [ ] Bounding boxes are tight around digits (not too much background)
- [ ] All coordinates are normalized (0-1)

