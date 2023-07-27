import streamlit as st 
st.set_page_config(page_title=" Movie Recommender App", layout="wide")
st.markdown("<h1 style='text-align: center; color: white;'> Movie Recommender System </h1>", unsafe_allow_html=True)

# img = Image.open('./images/favicon.png')
# st.set_page_config(page_title='Movie Recommender Engine' , page_icon=img , layout="centered",initial_sidebar_state="expanded")


import pickle
import requests



movies = pickle.load(open("movies.pkl" , 'rb'))

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Fetch poster
def fetch_poster(movie_id):
    url="https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    response_data = requests.get(url)
    response_data = response_data.json()
    poster_path = response_data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


# recommend function
def recommend(movie):
    movie_index = movies[movies['title']== movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)) , reverse = True , key = lambda x:x[1])[1:6]
    
    recommended_movie_names = []
    recommended_movie_posters = []
    
    # fetch poster 

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)  
        
        # fetch poster from API
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names , recommended_movie_posters



# st.title("Movie Recommender System")


selected_mname = st.selectbox(
    'Type or select the Movie.', movies['title'].values )
st.write('You selected:', selected_mname)


if st.button("Recommend "):
    
    recommended_movie_names , recommended_movie_posters = recommend(selected_mname)

    col1, col2, col3, col4, col5 = st.columns(5)
     # Loop through the recommended movies and display them in columns
    for i, (name, poster) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
        with col1 if i == 0 else col2 if i == 1 else col3 if i == 2 else col4 if i == 3 else col5:
            st.text(name)
            st.image(poster, use_column_width=True)
