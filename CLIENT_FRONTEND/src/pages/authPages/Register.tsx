import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Container from "react-bootstrap/Container";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import FetchBaseError from "../../components/FetchBaseError";
import {
  useAppDispatch,
  useAppSelector,
} from "../../redux-toolkit-config/hooks";
import {
  useLogoutUserMutation,
  useRegisterUserMutation,
} from "../../redux-toolkit-config/api-services/authApiService";
import Loading from "../../components/Loading";
import { useCheckUserIsAuthenticatedMutation } from "../../redux-toolkit-config/api-services/authApiServiceOLDWithRecaptcha";
import { apiSlice } from "../../redux-toolkit-config/apiSlice";
import {
  removeCredentials,
  setCredentials,
} from "../../redux-toolkit-config/slices/authSlice";

/**
 *
 * @returns Page where a user can register.
 */
function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const navigate = useNavigate();
  const [register, { data, error, isLoading: loadingRegister }] =
    useRegisterUserMutation();
  const [formIsValidated, setFormIsValidated] = useState(false);
  const [
    checkUserIsAuthenticated,
    {
      isLoading: loadingCheckUserIsAuthenticated,
      error: checkUserIsAuthenticatedError,
    },
  ] = useCheckUserIsAuthenticatedMutation();
  const [logout] = useLogoutUserMutation();
  const dispatch = useAppDispatch();

  /**
   * Make a POST request to create a new account when the user clicks the "Register" button.
   * @param e
   */
  async function handleRegister(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    // validated = false --> client validation messages are NOT shown
    // validated = true --> client validation messages are shown
    setFormIsValidated(true);

    const form = e.currentTarget;

    if (form.checkValidity() === false) {
      e.stopPropagation();
      return;
    }

    await register({
      username,
      email,
      password,
      confirmPassword,
    }).unwrap();
    // navigate("/login"); // don't navigate to login page,
    // instead wait for the response that an account activation email has been sent
  }
  const user = useAppSelector((state) => state.auth.user);

  // check when the component mounts if the user is authenticated. If yes redirect him to the home page.
  // check when the component mounts if the user is authenticated. If yes redirect him to the home page.
  useEffect(() => {
    async function verifyUserIsAuthenticated() {
      if (user) {
        navigate("/");
        return;
      }
      const data = await checkUserIsAuthenticated().unwrap();
      if (checkUserIsAuthenticatedError) {
        await logout().unwrap();
        dispatch(removeCredentials());
        dispatch(apiSlice.util.resetApiState());
        return;
      }
      if (data && data.user && !ignore) {
        dispatch(setCredentials({ ...data }));
        navigate("/");
      }
    }

    let ignore = false;

    verifyUserIsAuthenticated();

    return () => {
      ignore = true;
    };
  }, []);

  if (loadingCheckUserIsAuthenticated || loadingRegister) {
    return <Loading />;
  }

  return (
    // Center the container (which contains the Form and the h1 tag) horizontally and vertically,
    // and align items in a "column" direction (from top to bottom).
    <Container className="d-flex min-vh-100 justify-content-center align-items-center flex-column">
      <h1>Register</h1>
      <Form noValidate validated={formIsValidated} onSubmit={handleRegister}>
        <Form.Group className="mb-3 my-3" controlId="formBasicEmail">
          <Form.Label>Username</Form.Label>
          <Form.Control
            required
            type="text"
            placeholder="Enter username"
            onChange={(e) => setUsername(e.target.value)}
          />
          <Form.Control.Feedback type="invalid">
            Username is required.
          </Form.Control.Feedback>
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Email address</Form.Label>
          <Form.Control
            required
            type="email"
            placeholder="Enter email"
            onChange={(e) => setEmail(e.target.value)}
          />
          <Form.Control.Feedback type="invalid">
            Email is required.
          </Form.Control.Feedback>
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control
            required
            type="password"
            placeholder="Password"
            onChange={(e) => setPassword(e.target.value)}
          />
          <Form.Text className="text-muted">
            Password must contain at least 8 characters and not be common!
          </Form.Text>

          <Form.Control.Feedback type="invalid">
            Password is required.
          </Form.Control.Feedback>
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Confirm Password</Form.Label>
          <Form.Control
            required
            type="password"
            placeholder="Confirm Password"
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          <Form.Text className="text-muted">
            Password must contain at least 8 characters and not be common!
          </Form.Text>

          <Form.Control.Feedback type="invalid">
            Password confirmation is required.
          </Form.Control.Feedback>
        </Form.Group>

        {data && <p style={{ color: "green", marginTop: "3px" }}>{data}</p>}

        {error && <FetchBaseError error={error} />}

        <Button variant="primary" type="submit">
          Register
        </Button>
      </Form>
    </Container>
  );
}

export default Register;
