/*
  Copyright (C) L'Air Liquide S.A. 2023
  No license. All rights reserved.
*/

import React from "react";
import Select from "react-select";
import { RouteComponentProps, withRouter } from "react-router-dom";
import styles from "./styles.module.css";

class DropDown<P> extends React.Component<P & RouteComponentProps, {}> {}

interface DropDownProps extends RouteComponentProps {
  name: string;
  versions: any;
}

class Header extends DropDown<DropDownProps> {
  render() {
    const { history } = this.props;
    const page = this.props.name;
    const options = this.props.versions[page];
    const { pathname } = this.props.location;
    const pagename = pathname
      .replace(/\/$/, "")
      .slice(pathname.replace(/\/$/, "").lastIndexOf("/") + 1);
    /*
      Keep only pagename from pathname for example:
        pathname = /docs/test/ningines/interface-1-3/
        pagename = interface-1-3
    */
    const defaultValue = {
      ...options.filter((item) => item.value === pagename),
    };
    // Select value and label from options

    return (
      <Content
        options={options}
        onChange={(opt) => {
          history.push("../" + opt.value + "/");
        }}
        defaultValue={defaultValue[0]}
      />
    );
  }
}

function isArray<T>(arg: unknown): arg is readonly T[] {
  return Array.isArray(arg);
}

interface Change {
  value: string;
  label: string;
}

interface ContentProps {
  readonly options: any;
  readonly onChange: (option: Change) => void;
  readonly defaultValue: any;
}

const Content = ({ options, onChange, defaultValue }: ContentProps) => (
  <div className={styles.versionDropDownContainer}>
    <div className={styles.versionDropDown}>
      <Select
        classNamePrefix="react-select"
        styles={{
          control: (base, state) => ({
            ...base,
            backgroundColor: "var(--vdd-color-control-background)",
          }),
          singleValue: (base, state) => ({
            ...base,
            color: "var(--vdd-color-singleValue-text)",
          }),
          menu: (base, state) => ({
            ...base,
            backgroundColor: "var(--vdd-color-menu-background)",
          }),
          option: (base, state) => ({
            ...base,
            backgroundColor: state.isSelected
              ? "var(--vdd-color-option-background-selected)"
              : state.isFocused
              ? "var(--vdd-color-option-background-focus)"
              : "var(--vdd-color-option-background-default)",
            color: state.isSelected
              ? "var(--vdd-color-option-text-default-selected)"
              : state.isFocused
              ? "var(--vdd-color-option-text-default-focus)"
              : "var(--vdd-color-option-text-default)",
            ":hover": {
              backgroundColor: "var(--vdd-color-option-background-hover)",
              color: "var(--vdd-color-option-text-hover)",
            },
          }),
        }}
        isSearchable={false}
        options={options}
        onChange={(option) => {
          if (option && !isArray(option)) {
            onChange(option);
          }
        }}
        defaultValue={defaultValue}
      />
    </div>
  </div>
);

export default withRouter(Header);
