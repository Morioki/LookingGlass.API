from api import db
from api.models import Platforms, PlatformGenerations, PlaythroughStatuses, \
        PlaythroughTypes, Genres, Users, UserRoles, Games, Playthroughs, \
        Sessions
from api.helpers import random_string_generator
import pytest

name = random_string_generator(20)
status_desc = random_string_generator(10)
type_desc = random_string_generator(10)

record_to_acquire = 1

# * Platform
def test_platform_queryable():
    test_record = Platforms.query.get(record_to_acquire)
    assert record_to_acquire == test_record.id

def test_platform_insertable():
    test_record = Platforms(generationid=1, platformcode='Pytest',
            description='Pytest', handheld=True, active=False)
    db.session.add(test_record)
    db.session.commit()
    assert test_record.id is not None

def test_platform_bad_id_failure():
    with pytest.raises(Exception) as e_info:
        test_record = Platforms(generationid=99999999, platformcode='BADRECORD',
                description='BADRECORD', handheld=True, active=False)
        db.session.add(test_record)
        db.session.commit()
    db.session.rollback()

# * Platform Generations
def test_platformgenerations_queryable():
    test_record = PlatformGenerations.query.get(record_to_acquire)
    assert record_to_acquire == test_record.id

def test_platformgenerations_insertable():
    test_record = PlatformGenerations(generationcode='99', description='Test')
    db.session.add(test_record)
    db.session.commit()
    assert test_record.id is not None

# * Playthrough Status 
def test_playthroughstatus_queryable():
    test_record = PlaythroughStatuses.query.get(record_to_acquire)
    assert record_to_acquire == test_record.id

def test_playthroughstatus_insertable():
    test_record = PlaythroughStatuses(description=status_desc, active=False)
    db.session.add(test_record)
    db.session.commit()
    assert test_record.id is not None

# * Playthrough Types 
def test_playthroughtypes_queryable():
    test_record = PlaythroughTypes.query.get(record_to_acquire)
    assert record_to_acquire == test_record.id

def test_playthroughtypes_insertable():
    test_record = PlaythroughTypes(description=type_desc, active=False)
    db.session.add(test_record)
    db.session.commit()
    assert test_record.id is not None

# * Genres
def test_genres_queryable():
    test_record = Genres.query.get(record_to_acquire)
    assert record_to_acquire == test_record.id

def test_genres_insertable():
    test_record = Genres(description='Test', parent=None,active=False)
    db.session.add(test_record)
    db.session.commit()
    assert test_record.id is not None

def test_genres_badid_failure():
    with pytest.raises(Exception) as e_info:
        test_record = Genres(description='Test', parent=9999,active=False)
        db.session.add(test_record)
        db.session.commit()
    db.session.rollback()

# * Users
def test_users_queryable():
    test_record = Users.query.get(record_to_acquire)
    assert record_to_acquire == test_record.id

def test_users_insertable():
    test_record = Users(username='testuser', firstname='t', lastname='u', \
            accesstoken='12345')
    db.session.add(test_record)
    db.session.commit()
    assert test_record.id is not None

# * UserRoles
def test_userroles_queryable():
    test_record = UserRoles.query.get(record_to_acquire)
    assert record_to_acquire == test_record.id

def test_userroles_insertable():
    test_record = UserRoles(rolename='TESTING')
    db.session.add(test_record)
    db.session.commit()
    assert test_record.id is not None

# * Games
def test_games_queryable():
    test_record = Games.query.get(record_to_acquire)
    assert record_to_acquire == test_record.id

def test_games_insertable():
    # remove_rec = Games.query.filter_by(userid=record_to_acquire, gamename='TESTGAME', releaseyear=2021).one()
    # db.session.delete(remove_rec)
    # db.session.commit()

    test_record = Games(userid=record_to_acquire, gamename=name, releaseyear=2021)
    db.session.add(test_record)
    db.session.commit()
    assert test_record.id is not None

def test_games_unique_failure():
    with pytest.raises(Exception) as e_info:
        test_record = Games(userid=record_to_acquire, gamename=name, releaseyear=2021)
        db.session.add(test_record)
        db.session.commit()
    db.session.rollback()

def test_games_baduser_failure():
    with pytest.raises(Exception) as e_info:
        test_record = Games(userid=99999, gamename='None',releaseyear=2021)
        db.session.add(test_record)
        db.session.commit()
    db.session.rollback()

def test_games_badname_failure():
    with pytest.raises(Exception) as e_info:
        test_record = Games(userid=record_to_acquire, gamename=None,releaseyear=2021)
        db.session.add(test_record)
        db.session.commit()
    db.session.rollback()

def test_games_badyear_failure():
    with pytest.raises(Exception) as e_info:
        test_record = Games(userid=record_to_acquire, gamename='None',releaseyear=None)
        db.session.add(test_record)
        db.session.commit()
    db.session.rollback()

# * Playthrough
def test_playthrough_queryable():
    test_record = Playthroughs.query.get(record_to_acquire)
    assert record_to_acquire == test_record.id

def test_playthrough_insertable():
    test_record = Playthroughs(userid=1,gameid=1,typeid=1,statusid=1)
    db.session.add(test_record)
    db.session.commit()
    assert test_record.id is not None

@pytest.mark.parametrize(('user', 'game', 'type', 'status'), (
    (999999,1,1,1),
    (1,999999,1,1),
    (1,1,999999,1),
    (1,1,1,999999)
))
def test_playthrough_fk_failures(user, game, type, status):
    with pytest.raises(Exception) as e_info:
        test_record = Playthroughs(userid=user,gameid=game,typeid=type,statusid=status)
        db.session.add(test_record)
        db.session.commit()
    db.session.rollback()

# * Session
def test_session_queryable():
    test_record = Sessions.query.get(record_to_acquire)
    assert record_to_acquire == test_record.id

def test_session_insertable():
    test_record = Sessions(userid=1,gameid=1,playthroughid=1,startdate='2021-04-10T21:03:10.081979-07:00', \
            stopwatchhours=1, stopwatchminutes=1, stopwatchseconds=1, stopwatchmilliseconds=1)
    db.session.add(test_record)
    db.session.commit()
    assert test_record.id is not None

@pytest.mark.parametrize(('user', 'game', 'playthrough'), (
    (99999,1,1),
    (1,99999,1),
    (1,1,99999)
))
def test_session_fk_failures(user, game, playthrough):
    with pytest.raises(Exception) as e_info:
        test_record = Sessions(userid=user,gameid=game,playthroughid=playthrough,startdate='2021-04-10T21:03:10.081979-07:00', \
            stopwatchhours=1, stopwatchminutes=1, stopwatchseconds=1, stopwatchmilliseconds=1)
        db.session.add(test_record)
        db.session.commit()
    db.session.rollback()
