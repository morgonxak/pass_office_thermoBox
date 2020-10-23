# -*- coding: utf-8 -*-
## -*- coding: utf-8 -*-
'''
Модуль предназначен для создания классификаторов CVM и KNN по фотографиям из базы данных
'''

from sklearn import svm, neighbors
import math
import cv2
import time
import os
import os.path
import pickle
import face_recognition


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
encodings = []  # 128 уникальных признаков
person_id = []  # Уникальный ключ пользователя


def train_cvm():
    '''
    Тренировка cvm классификатора
    :return:
    '''
    clf_svm = svm.SVC(gamma='scale')
    clf_svm.fit(encodings, person_id)
    return clf_svm

def train_knn(n_neighbors=None, knn_algo='ball_tree'):
    # Определите, сколько соседей использовать для взвешивания в классификаторе KNN
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(encodings))))

    clf_knn = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    clf_knn.fit(encodings, person_id)
    return clf_knn

def load_image(path_Image, person):
    '''
    Загружаем изображения в память и формируем базу для обучения
    :param path_Image:
    :param person:
    :return:
    '''
    image = face_recognition.load_image_file(path_Image)
    face_bounding_boxes = face_recognition.face_locations(image)

    if len(face_bounding_boxes) != 1:
        # если изображения не подходит.
        print("Изображение {} не может учавствовать в трененровки: {}".format(path_Image, "Нет лица" if len(face_bounding_boxes) < 1 else "Более одного лица"))
    else:
        # Доболяем изображения
        print("Изображения добавлено: ", path_Image)
        encodings.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
        person_id.append(person)

def save_model(clf, path_save):
    '''
    Сохраняет данные обучения
    :param clf:
    :param path_save:
    :return:
    '''
    with open(path_save, 'wb') as f:
        pickle.dump(clf, f)

    return path_save

def save_BD_signs(path_save):
    '''
    Сохраняем базу данных признаков для переобучения
    :param path_save:
    :return:
    '''
    data = [encodings, person_id]
    with open(path_save, 'wb') as f:
        pickle.dump(data, f)

    return path_save

def load_BD_signs(path_pl):
    encodings, person_id = pickle.load(open(path_pl, 'rb'))

    return encodings, person_id

def pull_list_trening(data):
    for personId_data, descriptor_rgbd_data_list in data:
        if personId_data == 'test': continue
        try:
            for descriptor_rgbd_person in descriptor_rgbd_data_list:
                person_id.append(personId_data)
                encodings.append(descriptor_rgbd_person)
        except TypeError as e:
            print("error {}".format(e))


def main(path_BD, path_save_clf, pref='v2', dir_photo = 'photo_RGB'):
    '''
    Проходит по всем фотографиям и загружает данные после тренировка
    :param path_BD:
    :return:
    '''
    global encodings, person_id
    train_dir = os.listdir(path_BD)
    print("В тренировке учавствуют количество людей:", len(train_dir))
    old_time_load_data = time.time()

    for count_key, person in enumerate(train_dir):
        path_person = os.path.join(path_BD, person, dir_photo)

        pix = os.listdir(path_person)
        print("Начало загрузки фотографий для:", person)
        print("Номерн пользователя:", count_key)
        print("Количество фотографий:", len(pix))
        print("Путь до фотографий:", path_person)

        for person_img in pix:
            path_image_person = os.path.join(path_person, person_img)

            #Проверяем изображения на формат и на присутствие
            if not os.path.isfile(path_image_person) or os.path.splitext(path_image_person)[1][1:] not in ALLOWED_EXTENSIONS:
                raise Exception("Invalid image path: {}".format(path_image_person))

            load_image(path_image_person, person)

    print("Загрузка данных завершена", time.time() - old_time_load_data)

    #Обучаем нейросеть
    print('обучаем нейросети')
    clf_svm = train_cvm()
    clf_knn = train_knn()
    print("обучение завершено")
    #Сохраняем данные
    # save_model(clf_svm, os.path.join(path_save_clf, "svm_model_"+pref+'.pk'))
    # save_model(clf_knn, os.path.join(path_save_clf, "knn_model_"+pref+'.pk'))

    save_BD_signs(r'/home/dima/PycharmProjects/fase_idTest/app_faceId/models/bd' + pref + '.pl')



def branch_3(path_dataset, pathSave):
    '''
    вытаскивает из пикл файла пользователей и обучает нейросеть по ней
    :return:
    '''
    def load_image_people(pathPhoto):
        def loadImage_pickl(path):
            with open(path, 'rb') as f:
                list_photo = pickle.load(f)
            return list_photo

        def addFace_by_classification(color_image, people):
            '''
            Добовляет пользователя для классификации
            :param color_image:
            :param people:
            :return:
            '''
            face_bounding_boxes = face_recognition.face_locations(color_image)
           
            print(people)
            print(face_bounding_boxes)
            cv2.imshow('window', color_image)
            time_temp1 = time.time()
            while(time_temp1+1 > time.time()):
                None
            #time.sleep(3)
            cv2.destroyAllWindows()
            if len(face_bounding_boxes) != 1:
                # если изображения не подходит (нет человека или их много).
                print("Изображение ({}) не может учавствовать в трененровки: {}".format(people,"Нет лица" if len(
                    face_bounding_boxes) < 1 else "Более одного лица"))
            else:
                # Доболяем изображения
                encodings.append(face_recognition.face_encodings(color_image, known_face_locations=face_bounding_boxes)[0])  # 128 уникальных признаков
                person_id.append(people)  # Уникальный ключ пользователя

        i_for = 0 # кол-во успешных обработок
        list_people = os.listdir(pathPhoto)
        print("Количество пользователей в базе:", len(list_people))
        
        for people in list_people:
            if not os.path.isdir(os.path.join(pathPhoto, people)): #  проверка на файлы
                continue
            
            listRGBPhoto = os.listdir(os.path.join(pathPhoto, people, 'RGB'))
            print("Кличество RGB фото: {}".format(len(listRGBPhoto)))
            for namePhoto in listRGBPhoto: ## от нестандарта. если не стондарт, то попятка преобразовать
                if namePhoto == 'photo.png': continue
                if namePhoto == 'photo.pickl': continue
                color_image = cv2.imread(os.path.join(pathPhoto, people, 'RGB', namePhoto))
                print("0 0 0")  
                addFace_by_classification(color_image, people)
            i_for += 1
            try:
                listPhoto = loadImage_pickl(os.path.join(pathPhoto, people, 'RGB/photo.pickl'))
            except BaseException as e:
                print("error {}".format(e))
            else:
                print("Количество фото", len(listPhoto))
                for color_image in listPhoto:
                    addFace_by_classification(color_image, people)

        
        print("Загрузка данных завершена")
        return i_for
    print("0 0")    
    i = load_image_people(path_dataset)
    print("kol-vo = {}".format(i))
    print("0 1")  
    print('обучаем нейросети')
    clf_svm = train_cvm()
    clf_knn = train_knn()
    print("обучение завершено")
    # # Сохраняем данные

    pref = str(1)
    save_model(clf_svm, os.path.join(pathSave, "svm_model_" + pref + '.pk'))
    save_model(clf_knn, os.path.join(pathSave, "knn_model_" + pref + '.pk'))
    save_BD_signs(os.path.join(pathSave, "dataBase_" + pref + '.pk'))

def ViverPhoto():
    def load_image_people(pathPhoto):
        def loadImage_pickl(path):
            with open(path, 'rb') as f:
                list_photo = pickle.load(f)
            return list_photo

        def addFace_by_classification(color_image, people):
            '''
            Добовляет пользователя для классификации
            :param color_image:
            :param people:
            :return:
            '''
            face_bounding_boxes = face_recognition.face_locations(color_image)
            if len(face_bounding_boxes) != 1:
                # если изображения не подходит.
                print("Изображение не может учавствовать в трененровки: {}".format("Нет лица" if len(
                    face_bounding_boxes) < 1 else "Более одного лица"))
            else:
                # Доболяем изображения
                encodings.append(face_recognition.face_encodings(color_image, known_face_locations=face_bounding_boxes)[
                                     0])  # 128 уникальных признаков
                person_id.append(people)  # Уникальный ключ пользователя

                cv2.imshow("image", color_image)
                cv2.waitKey()

        list_people = os.listdir(pathPhoto)
        print("Количество пользователей в базе:", len(list_people))
        for people in list_people:
            listRGBPhoto = os.listdir(os.path.join(pathPhoto, people, 'RGB'))
            print("Кличество RGB фото: {}".format(len(listRGBPhoto)))
            for namePhoto in listRGBPhoto:
                if namePhoto == 'photo.png': continue
                if namePhoto == 'photo.pickl': continue
                color_image = cv2.imread(os.path.join(pathPhoto, people, 'RGB', namePhoto))
                addFace_by_classification(color_image, people)
            try:
                listPhoto = loadImage_pickl(os.path.join(pathPhoto, people, 'RGB/photo.pickl'))
            except BaseException as e:
                print("error {}".format(e))
            else:
                print("Количество фото", len(listPhoto))
                for color_image, image_RGBD in listPhoto:

                    color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
                    addFace_by_classification(color_image, people)


        print("Загрузка данных завершена")

    pathPhoto = r'/home/dima/Документы/photoBR'


    load_image_people(pathPhoto)


if __name__ == '__main__':
    branch_3('/home/dima/Документы/photoBR_test', '/home/dima/PycharmProjects/recognition_service_client_simplified/rc')
    # ViverPhoto()