from sqlalchemy import select

from fast_zero.models.user import User


def test_create_user(session):
    user = User(username='test', password='secret', email='test@test.com')

    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == 'test@test.com'))

    assert result.id == 1
