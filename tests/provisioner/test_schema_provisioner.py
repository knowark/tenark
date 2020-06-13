# from pytest import fixture, mark
# # from psycopg2 import connect
# from tenark.models import Tenant
# from tenark.provisioner import SchemaProvisioner


# pytestmark = mark.sql


# @fixture(scope="session")
# def template_setup():
#     database = "tenark"
#     postgres_dsn = f"dbname=postgres user=postgres"
#     database_dsn = f"dbname={database} user=postgres"
#     with connect(postgres_dsn) as connection:
#         connection.autocommit = True
#         with connection.cursor() as cursor:
#             cursor.execute("DROP DATABASE IF EXISTS tenark")
#             cursor.execute("CREATE DATABASE tenark")

#     with connect(database_dsn) as connection:
#         with connection.cursor() as cursor:
#             cursor.execute("CREATE SCHEMA IF NOT EXISTS __template__")
#             cursor.execute(
#                 "CREATE TABLE __template__.users("
#                 "id serial PRIMARY KEY, "
#                 "created_at TIMESTAMP NOT NULL, "
#                 "username VARCHAR(50) UNIQUE NOT NULL, "
#                 "email VARCHAR(50) UNIQUE NOT NULL);")

#     return database


# @fixture
# def provisioner(template_setup) -> SchemaProvisioner:
#     database = template_setup
#     zones = {
#         'default': f"postgresql://postgres:postgres@localhost/{database}"
#     }
#     return SchemaProvisioner(zones=zones)


# def test_schema_provisioner_setup(provisioner):
#     assert 'tenark' in provisioner.zones['default']
#     assert provisioner.template == '__template__'


# def test_schema_provisioner_provision_tenant(provisioner):
#     tenant = Tenant(id='001', name="Knowark")
#     provisioner.provision_tenant(tenant)

#     with connect(provisioner.zones['default']) as connection:
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "SELECT EXISTS("
#                 "SELECT 1 "
#                 "FROM pg_tables "
#                 "WHERE schemaname = 'knowark' "
#                 "AND tablename = 'users');")
#             result = cursor.fetchone()
#             assert result[0] is True
