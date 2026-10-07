import pytest
from instance_isolation import InstanceIsolation


def test_master_and_shared_are_distinct():
    iso = InstanceIsolation(); master = iso.create_master("klaus"); shared = iso.create_shared(master.instance_id, "son")
    assert master.role == "master" and shared.role == "shared" and master.instance_id != shared.instance_id


def test_shared_cannot_access_master():
    iso = InstanceIsolation(); master = iso.create_master("klaus"); shared = iso.create_shared(master.instance_id, "son")
    assert not iso.can_access(shared.instance_id, master.instance_id, "memory")
    assert not iso.can_access(shared.instance_id, master.instance_id, "transfer")


def test_master_has_no_access_until_explicit_link():
    iso = InstanceIsolation(); master = iso.create_master("klaus"); shared = iso.create_shared(master.instance_id, "son")
    assert not iso.can_access(master.instance_id, shared.instance_id, "status")


def test_explicit_master_to_shared_link_is_one_way():
    iso = InstanceIsolation(); master = iso.create_master("klaus"); shared = iso.create_shared(master.instance_id, "son")
    iso.authorize_master_to_shared(master.instance_id, shared.instance_id, {"status"})
    assert iso.can_access(master.instance_id, shared.instance_id, "status")
    assert not iso.can_access(shared.instance_id, master.instance_id, "status")


def test_link_scope_is_limited():
    iso = InstanceIsolation(); master = iso.create_master("klaus"); shared = iso.create_shared(master.instance_id, "son")
    iso.authorize_master_to_shared(master.instance_id, shared.instance_id, {"status"})
    assert not iso.can_access(master.instance_id, shared.instance_id, "memory")


def test_revocation_blocks_link():
    iso = InstanceIsolation(); master = iso.create_master("klaus"); shared = iso.create_shared(master.instance_id, "son")
    link = iso.authorize_master_to_shared(master.instance_id, shared.instance_id, {"status"})
    iso.revoke(link.link_id)
    assert not iso.can_access(master.instance_id, shared.instance_id, "status")


def test_transfer_requires_explicit_transfer_scope():
    iso = InstanceIsolation(); master = iso.create_master("klaus"); shared = iso.create_shared(master.instance_id, "son")
    with pytest.raises(PermissionError):
        iso.transfer_payload(master.instance_id, shared.instance_id, {"version": "v33"})


def test_transfer_does_not_copy_private_state():
    iso = InstanceIsolation(); master = iso.create_master("klaus"); shared = iso.create_shared(master.instance_id, "son")
    iso.authorize_master_to_shared(master.instance_id, shared.instance_id, {"transfer"})
    result = iso.transfer_payload(master.instance_id, shared.instance_id, {"version": "v33", "features": ["speech"]})
    assert result["bootstrap"]["version"] == "v33"
    assert "memory" not in result and "credentials" not in result and "approvals" not in result


def test_only_master_can_create_shared_instance():
    iso = InstanceIsolation(); master = iso.create_master("klaus"); shared = iso.create_shared(master.instance_id, "son")
    with pytest.raises(PermissionError):
        iso.create_shared(shared.instance_id, "third")


def test_duplicate_master_is_rejected():
    iso = InstanceIsolation(); iso.create_master("klaus")
    with pytest.raises(ValueError):
        iso.create_master("klaus")


def test_model_cannot_override_isolation_without_link():
    iso = InstanceIsolation(); master = iso.create_master("klaus"); shared = iso.create_shared(master.instance_id, "son")
    assert not iso.can_access(shared.instance_id, master.instance_id, "anything")
