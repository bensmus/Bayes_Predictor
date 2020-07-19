import pandas as pd
import sys
import pygame
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

size = 640, 480
white = 255, 255, 255
black = 0, 0, 0
red = 150, 0, 0
blue = 0, 0, 150
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

data = pd.read_csv('golf_data.csv', index_col=0)


def sum_row(df, index):
    result = 0
    for col in df:
        result += df[col][index]
    return result


data['total'] = [sum_row(data, 'no'), sum_row(data, 'yes')]
print(data)
'''
     overcast  rainy  sunny  total
no          0      3      2      5
yes         4      2      3      9
'''


def return_yes_prob_weather(data, weather):
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
    return yes_prob_weather


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


def draw_bayes_square(yes_prob, weather_prob_yes, weather_prob_no, edge, offset):
    no_prob = 1 - yes_prob
    
    square = np.array([0, 0, 1, 1])  # doing in unit coordinates, in left, top, width, height
    yesrect = np.array([0, 0, yes_prob, weather_prob_yes])
    norect = np.array([yes_prob, 0, no_prob, weather_prob_no])

    square = topixel(square, edge, offset)
    yesrect = topixel(yesrect, edge, offset)
    norect = topixel(norect, edge, offset)

    screen.fill(black, square)
    screen.fill(blue, yesrect)
    screen.fill(red, norect)


while True:
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    draw_bayes_square(0.5, 0.2, 0.3, 300, (100, 100))

    pygame.display.flip()