# Car Notes Application

- Application for car enthusiasts to easily organize and track their personal notes when considering the
  purchase of a vehicle.

- The project utilizes Django's session uthentication system.

- Email activation is required before user accounts become active.

- Authenticated users can add, view, edit, or delete their own car notes. Administrators have the ability to
  access and delete all notes in the database.

- Users can filter their cars by motor/engine and brand using checkboxes. The selected values are appended to the
  URL as query parameters and the filtered data is retrieved automatically when URL changes.

- Integrated server-side pagination to efficiently handle a large number of car botes and reduce the server’s response times.

- Unit Tests

- Used separate Dockerfiles to containerize the frontend and backend, and Docker Compose to build and run the services together.
