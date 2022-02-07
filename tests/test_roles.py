from src.roles import *


def test_canCreatePersonwithNameandRole():
    jack = Person("No_name", "Pod Lead")
    assert "No_name" in str(jack) and ("Pod" in str(jack))


def test_canParseCSVwithRolesandPersonName():
    df = Roles().parse_csv_of_roles()
    assert all(elem in ["Person", "Role"] for elem in df.columns)


def test_singleMemberCanBeRegisteredToRoleDictionary():
    jack = Person("No_name", "Pod Leads")
    Roles().registerMember(jack)
    assert "No_name" in str(Roles().all_team_members_in_company)


def test_singleMemberCanBeRegisteredToTeamList():
    jack = Person("No_name", "Pod Leads")
    registered = Roles().registerMember(jack)
    item_in_team_register = list(Roles().all_team_members_in_company)[0]
    assert isinstance(item_in_team_register, type(jack))


def test_canRegisterAllMembers():
    new_roles = Roles()
    new_roles.register_all_members()
    df = Roles().parse_csv_of_roles()
    assert len(new_roles.all_team_members_in_company) == (
        df["Role"].count() + 1
    )
