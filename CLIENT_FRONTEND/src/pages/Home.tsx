import Container from "react-bootstrap/Container";
import Car from "../components/Car";
import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import Row from "react-bootstrap/Row";
import Loading from "../components/Loading";
import FetchBaseError from "../components/FetchBaseError";
import { useGetAllCarsQuery } from "../redux-toolkit-config/api-services/carsApiService";
import { useAppSelector } from "../redux-toolkit-config/hooks";
import Pagination from "react-bootstrap/Pagination";
// import { useGetAllCarsQuery } from "../features/cars/carsApiSliceV2";

/**
 *
 * @returns A page which dispays all the car notes created by the current user.
 */
function Home() {
  const navigate = useNavigate();
  const location = useLocation();
  const currentUser = useAppSelector((state) => state.auth.user);

  // If a user is redirected to this page after editing an item, for example on page 2,
  // the page will always be page 1, even if the edited item was on another page.
  const [page, setPage] = useState(1);

  // If the url does not contain any query param, append the page param to RTK Query like this: ?page={...}
  // If the url does already contain query params, append the page param to RTK Query like this: &page={...}
  // let queryString = location.search;
  // if (queryString) {
  //   queryString += `&page=${page}`;
  // } else {
  //   queryString += `?page=${page}`;
  // }
  const queryString = `${location.search}${location.search ? "&" : "?"}page=${page}`;

  // This query will run / the data will refetch, whenever the query parameters in the url change.
  // const { data: cars, isLoading, error } = useGetAllCarsQuery(location.search);
  const { data: result, isLoading, error } = useGetAllCarsQuery(queryString);
  const cars = result?.data;

  // whenever filters change (location.search), go back to page 1
  useEffect(() => {
    setPage(1);
  }, [location.search]);

  // When the component mounts, check if the user is an admin. If yes, redirect to admin page.
  useEffect(() => {
    if (currentUser && currentUser.is_staff) {
      navigate("/admin");
    }
  }, []);

  return (
    <Container>
      {error ? (
        <FetchBaseError error={error} />
      ) : isLoading ? (
        <Loading />
      ) : cars && cars.length > 0 ? (
        <>
          <Pagination>
            {/* Make a list of buttons, from 0, to the [(total nr. of pages returned by the server) - 1] */}
            {[...Array(result.pages).keys()].map((x) => {
              // Add 1 to the page numbers, so the buttons start with 1
              const p = x + 1;
              return (
                <Pagination.Item
                  key={p}
                  active={p === page}
                  // Set the page number to the number of the button clicked.
                  // This will cause RTK Query to fetch that particular page.
                  onClick={() => {
                    setPage(p);
                  }}
                >
                  {p}
                </Pagination.Item>
              );
            })}
          </Pagination>

          {/* Bootstrap Grid System has 12 spaces on the width in total.
          Make the page responsive by specifying the number of columns per row: a column:
          - takes all 12 / 1 = 12 spaces (full width of the screen) if the screen is extra small -> 1 column per row on extra small screens.
          - takes all 12 / 2 = 6 spaces (half width of the screen) if the screen is medium -> 2 columns per row on medium screens.
          - takes all 12 / 3 = 4 spaces (1/3 width of the screen) if the screen is large -> 3 columns per row on large screens. */}
          <Row xs={1} md={2} lg={3}>
            {cars.map((car) => (
              <Car key={car.id} car={car} />
            ))}
          </Row>
        </>
      ) : (
        <p className="my-3">No car notes.</p>
      )}
    </Container>
  );
}

export default Home;
