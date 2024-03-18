from dependency_injector import containers, providers

from gns_api_gateway.api import GNS3Router
from gns_api_gateway.application import GNS3Service
from gns_api_gateway.infrastructure import GNS3Proxy


class ExternalServices(containers.DeclarativeContainer):
    config = providers.Configuration()

    gns3_proxy: providers.Singleton[GNS3Proxy] = providers.Singleton(
        GNS3Proxy,
        base_url=config.gns3_url,
    )


class Routers(containers.DeclarativeContainer):
    external_services = providers.DependenciesContainer()
    application = providers.DependenciesContainer()

    gns3_router: providers.Singleton[GNS3Router] = providers.Singleton(
        GNS3Router,
        client=external_services.gns3_proxy,
    )


class Application(containers.DeclarativeContainer):
    external_services = providers.DependenciesContainer()

    gns3: providers.Singleton[GNS3Service] = providers.Singleton(
        GNS3Service,
        gns3_proxy=external_services.gns3_proxy,
    )


class Containers(containers.DeclarativeContainer):
    config = providers.Configuration()

    external_services: providers.Container[ExternalServices] = providers.Container(
        ExternalServices,
        config=config,
    )
    application: providers.Container[Application] = providers.Container(
        Application,
        external_services=external_services,
    )
    routers: providers.Container[Routers] = providers.Container(
        Routers,
        external_services=external_services,
        application=application,
    )
