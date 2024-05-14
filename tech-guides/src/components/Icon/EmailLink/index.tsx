import React from 'react';
import styles from './styles.module.css';

export default function IconEmailLink({
  className,
  ...restProps
}): JSX.Element {
  return (
    <svg
      fill="currentColor"
      height="20"
      width="20"
      viewBox="0 0 40 40"
      fill-rule="evenodd"
      clip-rule="evenodd"
      className={styles.iconEmailLink}
      {...restProps}>
      <g>
        <path d="M5 9.7C5 8.8 5.8 8.1 6.7 8.1H33.3C34.3 8.1 35 8.8 35 9.7V28.6C35 30.4 33.5 31.9 31.7 31.9H8.3C6.5 31.9 5 30.4 5 28.6V10.3C5 10.2 5 10.1 5 10V9.7ZM8.3 13.4V28.6H31.7V13.4L23.5 21.6C21.6 23.5 18.4 23.5 16.5 21.6L8.3 13.4ZM11 11.3H29L21.2 19.2C20.5 19.9 19.5 19.9 18.8 19.2L11 11.3Z" />
      </g>
    </svg>
  );
}
