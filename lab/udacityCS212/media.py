import webbrowser

class Movie():
    VALID_RATINGS = ["G", "PG", "PG-13", "R"]
    def __init__(ajay, movie_title, movie_storyline,  
                 poster_image, youtube_trailer):        
        ajay.title = movie_title
        ajay.storyline = movie_storyline
        ajay.poster_image_url = poster_image
        ajay.trailer_youtube_url = youtube_trailer

    def show_trailer(self): #show trailer will be an instance method
        webbrowser.open(self.trailer_youtube_url)
        

# here we have replaced self by ajay it will still work because self
# is not a python keyword

# if you remove ajay from ajay.storyline then storyline won't be
# instance variable anymore


#valid ratings is a class variable, so all instance of class Movie will share the variable valid_ratings
