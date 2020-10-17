'''
модуль для работы с поьзовательскими настройками:
Функционал:
1) update - Обновляет данные из файла
2) load - Загружает данные из файла
3) create_default_settings
4) save
'''
import os
import json

DEFAULT_SETTINGS = {'PATH_DATA_BASE': './rc/database',
                    'PATH_DATASET': '',
                    'PATH_SAVE_MODEL': './rc',
                    'ID_CARARA': 0,
                    'IP_RASPBERRY': ''
                    }

class Settings:
    '''
    Модуль для ранения настроек пользолователя
    '''

    def __init__(self, path_settings):
        '''
        Начало
        :param path_settings:
        '''
        self.path_settings = path_settings
        self.settings = DEFAULT_SETTINGS
        
        


    def update(self, setting: dict=None):
        '''
        Обновляет настройки
        :return:
        '''
        if setting is None:
            setting = self.settings

        self.settings.update(setting)
        self.save()

    def load(self):
        '''
        Загружает настройки
        :return:
        '''
        def load_json():
            '''
            ОТкрываем json
            :return:
            '''
            with open(self.path_settings, "r") as read_file:
                self.settings = json.load(read_file)
        if os.path.isfile(self.path_settings):

            load_json()
            return 0
        else:
            print("Файла с настрйками не найдено")
            print("Создаем файл со стандартными настройками")
            if self.create_default_settings() != -1:
                print("файл с настройками создан успешно")
                load_json()
                return 0
            return -1

    def create_default_settings(self):
        '''
        Создаем файл со стандартными настройками
        :return:
        '''
        return self.save()

    def save(self):
        '''
        Сохранить настройки
        :return:
        '''
        try:
            with open(self.path_settings, "w") as write_file:
                json.dump(self.settings, write_file)
        except BaseException as e:
            print("Error {}".format(e))
            return -1
        return 0

if __name__ == '__main__':
    path_sattings = os.path.join('.','rc','settings')
    
    settings = Settings(path_sattings)
    print(settings.settings)
    settings.load()

    settings.update()
    print(settings.settings)