import pandas as pd
'''
This program aims to predict whether an individual will respond 
yes or no to 'Do you want to play golf in the (weather)?' 
based on past weather play history.

Example taken from https://www.analyticsvidhya.com/blog/2017/09/naive-bayes-explained/.
For more info about Baye's Theorem: https://www.youtube.com/watch?v=HZGCoVF3YvM (3Blue1Brown).
'''

data = pd.DataFrame(
    {
        'overcast': [0, 4], 
        'rainy': [3, 2],
        'sunny': [2, 3]
    }, 
    index=['no', 'yes']
)


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


breakpoint()