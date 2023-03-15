import threading

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Text,
    Integer,
    select,
    delete,
    DateTime,
    func, exc
)

from config import MYSQL_URL

engine = create_engine(MYSQL_URL)
meta = MetaData()


class HouseManager():

    def __init__(self, engine) -> None:
        self.engine = engine
        self.house = self.get_table_schema()
        # self.mutex = threading.Lock()

    def get_table_schema(self):
        house = Table(
            "houses5", meta,
            Column("id", Integer, primary_key=True),
            Column("title", String(200)),
            Column("som", Integer),
            Column("dollar", Integer),
            Column("mobile", String(50)),
            Column("description", Text),
            Column('link', String(255), nullable=False, unique=True),
            Column('created', DateTime(timezone=True), server_default=func.now())
        )
        return house

    def create_table(self):
        meta.create_all(self.engine, checkfirst=True)
        print("Таблица успешно создана")

    def insert_house(self, data):
        ins = self.house.insert().values(
            **data
        )
        connect = self.engine.connect()
        result = connect.execute(ins)
        connect.commit()
        connect.close()


    def check_house_in_db(self, url):
        query = select(self.house).where(self.house.c.link == url)
        connect = self.engine.connect()
        result = connect.execute(query)
        connect.close()

        result = result.fetchone()
        return result is not None

    # def check_house_in_db(self, url):
    #     # self.mutex.acquire()
    #
    #     query = select(self.house).where(self.house.c.link == url)
    #     try:
    #         with self.engine.connect() as connect:
    #             result = connect.execute(query)
    #             # result = result.fetchone()
    #
    #     except exc.OperationalError as err:
    #         if err.connection_invalidated:
    #             print('обходим ошибку')
    #             with self.engine.connect() as connect:
    #                 result = connect.execute(query)
    #                 # result = result.fetchone()
    #
    #     result = result.fetchone()
    #     # self.mutex.release()
    #     return result is not None


    def search_by_room_count(self, count):
        query = select(self.house).where(self.house.c.title.like(f'{count}%'))
        connect = self.engine.connect()
        result = connect.execute(query)
        connect.close()

        houses = result.fetchall()
        return houses

    def search_by_price(self, start, end):
        query = select(self.house).where(self.house.c.som.between(start, end))
        connect = self.engine.connect()
        result = connect.execute(query)
        connect.close()

        houses = result.fetchall()
        return houses

    def delete_post(self, old_time):
        query = delete(self.house).where(self.house.c.created <= old_time) # создание запроса
        connect = self.engine.connect()
        result = connect.execute(query)
        connect.commit()
        connect.close()


manager = HouseManager(engine=engine)
