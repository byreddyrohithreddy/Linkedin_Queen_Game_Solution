import cv2
import numpy as np
import math
from collections import Counter
import sys

def get_grid_image(path):
    full_image = cv2.imread(path)
    gray = cv2.cvtColor(full_image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    x, y, w, h = cv2.boundingRect(contours[0])
    image = full_image[y:y+h, x:x+w]

    return image

def get_major_color(roi):
    pixels = roi.reshape(-1, 3)
    pixels = [tuple(p) for p in pixels]
    most_common_color = Counter(pixels).most_common(1)[0][0]
    
    return most_common_color

def get_2d_color_list(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray_image, 50, 255,0)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    num_contours = len(contours)

    width = math.floor(math.sqrt(num_contours))

    positions = []
    color_map = []
    i =0
    for cnt in contours:
        x1, y1 = cnt[0][0]
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)

        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(cnt)
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            cv2.drawContours(mask, [cnt], -1, 255, -1)

            roi = cv2.bitwise_and(image, image, mask=mask)[y:y+h, x:x+w]

            major_color = get_major_color(roi)
            positions.append((x, y))

            color_map.append(major_color[0])

    max_x = max([pos[0] for pos in positions]) // w

    max_y = max([pos[1] for pos in positions]) // h

    colors = np.zeros((max_y + 1, max_x + 1), dtype=np.uint8)

    position_map={}
    for (x, y), color in zip(positions, color_map):
        grid_x = x // w
        grid_y = y // h
        colors[grid_y, grid_x] = color
        position_map[(grid_y,grid_x)]=(x,y)
    
    return w,h,max_x,position_map,colors

class NQueens:
    def __init__(self, size):
        self.size = size
        self.tt=[]
        self.solutions = 0
        self.solve()

    def solve(self):
        positions = [-1] * self.size
        self.put_queen(positions, 0)

    def put_queen(self, positions, target_row):
        if target_row == self.size:
            r=positions.copy()
            self.tt.append(r)
            self.solutions += 1
        else:
            for column in range(self.size):
                if self.check_place(positions, target_row, column):
                    positions[target_row] = column
                    self.put_queen(positions, target_row + 1)

    def check_place(self, positions, ocuppied_rows, column):
        rows=ocuppied_rows
        for i in range(ocuppied_rows):
            if positions[i] == column:
                return False
            if abs(positions[i] - column) <= 1 and abs(i - rows) <= 1:
                return False
        return True
    
def get_solution(w,h,n,position_map,c_list,image):
    
    t=NQueens((n+1))

    li=t.tt
    for i in li:
        dic={}
        lol=0
        for j,k in enumerate(i):
            if c_list[j][k] not in dic:
                dic[c_list[j][k]] =1
            else:
                dic[c_list[j][k]]+=1
        count=0
        for k in dic:
            if dic[k]==1:
                count+=1
        if count==(n+1):
            j = 0
            for k in i:
                grid_x, grid_y = position_map[(j,k)]
                center_x = grid_x + w // 2
                center_y = grid_y + h // 2
                cv2.circle(image, (center_x,center_y), 10, (0, 0, 255), -1)

                j=j+1

    cv2.imwrite("Queens_positions.png", image)

    return "image saved at queens_positions.png"

path = sys.argv[1]

image = get_grid_image(path)

w, h, n, position_map, colors = get_2d_color_list(image)


print(get_solution(w,h,n,position_map,colors,image))
