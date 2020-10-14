'''
Функционал:
1) connect  Соедениться с базой данных
2) create_table_default Создать стандартную таблицу
3) get_users Получить информацию о пользователях
4) del_user Удалить пользователя
5) add_user Добавить пользователя
6) update_user_by_personId Обновляем информацию о пользователе
'''

import sqlite3
from sqlite3 import Error
import uuid
import datetime

class DataBase:
    '''
    Класс для работы с базой данных пользователя для бюро пропусков
    '''
    def __init__(self, pathDataBase:str):
        '''
        Открывает работу с базой данныз
        :param pathDataBase:
        '''
        self.pathDataBase = pathDataBase
        self.con = self.connect(self.pathDataBase)

    def connect(self, pathDataBase:str):
        '''
        Соеденяемся с базой данных
        :param pathDataBase:
        :return:
        '''
        try:
            con = sqlite3.connect(pathDataBase)
            return con
        except Error:
            print(Error)

    def __availability_table(self):
        '''

        :return:
        '''
        cursor = self.con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        rows = cursor.fetchall()
        if len(rows) == 0:
            return False
        else:
            return True

    def create_table_default(self):
        '''
        Создает стандартную базу данных
        :return:
        '''
        if self.__availability_table():
          return 0

        print("Таблица с пользователями не найдена:")
        cursor = self.con.cursor()
        cursor.execute(
            '''create table users
                (
                    personId text
                        constraint users_pk
                            primary key,
                    last_name text,
                    first_name text,
                    middle_name text,
                    mode_skip integer not null,
                    del DATETIME, 
                    status_photo integer
                );''')
        self.con.commit()
        print("Былы созданна Таблица с пользователями")
        return 0

    def get_users(self, count=20, remote_users=False):
        '''
        получает count пользователей с таблици с пользователями
        :param count: Количество пользователей которые необходимо вывести
        :param remote_users: Стоит ли выводить удаленных пользователей
        :return: ('038dfb1f-fc43-4ac7-bf4d-55f9d732b59c', 'Шумелев', 'Дмитрий', 'Игореви', 1, None)
        '''
        try:
            cursor = self.con.cursor()

            if remote_users:
                sql = "SELECT * FROM users LIMIT '{}'".format(count)
            else:
                sql = "SELECT * FROM users where del is NULL LIMIT '{}'".format(count)

            cursor.execute(sql)
            rows = cursor.fetchall()

        except BaseException as e:
            print("error get users {}".format(e))
            return -1
        else:
            return rows

    def del_user(self, person_id):
        '''
        Удаляет поьзователя
        :param person_id:
        :return:
        '''
        try:
            cursor = self.con.cursor()
            cursor.execute("UPDATE users SET del = '{}' where personId = '{}' ".format(datetime.datetime.now(), person_id))
            cursor.execute("UPDATE users SET mode_skip = '0' where personId = '{}' ".format(person_id))
            self.con.commit()
        except BaseException as e:
            print("error del user {}".format(e))
            return -1
        print("Пользователь удале")
        return 0

    def add_user(self, last_name, first_name, middle_name, mode_skip=1, status_photo=0):
        '''
        Добавить поьзователя
        :param last_name:
        :param first_name:
        :param middle_name:
        :param mode_skip: Изначально = 1 провускать везде
        :return: 0- все зорошо -1- Что то не так
        '''
        personId = str(uuid.uuid4())
        try:
            cursor = self.con.cursor()
            cursor.execute("INSERT INTO users(personId, last_name, first_name, middle_name, mode_skip, status_photo) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(personId, last_name, first_name, middle_name, mode_skip, status_photo))
            self.con.commit()
        except BaseException as e:
            print("error add User")
        else:
            print("Пользователь добавлен")
            return 0

    def update_user_by_personId(self, personId, last_name='', first_name='', middle_name='', mode_skip=1):
        '''
        Обновить информацию о пользователе
        :param personId: Уникальный идентификатор
        :param last_name: Фамилия
        :param first_name: Имя
        :param middle_name: Отчество
        :param mode_skip: Права на вход
        :param status_photo: Было ли проезведенно фотографирование
        :return:
        '''
        try:
            cursor = self.con.cursor()

            sql = "SELECT * FROM users where personId = '{}' ".format(personId)
            cursor.execute(sql)
            rows = cursor.fetchall()  #('091bd8f9-25ed-4c64-a2d6-4a00871d7b90', 'Шумелев', 'Дмитрий', 'Игореви', 1, None)

            last_name_old = rows[0][1]
            first_name_old = rows[0][2]
            middle_name_old = rows[0][3]
            mode_skip_old = rows[0][4]

            if last_name == '':
                last_name = last_name_old

            if first_name == '':
                first_name = first_name_old

            if middle_name == '':
                middle_name = middle_name_old

            if mode_skip == '':
                mode_skip = mode_skip_old


            cursor.execute("UPDATE users SET last_name= '{}', first_name='{}', middle_name='{}', mode_skip={} where personId = '{}' ".format(last_name, first_name, middle_name, mode_skip, personId))
            self.con.commit()
        except BaseException as e:
            print("error update {}".format(e))
            return -1

        print("Пользователь обнавлен")
        return 0

    def update_status_photo_by_personId(self, personId, status_photo):
        '''
        Обновляет статут Фотографирование
        :param personId:
        :return:
        '''
        try:
            cursor = self.con.cursor()
            cursor.execute(
                "UPDATE users SET status_photo={} where personId = '{}' ".format(status_photo, personId))
            self.con.commit()
        except BaseException as e:
            print("error update status photo {}".format(e))
            return -1
        return 0

    def __del__(self):
        print("Закрытия соеденения с базой данных")
        self.con.close()


if __name__ == '__main__':
    pathDataBase = '/home/dima/PycharmProjects/pass_office_thermoBox/rc/database'
    database = DataBase(pathDataBase)
    database.create_table_default()
    # database.add_user('Шумелев', 'Дмитрий', 'Игореви')
    # database.del_user('425abadc-0d77-4121-8353-cfc74b9772cd')
    # res = database.get_users()
    # for i in res:
    #     print(i)
    # database.update_user_by_personId('091bd8f9-25ed-4c64-a2d6-4a00871d7b90', "ntc", 'test', 'test', 2)
    database.update_status_photo_by_personId('091bd8f9-25ed-4c64-a2d6-4a00871d7b90', 2)
