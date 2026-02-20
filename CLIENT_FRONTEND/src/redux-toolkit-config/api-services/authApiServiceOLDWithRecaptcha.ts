import { apiSlice } from "../apiSlice";
import { IUser } from "../../types/types";

export const authApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getCSRFCookie: builder.mutation<string, void>({
      query: () => ({
        url: "/auth/csrf_cookie/",
        method: "POST",
      }),
    }),
    checkUserIsAuthenticated: builder.mutation<{ user: IUser }, void>({
      query: () => ({
        url: "/auth/is_authenticated/",
        method: "POST",
      }),
    }),
    registerUser: builder.mutation<
      string,
      {
        username: string;
        email: string;
        password: string;
        confirmPassword: string;
        captchaValue: string;
      }
    >({
      query: (body) => ({
        url: "/auth/register/",
        method: "POST",
        body,
      }),
    }),
    activateAccoumt: builder.mutation<string, { uid: string; token: string }>({
      query: ({ uid, token }) => ({
        url: `/auth/activate_account/${uid}/${token}/`,
        method: "POST",
      }),
    }),
    loginUser: builder.mutation<
      { user: IUser },
      { email: string; password: string; captchaValue: string }
    >({
      query: (body) => ({
        url: "/auth/login/",
        method: "POST",
        body,
      }),
    }),
    logoutUser: builder.mutation<void, void>({
      query: () => ({
        url: "/auth/logout/",
        method: "POST",
      }),
    }),
    logoutUserAllDevices: builder.mutation<void, void>({
      query: () => ({
        url: "/auth/logout_all/",
        method: "POST",
      }),
    }),
    deleteAccount: builder.mutation<void, { password: string }>({
      query: (body) => ({
        url: "/auth/delete_account/",
        method: "DELETE",
        body,
      }),
    }),
    // changeKnownPassword: builder.mutation<
    //   void,
    //   {
    //     oldPassword: string;
    //     newPassword: string;
    //     newPasswordConfirm: string;
    //   }
    // >({
    //   query: (body) => ({
    //     url: "/auth/change_known_password/",
    //     method: "PUT",
    //     body,
    //   }),
    // }),
    requestChangeForgottenPassword: builder.mutation<string, { email: string }>(
      {
        query: (body) => ({
          url: `/auth/request_change_known_password/`,
          method: "POST",
          body,
        }),
      },
    ),
    confirmChangeForgottenPassword: builder.mutation<
      string,
      {
        uid: string;
        token: string;
        newPassword: string;
        newPasswordConfirm: string;
      }
    >({
      query: (body) => ({
        url: `/auth/confirm_change_known_password/${body.uid}/${body.token}/`,
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
  useActivateAccoumtMutation,
  useLoginUserMutation,
  useLogoutUserMutation,
  useLogoutUserAllDevicesMutation,
  // useChangeKnownPasswordMutation, // not used anymore
  useRequestChangeForgottenPasswordMutation,
  useConfirmChangeForgottenPasswordMutation,
  useDeleteAccountMutation,
} = authApiSlice;
