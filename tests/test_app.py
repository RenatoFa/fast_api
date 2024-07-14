from http import HTTPStatus


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


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'id': 1, 'username': 'test', 'email': 'test@test.com'}]
    }


def test_read_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'email': 'test@test.com',
        'password': 'test',
        'username': 'test',
    }


def test_return_not_found_if_not_exist_get_user(client):
    response = client.get('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client):
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


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_return_not_found_if_not_exist_delete_user(client):
    response = client.delete(
        '/users/999',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
