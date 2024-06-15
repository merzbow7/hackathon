from functools import lru_cache

from keycloak import KeycloakAdmin

from app.config.settings import get_settings


@lru_cache
def get_keycloak_admin_provider() -> KeycloakAdmin:
    settings = get_settings()
    return KeycloakAdmin(
        server_url=settings.keycloak_server_url,
        client_id=settings.keycloak_client_id,
        client_secret_key=settings.keycloak_client_secret,
        realm_name="Steel",
        verify=True,
    )
