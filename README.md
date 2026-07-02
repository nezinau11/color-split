# color-split
A Python script to split an indexed color or an RGB image with less than 256 colors into b&amp;w channels of each color. Created to be used for printing color raster images on metal with a laser.

The Python script requires 3.x Python, the PIL and webcolors Python to be installed. It has some additional simple functionality besides the color splitting, such as upscaling, outputting the color palette and more for convenience. Here’s how you use it for an image named `dith.png` that you’d engrave using 635 DPI (0.04mm line width):
```
PS C:\colors> .\colors.py --dpi 635 --scale 2 dith.png
Image size is 1200x1200. Image mode is RGBA, number of colors is 8.
Image size after rescaling 2x is 2400x2400.
Processing #000000 (black) color.
Processing #4B52DD (royalblue) color.
Processing #D26F1D (chocolate) color.
Processing #DDCD3E (goldenrod) color.
Processing #87BAB2 (darkseagreen) color.
Processing #84227C (purple) color.
Processing #F2F2F2 (whitesmoke) color.
Processing #992736 (brown) color.
Physical print size for 635 DPI/PPI (line interval 0.04mm):
width: 96.00mm
height: 96.00mm
```
It will write separate images for each color into the same folder it is run from. For laser printing add them to a Lightburn project, set the correct physical size for each image as specified by the script, turn on pass-through mode for each of them and set the frequency/speed/power/pulse width parameters for each image for specific color.

Here are a few sample color engravings on 10x10cm titanium metal plates using a MOPA Fiber laser.

<img width="30%" height="30%" alt="" src="https://github.com/user-attachments/assets/c1328cbd-c2de-4b45-8292-c76edf5a41ac" />

<img width="30%" height="30%" alt="" src="https://github.com/user-attachments/assets/e0aa767a-e46c-4915-b7d9-c1f29dbe0e5a" />

<img width="30%" height="30%" alt="" src="https://github.com/user-attachments/assets/4a17eaa7-17ea-4ad7-8076-e2f53c89e065" />
