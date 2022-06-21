import pytest
from module.auth.commands import AuthCommand
from db.connection import ENGINE
from sqlalchemy.orm import Session
from models import User
import json


def test_registration_with_full_data():
    authCommand = AuthCommand()
    with open('tests/mock_data/registration_full_data.json') as f:
        data = json.load(f)
    
    for req in data:
        user, token = authCommand.registration(req['email'], req['login'],req['password'],req['password'],req['name'])
        session = Session(bind=ENGINE)
        user = session.query(User).get(user.id)
        session.delete(user)
        session.commit()
        session.close()


def test_registration_without_full_data():
    authCommand = AuthCommand()
    with open('tests/mock_data/registration_data.json') as f:
        data = json.load(f)
    
    for req in data:
        user, token = authCommand.registration(req['email'], req['login'],req['password'],req['password'],req['name'])
        session = Session(bind=ENGINE)
        user = session.query(User).get(user.id)
        session.delete(user)
        session.commit()
        session.close()