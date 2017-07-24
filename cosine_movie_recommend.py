####################################Importing Necessary Libraries######################################## 

import pandas as pd
import numpy as np

###################################Creating Dataframe of Required Data#####################################

#fetching user data about ratings of movies
column_names = ['user_id', 'item_id', 'rating', 'timestamp']
users = pd.read_csv('Data\\u.data', sep='\t', names=column_names)

#fetching data about movies according to their features
i_cols = ['movie id', 'movie title' ,'release date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
movies = pd.read_csv('Data\\u.item', sep='|', names=i_cols,encoding='latin-1')

#creating a table for movies with their average rating (using users dataframe)
k = pd.DataFrame(users.groupby('item_id')['rating'].mean())
movies.drop(['release date','video release date','IMDb URL'],axis=1,inplace=True)
k.index.names = ['movie id']
movies.set_index('movie id',inplace=True)
movies = movies.join(k)

#################################Comparing Movies using Consine Similarity##################################
from sklearn.metrics.pairwise import cosine_similarity

movie_info = movies.drop([ 'unknown', 'Action', 'Adventure', 'Animation',
       "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
       'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
       'Thriller', 'War', 'Western'],axis=1)

#Function to find similar movies
def similar_movies(name):
    star_df = movies[movies['movie title'].str.contains(name)==True]

    if(len(star_df)>0):
        sim = cosine_similarity(star_df.drop(['movie title','rating'],axis=1),movies.drop(['movie title','rating'],axis=1))
        
        new_sim = np.empty(1682)
        new_sim.fill(0)

        if(len(star_df)>1):
            for i in range(len(star_df)):
                new_sim += (sim[i]/len(star_df))
        else:
            new_sim = sim
        
        new_sim = new_sim.reshape((1682,1))
        sim_df = pd.DataFrame(new_sim,columns=['Correlation'],index=range(1,1683))
        sim_df.index.name = 'movie id'
        sim_df = sim_df.join(movie_info)
        return sim_df
    return False

#Function to query the databese
def movie_n(name,correlation,number,rating):

    sim_df = similar_movies(name)
    #print(sim_df.head(2))
    if(type(sim_df)!=type(True)):
        k = sim_df[(sim_df['Correlation']>correlation) & (sim_df['rating']>rating)][['movie title','Correlation']]
        k.sort_values('Correlation',ascending=False,inplace=True)
        k.drop(['Correlation'],axis=1,inplace=True)
        if(len(k)>0):
            print(k.head(number))
        else:
            print("Sorry, movie can't be recommended with given constraint")
    else:
        print('Movie you like does not exist in database')

#########################################Query################################################
        
name = input('Enter the name of movie: ')
simi = float(input('Enter pecentage of similarity (1-100): '))/100
rating = float(input('Enter minimum ratings of recommended movies: '))
number = int(input('Enter number of movies to be recommended: '))

movie_n(name,simi,number,rating)

