from Handler import *

if __name__ == "__main__":
    movie_file = ObjectFileHandler("movie.csv", MovieEntity)
    movie_manager = MovieManager(movie_file.get_from_csv())
    print(movie_manager)


