import os
from loguru import logger
from peewee import (
    CharField,
    IntegerField,
    Model,
    SqliteDatabase
)
from config import DATE_FORMAT, DB_PATH


db = SqliteDatabase(DB_PATH)
if os.path.exists(DB_PATH):
    logger.info(f"База данных успешно создана.")
    
class BaseModel(Model):
    """Базовая модель
    """
    class Meta:
        database = db
        
class User(BaseModel):
    """Модель Пользователь

    BaseModel: Базовая модель
    """
    user_id = IntegerField(primary_key=True, unique=True)
    username = CharField(null=True)
    full_name = CharField()
    

def create_models():
    """Создание модели
    """
    db.create_tables(BaseModel.__subclasses__())