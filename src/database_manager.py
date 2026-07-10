from typeguard import typechecked
from src.Db_connector import Db_connector
from dotenv import load_dotenv
from os import getenv
#load .env file
load_dotenv()

#connect to root user
Db_connector()
root = Db_connector.instance

#create cursor
__cursor = root.cursor()

#!temp methods

#define a method for get cursor
def get_cursor():
    return __cursor

#!database methods

#*insert methods
#define a method for insert new genre
@typechecked
def insert_genre(genre_id: int, genre_name: str) -> bool:
    #check valid input
    if genre_id < 0:
        raise TypeError("invalid genre_id")
    if len(genre_name) > 50:
        raise ValueError("genre name is so big")
    
    #insert data
    __cursor.execute("INSERT INTO genre VALUES(%s, %s, DEFAULT)", [genre_id, genre_name])
    __cursor.execute("COMMIT;")
    
    return True

#define a method for save anime genres
@typechecked
def insert_anime_genres(anime_id: int, genre_id: int) -> bool:
    #check valid input
    if anime_id < 0:
        raise TypeError("invalid anime_id")
    if genre_id < 0:
        raise TypeError("invalid genre_id")
    
    #insert data
    __cursor.execute("INSERT INTO anime_genres VALUES(%s, %s)", [anime_id, genre_id])
    __cursor.execute("COMMIT;")
    
    return True

#define a method for save studio productions
@typechecked
def insert_studio_production(anime_id: int, studio_id: int) -> bool:
    #check valid input
    if anime_id < 0:
        raise TypeError("invalid anime_id")
    if studio_id < 0:
        raise TypeError("invalid studio_id")
    
    #insert data
    __cursor.execute("INSERT INTO anime_production_studio VALUES(%s, %s)", [anime_id, studio_id])
    __cursor.execute("COMMIT;")

    return True

#define a method for insert new studio
@typechecked
def insert_studio(studio_id: int, studio_name: str) -> bool:
    #check valid input
    if studio_id < 0:
        raise TypeError("invalid studio_id")
    if len(studio_name) > 50:
        raise ValueError("studio name is so big")
    
    #insert data
    __cursor.execute("INSERT INTO studio VALUES(%s, %s, DEFAULT)", [studio_id, studio_name])
    __cursor.execute("COMMIT;")

    return True

#define a method for insert new anime
@typechecked
def insert_anime(anime_id: int,
                anime_name: str,
                anime_status: str,
                episodes: int,
                year: int,
                season: str,
                avg_episode_time: float | int
                ) -> bool:
    #check valid input
    if anime_id < 0:
        raise TypeError("invalid anime_id")
    if len(anime_name) > 100:
        raise ValueError("anime name is so big")
    if anime_status not in ['currently_airing', 'not_yet_aired', 'finished_airing']:
        raise TypeError("invalid status")
    if episodes < 1:
        raise TypeError("invalid episodes")
    if year > 2026 or year < 1930:
        raise TypeError("invalid year")
    if season not in ['spring', 'summer', 'fall', 'winter']:
        raise TypeError("invalid season")
    if avg_episode_time < 0:
        raise TypeError("invalid avg_episode_time")
    
    #insert data
    __cursor.execute("INSERT INTO anime VALUES(%s, %s, %s, DEFAULT, %s, %s, %s, %s, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT)",
                    [anime_id, anime_name, anime_status, episodes, year, season, avg_episode_time])
    __cursor.execute("COMMIT;")

    return True

#define a method for create new account
@typechecked
def insert_account(user_name: str) -> bool:
    #check valid input
    if len(user_name) < 5:
        raise TypeError("invalid user name")
    
    #insert data
    __cursor.execute("INSERT INTO account VALUES(DEFAULT, %s, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT)", [user_name])
    __cursor.execute("COMMIT;")

    return True

#define a method for add anime to a list
@typechecked
def insert_to_list(anime_id: int, account_id: int, score: int, status: str, episodes_watched: int) -> bool:
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
    __cursor.execute("INSERT INTO list VALUES(%s, %s, %s, %s, %s)", [anime_id, account_id, score, status, episodes_watched])
    __cursor.execute("COMMIT;")

    return True

#*check exist methods
#check exist genre method
@typechecked
def check_exist_genre(genre_id: int) -> bool:
    #invalid input check
    if genre_id < 0:
        raise TypeError("invalid genre_id")
    
    #search genre
    __cursor.execute("SELECT genre_id FROM genre WHERE genre_id = %s", [genre_id])
    
    #check result
    return tuple([genre_id]) == __cursor.fetchone()

#check exist anime_genres method
@typechecked
def check_exist_anime_genres(anime_id: int, genre_id: int) -> bool:
    #check invalid input
    if anime_id < 0:
        raise TypeError("invalid anime_id")
    if genre_id < 0:
        raise TypeError("invalid genre_id")
    
    #search anime_genres
    __cursor.execute("SELECT anime_id, genre_id FROM anime_genres WHERE anime_id = %s AND genre_id = %s", [anime_id, genre_id])
    
    #check result
    return tuple([anime_id, genre_id]) == __cursor.fetchone()

#check exist studio_production method
@typechecked
def check_exist_studio_production(anime_id: int, studio_id: int) -> bool:
    #invalid input check
    if anime_id < 0:
        raise TypeError("invalid anime_id")
    if studio_id < 0:
        raise TypeError("invalid studio_id")
    
    #search studio_production
    __cursor.execute("SELECT anime_id, studio_id FROM anime_production_studio WHERE anime_id = %s AND studio_id = %s", [anime_id, studio_id])
    
    #check result
    return tuple([anime_id, studio_id]) == __cursor.fetchone()

#check exist studio method
@typechecked
def check_exist_studio(studio_id: int) -> bool:
    #invalid input check
    if studio_id < 0:
        raise TypeError("invalid studio_id")
    
    #search studio
    __cursor.execute("SELECT studio_id FROM studio WHERE studio_id = %s", [studio_id])
    
    #check result
    return tuple([studio_id]) == __cursor.fetchone()

#check exist anime method
@typechecked
def check_exist_anime(anime_id: int) -> bool:
    #invalid input check
    if anime_id < 0:
        raise TypeError("invalid anime_id")
    
    #search anime
    __cursor.execute("SELECT anime_id FROM anime WHERE anime_id = %s", [anime_id])
    
    #check result
    return tuple([anime_id]) == __cursor.fetchone()

#check exist account method
@typechecked
def check_exist_account(user_name: str) -> bool:
    #invalid input check
    if len(user_name) < 5:
        raise TypeError("invalid user_name")
    
    #search account
    __cursor.execute("SELECT user_name FROM account WHERE user_name = %s", [user_name])
    
    #check result
    return tuple([user_name]) == __cursor.fetchone()

#check exist on list method
@typechecked
def check_exist_on_list(anime_id: int, account_id: int) -> bool:
    #check invalid input
    if anime_id < 0:
        raise TypeError("invalid anime_id")
    if account_id < 0:
        raise TypeError("invalid account_id")
    
    #search on list
    __cursor.execute("SELECT anime_id, account_id FROM list WHERE anime_id = %s AND account_id = %s", [anime_id, account_id])
    
    #check result
    return tuple([anime_id, account_id]) == __cursor.fetchone()