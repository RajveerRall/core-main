import React from "react";
import Carousel from "nuka-carousel";
import ReactMarkdown from "react-markdown";
import rehypeRaw from 'rehype-raw'

import "../../css/lp_cards.css";

const CardItems = require("../../../data/cards.json");

function SectionContent({ name, icon, cards }) {
  if (process.env.NODE_ENV === 'development') {
    console.log("================================");
    console.log("sectioncontent");
    console.log(cards);
    console.log("================================");
  }
  const anchor = name.replace(/[^a-zA-Z0-9]/g, "_").toLowerCase();
  return (
    <div className>
      <div className="home-cards__group">
        <h2 id={anchor} className="lp_cards-section">
          {name}
        </h2>
        <div className="lp_cards-card-grid">
          {cards.map((item, index) => (
            <CardContent index={index} key={cards.id} {...item} />
          ))}
        </div>
      </div>
    </div>
  );
}

function CardContent({ size, pages }) {
  const hasCarousel = pages.length > 1;
  if (process.env.NODE_ENV === 'development') {
    console.log("================================");
    console.log("cardcontent");
    console.log(pages);
    console.log("pages.length: " + pages.length);
    console.log("hasCarousel:  " + hasCarousel);
    console.log("================================");
  }
  return (
    <div className="lp_cards-card-single">
      {/* Multiple pages */}
      {hasCarousel && (
        <Carousel
          renderTopCenterControls={() => null}
          renderCenterLeftControls={({ previousSlide }) => (
            <button
              onClick={previousSlide}
              id="linear-gradient"
              className="lp_cards-carousel-button-left"
            >
              &lsaquo;
            </button>
          )}
          renderCenterRightControls={({ nextSlide }) => (
            <button
              onClick={nextSlide}
              id="linear-gradient"
              className="lp_cards-carousel-button-right"
            >
              &rsaquo;
            </button>
          )}
        >
          {pages.map((item, index) => (
            <PagesContent index={index} key={pages.id} {...item} />
          ))}
        </Carousel>
      )}

      {/* Single page */}
      {!hasCarousel &&
        pages.map((item, index) => (
          <PagesContent index={index} key={pages.id} {...item} />
        ))}
    </div>
  );
}

function PagesContent({ title, icon, content, link, color }) {
  if (process.env.NODE_ENV === 'development') {
    console.log("================================");
    console.log("pagecontent");
    console.log('title:   ' + title);
    console.log('icon:    ' + icon);
    console.log('content: ' + content);
    console.log('link:    ' + link);
    console.log('color:   ' + color);
    console.log("================================");
  }

  return (
    <div className="lp_cards-card-content">
      <img src={icon} alt="" width="50" height="50" />
      <h3>{title}</h3>
      <p>
        <ReactMarkdown
          children={content}
          rehypePlugins={[rehypeRaw]}
        />
      </p>
      {!!link && (
        <a href={link} className="card_link">
          <strong>Read more...</strong>
        </a>
      )}
    </div>
  );
}
export default function Cards() {
  return (
    <div>
      {CardItems.sections.map((item, index) => (
        <SectionContent index={index} key={CardItems.id} {...item} />
      ))}
    </div>
  );
}
