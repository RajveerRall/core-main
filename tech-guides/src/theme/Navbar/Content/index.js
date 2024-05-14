import React from 'react';
import {useThemeConfig} from '@docusaurus/theme-common';
import {
  splitNavbarItems,
  useNavbarMobileSidebar,
} from '@docusaurus/theme-common/internal';
import NavbarItem from '@theme/NavbarItem';
import NavbarColorModeToggle from '@theme/Navbar/ColorModeToggle';
import SearchBar from '@theme/SearchBar';
import NavbarMobileSidebarToggle from '@theme/Navbar/MobileSidebar/Toggle';
import NavbarLogo from '@theme/Navbar/Logo';
import NavbarSearch from '@theme/Navbar/Search';
import styles from './styles.module.css';
// AL custom ==> Start
import {Helmet} from "react-helmet";
import { useLocation } from 'react-router-dom';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
// AL custom ==> End
function useNavbarItems() {
  // TODO temporary casting until ThemeConfig type is improved
  return useThemeConfig().navbar.items;
}
function NavbarItems({items}) {
  return (
    <>
      {items.map((item, i) => (
        <NavbarItem {...item} key={i} />
      ))}
    </>
  );
}
function NavbarContentLayout({left, right}) {
  return (
    <div className="navbar__inner">
      <div className="navbar__items">{left}</div>
      <div className="navbar__items navbar__items--right">{right}</div>
    </div>
  );
}
export default function NavbarContent() {
  // AL custom ==> Start
  const {siteConfig} = useDocusaurusContext();
  const baseUrl = siteConfig.baseUrl
  const isLandingPage = baseUrl == useLocation().pathname;
  // AL custom ==> End
  const mobileSidebar = useNavbarMobileSidebar();
  const items = useNavbarItems();
  const [leftItems, rightItems] = splitNavbarItems(items);
  const searchBarItem = items.find((item) => item.type === 'search');
  return (
    <NavbarContentLayout
      left={
        // TODO stop hardcoding items?
        <>
          {!mobileSidebar.disabled && <NavbarMobileSidebarToggle />}
          <NavbarLogo />
          <NavbarItems items={leftItems} />
        </>
      }
      right={
        // TODO stop hardcoding items?
        // Ask the user to add the respective navbar items => more flexible
        <>
          <NavbarItems items={rightItems} />
          {/* AL custom ==> Start (replace <NavbarColorModeToggle className={styles.colorModeToggle} />) */}
          {isLandingPage && (
            <NavbarColorModeToggle className={styles.colorModeToggle} />
          )}
          {/* Load search custom CSS when not on landing page */}
          {!isLandingPage && (
            <Helmet link={
                [{"rel": "stylesheet", type:"text/css", "href": baseUrl + "css/navbar_search.css"}]
            }/>
          )}
          {/* AL custom ==> End */}
          {!searchBarItem && (
            <NavbarSearch>
              {/* AL custom ==> Start (replace <SearchBar />) */}
              {!isLandingPage && <SearchBar />}
              {/* AL custom ==> End */}
            </NavbarSearch>
          )}
        </>
      }
    />
  );
}
