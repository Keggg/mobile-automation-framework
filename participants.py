from models import Company, Participant
from test_profiles import test_profiles
from scenarios import scenarios

def create_participants(scenario_name: str):
    scenario = scenarios[scenario_name]

    applicant_profile = test_profiles[scenario["applicant_phone"]]
    contender_profile = test_profiles[scenario["contender_phone"]]

    company = Company(
        bin="123456789123",
        entity_grnz="A123BC"
    )

    applicant = Participant(
        actor_name = "applicant",
        phone_number = applicant_profile["phone_number"],
        password = applicant_profile["password"],
        grnz = applicant_profile["grnz"],
        type = scenario["applicant_type"],
        has_driver = scenario["applicant_has_driver"],
        company = company,
        role = scenario["applicant_role"],
        #iin = applicant_profile["iin"]
    )

    contender = Participant(
        actor_name = "contender",
        phone_number = contender_profile["phone_number"],
        password = contender_profile["password"],
        grnz = contender_profile["grnz"],
        type = scenario["contender_type"],
        has_driver = scenario["contender_has_driver"],
        company = company,
        iin = contender_profile["iin"],
        #role = scenario["contender_role"]
    )

    settlement_type = scenario.get("settlement_type")

    return applicant, contender, settlement_type

drivers_data = {
    "applicant_driver": {"iin": "000111000111", "phone_number": "70711111111", "first_name": "Иван", "last_name": "Иванов", "middle_name": "Иванович"},
    "contender_driver": {"iin": "000222000222", "phone_number": "70722222222", "first_name": "Ахмет", "last_name": "Ахметов", "middle_name": "Ахметович"}
}
