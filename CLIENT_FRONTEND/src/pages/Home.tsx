import Container from "react-bootstrap/Container";
import Car from "../components/Car";
import { useAppSelector } from "../app/hooks";
import { useLocation, useNavigate } from "react-router-dom";
import { useEffect } from "react";
import Row from "react-bootstrap/Row";
import Loading from "../components/Loading";
import FetchBaseError from "../components/FetchBaseError";
import { useGetAllCarsQuery } from "../features/cars/carsApiSlice";
// import { useGetAllCarsQuery } from "../features/cars/carsApiSliceV2";

/**
 *
 * @returns A page which dispays all the car notes created by the current user.
 */
function Home() {
  const navigate = useNavigate();
  const location = useLocation();
  const currentUser = useAppSelector((state) => state.auth.user);

  // This query will run / the data will refetch, whenever the query parameters in the url change.
  const { data: cars, isLoading, error } = useGetAllCarsQuery(location.search);

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

export default Home;
