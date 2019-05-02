from pytest import fixture
from psycopg2 import connect
from tenark.models import Tenant
from tenark.provisioner import SchemaProvisioner


@fixture(scope="session")
def template_setup():
    database = "tenark"
    tenark_dsn = f"dbname=postgres user={database}"
    database_dsn = f"dbname={database} user={database}"
    with connect(tenark_dsn) as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS tenark")
            cursor.execute("CREATE DATABASE tenark")
            cursor.execute("GRANT ALL PRIVILEGES ON DATABASE tenark TO tenark")

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
    return SchemaProvisioner(database)


def test_schema_provisioner_setup(provisioner):
    assert provisioner.database == "tenark"
    assert provisioner.template == '__template__'
    assert provisioner.uri == ""


def test_schema_provisioner_provision_tenant(provisioner):
    tenant = Tenant(name="Knowark")
    provisioner.provision_tenant(tenant)

    database_dsn = f"dbname={provisioner.database}"
    with connect(database_dsn) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT EXISTS("
                "SELECT 1 "
                "FROM pg_tables "
                "WHERE schemaname = 'knowark' "
                "AND tablename = 'users');")
            result = cursor.fetchone()
            assert result[0] is True
