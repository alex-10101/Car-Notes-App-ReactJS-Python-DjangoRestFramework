import { SerializedError } from "@reduxjs/toolkit";
import { FetchBaseQueryError } from "@reduxjs/toolkit/query/react";

/**
 * Displays an error message from the server.
 * Component is used when data is added/retrieved from/to the server using the browsers' fetch api.
 * @param param0
 * @returns
 */
function FetchBaseError({
  error,
}: {
  error: FetchBaseQueryError | SerializedError | undefined;
}) {

  /**
   * 
   * @param string 
   * @returns A new string with all the characters of the given string,
   * but with the first letter (at position/index 0) converted to uppercase letter.
   */
  function capitalizeFirstLetter(string: string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

  //  @ts-ignore
  const errorFromServer = error.data.detail;

  if (typeof errorFromServer === "string") {
    return <p style={{ color: "red" }}>{errorFromServer}</p>;
  }

  if (typeof errorFromServer === "object") {
    return Object.keys(errorFromServer).map((key, id) => (
      <p key={id} style={{ color: "red" }}>
        {capitalizeFirstLetter(key)}: {errorFromServer[key].join(" ")}
      </p>
    ));
  }
}

export default FetchBaseError;
