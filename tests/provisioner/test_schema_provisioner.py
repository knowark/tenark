from pytest import fixture
from subprocess import PIPE
from tenark.models import Tenant
from tenark.provisioner import SchemaProvisioner
from tenark.provisioner import schema_provisioner


@fixture
def provisioner() -> SchemaProvisioner:
    zones = {
        'default': f"postgresql://postgres:postgres@localhost/tenark"
    }
    return SchemaProvisioner(zones=zones)


def test_schema_provisioner_setup(provisioner):
    assert 'tenark' in provisioner.zones['default']
    assert provisioner.template == '__template__'


def test_schema_provisioner_provision_tenant(provisioner, monkeypatch):
    parameters = {}

    def mock_run(command, shell, check, stdout, stderr):
        nonlocal parameters
        parameters['command'] = command
        parameters['shell'] = shell
        parameters['check'] = check
        parameters['stdout'] = stdout
        parameters['stderr'] = stderr

    monkeypatch.setattr(schema_provisioner, 'run', mock_run)

    tenant = Tenant(id='001', name="Knowark")
    provisioner.provision_tenant(tenant)

    assert parameters['shell'] is True
    assert parameters['check'] is True
    assert parameters['stdout'] is PIPE
    assert parameters['stderr'] is PIPE
    assert parameters['command'] == (
        '''/bin/bash -euxo pipefail -c "pg_dump '''
        '''postgresql://postgres:postgres@localhost/tenark '''
        '''--schema=__template__ | sed 's/__template__/knowark/g' | '''
        '''psql postgresql://postgres:postgres@localhost/tenark"'''
    )
