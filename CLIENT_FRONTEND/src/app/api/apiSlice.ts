import {
  createApi,
  fetchBaseQuery,
} from "@reduxjs/toolkit/query/react";
import Cookies from "js-cookie";


const baseQuery = fetchBaseQuery({
  baseUrl: "http://localhost:8000/api/",
  credentials: "include",
  prepareHeaders: (headers) => {
    const csrftoken = Cookies.get("csrftoken");
    if (csrftoken) {
      headers.set("X-CSRFToken", csrftoken);
    }
    return headers;
  },
});

export const apiSlice = createApi({
  baseQuery: baseQuery,
  tagTypes: ["cars"],
  endpoints: (_builder) => ({}),
});
