import sys

sys.path.insert(0, "/Users/louisrae/Documents/dev/dfy_setters")

from src.roles import *
import pytest
import pandas as pd
from src.constants import *
from sqlalchemy import create_engine


@pytest.fixture
def register():
    register = Roles.register_all_members()
    return register


def test_canCreatePerson():
    jack = Person("Jack", "Snr Specialist")
    assert jack.name == "Jack" and jack.role == "Snr Specialist"


def test_canRegisterAllMembers(register):
    engine = create_engine(DATABASE_URI)

    myQuery = "SELECT full_name,role FROM team"
    df = pd.read_sql_query(myQuery, engine)
    assert len(df.index) == len(Roles.all_team_members_in_company)


def test_canGetAllSnrSpecialists(register):
    ls = SnrSpecialist().all_members
    for ss in ls:
        print(ss)
    assert len(ls) == 5


def test_canGetAllJnrSpecialists(register):
    ls = JnrSpecialist().all_members
    assert len(ls) == 5


def test_canGetAllPodLeads(register):
    ls = PodLead().all_members
    assert len(ls) == 3


def test_canGetAllSetters(register):
    ls = Setter().all_members
    assert len(ls) == 6
