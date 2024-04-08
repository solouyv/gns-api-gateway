from dependency_injector import containers, providers, resources

from gns_api_gateway.api import GNS3Router
from gns_api_gateway.application import GNS3Service
from gns_api_gateway.datasource import Database
from gns_api_gateway.infrastructure import GNS3Proxy
from gns_api_gateway.infrastructure.repositories import UserRepository, TokenRepository


class DatabaseResource(resources.Resource):
    def init(self, username: str, password: str, host: str, port: int, database: str) -> Database:
        db = Database(username=username, password=password, host=host, port=port, database=database)
        db.connect()
        return db

    def shutdown(self, resource: Database) -> None:
        resource.close()


class Datasources(containers.DeclarativeContainer):
    config = providers.Configuration()

    postgres_datasource: providers.Provider[Database] = providers.Resource(
        DatabaseResource,
        config.user,
        config.password,
        config.host,
        config.port,
        config.db,
    )


class Repositories(containers.DeclarativeContainer):
    datasources = providers.DependenciesContainer()

    user: providers.Singleton[UserRepository] = providers.Singleton(
        UserRepository,
        datasources.postgres_datasource,
    )
    token: providers.Singleton[TokenRepository] = providers.Singleton(
        TokenRepository,
        datasources.postgres_datasource,
    )


class ExternalServices(containers.DeclarativeContainer):
    config = providers.Configuration()

    gns3_proxy: providers.Singleton[GNS3Proxy] = providers.Singleton(
        GNS3Proxy,
        base_url=config.gns3_url,
    )


class Routers(containers.DeclarativeContainer):
    application = providers.DependenciesContainer()
    external_services = providers.DependenciesContainer()

    gns3_router: providers.Singleton[GNS3Router] = providers.Singleton(
        GNS3Router,
        client=external_services.gns3_proxy,
        service=application.gns3,
    )


class Application(containers.DeclarativeContainer):
    external_services = providers.DependenciesContainer()
    repositories = providers.DependenciesContainer()

    gns3: providers.Singleton[GNS3Service] = providers.Singleton(
        GNS3Service,
        gns3_proxy=external_services.gns3_proxy,
        user_repository=repositories.user,
    )


class Containers(containers.DeclarativeContainer):
    config = providers.Configuration()

    datasources: providers.Container[Datasources] = providers.Container(
        Datasources,
        config=config.database,
    )
    repositories: providers.Container[Repositories] = providers.Container(
        Repositories,
        datasources=datasources,
    )
    external_services: providers.Container[ExternalServices] = providers.Container(
        ExternalServices,
        config=config,
    )
    application: providers.Container[Application] = providers.Container(
        Application,
        external_services=external_services,
        repositories=repositories,
    )
    routers: providers.Container[Routers] = providers.Container(
        Routers,
        application=application,
        external_services=external_services,
    )
