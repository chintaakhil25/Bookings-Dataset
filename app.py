import streamlit as st
import pickle
import pandas as pd
import requests

movies_list_dict = pickle.load(open('movies_dict.pkl','rb'))
movies_list = pd.DataFrame(movies_list_dict)
movie_names = movies_list['title'].values
similarity = pickle.load(open('similarity.pkl','rb'))


def fetch_posters(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjNGYzYThjMTc5OTE0YzEwMDQ3MTZiMzk2Njk0NDQzZiIsIm5iZiI6MTczMDk4ODI4Mi44MDAwOTg3LCJzdWIiOiI2NzJjYzU0NDI2YjYwNWJjMTllNWM3NDMiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.Rv1OtjdBso7DbGpl-7RoyJUlIbOOA05c3jdm6hou_Ss"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(movie):
    movie_index =movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_lis = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_lis:
        movie_id = movies_list.iloc[i[0]].movie_id
        recommended_movies.append(movies_list.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_posters(movie_id))
    return recommended_movies,recommended_movie_posters


st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Enter the Movie",
    (movie_names)
)

if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)
    col1, col2, col3,col4,col5= st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])



