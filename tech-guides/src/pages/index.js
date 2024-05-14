import React, { useState } from "react";
import Layout from "@theme/Layout";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import SearchBar from "@theme/SearchBar";
import Cards from "../components/LandingPage/cards";
import News from "../components/LandingPage/news";
import "../css/lp_home.css";
import "../css/lp_search.css";
import Top from "../components/LandingPage/top";
import Footer from "../components/LandingPage/footer";
import SideBar from "../components/LandingPage/sidebar";

function Home() {
  const context = useDocusaurusContext();
  const { siteConfig = {} } = context;
  const [newsBadge, setNewsBadge] = useState(0);

  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Technical Guides"
    >
      <div className="lp_home">
        <div className="lp_home-news">
          <h1 className="lp_home-news_title">
            Technical Guides and Associated News
          </h1>
        </div>
        <main>
          <div className="landing-search">
            <SearchBar />
          </div>
          <div className="lp_home-wrapper">
            <div className="lp_home-left">
              <SideBar newsBadge={newsBadge} />
            </div>
            <div className="lp_home-middle">
              <Cards />
              <News setNewsBadge={setNewsBadge} />
            </div>
            <div className="lp_home-right"></div>
          </div>
          <Top />
        </main>
      </div>
      <Footer />
    </Layout>
  );
}

export default Home;
