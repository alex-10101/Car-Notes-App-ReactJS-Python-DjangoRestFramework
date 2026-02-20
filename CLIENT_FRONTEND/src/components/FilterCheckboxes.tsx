import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
// import { carBrands, motors } from "../data/data";
import FilterCheckbox from "./FilterCheckbox";
import { useGetCarFilterOptionsQuery } from "../redux-toolkit-config/api-services/carsApiService";
import Loading from "./Loading";
import FetchBaseError from "./FetchBaseError";

/**
 *
 * @returns A form which contains all the checkboxes. The checkboxes are used to filter the car notes.
 */
function FilterCheckboxes() {
  const { data, isLoading, error } = useGetCarFilterOptionsQuery();

  if (isLoading) {
    return <Loading />;
  }

  if (error) {
    return <FetchBaseError error={error} />;
  }

  return (
    <Form>
      <fieldset>
        <Form.Group as={Row}>
          <Form.Label as="legend" column sm={2}>
            Brand
          </Form.Label>
          <Col sm={10} className="mt-2">
            {data &&
              data.brands.map((carBrand, index) => (
                <FilterCheckbox key={index} filter={carBrand} data={data} />
              ))}
          </Col>

          <Form.Label as="legend" column sm={2}>
            Engine/Motor
          </Form.Label>
          <Col sm={10} className="mt-2">
            {data &&
              data.motors.map((motor, index) => (
                <FilterCheckbox key={index} filter={motor} data={data} />
              ))}
          </Col>
        </Form.Group>
      </fieldset>
    </Form>
  );
}

export default FilterCheckboxes;
