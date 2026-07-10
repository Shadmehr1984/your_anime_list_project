from src import data_handling
from src import database_manager
from typeguard import typechecked, TypeCheckError

#!temp methods:

#find right title
@typechecked
def __get_right_title(en_title: str, title: str) -> str:
    if en_title == '': return title
    return en_title

#write correct status
@typechecked
def __get_right_status(status: str) -> str:
    status = status.replace('_', ' ', status.count('_'))
    return status

#!loading data from mal to database:

#load all anime info from mal into database (inside this method all genres and studios the anime have will be added)
@typechecked
def load_anime(anime_id: int) -> bool :
    #invalid input checking
    if anime_id < 0:
        raise TypeError("invalid anime_id")
    
    #get anime info
    try:
        result: dict = data_handling.get_anime_info(anime_id, False)
    except KeyError as e:
        print(e.__str__() + '\n')
        return False
    
    #check anime exist
    if database_manager.check_exist_anime(anime_id):
        print("anime already exist")
        return False
    
    #load anime info to database
    anime_name: str = __get_right_title(result['alternative_titles']['en'], result['title'])
    try:
        year: int = result['start_season']['year']
        season: str = result['start_season']['season']
        database_manager.insert_anime(
            anime_id=anime_id,
            anime_name=anime_name,
            anime_status=result['status'],
            episodes=result['num_episodes'],
            year=year,
            season=season,
            avg_episode_time=(result['average_episode_duration'])/60
        )
    except TypeCheckError as e:
        print(e.__str__() + '\n')
        return False
    except TypeError as e:
        print(e.__str__() + '\n')
        return False
    except ValueError as e:
        print(e.__str__() + '\n')
        return False
    except KeyError as e:
        print(e.__str__())
        return False
    
    print('anime inserted')
    
    #add new genres
    try:
        for genre in result['genres']:
            if not database_manager.check_exist_genre(genre['id']):
                database_manager.insert_genre(genre['id'], genre['name'])
    except TypeCheckError as e:
        print(e.__str__() + '\n')
    except TypeError as e:
        print(e.__str__() + '\n')
    finally:
        print("all anime genres checked")
    
    #add anime genres
    try:
        for genre in result['genres']:
            database_manager.insert_anime_genres(anime_id, genre['id'])
    except TypeCheckError as e:
        print(e.__str__() + '\n')
    except TypeError as e:
        print(e.__str__() + '\n')
    except ValueError as e:
        print(e.__str__() + '\n')
    finally:
        print("all anime genres added")
    
    #add new studios
    try:
        for studio in result['studios']:
            if not database_manager.check_exist_studio(studio['id']):
                database_manager.insert_studio(studio['id'], studio['name'])
    except TypeCheckError as e:
        print(e.__str__() + '\n')
    except TypeError as e:
        print(e.__str__() + '\n')
    except ValueError as e:
        print(e.__str__() + '\n')
    finally:
        print('all anime studios checked')
    
    #add anime studio production
    try:
        for studio in result['studios']:
            database_manager.insert_studio_production(anime_id, studio['id'])
    except TypeCheckError as e:
        print(e.__str__() + '\n')
    except TypeError as e:
        print(e.__str__() + '\n')
    finally:
        print("all anime studio production added")
    
    print('\n')
    return True

#load all seasonal anime info from mal into database (inside this method all genres and studios the anime have will be added)
@typechecked
def load_seasonal_anime(year: int, season: str, limit: int = 1000) -> bool:
    #invalid input checking
    if year not in range(1930, 2028):
        raise TypeError("invalid year")
    if season not in ('spring', 'summer', 'fall', 'winter'):
        raise TypeError("invalid season")
    
    #get seasonal anime info
    result: dict = data_handling.get_seasonal_animes(season, year, False, limit)
    for anime in result['data']:
        load_anime(anime['node']['id'])
    
    print("all seasonal anime added")
    print('\n')
    return True

#load all account info from mal into database (inside this method all genres and studios the anime have will be added)
def load_account_info(user_name: str, limit: int = 1000) -> bool:
    #invalid input checking
    if len(user_name) < 5:
        raise TypeError("invalid user_name")
    
    #get account info
    try:
        result: dict = data_handling.get_user_list(user_name, False, limit)
    except KeyError as e:
        print(e)
        return False
    
    #load user if not exist
    if not database_manager.check_exist_account(user_name):
        database_manager.insert_account(user_name)
        print("user added")
    else:
        print("user already exist")
        return False
    
    #get account id on database
    cursor = database_manager.get_cursor()
    cursor.execute(f"SELECT account_id FROM account WHERE user_name = '{user_name}'")
    account_id: int = cursor.fetchone()[0]
    
    #load user list
    for anime in result['data']:
        #load anime if not exist on database
        anime_id: int = anime['node']['id']
        anime_inserted: bool = True
        if not database_manager.check_exist_anime(anime_id):
            anime_inserted = load_anime(anime_id)
        if not anime_inserted:
            print("anime not inserted")
            continue
        
        #add anime to user's list
        score: int = anime['list_status']['score']
        status: str = __get_right_status(anime['list_status']['status'])
        episodes_watched: int = anime['list_status']['num_episodes_watched']
        database_manager.insert_to_list(anime_id, account_id, score, status, episodes_watched)
        print(f"{anime_id} anime added to {user_name} list\n")
    
    print("finish")
    return True

