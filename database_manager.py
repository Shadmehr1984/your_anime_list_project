import mysql.connector
from typeguard import typechecked

# take __password from txt file
__password: str
with open('mysql root password.txt') as file:
    __password = file.readline()

#connect to root user
root = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    database='your_anime_list',
    password=__password,
    use_pure=True
)

#create cursor
__cursor = root.cursor()

#define a method for get cursor
def get_cursor():
    return __cursor

#!database functions

#define a method for insert new genre
@typechecked
def insert_genre(genre_id: int, genre_name: str) -> bool:
    #check valid input
    if genre_id < 0:
        raise TypeError("invalid genre_id")
    
    #insert data
    __cursor.execute(f"INSERT INTO genre VALUES({genre_id}, '{genre_name}', DEFAULT)")
    
    #check insert
    __cursor.execute(f"SELECT * FROM genre WHERE genre_id = {genre_id}")
    
    inputs: tuple = (genre_id, genre_name, 0)
    
    return inputs == __cursor.fetchone()

#define a method for save anime genres
@typechecked
def insert_anime_genres(anime_id: int, genre_id: int) -> bool:
    #check valid input
    if anime_id < 0:
        raise TypeError("invalid anime_id")
    if genre_id < 0:
        raise TypeError("invalid genre_id")
    
    #insert data
    __cursor.execute(f"INSERT INTO anime_genres VALUES({anime_id}, {genre_id})")
    
    #check insert
    __cursor.execute(f"SELECT * FROM anime_genres WHERE anime_id = {anime_id} AND genre_id = {genre_id}")
    
    inputs: tuple = (anime_id, genre_id)
    
    return inputs == __cursor.fetchone()

#define a method for save studio productions
@typechecked
def insert_studio_production(anime_id: int, studio_id: int) -> bool:
    #check valid input
    if anime_id < 0:
        raise TypeError("invalid anime_id")
    if studio_id < 0:
        raise TypeError("invalid studio_id")
    
    #insert data
    __cursor.execute(f"INSERT INTO anime_production_studio VALUES({anime_id}, {studio_id})")
    
    #check insert
    __cursor.execute(f"SELECT * FROM anime_production_studio WHERE anime_id = {anime_id} AND studio_id = {studio_id}")
    
    inputs: tuple = (anime_id, studio_id)
    
    return inputs == __cursor.fetchone()

#define a method for insert new studio
@typechecked
def insert_studio(studio_id: int, studio_name: str) -> bool:
    #check valid input
    if studio_id < 0:
        raise TypeError("invalid studio_id")
    
    #insert data
    __cursor.execute(f"INSERT INTO studio VALUES({studio_id}, '{studio_name}', DEFAULT)")
    
    #check insert
    __cursor.execute(f"SELECT * FROM studio WHERE studio_id = {studio_id}")
    
    inputs: tuple = (studio_id, studio_name, 0)
    
    return inputs == __cursor.fetchone()

#define a method for insert new anime
@typechecked
def insert_anime(anime_id: int,
                anime_name: str,
                anime_status: str,
                episodes: int,
                year: str,
                season: str,
                avg_episode_time: float
                ) -> bool:
    #check valid input
    if anime_status not in ['currently_airing', 'not_yet_aired', 'finished_airing']:
        raise TypeError("invalid status")
    if episodes < 1:
        raise TypeError("invalid episodes")
    if season not in ['spring', 'summer', 'fall', 'winter']:
        raise TypeError("invalid season")
    
    #insert data
    __cursor.execute(f"INSERT INTO anime VALUES({anime_id}, '{anime_name}', '{anime_status}', DEFAULT, {episodes}, '{year}', '{season}', {avg_episode_time}, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT)")
    
    #check insert
    __cursor.execute(f"SELECT * FROM anime WHERE anime_id = {anime_id}")
    
    inputs: tuple = (anime_id, anime_name, anime_status, episodes, year, season, avg_episode_time)
    
    return inputs == __cursor.fetchone()

#define a method for create new account
@typechecked
def insert_account(account_id: int, user_name: str) -> bool:
    #check valid input
    if account_id < 0:
        raise TypeError("invalid account_id")
    
    #insert data
    __cursor.execute(f"INSERT INTO account VALUES({account_id}, '{user_name}', DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT)")
    
    #check insert
    __cursor.execute(f"SELECT * FROM account WHERE account_id = {account_id}")
    
    inputs: tuple = (account_id, user_name, 0, 0, 0, 0, 0, 0)
    
    return inputs == __cursor.fetchone()

#define a method for add anime to a list
@typechecked
def insert_to_list(anime_id: int, account_id: int, score: float, status: str, episodes_watched: int) -> bool:
    #check valid input
    if anime_id < 0:
        raise TypeError("invalid anime_id")
    if account_id < 0:
        raise TypeError("invalid account_id")
    if score < 0 or score > 10:
        raise TypeError("invalid score")
    if status not in ['plan to watch', 'completed', 'dropped', 'on hold', 'watching']:
        raise TypeError("invalid status")
    if episodes_watched < 0:
        raise TypeError("invalid episodes number")
    
    #insert data
    __cursor.execute(f"INSERT INTO list VALUES({anime_id}, {account_id}, {score}, '{status}', {episodes_watched})")
    
    #check insert
    __cursor.execute(f"SELECT * FROM list WHERE anime_id = {anime_id} AND account_id = {account_id}")
    
    inputs: tuple = (anime_id, account_id, score, status, episodes_watched)
    
    return inputs == __cursor.fetchone()