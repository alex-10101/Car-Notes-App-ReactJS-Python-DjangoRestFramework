import { BrowserRouter, Route, Routes } from "react-router-dom";
import Login from "./pages/authPages/Login";
import Register from "./pages/authPages/Register";
import Home from "./pages/Home";
import EditCar from "./pages/EditCar";
import Layout from "./pages/Layout";
import NoPage from "./pages/NoPage";
import AddCar from "./pages/AddCar";
import DeleteAccount from "./pages/authPages/DeleteAccount";
import HomeAdmin from "./pages/HomeAdmin";
// import ChangeKnownPassword from "./pages/authPages/ChangeKnownPassword";
import { useEffect } from "react";
import ActivateAccount from "./pages/authPages/ActivateAccount";
import PersistLogin from "./components/authComponents/PersistLogin";
import { PrivateOutlet } from "./components/authComponents/PrivateOutlet";
import { PrivateOutletAdmin } from "./components/authComponents/PrivateOutletAdmin";
import RequestChangeForgottenPassword from "./pages/authPages/RequestChangeForgottenPassword";
import ConfirmChangeForgottenPassword from "./pages/authPages/ConfirmChangeForgottenPassword";

/**
 *
 * @returns Component that defines the routes of the application
 */
function App() {
  // When the component mounts, get the CSRF cookie.
  useEffect(() => {
    async function getCSRFCookie() {
      try {
        const result = await fetch(
          "http://localhost:8000/api/auth/csrf_cookie/",
          {
            method: "GET",
            credentials: "include",
          },
        );
        await result.json();
      } catch (err) {
        // console.log(err);
      }
    }

    getCSRFCookie();
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route element={<PersistLogin />}>
            <Route element={<PrivateOutlet />}>
              <Route index element={<Home />} />
              <Route path="edit/:id" element={<EditCar />} />
              <Route path="addCar" element={<AddCar />} />
              <Route path="deleteAccount" element={<DeleteAccount />} />
              {/* <Route path="changePassword" element={<ChangeKnownPassword />} /> */}
              <Route element={<PrivateOutletAdmin />}>
                <Route path="admin" element={<HomeAdmin />} />
                <Route path="admin/edit/:id" element={<EditCar />} />
              </Route>
            </Route>
          </Route>
          <Route path="register" element={<Register />} />
          <Route path="activate/:uid/:token/" element={<ActivateAccount />} />
          <Route path="login" element={<Login />} />
          <Route
            path="requestChangeForgottenPassword"
            element={<RequestChangeForgottenPassword />}
          />
          <Route
            path="confirmChangeForgottenPassword/:uid/:token"
            element={<ConfirmChangeForgottenPassword />}
          />
          <Route path="*" element={<NoPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
