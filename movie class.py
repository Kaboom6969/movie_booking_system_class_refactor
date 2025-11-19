from datetime import datetime



class Movie:
    def __init__(self,movie_code,movie_name,cinema_number,cinema_start_time,cinema_end_time,date,original_price,discount):
        self.movie_code = movie_code
        self.movie_name = movie_name
        self.cinema_number = cinema_number
        self.cinema_start_time = cinema_start_time
        self.cinema_end_time = cinema_end_time
        self.date = date

        try:
            self.original_price = int(original_price)
            self.discount = int(discount)
        except ValueError:
            raise ValueError("Error From class Movie: Please enter numeric value")
        except Exception as e:
            raise Exception(f"Unknown Error From class Movie: {e}")

        try:
            datetime.strptime(self.date, "%Y/%m/%d")
        except ValueError:
            raise ValueError("Error From class Movie: Invalid date (format YY/MM/DD)")
        except Exception as e:
            raise Exception(f"Unknown Error From class Movie: {e}")

    def __str__(self):
        information = ""
        for key,value in self.__dict__.items():
            information += f"{key}: {value}\n"
        return information

    @property
    def start_time(self):
        return datetime.strptime(self.cinema_start_time, "%H:%M")

    @property
    def end_time(self):
        return datetime.strptime(self.cinema_end_time, "%H:%M")

    @property
    def final_price(self):
        return self.original_price * (100 - self.discount)/100

    @property
    def movie_time(self):
        duration = self.end_time - self.start_time
        minutes = int(duration.total_seconds() / 60)

        if minutes < 0:
            minutes += 24 * 60
        return minutes

# if __name__ == "__main__":
#     movie = Movie(
#         "M001","Joker","0003",
#                   "18:00","20:00","2025/08/17","30","25"
#     )
#     print(movie)



