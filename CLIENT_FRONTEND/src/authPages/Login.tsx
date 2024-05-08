import { useEffect, useRef, useState } from "react";
import { useAppDispatch } from "../app/hooks";
import { useCheckUserIsAuthenticatedMutation, useLoginUserMutation } from "../features/auth/authApiSlice";
import { setCredentials } from "../features/auth/authSlice";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Container from "react-bootstrap/Container";
import { Link, useNavigate } from "react-router-dom";
import Loading from "../components/Loading";
import FetchBaseError from "../components/FetchBaseError";
import CSRFToken from "../djangoCSRFToken/CSRFToken";

/**
 *
 * @returns a page where a user can login with email and password
 */
function Login() {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const [login, { error }] = useLoginUserMutation();
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [checkUserIsAuthenticated] = useCheckUserIsAuthenticatedMutation();

  // needed with react 18 (useEffect runs twice in dev mode with strict mode)
  const effectRan = useRef(false);

  /**
   * Make a POST request to log in when the user clicks the "Login" button.
   * @param e
   */
  async function handleLogin(
    e: React.MouseEvent<HTMLButtonElement, MouseEvent>
  ) {
    e.preventDefault();
    const loginData = await login({ username, password }).unwrap();
    dispatch(setCredentials({ ...loginData }));
    navigate("/");
  }

  // check when the component mounts if the user is authenticated. If yes redirect him to the home page.
  useEffect(() => {
    async function verifyUserIsAuthenticated() {
      try {
        const data = await checkUserIsAuthenticated().unwrap();
        if (data && data.user) {
          dispatch(setCredentials({ ...data }));
          navigate("/");
        }
      } finally {
        setIsLoading(false);
      }
    }
    if (effectRan.current === false) {
      verifyUserIsAuthenticated();
      return () => {
        effectRan.current = true;
      };
    }
  }, []);

  if (isLoading) {
    return <Loading />;
  }

  return (
    // Center the container (which contains the Form and the h1 tag) horizontally and vertically,
    // and align items in a "column" direction (from top to bottom).
    <Container className="d-flex min-vh-100 justify-content-center align-items-center flex-column">
      <h1>Login</h1>
      <Form>
        <CSRFToken />
        <Form.Group className="mb-3 my-3" controlId="formBasicEmail">
          <Form.Label>Username</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter username"
            onChange={(e) => setUsername(e.target.value)}
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Password"
            onChange={(e) => setPassword(e.target.value)}
          />
          <Form.Text className="text-muted">
            Did not register yet? Navigate to{" "}
            <Link
              to="/register"
              style={{
                textDecoration: "none",
                cursor: "pointer",
              }}
            >
              Register Page
            </Link>
          </Form.Text>
        </Form.Group>

        {error && <FetchBaseError error={error} />}

        <Button variant="primary" type="submit" onClick={handleLogin}>
          Login
        </Button>
      </Form>
    </Container>
  );
}

export default Login;
