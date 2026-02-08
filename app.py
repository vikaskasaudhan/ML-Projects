import streamlit as st
import pickle
import requests

st.set_page_config(
    page_title="myapp",
    page_icon="image.png",
    layout="wide"
)
movie_list = pickle.load(open('movies.pkl', 'rb'))
movie_titles = movie_list['title'].values

def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c6f02f98021d2512bc72a1c9e55217d2"
    )
    data = response.json()

    if data.get('poster_path') is None:
        return "https://via.placeholder.com/500x750?text=No+Image",f"https://www.themoviedb.org/movie/{movie_id}"

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path'],f"https://www.themoviedb.org/movie/{movie_id}"



def recommend_with_title(movie):
    movie_idx = movie_list[movie_list['title']==movie].index[0] #index of movie in dataset
    distances = similarity[movie_idx]    # index of similarity matrix
    movies_list = sorted(list(enumerate(distances)),
                         reverse=True,key=lambda x:x[1])[1:11]
    vote_averages = []
    release_date = []
    recommended_movie = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movie_list.iloc[i[0]].movie_id
        # fetch poster from API
        recommended_movie.append(movie_list.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
        release_date.append(movie_list.iloc[i[0]].release_date)
        vote_averages.append(movie_list.iloc[i[0]].vote_average)

    return recommended_movie, recommended_movie_posters, release_date, vote_averages


similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    'Select a movie:',movie_titles)



if st.button('Recommend_based_on_movie_name'):
    names, posters, release_dates, vote_averages = recommend_with_title(selected_movie_name)

    total_movies = len(names)
    cols_per_row = 5

    for i in range(0, total_movies, cols_per_row):
        cols = st.columns(cols_per_row)

        for j in range(cols_per_row):
            idx = i + j
            if idx < len(names):
                with cols[j]:
                    st.text(names[idx])
                    st.write("")
                    st.image(posters[idx][0])
                    st.write("")
                    st.link_button("View on TMDB", posters[idx][1])
                    st.text(f"Release Date: {release_dates[idx]}")
                    st.progress(vote_averages[idx] / 10)
                    st.write(f"⭐ {vote_averages[idx]}")



def recommend_with_genre(movie):
    movie_idx = movie_list[movie_list['genre']==movie].index[0] #index of movie in dataset
    distances = similarity[movie_idx]    # index of similarity matrix
    movies_list = sorted(list(enumerate(distances)),
                         reverse=True,key=lambda x:x[1])[1:51]
    recommended_movie = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movie_list.iloc[i[0]].movie_id
        # fetch poster from API
        recommended_movie.append(movie_list.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie, recommended_movie_posters


movie_geres = list(set(movie_list['genre'].values))

selected_movie_genre = st.selectbox(
    'Select a movie genre:',movie_geres)


if st.button('Recommend_based_on_genre'):
    names, posters = recommend_with_genre(selected_movie_genre)

    total_movies = len(names)
    cols_per_row = 5

    for i in range(0, total_movies, cols_per_row):
        cols = st.columns(cols_per_row)

        for j in range(cols_per_row):
            idx = i + j
            if idx < len(names):
                with cols[j]:
                    st.text(names[idx])
                    st.write("")
                    st.image(posters[idx])
