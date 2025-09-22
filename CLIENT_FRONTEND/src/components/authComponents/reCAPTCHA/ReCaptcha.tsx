import { useEffect, useState } from "react";

/**
 *
 * @param param0
 * @returns a reCAPTCHA widget.
 */
function ReCaptcha() {
  const [recaptchaIsReady, setRecaptchaIsReady] = useState(false);

  useEffect(() => {
    // after the script loads, set recaptchaIsReady to true
    // @ts-ignore
    window.onRecaptchaLoad = () => {
      setRecaptchaIsReady(true);
    };

    // @ts-ignore
    if (!window.grecaptcha) {
      // Load the script only if it's not already available
      const script = document.createElement("script");
      script.src =
        "https://www.google.com/recaptcha/api.js?onload=onRecaptchaLoad&render=explicit";
      script.async = true;
      script.defer = true;
      document.body.appendChild(script);
      // @ts-ignore
    } else if (window.grecaptcha && window.grecaptcha.render) {
      // If reCAPTCHA is already loaded, set recaptchaIsReady to true (otherwise it will remain false)
      setRecaptchaIsReady(true);
    }

    // Clean up the global callback on component unmount
    return () => {
      // @ts-ignore
      window.onRecaptchaLoad = null;
    };
  }, []);

  useEffect(() => {
    if (recaptchaIsReady) {
      // render the recaptcha widget (here a div with id "recaptcha")
      // @ts-ignore
      window.grecaptcha.render("recaptcha", {
        sitekey: "6LeJw9ArAAAAAKWncgGOQPXczV2uqYL70iSny6Fq",
      });
    }
  }, [recaptchaIsReady]);

  // show the recaptcha widget
  return <div id="recaptcha"></div>;
}
export default ReCaptcha;

