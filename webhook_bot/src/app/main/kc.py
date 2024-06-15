from pprint import pprint


def get_kc():
    from keycloak import KeycloakOpenID

    from app.config.settings import get_settings
    settings = get_settings()
    keycloak_server_url = "http://127.0.0.1:8080"

    return KeycloakOpenID(
        server_url=keycloak_server_url,  # https://sso.example.com/auth/
        client_id=settings.keycloak_client_id,  # backend-client-id
        realm_name=settings.keycloak_realm,  # example-realm
        client_secret_key=settings.keycloak_client_secret,  # your backend client secret
        verify=True
    )


if __name__ == '__main__':
    provider = get_kc()
    token = provider.token("moskvitin_vi", "4hakat0n")
    pprint(token)
