from flask import Flask , render_template , request , url_for
import pickle
import pandas as pd
import numpy as np


credit = pickle.load(open('MLmodels\credit.pkl'    , 'rb'))
dataframe  = pickle.load(open('MLmodels\dataframe.pkl' , 'rb'))
movie = pickle.load(open('MLmodels\movie.pkl'     , 'rb'))
similar_movies = pickle.load(open('MLmodels\simliar.pkl' , 'rb'))


df = pickle.load(open('MLmodels\df.pkl' , 'rb'))
similar = pickle.load(open('MLmodels\model.pkl' , 'rb'))

popular_df = pickle.load(open('MLmodels\popular.pkl','rb'))
pt = pickle.load(open('MLmodels\pt.pkl' , 'rb'))
book = pickle.load(open('MLmodels\_book_set.pkl' , 'rb'))
similar_score = pickle.load(open('MLmodels\similar_score.pkl' , 'rb'))

app = Flask(__name__)



@app.route("/")
def first_page():
    return render_template('firstpage.html')

#********************************Movieee*********************************************

#@app.route('/button' , methods = ["POST","GET"])



@app.route("/movie_rocommend" , methods = ["GET","POST"])
def movie_rocommend():
    return render_template('movie.html')

@app.route("/recommend_moviesss" , methods = ["GET" , "POST"])
def recommend_moviesss():
    user_input = request.form.get('Input')
    print(user_input)
    movie_index = dataframe[dataframe['title'] == user_input].index[0]
    distance = similar_movies[movie_index]
    movie_list = sorted(list(enumerate(distance)),reverse=True , key = lambda x:x[1])[1:5]
    print(movie_list)
    data = []
    description = []
    
    for i in movie_list:
        #item = []
        #print(i[0])for index only
        d = dataframe.iloc[i[0]].title
        t = dataframe.iloc[i[0]].Tags
        #item.append(df.iloc[i[0]].title)
        # item.append([movie['original_language'][0]])
        #c = movie['original_language'].values
        #l.append(c)
        data.append(d)
        description.append(t) 

        
    #print(data)
    return render_template('movie.html' ,  data_description = zip(data , description))

#@app.route("/movie_rocommend" , methods = ["GET","POST"])
#def movie_rocommend():
 #   return render_template('movie.html')



#*******************************Musicccc*************************************************

#@app.route('/button' , methods = ["POST","GET"])


@app.route('/music_rocommend' , methods = ["POST","GET"])   
def music_rocommend():
    return render_template('music.html')


@app.route('/recommend_music' , methods = ["POST","GET"])
def recommend_music():
    user_input = request.form.get('Input')
    print(user_input)
    song_index = df[df['song'] == user_input].index[0]
   # print(song_index)
    distance = similar[song_index]
    #print(distance)
    song_list = sorted(list(enumerate(distance)), reverse=True , key=lambda x:x[1]) [0:5]
    #print(song_list)
    data = []
    song = []
    artis = []


    for i in  song_list:
       
       d = df.iloc[i[0]].song
       t = df.iloc[i[0]].text[0:200]
       a = df.iloc[i[0]].artist
       #print(t)
       data.append(d)
       song.append(t)
       artis.append(a)

    #print(data)
    return render_template('music.html', data_songs_artis = zip(data,song,artis))
       
#def music_recommend():
   # return render_template('Music.html')


#*********************************************Book************************************************
@app.route('/Firstsearching_book' , methods = ['GET' , 'POST'])
def Firstsearching_book():
    return render_template("Book.html")


@app.route('/book_recommendd' , methods = ["GET","POST"])
#book_recommended
def book_recomm():
        user_input = request.form.get('user_input')
    
        index = np.where(pt.index == user_input)[0][0]
        similar_item = sorted(list(enumerate(similar_score[index])) , key=lambda z:z[1] , reverse=True) [1:6]
        data = []
        for i in similar_item:
        # print(pt.index[i[0]])
            item = []
            temp_df = book[book['Book-Title'] == pt.index[i[0]]]
            item.extend(temp_df.drop_duplicates('Book-Title')['Book-Title'].values)
            item.extend(temp_df.drop_duplicates('Book-Title')['Book-Author'].values)
            item.extend(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values)
            item.extend(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values)
        
            data.append(item)
        #print(data)
        return render_template('Book.html' , data = data)
    












if __name__ == '__main__':
    app.run(debug=True)