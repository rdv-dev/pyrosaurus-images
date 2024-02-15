# Image Extractor for Pyrosaurus
This is a tool to unpack/view images from Pyrosaurus game data stored in the CELS3 file.

The CELS3 file contains image data for buttons, backgrounds, and the Evryware banner, the Pyrosaurus flying letters, and the roaring dino head. The animation does not appear to be stored in this file, I believe this is controlled by the game's programming. The scope of this utility is only for the background images.

## CELS3 File
### Header
The CELS3 file starts with the number of bytes contained within an array of absolute file offsets to a data structures in the file. This array is then read by the game and these indexes are accessed from the file when as needed by the game.

### Data Stucture
The first two bytes of the data stucture is the number of bytes to read for the palette of the images. This number is divisible by 3 which will result in the number of colors in the palette. Each of the palette triplets correspond to the Red, Green and Blue channel in that order. Looking at the colors directly without any modification, they are muted colors. The simple way I came up with to deal with this is to multiply each color channel by 4, and this brightens it sufficiently to match how the game appears in DOSBox.

The game may be doing something more complicated but this is left as an exercise to the reader to figure out. However, if this how the game does it, at least it is fast to compute (2 bit shifts left).

After the palette colors is an array of absolute offsets to each of the images contained within the data structure. The value of the first offset can act as a stop point for reading this array of offsets.

#### Image Data

Next, is the metadata and data for images. The image data starts with a 2-byte integer representing the number of bytes which makes up the image. Next, there are 2 2-byte numbers representing the width and height of the image respectively. Therefore, the image data is actually 4 bytes less than the first 2-byte integer.

The actual image data is not exactly straightforward. It is a mixture of control characters and indexes relative to the palette earlier in the data structure. Firstly, each of the indexes of the palette has 16 subtracted from them.

Here is the list of control characters and the function they perform.
Each control character follows this pattern: The high 8 bits control the functionality and the low 8 bits represent some number of pixels, usually. So the high 8 bits will be correct number, and the low bits will be represented by N to signify that this is some number.

The way the image is drawn using vertical lines starting from the screen origin. Once one column is drawn then it moves to the next.
For background images, they are broken up into 4 smaller images which are stitched together on screen.

Control Character|Arguments|Description
---|---|---
0xEN|1|Repeat the color argument 32 + N times
0xDN|1|Repeat the color argument 16 + N times
0xCN|1|Repeat the color argument N times
0xBN|N + 48|Read the following N + 48 bytes for pixel data
0xAN|N + 32|Read the following N + 32 bytes for pixel data
0x9N|N + 16|Read the following N + 16 bytes for pixel data
0x8N|N|Read the following N bytes for pixel data
0x0N|0|Repeat black color N times
0x40|0|Signifies the maximum height of pixels and to start the next vertical line

