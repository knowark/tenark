import json
from pathlib import Path
from pytest import fixture
from tenark.models import Tenant
from tenark.provisioner import DirectoryProvisioner


@fixture
def template_setup(tmp_path):
    templates = tmp_path / "templates"
    templates.mkdir()
    data = tmp_path / "data"
    data.mkdir()
    tenant_template = templates / "__template__"
    tenant_template.mkdir()

    collection_1 = tenant_template / "collection_1.json"
    collection_1.write_text(json.dumps({
        "collection_1": {
            "item_1": "value_1",
            "item_2": "value_2",
            "item_3": "value_3",
        }
    }))
    collection_2 = tenant_template / "collection_2.json"
    collection_2.write_text(json.dumps({
        "collection_2": {
            "item_1": "value_1",
            "item_2": "value_2",
            "item_3": "value_3",
        }
    }))
    return tenant_template, data


@fixture
def provisioner(template_setup) -> DirectoryProvisioner:
    tenant_template, data = template_setup
    zones = {
        'default': str(data)
    }
    return DirectoryProvisioner(zones, str(tenant_template))


def test_directory_provisioner_setup(provisioner):
    assert isinstance(provisioner.template, str)
    assert isinstance(provisioner.zones['default'], str)


def test_directory_provisioner_provision_tenant(provisioner):
    tenant = Tenant(id='001', name="Servagro")
    provisioner.provision_tenant(tenant)

    data = Path(provisioner.zones['default'])
    subdirectories = [
        directory for directory in data.iterdir()
        if directory.is_dir()]

    assert len(subdirectories) == 1
    assert 'servagro' == subdirectories[0].name
