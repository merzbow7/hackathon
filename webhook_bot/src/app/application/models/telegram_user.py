import uuid
from dataclasses import dataclass, field


@dataclass
class User:
    id: int = field(init=False)
    telegram_id: int
    keycloak_id: uuid.UUID = field(init=False)
    verification_code: uuid.UUID = field(default_factory=uuid.uuid4)
