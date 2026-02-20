// import { useEffect, useState } from "react";
// import {
//   useCheckUserIsAuthenticatedMutation,
//   useLoginUserMutation,
//   useLogoutUserMutation,
// } from "../../redux-toolkit-config/api-services/authApiService";
// import {
//   removeCredentials,
//   setCredentials,
// } from "../../redux-toolkit-config/slices/authSlice";
// import Button from "react-bootstrap/Button";
// import Form from "react-bootstrap/Form";
// import Container from "react-bootstrap/Container";
// import { Link, useNavigate } from "react-router-dom";
// import Loading from "../../components/Loading";
// import FetchBaseError from "../../components/FetchBaseError";
// import { apiSlice } from "../../redux-toolkit-config/apiSlice";
// import ReCaptcha from "../../components/authComponents/reCAPTCHA/ReCaptcha";
// import { useAppDispatch } from "../../redux-toolkit-config/hooks";

// /**
//  *
//  * @returns a page where a user can login with email and password
//  */
// function Login() {
//   const [email, setEmail] = useState<string>("");
//   const [password, setPassword] = useState<string>("");
//   const dispatch = useAppDispatch();
//   const navigate = useNavigate();
//   const [login, { error }] = useLoginUserMutation();
//   const [isLoading, setIsLoading] = useState<boolean>(true);
//   const [checkUserIsAuthenticated] = useCheckUserIsAuthenticatedMutation();
//   const [logout] = useLogoutUserMutation();

//   /**
//    * Make a POST request to log in when the user clicks the "Login" button.
//    * @param e
//    */
//   async function handleLogin(
//     e: React.MouseEvent<HTMLButtonElement, MouseEvent>,
//   ) {
//     e.preventDefault();

//     // @ts-ignore
//     const captchaValue = grecaptcha.getResponse();

//     const loginData = await login({ email, password, captchaValue }).unwrap();
//     dispatch(setCredentials({ ...loginData }));
//     navigate("/");
//   }

//   // check when the component mounts if the user is authenticated. If yes redirect him to the home page.
//   useEffect(() => {
//     async function verifyUserIsAuthenticated() {
//       try {
//         const data = await checkUserIsAuthenticated().unwrap();
//         if (data && data.user && !ignore) {
//           // console.log("user");
//           // console.log(data);
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

//   if (isLoading) {
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
//       <h1>Login</h1>
//       <Form>
//         <Form.Group className="mb-3 my-3" controlId="formBasicEmail">
//           <Form.Label>Email</Form.Label>
//           <Form.Control
//             type="text"
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
//             Did not register yet? Navigate to{" "}
//             <Link
//               to="/register"
//               style={{
//                 textDecoration: "none",
//                 cursor: "pointer",
//               }}
//             >
//               Register Page
//             </Link>
//             . Forgot password? Click{" "}
//             <Link
//               to="/requestChangeForgottenPassword"
//               style={{
//                 textDecoration: "none",
//                 cursor: "pointer",
//               }}
//             >
//               here.
//             </Link>
//           </Form.Text>
//         </Form.Group>

//         <ReCaptcha />

//         {error && <FetchBaseError error={error} />}

//         <Button variant="primary" type="submit" onClick={handleLogin}>
//           Login
//         </Button>
//       </Form>
//     </Container>
//   );
// }

// export default Login;
