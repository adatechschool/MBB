# services\roles\domain\value_objects.py

from dataclasses import dataclass
from services.roles.domain.models import RoleModel

@dataclass(frozen=True)
class RoleDTO:
    role_name: RoleModel

    def __init__(self):
        self.role_name = RoleModel.USER
