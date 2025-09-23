import data_handling
import database_manager
from typeguard import TypeCheckError
import json
import pytest


#*test data_handling module
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
    @pytest.mark.need_vpn
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
    @pytest.mark.need_vpn
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
@pytest.mark.database_manager
class test_database_manager:
    cursor = database_manager.get_cursor()
    
    #*insert tests

    #test insert_genre method
    @pytest.mark.before_dml
    @pytest.mark.insert_test
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
    @pytest.mark.before_dml
    @pytest.mark.insert_test
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
    @pytest.mark.before_dml
    @pytest.mark.insert_test
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
    
    #test insert_studio method
    @pytest.mark.before_dml
    @pytest.mark.insert_test
    def test_insert_studio(self):
        #clear table
        self.cursor.execute("DELETE FROM studio")
        self.cursor.execute("COMMIT;")
        
        #simple test
        database_manager.insert_studio(88, 'kir_studio')
        
        #invalid input test
        with pytest.raises(TypeCheckError):
            database_manager.insert_studio('kir1', 'kir2')
        with pytest.raises(TypeCheckError):
            database_manager.insert_studio(88, 78)
        with pytest.raises(TypeCheckError):
            database_manager.insert_studio(88.8, 'kir2')
        with pytest.raises(TypeError):
            database_manager.insert_studio(-8, 'kir2')
        
        #insert test
        database_manager.insert_studio(99, 'an45')
        self.cursor.execute("SELECT * FROM studio WHERE studio_id = 99")
        inputs: tuple = (99, 'an45', 0)
        assert inputs == self.cursor.fetchone()
        
        #clear table
        self.cursor.execute("DELETE FROM studio")
        self.cursor.execute("COMMIT;")
    
    #test insert_anime method
    @pytest.mark.before_dml
    @pytest.mark.insert_test
    def test_insert_anime(self):
        #clear table
        self.cursor.execute("DELETE FROM anime")
        self.cursor.execute("COMMIT;")
        
        #simple test
        database_manager.insert_anime(111, 'shady', 'finished_airing', 56, 2005, 'spring', 24.5)
        
        #invalid input test
        with pytest.raises(TypeCheckError):
            database_manager.insert_anime('222', 'nah', 'currently_airing', 12, 2025, 'fall', 21.9)
        with pytest.raises(TypeCheckError):
            database_manager.insert_anime(222, 555, 'currently_airing', 12, 2025, 'fall', 21.9)
        with pytest.raises(TypeCheckError):
            database_manager.insert_anime(222, 'nah', 888888, 12, 2025, 'fall', 21.9)
        with pytest.raises(TypeCheckError):
            database_manager.insert_anime(222, 'nah', 'currently_airing', 12.5, 2025, 'fall', 21.9)
        with pytest.raises(TypeCheckError):
            database_manager.insert_anime(222, 'nah', 'currently_airing', 12, '2025', 'fall', 21.9)
        with pytest.raises(TypeCheckError):
            database_manager.insert_anime(222, 'nah', 'currently_airing', 12, 2025, ['fall', 'spring'], 21.9)
        with pytest.raises(TypeCheckError):
            database_manager.insert_anime(222, 'nah', 'currently_airing', 12, 2025, 'fall', 'kir')
        with pytest.raises(TypeError):
            database_manager.insert_anime(-222, 'nah', 'currently_airing', 12, 2025, 'fall', 21.9)
        with pytest.raises(TypeError):
            database_manager.insert_anime(222, 'nah', 'fuck', 12, 2025, 'fall', 21.9)
        with pytest.raises(TypeError):
            database_manager.insert_anime(222, 'nah', 'currently_airing', 0, 2025, 'fall', 21.9)
        with pytest.raises(TypeError):
            database_manager.insert_anime(222, 'nah', 'currently_airing', 12, 2027, 'fall', 21.9)
        with pytest.raises(TypeError):
            database_manager.insert_anime(222, 'nah', 'currently_airing', 12, 2025, 'the', 21.9)
        with pytest.raises(TypeError):
            database_manager.insert_anime(222, 'nah', 'currently_airing', 12, 2027, 'fall', -21.9)
        
        #insert test
        database_manager.insert_anime(565, "test_anime", "currently_airing", 24, 2011, 'winter', 20.3)
        self.cursor.execute("SELECT * FROM anime WHERE anime_id = 565")
        inputs: tuple = (565, "test_anime", "currently_airing", 0, 24, 2011, 'winter', 20.3, 0, 0, 0, 0, 0)
        assert inputs == self.cursor.fetchone()
        
        #clear table
        self.cursor.execute("DELETE FROM anime")
        self.cursor.execute("COMMIT;")
    
    #test insert_account method
    @pytest.mark.before_dml
    @pytest.mark.insert_test
    def test_insert_account(self):
        #clear table
        self.cursor.execute("DELETE FROM account")
        self.cursor.execute("COMMIT;")
        
        #simple test
        database_manager.insert_account(456, 'colorFull_woman')
        
        #invalid input test
        with pytest.raises(TypeCheckError):
            database_manager.insert_account('123', 'kir2025')
        with pytest.raises(TypeCheckError):
            database_manager.insert_account(123, 2025)
        with pytest.raises(TypeError):
            database_manager.insert_account(-123, 'kir2025')
        
        #insert test
        database_manager.insert_account(999, "mobMaster69")
        self.cursor.execute("SELECT * FROM account WHERE account_id = 999")
        inputs: tuple = (999, "mobMaster69", 0, 0, 0, 0, 0, 0)
        assert inputs == self.cursor.fetchone()
        
        #clear table
        self.cursor.execute("DELETE FROM account")
        self.cursor.execute("COMMIT;")
    
    #test insert_to_list method
    @pytest.mark.before_dml
    @pytest.mark.insert_test
    def test_insert_to_list(self):
        #off foreign key check
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        #clear table
        self.cursor.execute("DELETE FROM list")
        self.cursor.execute("COMMIT;")
        
        #simple test
        database_manager.insert_to_list(12, 5858, 9, 'completed', 5)
        
        #invalid input test
        with pytest.raises(TypeCheckError):
            database_manager.insert_to_list('66', 9119, 8, 'on hold', 11)
        with pytest.raises(TypeCheckError):
            database_manager.insert_to_list(66, 9119.9, 8, 'on hold', 11)
        with pytest.raises(TypeCheckError):
            database_manager.insert_to_list(66, 9119, 8, 8.8, 11)
        with pytest.raises(TypeCheckError):
            database_manager.insert_to_list(66, 9119, 8, 'on hold', '11')
        with pytest.raises(TypeError):
            database_manager.insert_to_list(-66, 9119, 8, 'on hold', 11)
        with pytest.raises(TypeError):
            database_manager.insert_to_list(66, -9119, 8, 'on hold', 11)
        with pytest.raises(TypeError):
            database_manager.insert_to_list(66, 9119, -2, 'on hold', 11)
        with pytest.raises(TypeError):
            database_manager.insert_to_list(66, 9119, 18, 'on hold', 11)
        with pytest.raises(TypeError):
            database_manager.insert_to_list(66, 9119, 8, 'on holding', 11)
        with pytest.raises(TypeError):
            database_manager.insert_to_list(66, 9119, 8, 'on hold', -111)
        
        #insert test
        database_manager.insert_to_list(14, 3693, 5, 'dropped', 12)
        self.cursor.execute("SELECT * FROM list WHERE anime_id = 14 AND account_id = 3693")
        inputs: tuple = (14, 3693, 5, 'dropped', 12)
        assert inputs == self.cursor.fetchone()
        
        #clear table
        self.cursor.execute("DELETE FROM list")
        self.cursor.execute("COMMIT;")
        
        #on foreign key check
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    
    #*check tests
    
    #test check_exist_genre method
    @pytest.mark.before_dml
    @pytest.mark.check_test
    def test_check_exist_genre(self):
        #clear table
        self.cursor.execute("DELETE FROM genre")
        self.cursor.execute("COMMIT;")
        
        #invalid input check
        with pytest.raises(TypeCheckError):
            database_manager.check_exist_genre('na')
        with pytest.raises(TypeError):
            database_manager.check_exist_genre(-55)
        
        #simple test
        database_manager.insert_genre(12, 'kir')
        assert database_manager.check_exist_genre(12)
        
        #not found test
        assert not database_manager.check_exist_genre(66)
        
        #clear table
        self.cursor.execute("DELETE FROM genre")
        self.cursor.execute("COMMIT;")
    
    #test check_exist_anime_genres method
    @pytest.mark.before_dml
    @pytest.mark.check_test
    def test_check_exist_anime_genres(self):
        #off foreign key check
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        #clear table
        self.cursor.execute("DELETE FROM anime_genres")
        self.cursor.execute("COMMIT;")
        
        #invalid input test
        with pytest.raises(TypeCheckError):
            database_manager.check_exist_anime_genres('an', 55)
        with pytest.raises(TypeCheckError):
            database_manager.check_exist_anime_genres(54, 'an')
        with pytest.raises(TypeError):
            database_manager.check_exist_anime_genres(54, -87)
        with pytest.raises(TypeError):
            database_manager.check_exist_anime_genres(-54, 87)
        
        #simple test
        database_manager.insert_anime_genres(32, 39)
        assert database_manager.check_exist_anime_genres(32, 39)
        
        #not fount test
        assert not database_manager.check_exist_anime_genres(65, 78)
        
        #clear table
        self.cursor.execute("DELETE FROM anime_genres")
        self.cursor.execute("COMMIT;")
        
        #on foreign key check
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    
    #test check_exist_studio_production method
    @pytest.mark.before_dml
    @pytest.mark.check_test
    def test_check_exist_studio_production(self):
        #off foreign key check
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        #clear table
        self.cursor.execute("DELETE FROM anime_production_studio")
        self.cursor.execute("COMMIT;")
        
        #invalid input test
        with pytest.raises(TypeCheckError):
            database_manager.check_exist_studio_production('an', 45)
        with pytest.raises(TypeCheckError):
            database_manager.check_exist_studio_production(77, "an")
        with pytest.raises(TypeError):
            database_manager.check_exist_studio_production(-77, 45)
        with pytest.raises(TypeError):
            database_manager.check_exist_studio_production(77, -45)
        
        #simple test
        database_manager.insert_studio_production(55, 555)
        assert database_manager.check_exist_studio_production(55, 555)
        
        #not found test
        assert not database_manager.check_exist_studio_production(88, 888)
        
        #clear table
        self.cursor.execute("DELETE FROM anime_production_studio")
        self.cursor.execute("COMMIT;")
        
        #on foreign key check
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    
    #test check_exist_studio method
    @pytest.mark.before_dml
    @pytest.mark.check_test
    def test_check_exist_studio(self):
        #clear table
        self.cursor.execute("DELETE FROM studio")
        self.cursor.execute("COMMIT;")
        
        #invalid input test
        with pytest.raises(TypeCheckError):
            database_manager.check_exist_studio('an')
        with pytest.raises(TypeError):
            database_manager.check_exist_studio(-51)
        
        #simple test
        database_manager.insert_studio(64, 'kir studio')
        assert database_manager.check_exist_studio(64)
        
        #not found test
        assert not database_manager.check_exist_studio(31)
        
        #clear table
        self.cursor.execute("DELETE FROM studio")
        self.cursor.execute("COMMIT;")
    
    #test check_exist_anime method
    @pytest.mark.before_dml
    @pytest.mark.check_test
    def test_check_exist_anime(self):
        #clear table
        self.cursor.execute("DELETE FROM anime")
        self.cursor.execute("COMMIT;")
        
        #invalid input test
        with pytest.raises(TypeCheckError):
            database_manager.check_exist_anime('an')
        with pytest.raises(TypeError):
            database_manager.check_exist_anime(-11)
        
        #simple test
        database_manager.insert_anime(39, "koskhar abol", 'not_yet_aired', 65, 2025, 'fall', 26.1)
        assert database_manager.check_exist_anime(39)
        
        #not found test
        assert not database_manager.check_exist_anime(65)
        
        #clear table
        self.cursor.execute("DELETE FROM anime")
        self.cursor.execute("COMMIT;")
    
    #test check_exist_account method
    @pytest.mark.before_dml
    @pytest.mark.check_test
    def test_check_exist_account(self):
        #clear table
        self.cursor.execute("DELETE FROM account")
        self.cursor.execute("COMMIT;")
        
        #invalid input test
        with pytest.raises(TypeCheckError):
            database_manager.check_exist_account('an')
        with pytest.raises(TypeError):
            database_manager.check_exist_account(-11)
        
        #simple test
        database_manager.insert_account(1384, 'ssszzzast')
        assert database_manager.check_exist_account(1384)
        
        #not found test
        assert not database_manager.check_exist_account(6)
        
        #clear table
        self.cursor.execute("DELETE FROM account")
        self.cursor.execute("COMMIT;")
    
    #test check_exist_on_list method
    @pytest.mark.before_dml
    @pytest.mark.check_test
    def test_check_exist_on_list(self):
        #off foreign key check
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        #clear table
        self.cursor.execute("DELETE FROM list")
        self.cursor.execute("COMMIT;")
        
        #invalid input test
        with pytest.raises(TypeCheckError):
            database_manager.check_exist_on_list('an', 45)
        with pytest.raises(TypeCheckError):
            database_manager.check_exist_on_list(77, "an")
        with pytest.raises(TypeError):
            database_manager.check_exist_on_list(-77, 45)
        with pytest.raises(TypeError):
            database_manager.check_exist_on_list(77, -45)
        
        #simple test
        database_manager.insert_to_list(66, 1384, 9, 'dropped', 11)
        assert database_manager.check_exist_on_list(66, 1384)
        
        #not found test
        assert not database_manager.check_exist_on_list(99, 474)
        
        #clear table
        self.cursor.execute("DELETE FROM list")
        self.cursor.execute("COMMIT;")
        
        #on foreign key check
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")