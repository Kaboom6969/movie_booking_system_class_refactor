from Manager import *

if __name__ == "__main__":
     movie_all = MovieManager()
     movie_all.add_for_non_entity('M001', 'Joker', '0001', '18:00', '20:00',
                   '2025/01/12','30','25')
     movie_all.add_for_non_entity('M002', 'Joker', '0001', '18:00', '20:00',
                   '2025/01/12','30','25')
     print(movie_all)


