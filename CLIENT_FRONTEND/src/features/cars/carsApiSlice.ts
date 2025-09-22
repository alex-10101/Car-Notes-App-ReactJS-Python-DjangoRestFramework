import { ICar } from "../../types/types";
import { apiSlice } from "../../app/api/apiSlice";

// Define a service using a base URL and expected endpoints
export const carsApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getAllCars: builder.query<ICar[], string>({
      query: (url) => `/cars/${url}`,
      providesTags: ["cars"],
    }),
    getAllCarsAdminPriviledge: builder.query<ICar[], string>({
      query: (url) => `/cars/admin/${url}`,
      providesTags: ["cars"],
    }),
    getCar: builder.query<ICar, number>({
      query: (carId) => "/cars/" + carId,
      providesTags: ["cars"],
    }),
    createCar: builder.mutation<
      ICar,
      { model: string; brand: string; motor: string }
    >({
      query: (body) => ({
        url: "/cars/",
        method: "POST",
        body,
      }),
      invalidatesTags: ["cars"],
    }),
    updateCar: builder.mutation<
      void,
      { model: string; brand: string; motor: string; carId: number }
    >({
      query: (body) => ({
        url: "/cars/" + body.carId + "/",
        method: "PUT",
        body,
      }),
      invalidatesTags: ["cars"],
    }),
    deleteCar: builder.mutation<void, number>({
      query: (carId) => ({
        url: "/cars/" + carId + "/",
        method: "DELETE",
      }),
      invalidatesTags: ["cars"],
    }),
    deleteCarAdminPriviledge: builder.mutation<void, number>({
      query: (carId) => ({
        url: "/cars/admin/" + carId + "/",
        method: "DELETE",
      }),
      invalidatesTags: ["cars"],
    }),
  }),
});

// Export hooks for usage in functional components, which are
// auto-generated based on the defined endpoints
export const {
  useGetAllCarsQuery,
  useGetAllCarsAdminPriviledgeQuery,
  useGetCarQuery,
  useCreateCarMutation,
  useUpdateCarMutation,
  useDeleteCarMutation,
  useDeleteCarAdminPriviledgeMutation,
} = carsApiSlice;
