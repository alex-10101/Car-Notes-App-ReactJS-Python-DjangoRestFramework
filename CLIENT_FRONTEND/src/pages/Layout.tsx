import Container from "react-bootstrap/Container";
import Navbar from "react-bootstrap/Navbar";
import { Link, Outlet, useNavigate } from "react-router-dom";
import { removeCredentials } from "../redux-toolkit-config/slices/authSlice";
import { apiSlice } from "../redux-toolkit-config/apiSlice";
import {
  useLogoutUserAllDevicesMutation,
  useLogoutUserMutation,
} from "../redux-toolkit-config/api-services/authApiService";
import Nav from "react-bootstrap/Nav";
import NavDropdown from "react-bootstrap/NavDropdown";
import { Button, Offcanvas } from "react-bootstrap";
import { useState } from "react";
import FilterCheckboxes from "../components/FilterCheckboxes";
import FetchBaseError from "../components/FetchBaseError";
import { useAppDispatch, useAppSelector } from "../redux-toolkit-config/hooks";

/**
 *
 * @returns A page (/component), which renders the layout of the application: the navbar, and the pages rendered under the navbar (the outlet).
 * The <Outlet /> component renders the child route's element, if there is one. (The routes and their children are defined in App.tsx).
 */
function Layout() {
  const currentUser = useAppSelector((state) => state.auth.user);
  const dispatch = useAppDispatch();
  const [logout, { error: logoutError }] = useLogoutUserMutation();
  const [logoutAllDevices, { error: logoutAllDevicesError }] =
    useLogoutUserAllDevicesMutation();

  const navigate = useNavigate();
  const [showOffcanvas, setShowOffcanvas] = useState(false);

  function handleCloseOffcanvas() {
    setShowOffcanvas(false);
  }

  function handleShowOffcanvas() {
    setShowOffcanvas(true);
  }

  /**
   * Make a POST request to log out when the user clicks "Log Out".
   */
  async function handleLogout(e: React.MouseEvent<HTMLElement, MouseEvent>) {
    e.preventDefault();
    await logout().unwrap();
    dispatch(removeCredentials());
    dispatch(apiSlice.util.resetApiState());
    // navigate("/login")
  }

  /**
   * Make a POST request to log out of all devices when the user clicks "Log Out All Devices".
   */
  async function handleLogoutAllDevices(
    e: React.MouseEvent<HTMLElement, MouseEvent>,
  ) {
    e.preventDefault();
    await logoutAllDevices().unwrap();
    dispatch(removeCredentials());
    dispatch(apiSlice.util.resetApiState());
    // navigate("/login")
  }

  /**
   * Navigate to the change password page when the user clicks "Change Password".
   * @param e
   */
  function handleNavigateToChangePasswordPage(
    e: React.MouseEvent<HTMLElement, MouseEvent>,
  ) {
    e.preventDefault();
    // navigate("/changePassword");
    navigate("/requestChangeForgottenPassword");
  }

  /**
   * Navigate to the delete account page when the user clicks "Delete Account".
   * @param e
   */
  function handleNavigateToDeleteAccountPage(
    e: React.MouseEvent<HTMLElement, MouseEvent>,
  ) {
    e.preventDefault();
    navigate("/deleteAccount");
  }

  return (
    <>
      {currentUser && (
        <Navbar collapseOnSelect className="bg-body-tertiary" sticky="top">
          {/* Button to show / hide the offcanvas with checkboxes. */}
          {/* position: "absolute" places the filter button outside the container flow, */}
          {/* but causes overlapping with the container on smaller screens */}
          <Button
            style={{
              position: "absolute",
              backgroundColor: "transparent",
              border: "none",
              top: 10,
            }}
            onClick={handleShowOffcanvas}
          >
            <span className="navbar-toggler-icon"></span>
          </Button>

          {/* The offcanvas with the checkboxes */}
          {/* The checkboxes are used for filtering the car notes. */}
          <Offcanvas show={showOffcanvas} onHide={handleCloseOffcanvas}>
            <Offcanvas.Header closeButton>
              <Offcanvas.Title>Filters</Offcanvas.Title>
            </Offcanvas.Header>
            <Offcanvas.Body>
              <FilterCheckboxes />
            </Offcanvas.Body>
          </Offcanvas>

          {/* the container in the navbar */}
          <Container>
            <Link
              to="/"
              style={{
                textDecoration: "none",
                cursor: "pointer",
              }}
            >
              {/* Hide this element on screens smaller than large */}
              {/* To avoid overlapping with the filters button */}
              <Navbar.Brand className="d-none d-lg-block">
                Welcome {currentUser.username}
              </Navbar.Brand>
            </Link>

            <Navbar.Toggle aria-controls="responsive-navbar-nav" />

            <Nav className="me-auto"></Nav>

            <Nav>
              <Link
                style={{
                  textDecoration: "none",
                  cursor: "pointer",
                  display: "flex", // otherwise it is not centered vertically
                  marginRight: "20px", // to add more space to the text right of the link
                }}
                to="/addCar"
              >
                <Navbar.Text>Add Car </Navbar.Text>
              </Link>

              <NavDropdown
                title="Account Settings"
                id="navbarScrollingDropdown"
              >
                <NavDropdown.Item
                  onClick={handleLogout}
                  style={{
                    cursor: "pointer",
                  }}
                >
                  Log Out
                </NavDropdown.Item>

                <NavDropdown.Item
                  onClick={handleLogoutAllDevices}
                  style={{
                    cursor: "pointer",
                  }}
                >
                  Log Out All Devices
                </NavDropdown.Item>

                <NavDropdown.Item
                  onClick={handleNavigateToChangePasswordPage}
                  style={{
                    cursor: "pointer",
                  }}
                >
                  Change Password
                </NavDropdown.Item>

                <NavDropdown.Divider />
                <NavDropdown.Item
                  onClick={handleNavigateToDeleteAccountPage}
                  style={{
                    cursor: "pointer",
                  }}
                >
                  Delete Account
                </NavDropdown.Item>
              </NavDropdown>
            </Nav>
          </Container>
        </Navbar>
      )}

      {logoutError && <FetchBaseError error={logoutError} />}
      {logoutAllDevicesError && (
        <FetchBaseError error={logoutAllDevicesError} />
      )}

      <Outlet />
    </>
  );
}

export default Layout;
