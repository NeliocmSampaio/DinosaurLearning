from PIL import Image
from datetime import datetime
import pyautogui
import cv2
import numpy as np

from mss.linux import MSS as mss

import time
import sys

dino_color = (84, 84, 84, 255)

def capture(x, y, w, h):
    with mss() as sct:
        region = { 'top': y, 'left': x, 'width': w, 'height': h}
        sct_img = sct.grab(region)
    img = Image.fromarray(np.array(sct_img))

    #region = (x, y, w, h)
    #img = pyautogui.screenshot( region=region )
    #img2 = cv2.cv2.cvtColor( np.array(img), cv2.cv2.COLOR_RGB2GRAY )

    return img

def obstacle(distance, length, height, speed, time):
    return {'distance': distance, 'lenght': length, 'height': height, 'speed': speed, 'time': time}

def is_dino_color(pixel):
    return pixel==dino_color

class Vision:
    def __init__(self):
        self.dino_start = (0,0)
        self.dino_end   = (0,0)
        self.last_obstacle = obstacle(0, 0, 0, 0, 0)
        self.__current_fitness = 0
        self.__change_fitness = False

    def find_game(self):
        #image = capture(100, 330, 850, 155)

        #while True:
        image = capture(100, 330, 850, 155)

            #print("find")
            #img2 = cv2.cv2.cvtColor( np.array(image), cv2.cv2.COLOR_RGB2GRAY )
            #cv2.cv2.imshow('DINO', img2)
            #time.sleep(5)
            #if cv2.cv2.waitKey(25) & 0xFF == ord('q'):
            #    cv2.cv2.destroyAllWindows()

        pix = image.getpixel( (0,0) )
        #print ("pix: ", pix)
        if(pix==(0,0,0,255)):
            image = self.transform(image)

        #img2 = cv2.cv2.cvtColor( np.array(image), cv2.cv2.COLOR_RGB2GRAY )     
        #cv2.cv2.imshow('DINO', img2)

        size = image.size
        pixels = []
        #print (size)
        for y in range(0, size[1], 10):
            for x in range(0, size[0], 10):
                color = image.getpixel( (x,y) )
                #print (color)
                if is_dino_color(color):
                    pixels.append((x,y))

        if not pixels:
            raise Exception("Game not found!")

        self.__find_dino(pixels)

    def transform(self, image):
        pix = np.array(image)
        size = image.size
        xs = size[1]
        sd = pix.size
        #print (sd)

        '''
        for y in range(0, size[1], 10):
            for x in range(0, size[0], 10):
                #print (image.getpixel( (x,y) ))
                if image.getpixel( (x,y) )==(0,0,0,255):
                    pix[x][y] = (255,255,255,255)
                else:
                    pix[x][y] = (84,84,84,255)
        '''

        for x, tmp in enumerate( pix ):
            for y, _ in enumerate(tmp):
                #print(type(pix[x][y]) )
                #if pix[x][y].tolist()==[0,0,0,255] or pix[x][y].tolist()==[168, 168, 168, 255] or pix[x][y].tolist()==[8,8,8,255] or pix[x][y].tolist()==[38,38,38,255] or pix[x][y].tolist()==[69,69,69,255] or pix[x][y].tolist()==[70,70,70,255] or pix[x][y].tolist()==[170,170,170,255] or pix[x][y].tolist()==[169,169,169,255]:
                #    pix[x][y] = (255,255,255,255)
                if pix[x][y].tolist()==[171, 171, 171, 255]:
                    
                    #print ("pix: ", pix[x][y])
                    pix[x][y] = (84,84,84,255)
                else:
                        pix[x][y] = (255,255,255,255)
        
        return Image.fromarray(pix)


    def __find_dino(self, pixels):
        start = pixels[0]
        end = pixels[1]
        for pixel in pixels:
            if pixel[0] < start[0] and pixel[1] > start[1]:
                start = pixel
            if pixel[0] > end[0] and pixel[1] > end[1]:
                end = pixel
        self.dino_start = start
        self.dino_end = end

    def find_next_obstacle(self):
        #image = capture(178, 330, 422, 155)
        #image = capture(184, 330, 390, 135)
        #image = capture(175, 330, 390, 135)
        image = capture(175, 330, 700, 135)

        pix = image.getpixel( (0,0) )
        if(pix==(0,0,0,255)):
            image = self.transform(image)

        img2 = cv2.cv2.cvtColor( np.array(image), cv2.cv2.COLOR_RGB2GRAY )     
        #pt = (319,58)
        #cv2.cv2.rectangle(img2, pt, (pt[0]+50, pt[1]+40), (0,0,0), 1)
        cv2.cv2.imshow('DINO', img2)
        if cv2.cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.cv2.destroyAllWindows()

        dist, s, y = self.__next_obstacle_dist(image)
        if dist<25 and not self.__change_fitness:
            self.__current_fitness += 1
            self.__change_fitness = True
        elif dist > 25:
            self.__change_fitness = False
        time = datetime.now()
        delta_dist=0
        speed = 0
        if self.last_obstacle:
            if self.last_obstacle['distance']!=1000000:
                delta_dist = self.last_obstacle['distance'] - dist
                speed = (delta_dist / ((time - self.last_obstacle['time']).microseconds) * 10000)
        self.last_obstacle = obstacle(dist, s, y, speed, time)
        return self.last_obstacle

    def __next_obstacle_dist(self, image):
        s = 0
        #pt = (319,58)
        pt = (327,58)
        for y in range(pt[1], pt[1]+40 , 5):
            for x in range (pt[0], pt[0]+50, 5):
                color = image.getpixel((x,y))
                if is_dino_color(color):
                    s += 1
        #print("s: ", s)
        if s >= 64:
            raise Exception('game over!')

        size = image.size

        for x in range( 0, size[0], 5):
            for y in range(0, size[1], 5):  
                color = image.getpixel((x, y))

                if is_dino_color(color):
                    if x+100 >size[0]:
                        max_x = size[0]-x
                    else:
                        max_x = 100

                    if y+70 >size[1]:
                        max_y = size[1]-y
                    else:
                        max_y = 70

                    s=0
                    for i in range(x, x+max_x):
                        for j in range(y, y+max_y):
                            s+=1
                    return x, s, y
        return 1000000, 0, 0

    def reset(self):
        self.last_obstacle = {}
        self.__current_fitness = 0
        self.__change_fitness = False

    def get_fitness(self):
        return self.__current_fitness
        
def main():
    while True:
        vision = Vision()
        cv2.cv2.imshow('dino', capture(100, 330, 500, 155) )

        if cv2.cv2.waitKey(25) & 0xFF==ord('q'):
            cv2.cv2.destroyAllWindows()
            break

if __name__=='__main__':
    main()