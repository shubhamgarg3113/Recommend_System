import numpy as np
import pandas as pd
import ast

movies = pd.read_csv(r"C:\Users\shubh\OneDrive\Desktop\python_VS\movie_add\tmdb_5000_movies.csv")
credits = pd.read_csv(r"C:\Users\shubh\OneDrive\Desktop\python_VS\movie_add\tmdb_5000_credits.csv")
movies.head(1)
credits.head(1)
movies = movies.merge(credits ,on='title')
# genres, 	keywords, id, title, overview, cast, crew

movies = movies[["id","title","genres", "keywords",   "overview", "cast", "crew"]]
movies.head(1)
movies.isnull().sum()
movies.dropna(inplace=True)
movies.duplicated().sum()
movies.iloc[0].genres
def convert(obj):
    l = []
    for i in ast.literal_eval(obj):
        l.append(i['name'])
    return l    
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
import ast

def convert4(obj):
    l = []
    counter = 0
    try:
        data = ast.literal_eval(obj)
        for i in data:
            if counter != 3:
                l.append(i['name'])
                counter += 1
            else:
                break
    except (ValueError, SyntaxError, TypeError):
        pass
    return l
movies['cast'] = movies['cast'].apply(convert4)
def fatch_dir(obj):
  l=[]
  for i in ast.literal_eval(obj):
    if i['job'] == 'Director':
      l.append(i['name'])
      break
  return l
movies['crew'] = movies['crew'].apply(fatch_dir)
movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])
movies['tags'] = movies['genres'] + movies['cast'] + movies['crew'] + movies['keywords'] + movies['overview']
new_df= movies[['id', 'title', 'tags']]
new_df.head()
new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())
new_df.head()
import nltk
from nltk.stem.porter import PorterStemmer
ps= PorterStemmer()
def stem(text):
  y=[]
  for i in text.split():
    y.append(ps.stem(i))
  return " ".join(y)
new_df['tags'] = new_df['tags'].apply(stem)
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words="english")
vector = cv.fit_transform(new_df['tags']).toarray()
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vector)
sorted(list(enumerate(similarity[0])),reverse=True, key=lambda x:x[1])[1:6]
def recommend(movie):
  movie_index = new_df[new_df['title']== movie].index[0]
  distance = similarity[movie_index]
  movie_list = sorted(list(enumerate(distance)),reverse=True, key=lambda x:x[1])[1:6]
  for i in movie_list:
    print(new_df.iloc[i[0]].title)
print(recommend("Spectre"))
import pickle
pickle.dump(new_df,open('movie_dict.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))
