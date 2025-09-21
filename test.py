import data_handling
import database_manager
from typeguard import TypeCheckError
import json
import pytest


#*test data_handling module
class test_data_handling:
    
    #test get_anime_info method
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

    #test get_user_list method
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
    
    #test get_seasonal_animes method
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

#*test database_manager module
class test_database_manager:
    cursor = database_manager.get_cursor()

    #test insert_genre method
    def test_insert_genre(self):
        #clear table
        self.cursor.execute("DELETE FROM genre")
        self.cursor.execute("COMMIT;")
        
        #simple test
        database_manager.insert_genre(13, 'action')
        
        #invalid input test
        with pytest.raises(TypeCheckError):
            database_manager.insert_genre('an1', 'an2')
        with pytest.raises(TypeCheckError):
            database_manager.insert_genre('an1', 5)
        with pytest.raises(TypeCheckError):
            database_manager.insert_genre(12.1, 'an2')
        with pytest.raises(TypeError):
            database_manager.insert_genre(-16, 'an2')
        
        #insert test
        database_manager.insert_genre(45, 'isekai')
        self.cursor.execute("SELECT * FROM genre WHERE genre_id = 45")
        new_genre: tuple = (45, 'isekai', 0)
        assert new_genre == self.cursor.fetchone()
        
        #clear table
        self.cursor.execute("DELETE FROM genre")
        self.cursor.execute("COMMIT;")
    
    #test insert_anime_genres method
    def test_insert_anime_genres(self):
        # off foreign key check
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        #clear table
        self.cursor.execute("DELETE FROM anime_genres")
        self.cursor.execute("COMMIT;")
        
        #simple test
        database_manager.insert_anime_genres(12, 45)
        
        #invalid input test
        with pytest.raises(TypeCheckError):
            database_manager.insert_anime_genres(1.1, 5)
        with pytest.raises(TypeCheckError):
            database_manager.insert_anime_genres(1, 5.9)
        with pytest.raises(TypeCheckError):
            database_manager.insert_anime_genres("str", 5)
        with pytest.raises(TypeCheckError):
            database_manager.insert_anime_genres(1, '5')
        with pytest.raises(TypeError):
            database_manager.insert_anime_genres(-45, 5)
        with pytest.raises(TypeError):
            database_manager.insert_anime_genres(11, -5)
        
        #insert test
        database_manager.insert_anime_genres(13, 46)
        self.cursor.execute("SELECT * FROM anime_genres WHERE anime_id = 13 AND genre_id = 46")
        new_anime_genres: tuple = (13, 46)
        assert new_anime_genres == self.cursor.fetchone()
        
        #clear table
        self.cursor.execute("DELETE FROM anime_genres")
        self.cursor.execute("COMMIT;")
        
        # on foreign key check
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    
    #test insert_studio_production method
    def test_insert_studio_production(self):
        # off foreign key check
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        #clear table
        self.cursor.execute("DELETE FROM anime_production_studio")
        self.cursor.execute("COMMIT;")
        
        #simple test
        database_manager.insert_studio_production(66, 77)
        
        #invalid input test
        with pytest.raises(TypeCheckError):
            database_manager.insert_studio_production('goh', 78)
        with pytest.raises(TypeCheckError):
            database_manager.insert_studio_production(67, '78')
        with pytest.raises(TypeCheckError):
            database_manager.insert_studio_production(67.7, 78)
        with pytest.raises(TypeCheckError):
            database_manager.insert_studio_production(67, 78.7)
        with pytest.raises(TypeError):
            database_manager.insert_studio_production(67, -78)
        with pytest.raises(TypeError):
            database_manager.insert_studio_production(-67, 78)
        
        #insert test
        database_manager.insert_studio_production(14, 41)
        self.cursor.execute('SELECT * FROM anime_production_studio WHERE anime_id = 14 AND studio_id = 41')
        inputs: tuple = (14, 41)
        assert inputs == self.cursor.fetchone()
        
        #clear table
        self.cursor.execute("DELETE FROM anime_production_studio")
        self.cursor.execute("COMMIT;")
        
        # on foreign key check
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")