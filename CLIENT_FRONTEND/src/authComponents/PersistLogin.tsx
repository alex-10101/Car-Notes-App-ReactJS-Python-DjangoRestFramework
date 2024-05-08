import { Outlet } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import { removeCredentials, setCredentials } from "../features/auth/authSlice";
import { apiSlice } from "../app/api/apiSlice";
import {
  useCheckUserIsAuthenticatedMutation,
  useLogoutUserMutation,
} from "../features/auth/authApiSlice";
import { useAppDispatch, useAppSelector } from "../app/hooks";
import Loading from "../components/Loading";

/**
 *
 * @returns Component to persist login state after page refresh. Component is used in App.tsx
 */
function PersistLogin() {
  const currentUser = useAppSelector((state) => state.auth.user);
  const dispatch = useAppDispatch();
  const [isLoading, setIsLoading] = useState(true);

  const [checkUserIsAuthenticated] = useCheckUserIsAuthenticatedMutation();
  const [logout] = useLogoutUserMutation();

  // needed with react 18 (useEffect runs twice in dev mode with strict mode)
  const effectRan = useRef(false);

  // check when the component mounts if the user is authenticated.
  // If yes, dispatch an action to set the user in the global state.
  // If no, log user out and clear all previous state.
  useEffect(() => {
    async function verifyUserIsAuthenticated() {
      try {
        const data = await checkUserIsAuthenticated().unwrap();
        if (data && data.user) {
          dispatch(setCredentials({ ...data }));
        }
      } catch {
        await logout().unwrap();
        dispatch(removeCredentials());
        dispatch(apiSlice.util.resetApiState());
      } finally {
        setIsLoading(false);
      }
    }

    if (effectRan.current === false) {
      if (!currentUser) {
        verifyUserIsAuthenticated();
      } else {
        setIsLoading(false);
      }

      return () => {
        effectRan.current = true;
      };
    }
  }, []);

  if (isLoading) {
    return <Loading />;
  }
  return <Outlet />;
}

export default PersistLogin;
