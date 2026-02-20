import { useLocation } from "react-router-dom";
import EditCarForm from "../components/EditCarForm";
import Loading from "../components/Loading";
import FetchBaseError from "../components/FetchBaseError";
import { useGetCarQuery } from "../redux-toolkit-config/api-services/carsApiService";

/**
 *
 * @returns A page, where the user can edit a car note.
 */
function EditCar() {
  const location = useLocation();

  let carId: number;

  if (!location.pathname.includes("admin")) {
    carId = Number(location.pathname.split("/")[2]);
  } else {
    carId = Number(location.pathname.split("/")[3]);
  }

  const { data: car, error, isLoading } = useGetCarQuery(carId);

  if (error) {
    return <FetchBaseError error={error} />;
  }

  if (isLoading || !car) {
    return <Loading />;
  }

  return <EditCarForm car={car} />;
}

export default EditCar;
