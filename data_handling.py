import requests
import json
from time import sleep

__client_id: str
with open('client id.txt') as file:
    client_id = file.readline().rstrip('\n')


def get_anime_info(anime_id: int, save_data: bool) -> dict:
    if type(anime_id) != int or type(save_data) != bool:
        raise TypeError
    
    response = requests.get(url=f'https://api.myanimelist.net/v2/anime/{str(anime_id)}', 
                            headers={'X-MAL-CLIENT-ID' : client_id}, 
                            params={'fields': 'id,alternative_titles,status,genres,num_episodes,start_season,source,average_episode_duration,rating,studios'}
                            )
    
    result: dict = response.json()
    if response.status_code != 200:
        raise KeyError('anime dont exist')
    else:
        anime_name: str = result['alternative_titles']['en']
        if len(anime_name) == 0: anime_name = result['title']
        print(f'anime {anime_name} find with {anime_id} ID')
    
    if save_data:
        with open('temp_json.json', 'w') as file:
            json.dump(result, file, indent=4)
    
    
    sleep(1)
    return result


def get_user_list(user_name: str, save_data: bool) -> dict:
    if type(user_name) != str or type(save_data) != bool:
        raise TypeError
    
    response = requests.get(url=f'https://api.myanimelist.net/v2/users/{user_name}/animelist',
                            headers={'X-MAL-CLIENT-ID' : client_id},
                            params={'fields': 'list_status', 'limit': 300}
                            )
    
    result: dict = response.json()
    if response.status_code != 200:
        raise KeyError("user dont exist")
    else:
        print(f'user {user_name} find')
    
    if save_data:
        with open('temp_json.json', 'w') as file:
            json.dump(result, file, indent=4)
    
    sleep(1)
    return result

