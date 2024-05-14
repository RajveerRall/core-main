import React, { useEffect, useState } from "react";
import "../../css/lp_top.css";

const Top = () => {
  // The back-to-top button is hidden at the beginning
  const [showButton, setShowButton] = useState(false);

  useEffect(() => {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 308) {
        setShowButton(true);
      } else {
        setShowButton(false);
      }
    });
  }, []);

  // This function will scroll the window to the top
  const scrollToTop = () => {
    window.scrollTo({
      top: 270,
      behavior: 'smooth' // for smoothly scrolling
    });
  };

  return (
    <>
      {showButton && (
        <button onClick={scrollToTop} className="lp_top">
          <i class="fas fa-angle-double-up"></i>
        </button>
      )}
      {/* &#8679; is used to create the upward arrow */}
    </>
  );
};

export default Top;
