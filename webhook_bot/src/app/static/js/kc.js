const keycloak = new Keycloak({
  url: "http://127.0.0.1:8080/auth",
  realm: "Steel",
  clientId: "steel_front",
  "public-client": true,
});

keycloak
  .init()
  .then(function (authenticated) {
    console.log(authenticated ? "authenticated" : "not authenticated");
  })
  .catch(function () {
    console.log("failed to initialize");
  });
