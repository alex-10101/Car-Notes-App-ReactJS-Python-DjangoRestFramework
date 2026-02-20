import { useState } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Container from "react-bootstrap/Container";
import { useNavigate } from "react-router-dom";
import FetchBaseError from "../components/FetchBaseError";
import { useCreateCarMutation } from "../redux-toolkit-config/api-services/carsApiService";

/**
 *
 * @returns A page, where users can add a car note.
 */
function AddCar() {
  const [carProperties, setCarProperties] = useState({
    brand: "",
    model: "",
    motor: "",
  });

  const navigate = useNavigate();

  const [addCar, { error }] = useCreateCarMutation();

  /**
   * Handles changes in text / number / textarea inputs.
   * Uses the input's `name` attribute to update the corresponding
   * field in `carProperties` while preserving the rest of the state.
   * @param e
   */
  function handleChangeCarProperties(e: React.ChangeEvent<HTMLInputElement>) {
    e.preventDefault();
    setCarProperties((previousCarProperties) => ({
      ...previousCarProperties,
      [e.target.name]: e.target.value,
    }));
  }

  /**
   * Make a POST request to add a car note to the database when the user clicks the "Add Car" button.
   */
  async function handleAddCar(
    e: React.MouseEvent<HTMLButtonElement, MouseEvent>,
  ) {
    e.preventDefault();
    await addCar({
      model: carProperties.model,
      brand: carProperties.brand,
      motor: carProperties.motor,
    }).unwrap();
    navigate("/");
  }

  return (
    <Container className="my-5">
      <h1>Add Car</h1>
      <Form>
        <Form.Group className="mb-3 my-3" controlId="formBasicEmail">
          <Form.Label>Brand</Form.Label>
          <Form.Control
            type="text"
            placeholder="Brand,  for  example:  Porsche,  Audi,  BMW,  Mercedes,  Volkswagen,  Skoda"
            name="brand"
            onChange={handleChangeCarProperties}
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Ḿodel</Form.Label>
          <Form.Control
            type="text"
            placeholder="Model,  for  example:  911  GT3RS  2022,  5  Series  2022"
            name="model"
            onChange={handleChangeCarProperties}
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Motor</Form.Label>
          <Form.Control
            type="text"
            placeholder="Motor,  for  example:  Petrol,  7.5  liters  pro  100km"
            name="motor"
            onChange={handleChangeCarProperties}
          />
        </Form.Group>

        {error && <FetchBaseError error={error} />}

        <Button variant="primary" type="submit" onClick={handleAddCar}>
          Add Car
        </Button>
      </Form>
    </Container>
  );
}

export default AddCar;
