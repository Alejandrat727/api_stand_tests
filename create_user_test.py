import sender_stand_request
import data

def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body

def positive_assert(first_name):
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body(first_name)
    # El resultado de la solicitud para crear un/a nuevo/a usuario/a se guarda en la variable user_response
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    # Comprueba que el campo authToken está en la respuesta y contiene un valor
    assert user_response.json()["authToken"] != ""
    # El resultado de la solicitud de recepción de datos de la tabla "user_model" se guarda en la variable "users_table_response"
    users_table_response = sender_stand_request.get_users_table()
    # String que debe estar en el cuerpo de respuesta
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]
    # Comprueba si el usuario o usuaria existe y es único/a
    assert users_table_response.text.count(str_user) == 1

# Prueba 1. Creación de un nuevo usuario o usuaria
# El parámetro "firstName" contiene dos caracteres
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

    ##Segunda Prueba.

def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")

##Prueba 3

def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
# Comprueba si la variable "response" almacena el resultado de la solicitud
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
# Comprueba si el atributo "message" en el cuerpo de respuesta se ve así:
    assert response.json()["message"] == "Has introducido un nombre de usuario no válido. " \
                                         "El nombre solo puede contener letras del alfabeto latino, " \
                                         "la longitud debe ser de 2 a 15 caracteres."

## Prueba 3

def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

## Prueba 4

def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaabaaaaa")

## Prueba 5

def test_create_user_has_space_in_first_name_get_error_response( ):
    negative_assert_symbol("A Aaa")

## Prueba 6

def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")

## Prueba 7

def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("23456789")

## Prueba 8

def negative_assert_no_firstname(user_body):
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code== 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "No se han aprobado todos los parámetros requeridos"

## 8

def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    # El parámetro "firstName" se elimina de la solicitud
    user_body.pop("firstName")
    # Comprueba la respuesta
    negative_assert_no_firstname(user_body)

# Prueba 9

def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    # Comprueba la respuesta
    negative_assert_no_firstname(user_body)

## Prueba 10

def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
