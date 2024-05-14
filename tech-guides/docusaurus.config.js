const editUrls = require("./config/edit_url.json");
const simplePlantUML = [require("@akebifiky/remark-simple-plantuml"), { baseUrl: "https://plantuml.apps.airliquide.com/svg" }];

async function createConfig() {
  const gfm = (await import('remark-gfm')).default;
  const rehypeExternalLinks = (await import('rehype-external-links')).default;
  const mdxMermaid = (await import('mdx-mermaid')).default;

  return {
    title: "Technical Guides",
    tagline: "Get started with GIO services",
    url: "http://localhost:3000",
    baseUrl: "/",
    trailingSlash: true,
    onBrokenLinks: "throw",
    onBrokenMarkdownLinks: "throw",
    onDuplicateRoutes: "throw",
    favicon: "img/favicon.ico",
    organizationName: "Air Liquide",
    plugins: [
      // The debug plugin is enabled automatically for development build (when using the yarn start command)
      [require.resolve("docusaurus-plugin-sass"),{}],
      [
        require.resolve("@easyops-cn/docusaurus-search-local"),
        {
          hashed: true,
          language: ["en"],
          blogRouteBasePath: "/news",
          blogDir: "news",
        },
      ],
    ],
    themeConfig: {
      colorMode: {
        defaultMode: "light",
      },
      prism: {
        additionalLanguages: ['powershell', 'regex', 'log', 'hcl', 'mermaid', 'plant-uml'],
      },
      docs: {
        sidebar: {
          autoCollapseCategories: true,
          hideable: true,
        },
      },
      navbar: {
        title: "Tech Guides",
        logo: {
          alt: "Tech Guides",
          src: "img/favicon.ico",
        },
        items: [
          {
            label: "Cloud",
            position: "left",
            items: [
              {
                label: "AWS",
                to: "docs/cs/aws/",
              },
              {
                label: "Azure",
                to: "docs/cs/azure/",
              },
              {
                label: "GCP",
                to: "docs/cs/gcp/",
              },
              {
                label: "Managed Solutions",
                to: "docs/cs/managed-solutions/",
              },
              {
                label: "Community",
                to: "docs/cs/community/",
              }
            ],
          },
          {
            label: "Products",
            position: "left",
            items: [
              {
                label: "Software Factory",
                to: "docs/cs/sf/offering/",
              },
              {
                label: "NinGines",
                to: "docs/cs/ningines/quick-start/",
              }
            ],
          },
          {
            label: "Handbook",
            position: "left",
            items: [
              {
                label: "Cloud Services",
                to: "docs/cs/handbook/",
              },
            ],
          },
        ],
        hideOnScroll: true,
      },
      footer: {
        style: "light",
        logo: {
          alt: "Logo",
          src: "img/common/air_liquide_logo_1.png",
          height: 30,
        },
        copyright: `Copyright © ${new Date().getFullYear()} — L'Air Liquide S.A.`,
      },
    },
    presets: [
      [
        "@docusaurus/preset-classic",
        {
          docs: {
            remarkPlugins: [
              gfm,
              mdxMermaid,
              simplePlantUML
            ],
            rehypePlugins: [
              [rehypeExternalLinks, {
                rel: ["nofollow"],
                target: ["_blank"],
                content: [
                  {
                    type: 'element',
                    tagName: 'i',
                    properties: {
                      className: ['fa-solid', 'fa-arrow-up-right-from-square', 'spacer_left'],
                    },
                    children: []
                  }
                ],
              }]
            ],
            sidebarPath: require.resolve("./sidebars.js"),
            showLastUpdateTime: true,
            editUrl: function ({ docPath }) {
              // Return edit_url according to file slug from edit_url.json
              let slug = docPath.split("/").slice(0, 1).join("/");
              if (editUrls[slug] == undefined) {
                return null;
              }
              return editUrls[slug] + "docs" + docPath.substr(slug.length);
            },
          },
          blog: {
            showReadingTime: false,
            path: "news",
            blogTitle: "news",
            blogSidebarCount: 8,
            blogSidebarTitle: "Recent news",
            routeBasePath: "news",
            feedOptions: {
              type: "all",
              copyright: `Copyright © ${new Date().getFullYear()} L'Air Liquide`,
              language: "en",
            },
          },
          theme: {
            customCss: [
              require.resolve("./src/css/bootstrap.scss"),
              require.resolve("./src/css/custom.css")
            ],
          },
          gtag: {
            trackingID: "G-EMXP6978NM",
            anonymizeIP: true,
          },
        },
      ],
    ],
    i18n: {
      defaultLocale: "en",
      locales: ["en"],
      localeConfigs: {
        en: {
          label: "English",
          direction: "ltr",
        },
      },
    },
    stylesheets: [
      "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.2/css/all.min.css",
    ],
  };
}

module.exports = createConfig;
