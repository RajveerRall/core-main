import React from 'react';
import {useThemeConfig} from '@docusaurus/theme-common';
import FooterLinks from '@theme/Footer/Links';
import FooterLogo from '@theme/Footer/Logo';
import FooterCopyright from '@theme/Footer/Copyright';
import FooterLayout from '@theme/Footer/Layout';
// AL custom ==> Start
import { useLocation } from "react-router-dom";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
// AL custom ==> End
function Footer() {
  const {footer} = useThemeConfig();
  // AL custom ==> Start
  const { siteConfig } = useDocusaurusContext();
  let isLandingPage = siteConfig.baseUrl == useLocation().pathname;
  // AL custom ==> End
  if (!footer) {
    return null;
  }
  const {copyright, links, logo, style} = footer;
  // AL custom ==> Start
  if (isLandingPage) {
    return null;
  }
  // AL custom ==> End
  return (
    <FooterLayout
      style={style}
      links={links && links.length > 0 && <FooterLinks links={links} />}
      logo={logo && <FooterLogo logo={logo} />}
      copyright={copyright && <FooterCopyright copyright={copyright} />}
    />
  );
}
export default React.memo(Footer);
