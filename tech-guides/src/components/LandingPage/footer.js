import React from "react";
import { useKeenSlider } from "keen-slider/react";
import "keen-slider/keen-slider.min.css";
import "../../css/lp_footer.css";

const FooterItems = require("../../../data/footer.json");

function Shuffle(array) {
  let currentIndex = array.length,
    randomIndex;
  while (currentIndex != 0) {
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;
    [array[currentIndex], array[randomIndex]] = [
      array[randomIndex],
      array[currentIndex],
    ];
  }
  return array;
}

function SliderItem({ id, index, name, url }) {
  return (
    <div className={`keen-slider__slide lp_footer-slide-slide${index}`}>
      <a href={url} className="lp_footer-slider-text">
        {name}
      </a>
    </div>
  );
}

export default function Footer() {
  const [sliderRef] = useKeenSlider(
    {
      loop: true,
      renderMode: "performance",
    },
    [
      (slider) => {
        let timeout;
        let mouseOver = false;
        function clearNextTimeout() {
          clearTimeout(timeout);
        }
        function nextTimeout() {
          clearTimeout(timeout);
          if (mouseOver) return;
          timeout = setTimeout(() => {
            slider.next();
          }, 3000);
        }
        slider.on("created", () => {
          slider.container.addEventListener("mouseover", () => {
            mouseOver = true;
            clearNextTimeout();
          });
          slider.container.addEventListener("mouseout", () => {
            mouseOver = false;
            nextTimeout();
          });
          nextTimeout();
        });
        slider.on("dragStarted", clearNextTimeout);
        slider.on("animationEnded", nextTimeout);
        slider.on("updated", nextTimeout);
      },
    ]
  );

  return (
    <div className="lp_footer-footer">
      <img
        src="img/common/air_liquide_logo_2.png"
        alt="logo-airLiquide"
        className="lp_footer-logo"
      ></img>
      <div className="lp_footer-slider">
        <div ref={sliderRef} className="keen-slider">
          {Shuffle(FooterItems.items).map((item, index) => (
            <SliderItem index={index} key={FooterItems.id} {...item} />
          ))}
        </div>
      </div>
    </div>
  );
}
