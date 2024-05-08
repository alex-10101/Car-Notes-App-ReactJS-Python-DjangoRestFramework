import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import { carBrands, motors } from "../data/data";
import FilterCheckbox from "./FilterCheckbox";
import CSRFToken from "../djangoCSRFToken/CSRFToken";

/**
 *
 * @returns A form which contains all the checkboxes. The checkboxes are used to filter the car notes.
 */
function FilterCheckboxes() {
  return (
    <Form>
      <CSRFToken />
      <fieldset>
        <Form.Group as={Row}>
          <Form.Label as="legend" column sm={2}>
            Brand
          </Form.Label>
          <Col sm={10} className="mt-2">
            {carBrands.map((carBrand, index) => (
              <FilterCheckbox key={index} filter={carBrand} />
            ))}
          </Col>

          <Form.Label as="legend" column sm={2}>
            Engine/Motor
          </Form.Label>
          <Col sm={10} className="mt-2">
            {motors.map((motor, index) => (
              <FilterCheckbox key={index} filter={motor} />
            ))}
          </Col>
        </Form.Group>
      </fieldset>
    </Form>
  );
}

export default FilterCheckboxes;
