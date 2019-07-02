from peewee import *
from playhouse.migrate import *

database = SqliteDatabase('/home/osboxes/progects/MedBot/mydatabase.db')
migrator = SqliteMigrator(database)

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class DictMedTest(BaseModel):
    med_test = TextField(column_name='medTest')

    class Meta:
        table_name = 'dict_med_test'

class DictCompanyMeasure(BaseModel):
    company_name = TextField(null=True)
    id_med_test = ForeignKeyField(column_name='id_med_test', field='id', model=DictMedTest, null=True)
    regexp_med_test_name = TextField(null=True)
    regexp_med_test_value = TextField(null=True)

    class Meta:
        table_name = 'dict_company_measure'

class DictGender(BaseModel):
    gender = TextField()

    class Meta:
        table_name = 'dict_gender'

class DictNormalMedTest(BaseModel):
    age = IntegerField(null=True)
    id_gender = ForeignKeyField(column_name='id_gender', field='id', model=DictGender, null=True)
    id_med_test = ForeignKeyField(column_name='id_medTest', field='id', model=DictMedTest, null=True)
    normal_lower_line_value = FloatField(column_name='normal_lowerLine_Value', null=True)
    normal_upper_line_value = FloatField(column_name='normal_upperLine_Value', null=True)

    class Meta:
        table_name = 'dict_normal_med_test'

class DictUserStatus(BaseModel):
    id = IntegerField()
    status = TextField()

    class Meta:
        table_name = 'dict_user_status'
        primary_key = False

class User(BaseModel):
    autorization = BlobField(null=True)
    birthday = TextField(null=True)
    email = TextField(null=True)
    id_gender = ForeignKeyField(column_name='id_gender', field='id', model=DictGender, null=True)
    id_status = ForeignKeyField(column_name='id_status', constraints=[SQL("DEFAULT 0")], field='id', model=DictUserStatus, null=True)
    name = TextField(null=True)
    telegram_chat_id = TextField(null=True)

    class Meta:
        table_name = 'user'

class UserMedTest(BaseModel):
    id_company = ForeignKeyField(column_name='id_company', field='id', model=DictCompanyMeasure, null=True)
    id_med_test = ForeignKeyField(backref='dict_med_test_id_med_test_set', column_name='id_medTest', field='id', model=DictMedTest)
    id_user = ForeignKeyField(column_name='id_user', field='id', model=User)
    med_test_date = TextField(column_name='medTest_date')
    med_test_value = FloatField(column_name='medTest_value')

    class Meta:
        table_name = 'user_med_test'