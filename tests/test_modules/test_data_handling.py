import pytest
from src.modules.main import data_handling
from typeguard import TypeCheckError
import json


@pytest.mark.data_handling
class test_data_handling:
    
    #test get_anime_info method
    @pytest.mark.need_vpn
    def test_get_anime_info(self):
        #normal using test
        data_handling.get_anime_info(1, False)
        
        #not found test
        with pytest.raises(KeyError):
            data_handling.get_anime_info(2, False)
        
        #invalid input test
        with pytest.raises(TypeCheckError):
            data_handling.get_anime_info('an', False)
        with pytest.raises(TypeCheckError):
            data_handling.get_anime_info(66, 45)
        with pytest.raises(TypeError):
            data_handling.get_anime_info(-1, True)
        
        #saving test
        dic: dict
        dic = data_handling.get_anime_info(1, True)
        with open('temp_json.json') as file:
            assert dic == json.load(file)
        
        assert True

    #test get_user_list method
    @pytest.mark.need_vpn
    def test_get_user_list(self):
        #simple test
        data_handling.get_user_list('ssszzzast', False, 20)
        
        #not found test
        with pytest.raises(KeyError):
            data_handling.get_user_list('sssazzzast', False, 25)
        
        #invalid input test
        with pytest.raises(TypeCheckError):
            data_handling.get_user_list(45, False, 30)
        with pytest.raises(TypeCheckError):
            data_handling.get_user_list('ssszzzast', 8, 30)
        with pytest.raises(TypeCheckError):
            data_handling.get_user_list('ssszzzast', False, True)
        with pytest.raises(TypeError):
            data_handling.get_user_list('up', False, 30)
        with pytest.raises(TypeCheckError):
            data_handling.get_user_list('i hate kh', False, 0)
        
        #saving test
        dic: dict
        dic = data_handling.get_user_list('ssszzzast', True, 20)
        with open('temp_json.json') as file:
            assert dic == json.load(file)
        
        assert True
    
    #test get_seasonal_animes method
    @pytest.mark.need_vpn
    def test_get_seasonal_animes(self):
        #simple test
        data_handling.get_seasonal_animes('winter', 2024, False, 50)
        
        #not found test
        with pytest.raises(KeyError):
            data_handling.get_seasonal_animes('spring', 2027, False, 6)
        
        #invalid input test
        with pytest.raises(TypeError):
            data_handling.get_seasonal_animes('an', 2020, False, 50)
        with pytest.raises(TypeCheckError):
            data_handling.get_seasonal_animes(45, 2020, False, 50)
        with pytest.raises(TypeError):
            data_handling.get_seasonal_animes('fall', 2028, False, 50)
        with pytest.raises(TypeCheckError):
            data_handling.get_seasonal_animes('winter', 'fall', False, 50)
        with pytest.raises(TypeCheckError):
            data_handling.get_seasonal_animes('summer', 2019, 'an', 50)
        with pytest.raises(TypeCheckError):
            data_handling.get_seasonal_animes('fall', 2020, False, 'kir')
        with pytest.raises(TypeError):
            data_handling.get_seasonal_animes('fall', 2028, False, 0)
        
        #saving test
        dic: dict
        dic = data_handling.get_seasonal_animes('winter', 2023, True)
        with open('temp_json.json') as file:
            assert dic == json.load(file)
        
        assert True
