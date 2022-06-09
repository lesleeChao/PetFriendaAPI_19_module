from api import PetFriends
from settings import *
import os
pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pet(auth_key, filter)
    assert status == 200
    assert len(result["pets"]) > 0


def test_add_new_pet_with_valid_data(name='Tom', animal_type='Cat', age='3', pet_photo='images/cat.jpeg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_delete_pet_from_self_list():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pet(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Jack", "cat", "2", "images/cat.jpeg")
        _, my_pets = pf.get_list_of_pet(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status,_ = pf.delete_pet_info(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pet(auth_key, my_pets)

    assert status == 200
    assert pet_id not in my_pets


def test_successful_update_self_pet_info(name='Ron', animal_type='cat', age=9):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pet(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name


# тест_1 Попытка получения api с не существующими данными
def test_get_api_with_wrong_data(email=non_existent_email, password=non_existent_pass):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


# тест_2 Создание животного без имени
def test_add_new_pet_with_empty_name(name='', animal_type='Cat', age='3', pet_photo='images/cat.jpeg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    if name == 0:
        assert status == 400
        assert result["message"] == 'Введите имя питомца!'


# тест_3 Создание животного без поля animal type
def test_add_new_pet_with_empty_animal_type(name='Jack', animal_type='', age='3', pet_photo='images/cat.jpeg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    if animal_type == 0:
        assert status == 400
        assert result["message"] == 'Введите породу питомца!'


# тест_4 создание нового питомца без фотографии
def test_add_new_pet_with_empty_photo(name='Jack', animal_type='Cat', age='3', pet_photo=''):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    if pet_photo == '':
        assert status == 400
        assert result["message"] == 'Загрузите фото питомца!'


# тест_5 Попытка изменить информацию с неправильным индексом
def test_update_self_pet_with_wrong_index(name='Jhon', animal_type='cat', age=9):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pet(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][2]['id'], name, animal_type, age)
        assert status == 400
        assert result['name'] != name


# тест_6 ввод отрицательных чисел в поле возраст
def test_add_new_pet_with_wrong_age(name='Jack', animal_type='Cat', age='-3', pet_photo='images/cat.jpeg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    if age < '':
        assert status == 400
        assert result['message'] == 'Веден некорректный возраст'


# тест_7 получение api с пустыми полями email password
def test_empty_email_password(email='', password=''):
    status, result = pf.get_api_key(valid_email, valid_password)
    if email or password == 0:
        assert status == 403
        assert result['message'] == 'Заполните пропущенные строки'

