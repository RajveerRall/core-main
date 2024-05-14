---
title: Links and images
sidebar_label: Links and images
doc_version: 2022-08-26
---

:::info

This a test page for links and images

:::

## Folder redirect

Click on this `[link](#folder-redirect)` then refresh the page, watch URL for any trailing slash change.

## Links

| Name                                   | Written                                                    | Excepted | Test                                                     |
| -------------------------------------- | ---------------------------------------------------------- | -------- | -------------------------------------------------------- |
| Relative link to index.md              | `[Test](../Test%20index-01/index.md)`                      | NA       | [Test](../Test%20index-01/index.md)                      |
| Relative link to `folder name`.md      | `[Test](../Test%20index-02/Test%20index-02.md)`            | NA       | [Test](../Test%20index-02/Test%20index-02.md)            |
| Relative link with trailing /          | `[Test](../Test%20index-01/)`                              | NA       | [Test](../Test%20index-01/)                              |
| Relative link without trailing /       | `[Test](../Test%20index-01)`                               | NA       | [Test](../Test%20index-01)                              |
| External link                          | `[Test](https://www.google.com)`                           | NA       | [Test](https://www.google.com)                           |
| HTML Relative link to index.md         | `<a href="../Test%20index-01/index.md">Test</a>`           | NA       | <a href="../Test%20index-01/index.md">Test</a>           |
| HTML Relative link to `folder name`.md | `<a href="../Test%20index-02/Test%20index-02.md">Test</a>` | NA       | <a href="../Test%20index-02/Test%20index-02.md">Test</a> |
| HTML Relative link with trailing /     | `<a href="../Test%20index-01/">Test</a>`                   | NA       | <a href="../Test%20index-01/">Test</a>                   |
| HTML Relative link without trailing /  | `<a href="../Test%20index-01">Test</a>`                    | NA       | <a href="../Test%20index-01">Test</a>                    |
| HTML External link                     | `<a href="http://www.google.com">Test</a>`                 | NA       | <a href="http://www.google.com">Test</a>                 |

## Images

TBC

<img
  src="img/valid.png"
  alt="Test"
  title="Test" />

```md
![banner](pathname:///img/knowledge/docusaurus-asset-example-banner.png)
```

This link will be generated as `<img src="/img/knowledge/docusaurus-asset-example-banner.png" alt="banner" />`, without any processing or file existence checking.
