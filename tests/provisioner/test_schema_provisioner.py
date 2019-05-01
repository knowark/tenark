from psycopg2 import connect
from pytest import fixture
from tenark.provisioner import SchemaProvisioner


@fixture(scope="session")
def template_setup():
    template_dsn = "dbname=postgres user=postgres"
    database_dsn = "dbname=postgres user=postgres"
    with connect(template_dsn) as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS tenark")
            cursor.execute("CREATE DATABASE tenark")

    return template_dsn, database_dsn


@fixture
def provisioner(template_setup) -> SchemaProvisioner:
    template_dsn, database_dsn = template_setup
    return SchemaProvisioner(template_dsn, database_dsn)


def test_directory_provisioner_setup(provisioner):
    assert isinstance(provisioner.template_dsn, str)
    assert isinstance(provisioner.database_dsn, str)
    assert provisioner.template == '__template__'
