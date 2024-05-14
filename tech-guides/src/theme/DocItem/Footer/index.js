// AL custom ==> Start
import React, {useState} from "react";
// Replace line: "import React from 'react';"
// AL custom ==> End
import clsx from 'clsx';
import {ThemeClassNames} from '@docusaurus/theme-common';
import {useDoc} from '@docusaurus/theme-common/internal';
import LastUpdated from '@theme/LastUpdated';
import EditThisPage from '@theme/EditThisPage';
import TagsListInline from '@theme/TagsListInline';
import styles from './styles.module.css';
// AL custom ==> Start
import BrowserOnly from '@docusaurus/BrowserOnly';
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import ReactGA from "react-ga4";
import { useLocation } from "react-router-dom";
import IconEmailLink  from "../../../components/Icon/EmailLink";

const SdEmails = require("../../../../config/service_desk_address.json");
// AL custom ==> End
function TagsRow(props) {
  return (
    <div
      className={clsx(
        ThemeClassNames.docs.docFooterTagsRow,
        'row margin-bottom--sm',//const docPath = useLocation().pathname.replace(/\/$/, "/")
      )}>
      <div className="col">
        <TagsListInline {...props} />
      </div>
    </div>
  );
}
function EditMetaRow({
  editUrl,
  lastUpdatedAt,
  lastUpdatedBy,
  formattedLastUpdatedAt,
}) {
  return (
    <div className={clsx(ThemeClassNames.docs.docFooterEditMetaRow, 'row')}>
      <div className="col">{editUrl && <EditThisPage editUrl={editUrl} />}</div>

      <div className={clsx('col', styles.lastUpdated)}>
        {(lastUpdatedAt || lastUpdatedBy) && (
          <LastUpdated
            lastUpdatedAt={lastUpdatedAt}
            formattedLastUpdatedAt={formattedLastUpdatedAt}
            lastUpdatedBy={lastUpdatedBy}
          />
        )}
      </div>
    </div>
  );
}
// AL custom ==> Start
function OpenIssueRow({ emailLink }) {
  return (
    <div className={clsx(ThemeClassNames.docs.docFooterEditMetaRow, 'row')}>
      <div className="col"><a target="_blank" href={emailLink}><IconEmailLink/>Report an issue</a></div>
    </div>
  );
}
// AL custom ==> End
export default function DocItemFooter() {
  const {metadata} = useDoc();
  const {editUrl, lastUpdatedAt, formattedLastUpdatedAt, lastUpdatedBy, tags} =
    metadata;
  const canDisplayTagsRow = tags.length > 0;
  const canDisplayEditMetaRow = !!(editUrl || lastUpdatedAt || lastUpdatedBy);
  const canDisplayFooter = canDisplayTagsRow || canDisplayEditMetaRow;
  // AL custom ==> Start
  const context = useDocusaurusContext();
  const { siteConfig = {} } = context;
  const trackingId = siteConfig.presets[0][1].gtag.trackingID;
  ReactGA.initialize(trackingId);
  const docPath = useLocation().pathname
  const [rateDescription, setRateDescription] = useState('');
  const [docRating, setDocRating] = useState(null);
  function getDocVersion(metadata, lastUpdatedAt) {
    // Force frontMatter.doc_version to string in case of a date otherwise value will be like 2022-07-28T00:00:00.000Z
    // TODO doc_version better handling
    if (metadata.frontMatter.hasOwnProperty('doc_version')) {
      if (!isNaN(new Date(metadata.frontMatter.doc_version).getDate())) {
        return new Date(metadata.frontMatter.doc_version).toISOString().substring(0, 10).toString()
      } else {
        return metadata.frontMatter.doc_version.toString();
      }
    } else {
      try {
        return lastUpdatedAt.toString();
      } catch (error) {
        return 'NA'
      }
    }
  }
  const docVersion = getDocVersion(metadata, lastUpdatedAt);
  const isoDate = new Date().toISOString().substring(0, 10)
  const eventRate = (category, action, label, value) => {
    if (docRating == null) {
      ReactGA.event({
        category: category,
        action: action,
        label: label,
        value: parseInt(value),
      });
      setRateDescription('Thank you for your feedback!');
      setDocRating(value);
      localStorage.setItem('rating:' + docPath, value + '|' + label + '|' + isoDate);
    }
  };
  function loadRating() {
    let rateData = localStorage.getItem('rating:' + docPath);
    if (rateData !== null) {
      // Cookie content: rateValue|rateVersion|rateDate
      let [rateValue, rateVersion, rateDate] = rateData.split('|');
      let rateDateReset = new Date(rateDate)
      rateDateReset.setDate(rateDateReset.getDate() + 7); // Can rate again after 7 days
      // TODO remove old entries every month (see explanations below)
        // --> Execute on landing page
        // --> Use cookie last clean reference
        // --> Generate at build a json file with all keys
        // --> Compare and remove non existing keys from the local storage
      if ((new Date > rateDateReset) && (rateVersion == 'undefined')) {
          // No doc_version stored, use 7 days rule. Vote date is reached, user can vote
          // The rateDateReset condition is true
          rateData = null;
      } else if ((rateVersion !== docVersion) && (rateVersion !== 'undefined')) {
        // doc_version has changed, user can vote
        rateData = null;
      } else {
        // User has already voted
        setDocRating(rateValue);
        setRateDescription('Thank you for your feedback!');
      }
    } else {
      setRateDescription('Rate this article');
    }
  }
  if (process.env.NODE_ENV === 'development') {
    console.log('docPath:                           ' + docPath);
    console.log('docVersion:                        ' + docVersion);
    if (typeof rateData !== 'undefined') {
      console.log('rateData:                          ' + rateData);
      console.log('rateValue:                         ' + rateValue);
      console.log('rateVersion:                       ' + rateVersion);
      console.log('rateDate:                          ' + rateDate);
      console.log('rateDateReset:                     ' + rateDateReset);
    }
    console.log('metadata.frontMatter.doc_version:  ' + metadata.frontMatter.doc_version);
  }
  // Email link start
  const [docSlug, emailAddress] = (function findEmails(docPath) {
    // Return project service desk email address according to file slug from service_desk_address.json
    let slug = docPath.split("/").slice(2, 4).join("/");
    if (process.env.NODE_ENV === 'development') {
      console.log('docPath:       ' + docPath);
      console.log('slug:          ' + slug);
    }
    if (SdEmails[slug] == undefined) {
      slug = docPath.split("/").slice(2, 3)[0];
      if (SdEmails[slug] == undefined) {
        if (process.env.NODE_ENV === 'development') {
          console.log("warning: no email address match for " + docPath);
        }
        return [slug, null];
      }
    }
    return [slug, SdEmails[slug]];
  })(docPath);
  const emailSubject = "Issue on " + docPath;
  const emailBody = "Url: " + siteConfig.url + docPath + "%0D%0APage: " + docPath + "%0D%0A%0D%0A";
  const emailLink = "mailto:" + emailAddress + "?subject=" + emailSubject + "&body=" + emailBody;
  if (process.env.NODE_ENV === 'development') {
    console.log('base url:      ' + siteConfig.url)
    console.log('docSlug:       ' + docSlug);
    console.log('emailAddress:  ' + emailAddress);
    console.log('emailSubject:  ' + emailSubject);
    console.log('emailBody:     ' + emailBody);
    console.log('emailLink:     ' + emailLink);
  }
  // Email link end
  // AL custom ==> End
  if (!canDisplayFooter) {
    return null;
  }
  return (
    <footer
      className={clsx(ThemeClassNames.docs.docFooter, 'docusaurus-mt-lg')}>
      {canDisplayTagsRow && <TagsRow tags={tags} />}
      {/* // AL custom ==> Start */}
      {emailAddress && (
        <OpenIssueRow
          emailLink={emailLink}
        />
      )}
      {/* // AL custom ==> End */}
      {canDisplayEditMetaRow && (
        <EditMetaRow
          editUrl={editUrl}
          lastUpdatedAt={lastUpdatedAt}
          lastUpdatedBy={lastUpdatedBy}
          formattedLastUpdatedAt={formattedLastUpdatedAt}
        />
      )}
      {/* // AL custom ==> Start */}
      <BrowserOnly>
        {() => loadRating()}
      </BrowserOnly>
      <div className={styles.doc_footerEmoji}>
        <span
          className={styles.emoji}
          id={docRating == '1' ? styles.emoji_click: null}
          onClick={eventRate.bind(this, "Doc", "Rate", docVersion, 1)}
        >
          &#128531;
        </span>
        <span
          className={styles.emoji}
          id={docRating == '2' ? styles.emoji_click: null}
          onClick={eventRate.bind(this, "Doc", "Rate", docVersion, 2)}
        >
          &#128550;
        </span>
        <span
          className={styles.emoji}
          id={docRating == '3' ? styles.emoji_click: null}
          onClick={eventRate.bind(this, "Doc", "Rate", docVersion, 3)}
        >
          &#128578;
        </span>
        <span
          className={styles.emoji}
          id={docRating == '4' ? styles.emoji_click: null}
          onClick={eventRate.bind(this, "Doc", "Rate", docVersion, 4)}
        >
          &#128515;
        </span>
        <span
          className={styles.emoji}
          id={docRating == '5' ? styles.emoji_click: null}
          onClick={eventRate.bind(this, "Doc", "Rate", docVersion, 5)}
        >
          &#128525;
        </span>
        <div className={styles.doc_footerEmojiText}>{rateDescription}</div>
      </div>
      {/* // AL custom ==> End */}
    </footer>
  );
}
