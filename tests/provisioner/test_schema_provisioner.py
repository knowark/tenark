from pytest import fixture, mark
from psycopg2 import connect
from tenark.models import Tenant
from tenark.provisioner import SchemaProvisioner


pytestmark = mark.sql


@fixture(scope="session")
def template_setup():
    database = "tenark"
    postgres_dsn = f"dbname=postgres user=postgres"
    database_dsn = f"dbname={database} user=postgres"
    with connect(postgres_dsn) as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS tenark")
            cursor.execute("CREATE DATABASE tenark")

    with connect(database_dsn) as connection:
        with connection.cursor() as cursor:
            cursor.execute("CREATE SCHEMA IF NOT EXISTS __template__")
            cursor.execute(
                "CREATE TABLE __template__.users("
                "id serial PRIMARY KEY, "
                "created_at TIMESTAMP NOT NULL, "
                "username VARCHAR(50) UNIQUE NOT NULL, "
                "email VARCHAR(50) UNIQUE NOT NULL);")

    return database


@fixture
def provisioner(template_setup) -> SchemaProvisioner:
    database = template_setup
    uri = f"postgresql://postgres:postgres@localhost/{database}"
    return SchemaProvisioner(uri=uri)


def test_schema_provisioner_setup(provisioner):
    assert 'tenark' in provisioner.uri
    assert provisioner.template == '__template__'


def test_schema_provisioner_properties(provisioner):
    assert provisioner.location == {
        'schema': provisioner.uri
    }


def test_schema_provisioner_provision_tenant(provisioner):
    tenant = Tenant(name="Knowark")
    provisioner.provision_tenant(tenant)

    with connect(provisioner.uri) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT EXISTS("
                "SELECT 1 "
                "FROM pg_tables "
                "WHERE schemaname = 'knowark' "
                "AND tablename = 'users');")
            result = cursor.fetchone()
            assert result[0] is True
