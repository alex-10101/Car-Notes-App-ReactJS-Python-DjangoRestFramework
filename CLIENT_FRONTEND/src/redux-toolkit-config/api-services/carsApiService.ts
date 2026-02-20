import { ICar, ICarsFilterOptions, PaginatedResponse } from "../../types/types";
import { apiSlice } from "../apiSlice";

// Define a service using a base URL and expected endpoints
export const carsApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    /**
     * Query which makes a request to the server to get all cars for the reqest user.
     */
    getAllCars: builder.query<PaginatedResponse<ICar>, string>({
      /**
       * Function, which attaches `/cars/${url}/` to the baseUrl. Final URL = baseUrl + `/cars/${url}/`.
       * @param url a string, which contains the query parameters / search parameters for filtering the data.
       * @returns all cars of the request user from the server.
       */
      query: (url) => ({
        url: `/cars/`,
        method: "GET",
        params: Object.fromEntries(new URLSearchParams(url)),
      }),

      /**
       * Function, which provides the cache tags for the results returned by the server.
       * @param result the list of cars of the request user
       * @returns a list of cache tags
       */
      providesTags: (result) =>
        // result
        //   ? [
        //       ...result.map(({ id }) => ({ type: "cars", id }) as const),
        //       { type: "cars", id: "LIST" },
        //     ]
        //   : [{ type: "cars", id: "LIST" }],
        result
          ? [
              // Adds the id of the item as individual cache tag for EACH item in the list:
              ...result.data.map(
                (item) => ({ type: "cars", id: item.id }) as const,
              ),
              // Adds LIST tag for the whole collection:
              { type: "cars", id: "LIST" },
            ]
          : // Adds LIST tag for the whole collection:
            [{ type: "cars", id: "LIST" }],
    }),

    /**
     * Query which makes a request to the server to get all cars.
     */
    getAllCarsAdminPriviledge: builder.query<ICar[], string>({
      /**
       * Function, which attaches `/cars/admin/${url}/` to the baseUrl. Final URL = baseUrl + `/cars/admin/${url}/`.
       * The function also determines the method of the request: GET request.
       * @param url
       * @returns the final URL
       */
      query: (url) => ({ url: `/cars/admin/${url}/`, method: "GET" }),

      /**
       * Function, which provides the cache tags for the results returned by the server.
       * @param result
       * @returns
       */
      providesTags: (result) =>
        // result
        //   ? [
        //       ...result.map(({ id }) => ({ type: "cars", id }) as const),
        //       { type: "cars", id: "LIST" },
        //     ]
        //   : [{ type: "cars", id: "LIST" }],
        result
          ? [
              // Adds the id of the item as individual cache tag for EACH item in the list:
              ...result.map((car) => ({ type: "cars", id: car.id }) as const),
              // Adds LIST tag for the whole collection:
              { type: "cars", id: "LIST" },
            ]
          : // Adds LIST tag for the whole collection:
            [{ type: "cars", id: "LIST" }],
    }),

    /**
     * Query, which makes a request to the server to get a single car.
     */
    getCar: builder.query<ICar, number>({
      /**
       * Function, which attaches the id of the car to the base url. Final URL = baseUrl + `/cars/${carId}/`.
       *  The function also determines the method of the request: GET request.
       * @param carId the id of the car
       * @returns the car with the given id from the server
       */
      query: (carId) => ({ url: `/cars/${carId}/`, method: "GET" }),

      /**
       * Function, which provides the cache tag for the car returned by the server.
       * @param _result the car returned by the server
       * @param _error the error returned by the server
       * @param id the id of the car
       * @returns a cache tag
       */
      providesTags: (_result, _error, id) => [{ type: "cars", id }],
    }),

    /**
     * Query, which makes a request to the server to retrie all distinct car motors with all distinct car brands.
     */
    getCarFilterOptions: builder.query<ICarsFilterOptions, void>({
      /**
       * Function, which attaches the "/cars/filters/" of the car to the base url. Final URL = baseUrl + `/cars/filters/`.
       * The function also determines the method of the request: GET request.
       * @returns the final URL
       */
      query: () => ({ url: "/cars/filters/", method: "GET" }),

      /**
       * Function, which provides the cache tag for the filters returned by the server.
       */
      providesTags: [{ type: "cars", id: "FILTERS" }],
    }),

    /**
     * Mutation, which makes a request to the server to add a new car.
     */
    createCar: builder.mutation<
      ICar,
      { model: string; brand: string; motor: string }
    >({
      /**
       * Function, which attaches "/cars/" to the base url. Final URL = baseUrl + `/cars/`.
       * The function also determines the method of the request: POST request.
       * @param body The data sent to the server, with which the server creates a new car.
       * @returns The created car.
       */
      query: (body) => ({
        url: "/cars/",
        method: "POST",
        body,
      }),

      /**
       * Function which invalidates the { type: "cars", id: "LIST" } cache tag.
       *
       * This will cause getAllCars, getAllCarsAdminPriviledge, getProductFilterOptions
       * queries to rerun everywhere they are used in the app,
       * because these queries provide this cache tag to the data returned by the server.
       *
       * The queries rerun everywhere they are used, in order to show the up-to-date data everywhere in the app.
       */
      invalidatesTags: [
        { type: "cars", id: "LIST" },
        { type: "cars", id: "FILTERS" },
      ],
    }),

    /**
     * Mutation, which makes a request to the server to update a car of the request user.
     */
    updateCar: builder.mutation<
      void,
      { model: string; brand: string; motor: string; carId: number }
    >({
      /**
       * Function, which attaches "/cars/" and the id of the car to the base url. Final URL = baseUrl + `/cars/${body.carId}/`.
       * The function also determines the method of the request: PUT request.
       * @param body The data sent to the server, with which the server updates the car.
       * @returns
       */
      query: (body) => ({
        url: `/cars/${body.carId}/`,
        method: "PUT",
        body,
      }),

      /**
       * Function which invalidates the { type: "cars", id: carId } cache tag.
       *
       * This will cause getAllCars, getAllCarsAdminPriviledge, getCar, getProductFilterOptions
       * queries to rerun everywhere they are used in the app,
       * because these queries provide this cache tag to the data returned by the server.
       *
       * The queries rerun everywhere they are used, in order to show the up-to-date data everywhere in the app.
       *
       * @param _result the data returned by the server (here no data is returned by the server)
       * @param _error the error returned by the server
       * @param param2 the id of the car
       * @returns a cache tag
       */
      invalidatesTags: (_result, _error, { carId }) => [
        { type: "cars", id: carId },
        { type: "cars", id: "FILTERS" },
      ],
    }),

    /**
     * Mutation, which makes a request to the server to delete a car of the request user.
     */
    deleteCar: builder.mutation<void, number>({
      /**
       * Function, which attaches "/cars/" and the id of the car to the base url. Final URL = baseUrl + `/cars/${carId}/`.
       * The function also determines the method of the request: DELETE request.
       * @param carId
       * @returns
       */
      query: (carId) => ({
        url: `/cars/${carId}/`,
        method: "DELETE",
      }),

      /**
       * Function which invalidates the { type: "cars", id: carId }, { type: "cars", id: "LIST" } cache tags.
       *
       * This will cause getAllCars, getAllCarsAdminPriviledge, getCar, getProductFilterOptions
       * queries to rerun everywhere they are used in the app,
       * because these queries provide this cache tag to the data returned by the server.
       * Invalidating the LIST tag causes queries to rerun for every page.
       *
       * The queries rerun everywhere they are used, in order to show the up-to-date data everywhere in the app.
       *
       * @param _result the data returned by the server (here no data is returned by the server)
       * @param _error the error returned by the server
       * @param carId the id of the car
       * @returns a cache tag
       */
      invalidatesTags: (_result, _error, carId) => [
        { type: "cars", id: carId },
        { type: "cars", id: "LIST" },
        { type: "cars", id: "FILTERS" },
      ],
    }),

    /**
     * Mutation, which makes a request to the server to delete a car.
     */
    deleteCarAdminPriviledge: builder.mutation<void, number>({
      /**
       * Function, which attaches "/cars/admin/" and the id of the car to the base url. Final URL = baseUrl + `/cars/admin/${carId}/`.
       * The function also determines the method of the request: DELETE request.
       * @param carId
       * @returns
       */
      query: (carId) => ({
        url: `/cars/admin/${carId}/`,
        method: "DELETE",
      }),

      /**
       * Function which invalidates the { type: "cars", id: carId } cache tag.
       *
       * This will cause getAllCars, getAllCarsAdminPriviledge, getCar, getProductFilterOptions
       * queries to rerun everywhere they are used in the app,
       * because these queries provide this cache tag to the data returned by the server.
       *
       * The queries rerun everywhere they are used, in order to show the up-to-date data everywhere in the app.
       *
       * @param _result the data returned by the server (here no data is returned by the server)
       * @param _error the error returned by the server
       * @param carId the id of the car
       * @returns a cache tag
       */
      invalidatesTags: (_result, _error, carId) => [
        { type: "cars", id: carId },
        { type: "cars", id: "LIST" },
        { type: "cars", id: "FILTERS" },
      ],
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
  useGetCarFilterOptionsQuery,
  useCreateCarMutation,
  useUpdateCarMutation,
  useDeleteCarMutation,
  useDeleteCarAdminPriviledgeMutation,
} = carsApiSlice;
