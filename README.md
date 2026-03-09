# BMP2PETSCII

## BMP2PETSCII converts your .bmp image file into a PETSCII array

* Currently requires dimensions to be 80x50

## Usage:  
```python3 bmp2petscii.py [filename] [-dither] [-invert]```

eg.

 ```python3 bmp2petscii.py success.bmp -dither```
 
 ```python3 bmp2petscii.py success.bmp -invert -dither```
 
 ```python3 bmp2petscii.py success.bmp -invert``` 

## Sprite variant generator (`bmp2petscii-sprite.py`)

This helper script takes a bitmap and generates PETSCII DATA blocks for a 2x2–block sprite in 9 positions: centre plus all 8 directions (N, NE, E, SE, S, SW, W, NW).  

### Usage

```bash
python3 bmp2petscii-sprite.py <filename> [-invert] [-dither]
```

- **`filename`**: input bitmap (e.g. 1‑bit or grayscale; will be converted internally).
- **`-invert`**: optional; invert the source image before thresholding.
- **`-dither`**: optional; enable dithering when converting to 1‑bit.

### Output

- **BMP files**: one per shift (`C-0-0.bmp`, `N-0--1.bmp`, `E-1-0.bmp`, etc.), showing each shifted version.
- **PETSCII DATA**: printed to stdout as BASIC‑style `DATA` blocks, with width/height labels (e.g. `C_W`, `C_H`, `C:`) for easy inclusion in your program.
