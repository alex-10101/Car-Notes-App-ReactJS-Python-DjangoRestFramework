import { ICar } from "../types/types";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import { useNavigate } from "react-router-dom";
import FetchBaseError from "./FetchBaseError";
import {
  useDeleteCarAdminPriviledgeMutation,
  useDeleteCarMutation,
} from "../redux-toolkit-config/api-services/carsApiService";
import { useAppSelector } from "../redux-toolkit-config/hooks";

/**
 *
 * @param car a car object
 * @returns A component which displays properties of a car.
 */
function Car({ car }: { car: ICar }) {
  const navigate = useNavigate();

  const [deleteCar, { error: regularUserError }] = useDeleteCarMutation();
  const [deleteCarAdminPriviledge, { error: adminError }] =
    useDeleteCarAdminPriviledgeMutation();

  const currentUser = useAppSelector((state) => state.auth.user);

  /**
   * Navigate to to edit car page when the user clicks the "Edit" button.
   */
  function handleGoToEditCarPage(
    e: React.MouseEvent<HTMLButtonElement, MouseEvent>,
  ) {
    e.preventDefault();
    navigate(`edit/${car.id}`);
  }

  /**
   * Make a DELETE request to delete a car note when the user clicks the "Delete" button.
   */
  async function handleDeleteCar(
    e: React.MouseEvent<HTMLButtonElement, MouseEvent>,
  ) {
    e.preventDefault();
    await deleteCar(car.id).unwrap();
  }

  /**
   * Make a DELETE request to delete a car note when an admin clicks the "Delete" button.
   */
  async function handleDeleteCarAdminPriviledge(
    e: React.MouseEvent<HTMLButtonElement, MouseEvent>,
  ) {
    e.preventDefault();
    await deleteCarAdminPriviledge(car.id).unwrap();
  }

  return (
    <Card>
      <Card.Body>
        <Card.Title>{car.model}</Card.Title>
        <Card.Text>{car.brand}</Card.Text>
        <Card.Text>{car.motor}</Card.Text>
        {currentUser?.is_staff && <Card.Text>User ID: {car.user}</Card.Text>}
        {car.user === currentUser?.id && (
          <Button
            variant="primary"
            onClick={handleGoToEditCarPage}
            style={{ marginRight: "9px" }}
          >
            Edit
          </Button>
        )}
        {!currentUser?.is_staff ? (
          <Button
            variant="danger"
            onClick={handleDeleteCar}
            style={{ marginRight: "9px" }}
          >
            Delete
          </Button>
        ) : (
          <Button
            variant="danger"
            onClick={handleDeleteCarAdminPriviledge}
            style={{ marginRight: "9px" }}
          >
            Delete
          </Button>
        )}
        {regularUserError && <FetchBaseError error={regularUserError} />}
        {adminError && <FetchBaseError error={adminError} />}
      </Card.Body>
    </Card>
  );
}

export default Car;
