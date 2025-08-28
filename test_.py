import data_handling
import pytest
import json


def test_finding_anime_and_it_data():
    #normal using test
    data_handling.get_anime_info(1, False)
    
    #not found test
    with pytest.raises(KeyError):
        data_handling.get_anime_info(2, False)
    
    #invalid input test
    with pytest.raises(TypeError):
        data_handling.get_anime_info('an', False)
    with pytest.raises(TypeError):
        data_handling.get_anime_info(66, 45)
    
    #saving test
    dic: dict
    dic = data_handling.get_anime_info(1, True)
    with open('temp_json.json') as file:
        assert dic == json.load(file)
    
    assert True

def test_user_finding():
    #simple test
    data_handling.get_user_list('ssszzzast', False)
    
    #not found test
    with pytest.raises(KeyError):
        data_handling.get_user_list('sssazzzast', False)
    
    #invalid input test
    with pytest.raises(TypeError):
        data_handling.get_user_list(45, False)
    
    assert True
