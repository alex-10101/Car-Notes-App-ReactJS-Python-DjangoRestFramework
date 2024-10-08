import { apiSlice } from "../../app/api/apiSlice";
import { IUser } from "../../types/types";

export const authApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getCSRFCookie: builder.mutation<string, void>({
      query: () => ({
        url: "/auth/csrf_cookie",
        method: "POST",
      }),
    }),
    checkUserIsAuthenticated: builder.mutation<{ user: IUser }, void>({
      query: () => ({
        url: "/auth/is_authenticated",
        method: "POST",
      }),
    }),
    registerUser: builder.mutation<
      void,
      {
        username: string;
        email: string;
        password: string;
        confirmPassword: string;
        captchaValue: string;
      }
    >({
      query: (body) => ({
        url: "/auth/register",
        method: "POST",
        body,
      }),
    }),
    loginUser: builder.mutation<
      { user: IUser },
      { email: string; password: string; captchaValue: string }
    >({
      query: (body) => ({
        url: "/auth/login",
        method: "POST",
        body,
      }),
    }),
    logoutUser: builder.mutation<void, void>({
      query: () => ({
        url: "/auth/logout",
        method: "POST",
      }),
    }),
    logoutUserAllDevices: builder.mutation<void, void>({
      query: () => ({
        url: "/auth/logout_all",
        method: "POST",
      }),
    }),
    deleteAccount: builder.mutation<void, { password: string }>({
      query: (body) => ({
        url: "/auth/delete_account",
        method: "DELETE",
        body,
      }),
    }),
    changePassword: builder.mutation<
      void,
      {
        oldPassword: string;
        newPassword: string;
        newPasswordConfirm: string;
      }
    >({
      query: (body) => ({
        url: "/auth/change_password",
        method: "PUT",
        body,
      }),
    }),
  }),
});

export const {
  useGetCSRFCookieMutation,
  useCheckUserIsAuthenticatedMutation,
  useRegisterUserMutation,
  useLoginUserMutation,
  useLogoutUserMutation,
  useLogoutUserAllDevicesMutation,
  useChangePasswordMutation,
  useDeleteAccountMutation,
} = authApiSlice;
