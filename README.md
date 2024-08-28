# Linkedin_Queen_Game_Solution
This project implements a computer vision-based solution for the classic Queen game, where users can upload an image of a grid, and the system automatically identifies and marks the positions where queens should be placed.

## Procedure

- First Download the project by running command

   ```` git clone https://github.com/byreddyrohithreddy/Linkedin_Queen_Game_Solution/ ````
- Then take screenshot of the linkedin queen game as shown below 
![Screenshot 2024-08-26 002053](https://github.com/user-attachments/assets/ca25aaeb-83c7-4acf-94fd-cefb30759027)
- Now goto the project directory and run command

  ```` python extract.py "screenshot_path" ````
- The above command will save a image into your directory as below

![Queens_positions](https://github.com/user-attachments/assets/87f70ab5-a158-4126-8ab5-78e32847f79f)

## Implementation

- There are two steps in this code implementation one is extracting color grid and mapping it into a color array and other one is using color array identifying the solution and mapping it.

### CV part:

- Used contours detection and extraction of colors from the grid.
- After mapping the colors, corresponding color positions were saved
- Later after identifying the points were the crown has be placed, using points of color map actual positions were drawn using opencv

### Queen identification:

- After getting the color map, found all sequences of the map of size n
- We know that each color should have one crown so using this condition identified the possible solution
- After finding the solution the positions were mapped on the image.

