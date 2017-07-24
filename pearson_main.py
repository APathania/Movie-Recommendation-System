# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 17:57:18 2017

@author: Abhishek Pathania

Examples to extract data from the file and how to use movie_recommend file
"""

import pearson_movie_recommend as pmr

movies = {}
for line in open('u.item',encoding='Latin 1'):
    (id,title) = line.split('|')[0:2]
    movies[id]=title
    
prefs = {}
for line in open('u.data'):
    user,movieid,rating = line.split('\t')[:3]
    prefs.setdefault(user,{})
    prefs[user][movies[movieid]] = float(rating)
    
 
#Ffunction examples    
pmr.sim_pearson(prefs['2'],prefs['200'])

person_rating = {
  'Face/Off (1997)': 3.0,
 'FairyTale: A True Story (1997)': 3.0,
 'Fargo (1996)': 5.0,
 'Fierce Creatures (1997)': 3.0,
 'Fly Away Home (1996)': 4.0,
 'Full Monty, The (1997)': 4.0,
 'Godfather, The (1972)': 5.0,
 'Good Will Hunting (1997)': 5.0,
 'Heat (1995)': 4.0,
 'Hoodlum (1997)': 4.0,
 'Ice Storm, The (1997)': 3.0,
 'In & Out (1997)': 4.0,
 'Jerry Maguire (1996)': 4.0,
 'Kolya (1996)': 5.0,
 'L.A. Confidential (1997)': 5.0,
 'Leaving Las Vegas (1995)': 4.0,
 'Liar Liar (1997)': 1.0,
 "Marvin's Room (1996)": 3.0,
 'Men in Black (1997)': 4.0,
}

pmr.similarity_matrix(prefs,person_rating,minimum_similar_movies=8)

pmr.recommendations(prefs,person_rating,minimum_similar_movies=7,number_of_movies=5)

