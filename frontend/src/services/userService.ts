import Keycloak from "keycloak-js";

const initOptions = {
  realm: import.meta.env.VITE_KK_REALM,
  url: import.meta.env.VITE_KK_HOST,
  clientId: import.meta.env.VITE_CLIENT_ID,
}

const _kc = new Keycloak(initOptions);

const initKeycloak = (onAuthenticatedCallback: () => unknown) => {
  _kc.init({
    onLoad: 'login-required',
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-expect-error
    checkLoginInIframe: true,
    pkceMethod: 'S256',
  })
    .then((authenticated) => {
      if (!authenticated) {
        console.log("user is not authenticated..!");
      }
      onAuthenticatedCallback();
    })
    .catch(console.error);
};

const doLogin = _kc.login;

const doLogout = _kc.logout;

const getToken = () => _kc.token;

const getTokenParsed = () => _kc.tokenParsed;

const isLoggedIn = () => !!_kc.token;

const isAdmin = () => _kc.hasRealmRole(import.meta.env.VITE_KK_ADMIN_ROLE);

const updateToken = (successCallback: () => unknown) =>
  _kc.updateToken(5)
    .then(successCallback)
    .catch(doLogin);

const getUsername = () => _kc.tokenParsed?.preferred_username;

const hasRole = (roles: string[]) => roles.some((role) => _kc.hasRealmRole(role));

const UserService = {
  initKeycloak,
  doLogin,
  doLogout,
  isLoggedIn,
  getToken,
  getTokenParsed,
  updateToken,
  getUsername,
  hasRole,
  isAdmin,
};

export default UserService;