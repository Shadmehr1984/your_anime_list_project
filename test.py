import data_handling
import pytest
import json

class test_data_handling:
    
    def test_get_anime_info(self):
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

    def test_get_user_list(self):
        #simple test
        data_handling.get_user_list('ssszzzast', False)
        
        #not found test
        with pytest.raises(KeyError):
            data_handling.get_user_list('sssazzzast', False)
        
        #invalid input test
        with pytest.raises(TypeError):
            data_handling.get_user_list(45, False)
        
        #saving test
        dic: dict
        dic = data_handling.get_user_list('ssszzzast', True)
        with open('temp_json.json') as file:
            assert dic == json.load(file)
        
        assert True
    
    def test_get_seasonal_animes(self):
        #simple test
        data_handling.get_seasonal_animes('winter', 2024, False)
        
        #not found test
        with pytest.raises(KeyError):
            data_handling.get_seasonal_animes('spring', 2026, False)
        
        #invalid input test
        with pytest.raises(TypeError):
            data_handling.get_seasonal_animes('an', 2020, False)
        with pytest.raises(TypeError):
            data_handling.get_seasonal_animes(45, 2020, False)
        with pytest.raises(TypeError):
            data_handling.get_seasonal_animes('fall', 2028, False)
        with pytest.raises(TypeError):
            data_handling.get_seasonal_animes('winter', 'fall', False)
        with pytest.raises(TypeError):
            data_handling.get_seasonal_animes('summer', 2019, 'an')
        
        #saving test
        dic: dict
        dic = data_handling.get_seasonal_animes('winter', 2023, True)
        with open('temp_json.json') as file:
            assert dic == json.load(file)
        
        assert True