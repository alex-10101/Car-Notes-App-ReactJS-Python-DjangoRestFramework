import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Container from "react-bootstrap/Container";
import { useEffect, useRef, useState } from "react";
import { useCheckUserIsAuthenticatedMutation, useRegisterUserMutation } from "../features/auth/authApiSlice";
import { useNavigate } from "react-router-dom";
import FetchBaseError from "../components/FetchBaseError";
import CSRFToken from "../djangoCSRFToken/CSRFToken";
import { setCredentials } from "../features/auth/authSlice";
import { useAppDispatch } from "../app/hooks";
import Loading from "../components/Loading";

/**
 *
 * @returns Page where a user can register.
 */
function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const [register, { error }] = useRegisterUserMutation();
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [checkUserIsAuthenticated] = useCheckUserIsAuthenticatedMutation();

  // needed with react 18 (useEffect runs twice in dev mode with strict mode)
  const effectRan = useRef(false);

  /**
   * Make a POST request to create a new account when the user clicks the "Register" button.
   * @param e
   */
  async function handleRegister(
    e: React.MouseEvent<HTMLButtonElement, MouseEvent>
  ) {
    e.preventDefault();
    await register({
      username,
      email,
      password,
      confirmPassword,
    }).unwrap();
    navigate("/login");
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
      <h1>Register</h1>
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

        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Email address</Form.Label>
          <Form.Control
            type="email"
            placeholder="Enter email"
            onChange={(e) => setEmail(e.target.value)}
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
            Password must contain at least 8 characters and not be common!
          </Form.Text>
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Confirm Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Confirm Password"
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
          <Form.Text className="text-muted">
            Password must contain at least 8 characters and not be common!
          </Form.Text>
        </Form.Group>

        {error && <FetchBaseError error={error} />}

        <Button variant="primary" type="submit" onClick={handleRegister}>
          Register
        </Button>
      </Form>
    </Container>
  );
}

export default Register;
