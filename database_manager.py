import mysql.connector
from typeguard import typechecked

# take password from txt file
password: str
with open('mysql root password.txt') as file:
    password = file.readline()

#connect to root user
root = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password=password,
    use_pure=True
)

#create cursor
cursor = root.cursor()


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
    #check correct input
    if anime_status not in ['currently_airing', 'not_yet_aired', 'finished_airing']:
        raise TypeError("invalid status")
    if episodes < 1:
        raise TypeError("invalid episodes")
    if season not in ['spring', 'summer', 'fall', 'winter']:
        raise TypeError("invalid season")
    
    #insert data
    cursor.execute(f"INSERT INTO anime VALUES({anime_id}, {anime_name}, {anime_status}, DEFAULT, {episodes}, {year}, {season}, {avg_episode_time}, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT)")
    
    #check insert
    cursor.execute(f"SELECT * FROM anime WHERE anime_id = {anime_id}")
    
    inputs: tuple = (anime_id, anime_name, anime_status, episodes, year, season, avg_episode_time)
    
    if inputs == cursor.fetchone(): return True
    else: return False