import requests
import json
from time import sleep

#take client id
__client_id: str
with open('client id.txt') as file:
    __client_id = file.readline().rstrip('\n')


#inner functions:

#sending request to mal
def __send_request(url_add: str, parameters: dict) -> dict | int:
    response = requests.get(url=f'https://api.myanimelist.net/v2/{url_add}', 
                            headers={'X-MAL-CLIENT-ID' : __client_id}, 
                            params=parameters
                            )
    
    result: dict = response.json()
    
    return result, response.status_code

#saving data in a json file
def __save_data(result: dict) -> None:
    with open('temp_json.json', 'w') as file:
            json.dump(result, file, indent=4)

#!get info methods

#get anime information with using his anime id
def get_anime_info(anime_id: int, save_data: bool) -> dict:
    #valid type checking
    if type(anime_id) != int or type(save_data) != bool:
        raise TypeError('invalid input')
    
    #send request
    url_add: str = f'anime/{str(anime_id)}'
    parameters: dict = {'fields': 'id,alternative_titles,status,genres,num_episodes,start_season,source,average_episode_duration,rating,studios'}
    result: dict
    status_code: int
    result, status_code = __send_request(url_add, parameters)
    
    #check response
    if status_code != 200:
        raise KeyError('anime dont exist')
    else:
        anime_name: str = result['alternative_titles']['en']
        if len(anime_name) == 0: anime_name = result['title']
        print(f'anime {anime_name} find with {anime_id} ID')
    
    #saving or not saving data
    if save_data:__save_data(result)
    
    #a delay for rest
    sleep(0.1)
    return result

#get list of a account by using his user name
def get_user_list(user_name: str, save_data: bool) -> dict:
    #valid type checking
    if type(user_name) != str or type(save_data) != bool:
        raise TypeError('invalid input')
    
    #send request
    url_add: str = f'users/{user_name}/animelist'
    parameters: dict = {'fields': 'list_status', 'limit': 300}
    result: dict
    status_code: int
    result, status_code = __send_request(url_add, parameters)
    
    #check response
    if status_code == 403:
        raise ConnectionRefusedError(f'{user_name} list is private')
    elif status_code != 200:
        raise KeyError("user dont exist")
    else:
        print(f'user {user_name} find')
    
    #saving or not saving data
    if save_data:__save_data(result)
    
    #a delay for rest
    sleep(0.1)
    return result

#get all animes from a season
def get_seasonal_animes(season: str, year: int, save_data: bool) -> dict:
    #valid type checking
    if type(season) != str or type(year) != int or type(save_data) != bool:
        raise TypeError("invalid input")
    if season not in ['spring', 'summer', 'fall', 'winter']:
        raise TypeError("invalid season")
    if year not in range(1930, 2028):
        raise TypeError("invalid year")
    
    #send request
    url_add: str = f'anime/season/{str(year)}/{season}'
    parameters: dict = {'limit': 500}
    result: dict
    status_code: int
    result, status_code = __send_request(url_add, parameters)
    
    #check response
    if status_code != 200:
        raise KeyError('seasonal animes dont exist')
    
    #saving or not saving data
    if save_data:__save_data(result)
    
    #a delay for rest
    sleep(0.1)
    return result