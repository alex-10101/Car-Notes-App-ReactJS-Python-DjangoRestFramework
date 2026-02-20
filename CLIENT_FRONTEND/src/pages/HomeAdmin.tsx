import Container from "react-bootstrap/Container";
import Car from "../components/Car";
import { useLocation } from "react-router-dom";
import Row from "react-bootstrap/Row";
import Loading from "../components/Loading";
import FetchBaseError from "../components/FetchBaseError";
import { useGetAllCarsAdminPriviledgeQuery } from "../redux-toolkit-config/api-services/carsApiService";

/**
 *
 * @returns Admin page, which displays all the car notes data available to an admin.
 */
function HomeAdmin() {
  const location = useLocation();

  // This query will run / the data will refetch, whenever the query parameters in the url change.
  const {
    data: cars,
    isLoading,
    error,
  } = useGetAllCarsAdminPriviledgeQuery(location.search);

  return (
    <Container>
      {error ? (
        <FetchBaseError error={error} />
      ) : isLoading ? (
        <Loading />
      ) : cars && cars.length > 0 ? (
        // Bootstrap Grid System has 12 spaces on the width in total.
        // Make the page responsive by specifying the number of columns per row: a column
        // - takes all 12 / 1 = 12 spaces (full width of the screen) if the screen is extra small -> 1 column per row on extra small screens.
        // - takes all 12 / 2 = 6 spaces (half width of the screen) if the screen is medium -> 2 columns per row on medium screens.
        // - takes all 12 / 3 = 4 spaces (1/3 width of the screen) if the screen is large -> 3 columns per row on large screens.
        <Row xs={1} md={2} lg={3}>
          {cars.map((car) => (
            <Car key={car.id} car={car} />
          ))}
        </Row>
      ) : (
        <p className="my-3">No car notes.</p>
      )}
    </Container>
  );
}

export default HomeAdmin;
