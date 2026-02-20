import { ICar } from "../types/types";
import { useState } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { useNavigate } from "react-router-dom";
import { useUpdateCarMutation } from "../redux-toolkit-config/api-services/carsApiService";
import Container from "react-bootstrap/Container";
import FetchBaseError from "./FetchBaseError";

/**
 *
 * @param car The properties of the car before the update
 * @returns Component that returns the form with which the user can update his/her car
 */
function EditCarForm({ car }: { car: ICar }) {
  const [carProperties, setCarProperties] = useState({
    brand: car.brand,
    model: car.model,
    motor: car.motor,
  });

  const navigate = useNavigate();

  const [updateCar, { error }] = useUpdateCarMutation();


  /**
   * Handles changes in text / number / textarea inputs.
   * Uses the input's `name` attribute to update the corresponding
   * field in `carProperties` while preserving the rest of the state.
   * @param e 
   */
  function handleChangeCarProperties(e: React.ChangeEvent<HTMLInputElement>) {
    e.preventDefault();
    setCarProperties({
      ...carProperties,
      [e.target.name]: e.target.value,
    });
  }

  /**
   * Make a PUT request to edit a car note when the user clicks the "Edit Car" button.
   */
  async function handleEditCar(
    e: React.MouseEvent<HTMLButtonElement, MouseEvent>,
  ) {
    e.preventDefault();
    await updateCar({
      model: carProperties.model,
      brand: carProperties.brand,
      motor: carProperties.motor,
      carId: car.id,
    }).unwrap();
    navigate("/");
  }

  return (
    <Container className="my-5">
      <h1>Edit Car</h1>
      <Form>
        <Form.Group className="mb-3 my-3" controlId="formBasicEmail">
          <Form.Label>Brand</Form.Label>
          <Form.Control
            type="text"
            name="brand"
            value={carProperties.brand}
            onChange={handleChangeCarProperties}
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Ḿodel</Form.Label>
          <Form.Control
            type="text"
            name="model"
            value={carProperties.model}
            onChange={handleChangeCarProperties}
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Motor</Form.Label>
          <Form.Control
            type="text"
            name="motor"
            value={carProperties.motor}
            onChange={handleChangeCarProperties}
          />
        </Form.Group>

        {/**If an error occured, show the error message. The error message comes from the server. */}
        {error && <FetchBaseError error={error} />}

        <Button variant="primary" type="submit" onClick={handleEditCar}>
          Edit Car
        </Button>
      </Form>
    </Container>
  );
}

export default EditCarForm;
