# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 17:14:23 2017

@author: Abhishek Pathania
"""

from math import sqrt

def sim_pearson(p1_movie_list, p2_movie_list, minimum_similar_movies = 10):
    '''
        This function calculates pearson correlation coffeicient that is adjusted 
        with average rating.
    '''
    
    # Get the list of shared_items
    si = []
    for item in p2_movie_list:
        if item in p1_movie_list:
            si.append(item)

    # If they have no ratings in common, return 0
    n = len(si)
    
    if n >= 0 and n<=minimum_similar_movies:
        return 0
    
    avg_rating_p1 = sum([p1_movie_list[item] for item in si])/n
    avg_rating_p2 = sum([p2_movie_list[item] for item in si])/n
    
    numerator = sum([(p1_movie_list[item]-avg_rating_p1) * 
                     (p2_movie_list[item]-avg_rating_p2) for item in si])

    d1 = sqrt(sum([(p1_movie_list[item]-avg_rating_p1)**2 for item in si]))
    d2 = sqrt(sum([(p2_movie_list[item]-avg_rating_p2)**2 for item in si]))

    denominator = d1*d2        
   
    if(denominator==0):
        return 0
    return numerator/denominator

def cal_average_rating(prefs):
    '''
        This function calculates the average rating given by various users
        that is returned in dictonary of users rating.
    '''
    
    rate = {}
    for people in prefs:
        number_of_movies = len(prefs[people])
        for movie in prefs[people]:
            if(people not in rate):
                rate[people] = prefs[people][movie]/number_of_movies
            else:
                rate[people] += prefs[people][movie]/number_of_movies
    return rate

def similarity_matrix(prefs,person_rating,minimum_similar_movies = 10):
    '''
        This function returns a list of users(Top 20) with thier similarity measure 
        calculated using sim_pearson function, sorted in descending order.
    '''
    
    value = []
    
    for other in prefs:
        value.append((float("{0:.2f}".format
                            (sim_pearson(person_rating,prefs[other],minimum_similar_movies))),other))
    value.sort(reverse=True)
    
    return value[:20]

def recommendations(prefs,person_rating,minimum_similar_movies = 10,number_of_movies=10):
    '''
    This function returns a list of movies and thier predicted ratings 
    sorted in descending order with ratings.
    '''
    
    top = {}
    sim_sum = {}
    rankings = []
    person_rating_average = sum([person_rating[x] for x in person_rating])/len(person_rating)
    
    similarity = similarity_matrix(prefs,person_rating,minimum_similar_movies)
    rating_average = cal_average_rating(prefs)
    
    for v in similarity:
        value = v[0]
        other = v[1]
        for item in prefs[other]:
            prop_rating = (prefs[other][item]-rating_average[other])*value
            if(item not in person_rating and value>0):
                if(item not in top):
                    top[item] = prop_rating
                    sim_sum[item] = value
                else:
                    top[item] += prop_rating
                    sim_sum[item] += value
        
    rankings = []
    for key in top:
        temp = float("{0:.2f}".format(person_rating_average+top[key]/sim_sum[key]))
        if(temp>5):
            temp = 5.00
        rankings.append((temp,key))

    rankings.sort(reverse=True)
    
    return rankings[:number_of_movies]