import { Container, Spinner } from "react-bootstrap";

/**
 * Displays a loading Spinner while a request made to the server is not completed.
 * @returns
 */
function Loading() {
  return (
    <Container className="d-flex min-vh-100 justify-content-center align-items-center">
      <Spinner animation="border" />
    </Container>
  );
}

export default Loading;
