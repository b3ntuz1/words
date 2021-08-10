from peewee import Model, SqliteDatabase, CharField, IntegerField, TextField, ForeignKeyField # noqa e501


db = SqliteDatabase('gamedata.db')


class BaseModel(Model):
    class Meta:
        database = db


class Rankings(BaseModel):
    user = CharField()
    count = IntegerField(default=0)

    class Meta:
        table_name = "rankings"


class Words(BaseModel):
    letter = CharField(1)
    word_lists = TextField()

    class Meta:
        table_name = "words"


class UsedWords(BaseModel):
    letter = CharField(1)
    word_lists = TextField()

    class Meta:
        table_name = "user_words"


class GameData(BaseModel):
    last_user = CharField(50)
    current_letter = CharField(1)
    words = TextField()

    class Meta:
        table_name = "gamedata"


db.connect()
