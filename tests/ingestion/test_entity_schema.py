from services.ingestion.entity_schema import Entity
import pytest

def test_valid_cpf():
    e = Entity(type='CPF', text='123.456.789-09', confidence=0.99, cpf='123.456.789-09')
    assert e.cpf == '12345678909'

def test_invalid_cpf():
    with pytest.raises(ValueError):
        Entity(type='CPF', text='111.111.111-11', confidence=0.99, cpf='111.111.111-11')

def test_valid_date():
    e = Entity(type='DATA', text='2025-07-22', confidence=0.99, data='2025-07-22')
    assert e.data == '2025-07-22'

def test_invalid_date():
    with pytest.raises(ValueError):
        Entity(type='DATA', text='22/07/2025', confidence=0.99, data='22/07/2025')
