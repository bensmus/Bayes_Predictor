import pandas as pd
import sys
import pygame
import pygame.freetype 
import numpy as np
'''
This program aims to predict whether an individual will respond 
yes or no to 'Do you want to play golf in the (weather)?' 
based on past weather play history.

Example taken from https://www.analyticsvidhya.com/blog/2017/09/naive-bayes-explained/.
For more info about Bayes' Theorem: https://www.youtube.com/watch?v=HZGCoVF3YvM (3Blue1Brown).
'''

#pylint: disable=no-member
pygame.init()

size = 600, 600
white = 255, 255, 255
black = 0, 0, 0
gray = 176, 176, 176
red = 235, 84, 73
blue = 73, 89, 235
font = pygame.freetype.Font(r'/Users/Ben Smus/SourceCodePro-Light.ttf', 20)
edge = 500
offset = (20, 20)
textoffset = (5, 5)

data = pd.read_csv('golf_data.csv', index_col=0)


def sum_row(df, index):
    result = 0
    for col in df:
        result += df[col][index]
    return result


data['total'] = [sum_row(data, 'no'), sum_row(data, 'yes')]
'''
     overcast  rainy  sunny  total
no          0      3      2      5
yes         4      2      3      9
'''


def return_probs(data, weather):
    '''
    Find probability of yes response given weather (hypothesis given evidence)
    A_prob_B --> probability of A given B
    '''

    # weather independent response probabilities
    yes_prob = data['total']['yes'] / sum(data['total'])  
    no_prob = 1 - yes_prob

    weather_prob_yes = data[weather]['yes'] / sum_row(data, 'yes')
    weather_prob_no = data[weather]['no'] / sum_row(data, 'no')     

    yes_prob_weather = yes_prob*weather_prob_yes / (yes_prob*weather_prob_yes + no_prob*weather_prob_no)
    return yes_prob, weather_prob_yes, weather_prob_no, yes_prob_weather


def topixel(rectarr, edge, offset):
    '''
    Take a numpy array that is meant as a rect input and 
    adjust it to display properly
    '''
    rectarr *= edge
    rectarr[0] += offset[0]
    rectarr[1] += offset[1]
    rectarr = rectarr.astype(int)
    return rectarr


def draw_bayes_square(yes_prob, weather_prob_yes, weather_prob_no, edge, offset, textoffset):
    no_prob = 1 - yes_prob
    
    squarearr = np.array([0, 0, 1, 1])  # doing in unit coordinates, in left, top, width, height
    yesarr = np.array([0, 0, yes_prob, weather_prob_yes])
    noarr = np.array([yes_prob, 0, no_prob, weather_prob_no])

    square = pygame.Rect(topixel(squarearr, edge, offset))
    yesrect = pygame.Rect(topixel(yesarr, edge, offset))
    norect = pygame.Rect(topixel(noarr, edge, offset))

    screen.fill(gray, square)
    screen.fill(blue, yesrect)
    screen.fill(red, norect)

    yesstr = f'{np.round(yes_prob*weather_prob_yes, 3)}'
    nostr = f'{np.round(no_prob*weather_prob_no, 3)}'

    font.render_to(screen, (yesrect.left+textoffset[0], yesrect.top+textoffset[1]), yesstr, black)
    font.render_to(screen, (norect.left+textoffset[0], norect.top+textoffset[1]), nostr, black)


print('--------------------')
print("Joe's golfing habits")
print(data)
weather = input('Find the probability that Joe will play golf when it is: ')

yes_prob, weather_prob_yes, weather_prob_no, yes_prob_weather = return_probs(data, weather)
print(yes_prob_weather)

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
while True:
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
     
    draw_bayes_square(yes_prob, weather_prob_yes, weather_prob_no, edge, offset, textoffset)

    pygame.display.flip()