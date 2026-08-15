from src.database.Db_connector import Db_connector

class ReportExtractor:
    __root = None
    
    @staticmethod
    def extract(query: str):
        if (ReportExtractor.__root == None):
            Db_connector()
            ReportExtractor.__root = Db_connector.instance
        
        cursor = ReportExtractor.__root.cursor()
        
        cursor.execute(query)
        
        return cursor.fetchall()