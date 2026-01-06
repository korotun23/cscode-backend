import pandas as pd
from app.domain.models import DatabaseFile

class DatabaseService:
    
    @staticmethod
    def get_stats(databaseFile: DatabaseFile):
        df = pd.read_csv(databaseFile.path)
        return {
            "rows": len(df),
            "columns": list(df.columns),
        }