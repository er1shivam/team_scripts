import sys

sys.path.insert(0, "/Users/louisrae/Documents/dev/dfy_setters")

from src.roles import *
import pytest
import pandas as pd
from src.constants import *


@pytest.fixture
def register():
    register = Roles.register_all_members()
    return register


def test_canCreatePerson():
    jack = Person("Jack", "Snr Specialist")
    assert jack.name == "Jack" and jack.role == "Snr Specialist"


def test_canRegisterAllMembers(register):
    df = pd.read_csv(PATH_TO_CSV)
    assert len(df.index) == len(Roles.all_team_members_in_company)


def test_canGetAllSnrSpecialists(register):
    ls = SnrSpecialist().all_members
    for ss in ls:
        print(ss)
    assert len(ls) == 6


def test_canGetAllJnrSpecialists(register):
    ls = JnrSpecialist().all_members
    assert len(ls) == 8


def test_canGetAllPodLeads(register):
    ls = PodLead().all_members
    assert len(ls) == 2


def test_canGetAllSetters(register):
    ls = Setter().all_members
    assert len(ls) == 7
