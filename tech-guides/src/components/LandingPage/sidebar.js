import React from "react";
import "../../css/lp_sidebar.css";

const CardItems = require("../../../data/cards.json");
const NewsConfig = require("../../../data/news_cfg.json");

function NewsBadge({ newsBadge }) {
  if (newsBadge === 0) {
    return null;
  }
  return <div className="badge lp_sidebar-badge">{newsBadge}</div>;
}

function SideBarContent({ name, icon, cards, lastItem }) {
  const anchor = name.replace(/[^a-zA-Z0-9]/g, "_").toLowerCase();
  const borderClass = lastItem
    ? ["lp_sidebar-border-last"]
    : ["lp_sidebar-border"];
  return (
    <div className={"lp_sidebar-element " + borderClass}>
      <img src={icon} width="20" height="20"></img>
      <h6>
        <a href={"#" + anchor}>{name}</a>
      </h6>
    </div>
  );
}

export default function SideBar({ newsBadge }) {
  const newsIcon = NewsConfig.icon;
  return (
    <div className="lp_sidebar-sidebar">
      <div className="lp_sidebar-box">
        {/* News item first */}
        <div className="lp_sidebar-element lp_sidebar-border lp_sidebar-badge">
          <img src={newsIcon} width="20" height="20"></img>
          <h6>
            <a href="#news">News</a>
          </h6>
          <NewsBadge newsBadge={newsBadge} />
        </div>
        {/* Side bar items */}
        {CardItems.sections.map((item, index, array) => {
          if (array.length - 1 === index) {
            { /* Side bar last item */ }
            return ( <SideBarContent index={index} key={CardItems.id} {...item} lastItem={true} /> );
          } else {
            { /* Side bar other items */ }
            return ( <SideBarContent index={index} key={CardItems.id} {...item} lastItem={false} /> );
          }
        })}
      </div>
    </div>
  );
}
