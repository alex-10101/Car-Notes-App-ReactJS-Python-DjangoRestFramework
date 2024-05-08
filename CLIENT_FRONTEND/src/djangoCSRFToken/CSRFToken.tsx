import { useState, useEffect, useRef } from "react";

function CSRFToken() {
  const [csrftoken, setcsrftoken] = useState("");
  const effectRan = useRef(false);

  function getCSRFCookie(name: string) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      let cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // When the component mounts, get the CSRF cookie.
  useEffect(() => {
    async function getCSRFToken() {
      try {
        const result = await fetch(
          "http://localhost:8000/api/auth/csrf_cookie",
          {
            method: "POST",
            credentials: "include",
          }
        );
        await result.json();
      } catch (err) {
        console.log(err);
      }
    }
    if (effectRan.current === false) {
      getCSRFToken();
      const csrf_cookie = getCSRFCookie("csrftoken");

      if (csrf_cookie) {
        setcsrftoken(csrf_cookie);
      }

      return () => {
        effectRan.current = true;
      };
    }
  }, []);

  return <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />;
}

export default CSRFToken;
