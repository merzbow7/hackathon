import { useRouteError } from "react-router-dom";
import { Center, Flex } from '@mantine/core';

export default function ErrorPage() {
  const error = useRouteError() as { statusText: string, message: string };

  return (
    <div id="error-page">
      <Center h={300}>
        <Flex
          gap="sm"
          justify="center"
          align="center"
          direction="column"
          wrap="wrap"
        >
          <h1>Oops!</h1>
          <p>Sorry, an unexpected error has occurred.</p>
          <p>
            <i>{error.statusText || error.message}</i>
          </p>
        </Flex>
      </Center>
    </div>
  );
}