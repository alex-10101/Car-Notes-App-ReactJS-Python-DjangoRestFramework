import { SerializedError } from "@reduxjs/toolkit";
import { FetchBaseQueryError } from "@reduxjs/toolkit/query/react";

/**
 * Displays an error message from the server.
 * Component is used when data is added/retrieved from/to the server using the Fetch API.
 * @param param0
 * @returns
 */
function FetchBaseError({
  error,
}: {
  error: FetchBaseQueryError | SerializedError | undefined;
}) {
  //  @ts-ignore
  const errorFromServer = error.data.detail;

  if (typeof errorFromServer === "string") {
    return <p style={{ color: "red" }}>{errorFromServer}</p>;
  }

  if (typeof errorFromServer === "object") {
    return Object.keys(errorFromServer).map((key, id) => (
      <p key={id} style={{ color: "red" }}>
        {errorFromServer[key].join(" ")}
      </p>
    ));
  }
}

export default FetchBaseError;
