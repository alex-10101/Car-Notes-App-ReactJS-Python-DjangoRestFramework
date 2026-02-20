// import Button from "react-bootstrap/Button";
// import Form from "react-bootstrap/Form";
// import Container from "react-bootstrap/Container";
// import { useEffect, useState } from "react";
// import {
//   useCheckUserIsAuthenticatedMutation,
//   useLogoutUserMutation,
//   useRegisterUserMutation,
// } from "../../redux-toolkit-config/api-services/authApiService";
// import { useNavigate } from "react-router-dom";
// import FetchBaseError from "../../components/FetchBaseError";
// import {
//   removeCredentials,
//   setCredentials,
// } from "../../redux-toolkit-config/slices/authSlice";
// import Loading from "../../components/Loading";
// import { apiSlice } from "../../redux-toolkit-config/apiSlice";
// import ReCaptcha from "../../components/authComponents/reCAPTCHA/ReCaptcha";
// import { useAppDispatch } from "../../redux-toolkit-config/hooks";

// /**
//  *
//  * @returns Page where a user can register.
//  */
// function Register() {
//   const [username, setUsername] = useState("");
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");
//   const [confirmPassword, setConfirmPassword] = useState("");
//   const dispatch = useAppDispatch();
//   const navigate = useNavigate();
//   const [register, { data, error, isLoading }] = useRegisterUserMutation();
//   const [__isLoading, setIsLoading] = useState<boolean>(true);
//   const [checkUserIsAuthenticated] = useCheckUserIsAuthenticatedMutation();
//   const [logout] = useLogoutUserMutation();

//   /**
//    * Make a POST request to create a new account when the user clicks the "Register" button.
//    * @param e
//    */
//   async function handleRegister(
//     e: React.MouseEvent<HTMLButtonElement, MouseEvent>,
//   ) {
//     e.preventDefault();

//     // @ts-ignore
//     const captchaValue = grecaptcha.getResponse();

//     await register({
//       username,
//       email,
//       password,
//       confirmPassword,
//       captchaValue,
//     }).unwrap();
//     // navigate("/login"); // don't navigate to login page,
//     // instead wait for the response that an account activation email has been sent
//   }

//   // check when the component mounts if the user is authenticated. If yes redirect him to the home page.
//   useEffect(() => {
//     async function verifyUserIsAuthenticated() {
//       try {
//         const data = await checkUserIsAuthenticated().unwrap();
//         if (data && data.user && !ignore) {
//           dispatch(setCredentials({ ...data }));
//           navigate("/");
//         }
//       } catch {
//         await logout().unwrap();
//         dispatch(removeCredentials());
//         dispatch(apiSlice.util.resetApiState());
//       } finally {
//         setIsLoading(false);
//       }
//     }

//     let ignore = false;

//     verifyUserIsAuthenticated();

//     return () => {
//       ignore = true;
//     };
//   }, []);

//   if (__isLoading || isLoading) {
//     return <Loading />;
//   }

//   // reset the captcha on wrong from submission
//   if (error) {
//     // @ts-ignore
//     grecaptcha.reset();
//   }

//   return (
//     // Center the container (which contains the Form and the h1 tag) horizontally and vertically,
//     // and align items in a "column" direction (from top to bottom).
//     <Container className="d-flex min-vh-100 justify-content-center align-items-center flex-column">
//       <h1>Register</h1>
//       <Form>
//         <Form.Group className="mb-3 my-3" controlId="formBasicEmail">
//           <Form.Label>Username</Form.Label>
//           <Form.Control
//             type="text"
//             placeholder="Enter username"
//             onChange={(e) => setUsername(e.target.value)}
//           />
//         </Form.Group>

//         <Form.Group className="mb-3" controlId="formBasicEmail">
//           <Form.Label>Email address</Form.Label>
//           <Form.Control
//             type="email"
//             placeholder="Enter email"
//             onChange={(e) => setEmail(e.target.value)}
//           />
//         </Form.Group>

//         <Form.Group className="mb-3" controlId="formBasicPassword">
//           <Form.Label>Password</Form.Label>
//           <Form.Control
//             type="password"
//             placeholder="Password"
//             onChange={(e) => setPassword(e.target.value)}
//           />
//           <Form.Text className="text-muted">
//             Password must contain at least 8 characters and not be common!
//           </Form.Text>
//         </Form.Group>

//         <Form.Group className="mb-3" controlId="formBasicPassword">
//           <Form.Label>Confirm Password</Form.Label>
//           <Form.Control
//             type="password"
//             placeholder="Confirm Password"
//             onChange={(e) => setConfirmPassword(e.target.value)}
//             required
//           />
//           <Form.Text className="text-muted">
//             Password must contain at least 8 characters and not be common!
//           </Form.Text>
//         </Form.Group>

//         <ReCaptcha />

//         {data && <p style={{ color: "green", marginTop: "3px" }}>{data}</p>}

//         {error && <FetchBaseError error={error} />}

//         <Button variant="primary" type="submit" onClick={handleRegister}>
//           Register
//         </Button>
//       </Form>
//     </Container>
//   );
// }

// export default Register;
