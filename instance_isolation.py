from dataclasses import dataclass
from typing import Dict, FrozenSet, Optional, Set
from uuid import uuid4


@dataclass(frozen=True)
class MilaInstance:
    instance_id: str
    owner_id: str
    role: str  # master or shared


@dataclass(frozen=True)
class DirectedLink:
    link_id: str
    master_id: str
    shared_id: str
    scopes: FrozenSet[str]
    active: bool = True


class InstanceIsolation:
    """Enforces one-way, explicit Master -> shared-instance access.

    This layer is intentionally independent from model prompts. It never copies
    memory, credentials, sessions, approvals, or private data between instances.
    """

    MASTER = "master"
    SHARED = "shared"

    def __init__(self):
        self._instances: Dict[str, MilaInstance] = {}
        self._links: Dict[str, DirectedLink] = {}

    def create_master(self, owner_id: str) -> MilaInstance:
        if not owner_id:
            raise ValueError("owner_id required")
        if any(i.role == self.MASTER and i.owner_id == owner_id for i in self._instances.values()):
            raise ValueError("master already exists")
        instance = MilaInstance(str(uuid4()), owner_id, self.MASTER)
        self._instances[instance.instance_id] = instance
        return instance

    def create_shared(self, master_id: str, owner_id: str) -> MilaInstance:
        master = self._require(master_id)
        if master.role != self.MASTER:
            raise PermissionError("only master may create shared instances")
        if not owner_id:
            raise ValueError("owner_id required")
        instance = MilaInstance(str(uuid4()), owner_id, self.SHARED)
        self._instances[instance.instance_id] = instance
        return instance

    def can_access(self, source_id: str, target_id: str, scope: str) -> bool:
        if source_id == target_id:
            return True
        source = self._require(source_id)
        target = self._require(target_id)
        if source.role != self.MASTER or target.role != self.SHARED:
            return False
        return any(link.active and link.master_id == source_id and link.shared_id == target_id and scope in link.scopes
                   for link in self._links.values())

    def authorize_master_to_shared(self, master_id: str, shared_id: str, scopes: Set[str]) -> DirectedLink:
        master = self._require(master_id)
        shared = self._require(shared_id)
        if master.role != self.MASTER or shared.role != self.SHARED:
            raise PermissionError("only Master -> shared links are allowed")
        if not scopes:
            raise ValueError("at least one scope required")
        link = DirectedLink(str(uuid4()), master_id, shared_id, frozenset(scopes), True)
        self._links[link.link_id] = link
        return link

    def revoke(self, link_id: str) -> None:
        link = self._links.get(link_id)
        if not link:
            raise KeyError("unknown link")
        self._links[link_id] = DirectedLink(link.link_id, link.master_id, link.shared_id, link.scopes, False)

    def transfer_payload(self, master_id: str, shared_id: str, payload: dict) -> dict:
        """Return only explicitly safe bootstrap data; never copy private state."""
        if not self.can_access(master_id, shared_id, "transfer"):
            raise PermissionError("transfer not authorized")
        return {"instance_id": shared_id, "bootstrap": dict(payload)}

    def _require(self, instance_id: str) -> MilaInstance:
        if instance_id not in self._instances:
            raise KeyError("unknown instance")
        return self._instances[instance_id]
