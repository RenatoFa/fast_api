from http import HTTPStatus

from fast_zero.schemas.user import UserPublic


def test_root_return_ok_and_hello_word_message(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'password': 'test',
            'email': 'test@test.com',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'email': 'test@test.com',
        'id': 1,
        'username': 'test',
    }


def test_create_user_should_handle_error_if_username_has_registration(
    client, user
):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'password': 'test',
            'email': 'test@test.com',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username alredy exists'}


def test_create_user_should_handle_error_if_email_has_registration(
    client, user
):
    response = client.post(
        '/users/',
        json={
            'username': 'teste1',
            'password': 'teste@test.com',
            'email': 'teste@test.com',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email alredy exists'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'email': 'teste@test.com',
        'password': 'testtest',
        'username': 'Teste',
    }


def test_return_not_found_if_not_exist_get_user(client):
    response = client.get('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'id': 1,
            'username': 'test2',
            'email': 'test@test.com',
            'password': 'test2',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'email': 'test@test.com',
        'id': 1,
        'username': 'test2',
    }


def test_return_not_found_if_not_update_exist_user(client):
    response = client.put(
        '/users/999',
        json={
            'id': 1,
            'username': 'test2',
            'email': 'test@test.com',
            'password': 'test2',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_return_not_found_if_not_exist_delete_user(client):
    response = client.delete(
        '/users/999',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
