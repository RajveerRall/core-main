import React, { useState } from "react";
import Cookies from "universal-cookie";
import { useInView } from "react-intersection-observer";
import { Row, Col } from "react-bootstrap";
import ReactHtmlParser from "react-html-parser";
import InfiniteScroll from "react-infinite-scroll-component";
import "../../css/lp_news.css";
import _HTMLEllipsis from "react-lines-ellipsis/lib/html";
import responsiveHOC from "react-lines-ellipsis/lib/responsiveHOC";

const HTMLEllipsis = responsiveHOC()(_HTMLEllipsis);
const NewsList = require("../../../data/news.json");
const NewsConfig = require("../../../data/news_cfg.json");
const cookies = new Cookies();

function NewsContent({ title, date, badge, image, description, badge_color }) {
  function handleReadMoreClick(e) {
    e.preventDefault();
    setUseEllipsis(false);
    setReadMoreClicked(true);
  }

  function handleReflow({ clamped, html }) {
    setClamped(clamped);
  }

  const [useEllipsis, setUseEllipsis] = useState(true);
  const [isClamped, setClamped] = useState(false);
  const [readMoreClicked, setReadMoreClicked] = useState(false);

  return (
    <Row className="lp_news">
      <Col xs={1} className="lp_news-block-image">
        <img src={image} width="70" className="lp_news-image"></img>
      </Col>
      <Col>
        <Row>
          <Col lg={2} md={2} sm={2}>
            <div className="badge lp_news-badge" style={{ backgroundColor: badge_color }}>
              {badge}
            </div>
          </Col>
          <Col  >
            <div className="lp_news-title">{title}</div>
          </Col>
          <Col lg={1}  md={2} sm={2}>
            <div className="lp_news-date">{date}</div>
          </Col>
        </Row>
        <Row>
          <div>
            {useEllipsis ? (
              <div
                className={
                  isClamped ? "lp_news-description-mask" : "lp_news-description"
                }
                onClick={isClamped ? handleReadMoreClick : undefined}
              >
                <HTMLEllipsis
                  unsafeHTML={description}
                  maxLine={4}
                  trimRight={false}
                  basedOn="words"
                  onReflow={handleReflow}
                />
              </div>
            ) : (
              <div className="lp_news-description">
                {ReactHtmlParser(description)}
              </div>
            )}
            {isClamped && !readMoreClicked && (
              <div
                className="lp_news-btn-read-more"
                onClick={handleReadMoreClick}
              >
                Read more
              </div>
            )}
          </div>
        </Row>
        <div className="lp_news-border-bottom"></div>
      </Col>
    </Row>
  );
}

export default function News({ setNewsBadge }) {
  // Unread news badge
  const updateNewsBadge = (count) => {
    setNewsBadge(count);
  };

  const lastNewsDate = NewsList.items.slice(0, 1)[0].date;
  let newsNotificationIndicator;

  if (cookies.get("news") === undefined) {
    // No news cookie
    // Set news cookie with last news date
    cookies.set("news", lastNewsDate, { path: "/" });
  } else {
    let cookieNewsDate = cookies.get("news");
    if (lastNewsDate !== cookieNewsDate) {
      newsNotificationIndicator = true;
      let cookieLastReadNewsDate = new Date(cookieNewsDate);
      let newsUnreadCount = 0;
      // Count number of unread news
      for (let newsItem of NewsList.items) {
        if (new Date(newsItem["date"]) < cookieLastReadNewsDate) {
          break;
        }
        newsUnreadCount++;
      }
      updateNewsBadge(newsUnreadCount); // Set news badge
    } else {
      newsNotificationIndicator = false;
      updateNewsBadge(0); // Remove news badge
    }
  }

  const { ref, inView } = useInView({
    /* Optional options */
    threshold: 0.3,
  });

  // Is news bloc visible? Removing notification indicator
  if (inView && newsNotificationIndicator) {
    // Update news cookie
    cookies.set("news", lastNewsDate, { path: "/" });
    updateNewsBadge(0); // Remove news badge
  }

  return (
    <section id="news">
      <h2 className="lp_news-latest-news">Latest News</h2>
      <div ref={ref} className="lp_news-block">
        <NewsDisplay />
      </div>
    </section>
  );
}

function NewsDisplay() {
  const [newsStart, setNewsStart] = useState(NewsConfig.display);
  const [newsItems, setNewsItems] = useState(
    NewsList.items.slice(0, NewsConfig.display)
  );
  const [hasMoreNews, setHasMoreNews] = useState(true);

  const fetchMoreNews = () => {
    if (newsStart >= NewsList.items.length) {
      setHasMoreNews(false);
      return;
    }

    setNewsStart((newsStart) => newsStart + NewsConfig.load_more);

    setTimeout(() => {
      setNewsItems(
        newsItems.concat(
          NewsList.items.slice(newsStart, newsStart + NewsConfig.load_more)
        )
      );
    }, 500);

    if (process.env.NODE_ENV === 'development') {
      console.log('--------------------------');
      console.log('fetchMoreNews > newsStart: ' + newsStart)
      console.log('fetchMoreNews > hasMoreNews: ' + hasMoreNews);
      console.log('fetchMoreNews > newsItems.length: ' + newsItems.length);
      console.log('--------------------------');
    }
  };

  if (process.env.NODE_ENV === 'development') {
    console.log('newsItems.length: ' + newsItems.length);
    console.log('NewsList.items.length: ' + NewsList.items.length);
    console.log('newsStart: ' + newsStart)
    console.log('hasMoreNews: ' + hasMoreNews);
    console.log('fetchMoreNews: ' + fetchMoreNews);
  }

  return (
    <InfiniteScroll
      dataLength={newsItems.length}
      next={fetchMoreNews}
      hasMore={hasMoreNews}
      loader={<h4>Loading...</h4>}
      endMessage={
        <p style={{ textAlign: "center" }}>
          <b>Yay! You have seen it all</b>
        </p>
      }
    >
      {newsItems.map((item, index) => (
        <NewsContent key={newsItems.date + '-' + newsItems.title} {...item} />
      ))}
    </InfiniteScroll>
  );
}
