from dataclasses import dataclass
from typing import Optional

@dataclass
class Company:
    bin: str
    entity_grnz: str

@dataclass
class Participant:
    actor_name: str
    phone_number: str
    password: str
    grnz: str
    type: str
    has_driver: bool
    company: Optional[Company] = None
    role: Optional[str] = None
    iin: Optional[str] = None
    settlement_type: Optional[str] = None
