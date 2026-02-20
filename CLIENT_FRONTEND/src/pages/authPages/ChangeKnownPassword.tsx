// import Button from "react-bootstrap/Button";
// import Form from "react-bootstrap/Form";
// import Container from "react-bootstrap/Container";
// import { useState } from "react";
// import { useAppDispatch } from "../../app/hooks";
// import { removeCredentials } from "../../features/auth/authSlice";
// import { apiSlice } from "../../app/api/apiSlice";
// import FetchBaseError from "../../components/FetchBaseError";
// import { useChangeKnownPasswordMutation } from "../../features/auth/authApiSlice";

// /**
//  *
//  * @returns A page where a user can change its password if the user knows its password.
//  *
//  * NOT USED ANYMORE.
//  */
// function ChangeKnownPassword() {
//   const [changePassword, { error }] = useChangeKnownPasswordMutation();

//   const dispatch = useAppDispatch();

//   const [userInput, setUserInput] = useState({
//     oldPassword: "",
//     newPassword: "",
//     newPasswordConfirm: "",
//   });

//   function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
//     e.preventDefault();
//     setUserInput({
//       ...userInput,
//       [e.target.name]: e.target.value,
//     });
//   }

//   /**
//    * Make a PUT request to change the password when the user clicks the "Change Password" button.
//    * @param e
//    */
//   async function handleChangePassword(
//     e: React.MouseEvent<HTMLButtonElement, MouseEvent>
//   ) {
//     e.preventDefault();
//     await changePassword({
//       oldPassword: userInput.oldPassword,
//       newPassword: userInput.newPassword,
//       newPasswordConfirm: userInput.newPasswordConfirm,
//     }).unwrap();
//     dispatch(removeCredentials());
//     dispatch(apiSlice.util.resetApiState());
//   }

//   return (
//     <Container className="d-flex align-items-center flex-column my-4">
//       <h1>Change Password</h1>
//       <Form>
//         <Form.Group className="mb-3" controlId="formBasicEmail">
//           <Form.Label>Old Password</Form.Label>
//           <Form.Control
//             name="oldPassword"
//             type="password"
//             placeholder="Enter old password"
//             onChange={handleChange}
//           />
//         </Form.Group>

//         <Form.Group className="mb-3" controlId="formBasicPassword">
//           <Form.Label>New Password</Form.Label>
//           <Form.Control
//             name="newPassword"
//             type="password"
//             placeholder="Enter  new  password"
//             onChange={handleChange}
//           />
//           <Form.Text className="text-muted">
//             Password must contain at least 8 characters and not be common!
//           </Form.Text>
//         </Form.Group>

//         <Form.Group className="mb-3" controlId="formBasicPassword">
//           <Form.Label>Confirm Password</Form.Label>
//           <Form.Control
//             name="newPasswordConfirm"
//             type="password"
//             placeholder="Confirm new password"
//             onChange={handleChange}
//           />
//           <Form.Text className="text-muted">
//             Password must contain at least 8 characters and not be common!
//           </Form.Text>
//         </Form.Group>

//         {error && <FetchBaseError error={error} />}

//         <Button variant="primary" type="submit" onClick={handleChangePassword}>
//           Change Password
//         </Button>
//       </Form>
//     </Container>
//   );
// }

// export default ChangeKnownPassword;
