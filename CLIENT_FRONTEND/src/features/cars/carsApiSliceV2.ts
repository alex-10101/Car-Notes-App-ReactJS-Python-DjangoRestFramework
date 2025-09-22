import { ICar } from "../../types/types";
import { apiSlice } from "../../app/api/apiSlice";

// Define a service using a base URL and expected endpoints
export const carsApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getAllCars: builder.query<ICar[], string>({
      query: (url) => ({ url: `/cars/${url}`, method: "GET" }),
      providesTags: (result) =>
        // is result available?
        result
          ? // successful query -> provide a cache tag for each car and for the whole list
            [
              ...result.map(({ id }) => ({ type: "cars", id } as const)),
              { type: "cars", id: "LIST" },
            ]
          : // an error occurred, but we still want to refetch this query when `{ type: 'Posts', id: 'LIST' }` is invalidated
            [{ type: "cars", id: "LIST" }],
    }),
    getAllCarsAdminPriviledge: builder.query<ICar[], string>({
      query: (url) => ({ url: `/cars/admin/${url}`, method: "GET" }),
      // Provides a list of `Cars` by `id`.
      // If any mutation is executed that `invalidate`s any of these tags, this query will re-run to be always up-to-date.
      // The `LIST` id is a "virtual id" we just made up to be able to invalidate this query specifically if a new `Posts` element was added.
      providesTags: (result) =>
        // is result available?
        result
          ? // successful query
            [
              ...result.map(({ id }) => ({ type: "cars", id } as const)),
              { type: "cars", id: "LIST" },
            ]
          : // an error occurred, but we still want to refetch this query when `{ type: 'cars', id: 'LIST' }` is invalidated
            [{ type: "cars", id: "LIST" }],
    }),
    getCar: builder.query<ICar, string>({
      query: (carId) => ({ url: `/cars/${carId}`, method: "GET" }), // attaches the following string to the baseURL. Request is being sent to `http://localhost:3000/api/cars/:carId`.
      providesTags: (_result, _error, id) => [{ type: "cars", id }], // provides a cache tag `cars` + `id` to the data retreived. The underscores `_` are added to please typescript (variables not used).
    }),
    // The `createCar` endpoint is a "query" operation / mutation that mutates data (here POST method/request).
    // The first parameter of the mutation is the type of the result of the request.
    // The second parameter of the mutation is the type of the body that is sent with the request.
    createCar: builder.mutation<
      ICar,
      { model: string; brand: string; fuel: string }
    >({
      query: (body) => ({
        url: "/cars", // attaches the following string to the baseURL. Request is being sent to `http://localhost:3000/api/cars`.
        method: "POST", // defines the method of the request
        body, // defines the body of the request, the client input with which we want to updata db documens
      }),
      // Invalidates all cars-type queries providing the `LIST` id - after all, depending of the sort order,
      // that newly created car could show up in any lists.
      invalidatesTags: [{ type: "cars", id: "LIST" }],
    }),
    updateCar: builder.mutation<
      void,
      { model: string; brand: string; fuel: string; carId: string }
    >({
      query: (body) => ({
        url: "/cars/" + body.carId,
        method: "PUT",
        body,
      }),
      // Invalidates all queries that subscribe to this cars `carId` only.
      // In this case, `getCar` will be re-run. `getAllCars` *might*  rerun, if this id was under its results.
      // (The updated post's id might not be part of the getPosts query result in scenarios
      //  where the getPosts query applies filters, sorting, or pagination that exclude the updated post from the returned list.)
      invalidatesTags: (_result, _error, { carId }) => [
        { type: "cars", carId },
      ],
    }),
    deleteCar: builder.mutation<void, string>({
      query: (carId) => ({
        url: "/cars/" + carId,
        method: "DELETE",
      }),
      // Invalidates all queries that subscribe to this cars `carId` only.
      invalidatesTags: (_result, _error, carId) => [{ type: "cars", carId }],
    }),
    deleteCarAdminPriviledge: builder.mutation<void, string>({
      query: (carId) => ({
        url: "/cars/admin/" + carId,
        method: "DELETE",
      }),
      // Invalidates all queries that subscribe to this cars `carId` only.
      invalidatesTags: (_result, _error, carId) => [{ type: "cars", carId }],
    }),
  }),
});

// Export hooks for usage in functional components, which are
// auto-generated based on the defined endpoints
export const {
  useGetAllCarsQuery,
  useLazyGetAllCarsQuery,
  useGetAllCarsAdminPriviledgeQuery,
  useLazyGetAllCarsAdminPriviledgeQuery,
  useGetCarQuery,
  useCreateCarMutation,
  useUpdateCarMutation,
  useDeleteCarMutation,
  useDeleteCarAdminPriviledgeMutation,
} = carsApiSlice;
