# Documentation server

Build and publish the Tech-Guides documentation.

## Build Tech-Guides

### Prerequisites
- Administrator permission (required for Node.js installation and configuration)
- Git v2.25+
- Node.js 16 LTS (16.14+)
  - Run `corepack disable` (Windows only, administrator permission required)
- Yarn
  - `npm install --location=global yarn`
- Python 3 (remember to disable App Execution Aliases in Windows settings)
- Clone this repository
- On Windows, use `Git Bash` to execute bash scripts

#### Initialize submodules
Required only if you plan to edit documentation locally without using the `build.bash` script (see below) of building the Tech-Guides website locally.
- `git submodule update --init`

### Tech-Guides build `[LOCAL]`
- `cd tools`
- `./build.bash`

### Tech-Guides serve for local test `[LOCAL]`
- `cd tools`
- `./serve.bash`

### Build.bash

The `build.bash` script performs all required actions to build the Tech-Guides website.  
It is compatible with Windows, MacOS and Linux.  

It checks the version between `package.json` and `.installed_version.txt`, if mismatch, the `install` action forcefully runs.

### Usage

`./build.bash "<action1,action2,action...>" "<build_mode>"`

### Options

| Action          | Description                                                                                                                    |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| install         | Force Tech-Guides installation<br/>Check prerequisites and dependencies, equivalent to `install,clear,prepare,pull,copy,build` |
| clear           | Clear cached elements                                                                                                          |
| prepare         | Update news and landing page content                                                                                           |
| pull            | Init and checkout submodules on production commit ID                                                                           |
| test            | Use test documentation only                                                                                                    |
| copy `default`  | Copy docs and images from submodule to tech-guides site<br/>Update slug, links and images path in docs                         |
| build `default` | Build tech-guides                                                                                                              |

| Build mode        | Description            |
| ----------------- | ---------------------- |
| production        | Enable all features    |
| preview `default` | Skip last updated date |

### Additional configuration

#### Disable SSL inspection

To accept MITM certificate from Zscaler, the `build.bash` script executes the following configuration commands:
- `npm config set strict-ssl false`
- `yarn config set strict-ssl false`

## Update and maintain documentation
- Create a new issue and merge request on the documentation project
- In core, cd docs/`<submodule>`
- git checkout on the newly created branch on the documentation project
- Work in submodule as a normal git repository
- Test changes locally
  - `cd tools`
  - `./build.bash`
  - `./serve.bash`

### Frontmatter
Use the Tech-Guides custom tag to get voting results grouped per `doc_version`.

> doc_version: "2022-01-12" `prefered format`  
> doc_version: "v1.2.3"

## Docusaurus upgrade

> Tech-Guides is build with [Docusaurus](https://docusaurus.io/).

- Clone repository (remember to create a new issue, merge request and branch)
- `cd tech-guides`
- `yarn install`
- `yarn up @docusaurus/core @docusaurus/plugin-debug @docusaurus/plugin-google-gtag @docusaurus/preset-classic @docusaurus/utils @docusaurus/module-type-aliases` ...and any module dependencies available in `package.json`
- Check if any [swizzle](#swizzle-theme-components) theme components update is required (found in `tech-guides\src\theme`)
- Update [Tech-Guides version](#tech-guides-version)

> Following packages are direct Docusaurus dependencies and should not be updated to latest version:  
> `@mdx-js/react`  
> `clsx`  
> `prism-react-renderer`  
> `react`  
> `react-dom`  

### Error while upgrading due to dependencies

In case of uncorrectable error with dependencies, you can apply the following:
- Create an empty folder
- Run command `yarn create docusaurus`
- Select the `classic` theme
- Respond `no` to `Do you want to use the TS variant?`
- Use `package.json` from `tech-guides` as a reference and add missing dependency using `yarn add <dependency_name_1> <dependency_name_2> <dependency_name_3>`
- Replace `package.json` from `tech-guides` with the new `package.json`
- Replace `yarn.lock` from the `tech-guides` folder with the new `yarn.lock`
- In the `tech-guides` folder, run the `yarn install` command
- Check if any swizzle theme components update is required (found in `tech-guides\src\theme`)

### Tech-Guides version

After any Docusaurus update or yarn package installation/removal, it's **mandatory** to update the `version` in `package.json`

## Swizzle theme components

Tech-Guides uses updated theme components, to maintain custom features.  
It is **mandatory** to swizzle components and update with `AL custom` code.

### Prerequisites
- `cd tools`
- `./build.bash "install,prepare"`

### Swizzle

> Already swizzle theme components are located in `tech-guides\src\theme`)

- Rename `theme` folders in `tech-guides\src\` to `theme_`
- cd tech-guides

> Perform swizzle operation for all component in `theme_` (for example `DocItem/Footer`)  
> Compare and merge to ensure there is no regression prior merging to main.  
> Remember to remove renamed `theme_` folders in `tech-guides\src\`.
  
> If `yarn swizzle` menu is not working in `gitbash`, `yarn swizzle` command can be executed in standard `cmd` prompt.

- Swizzle theme component
  - For Theme
    - `yarn swizzle @docusaurus/theme-classic`
  - For SearchBar (not working)
    - `yarn swizzle @easyops-cn/docusaurus-search-local`
  - Select any component that has already been swizzle
  - Which swizzle action do you want to do? `Eject` (use `Warp` for `DocSidebarItem`)
  - For `Unsafe` components
    - Do you really want to swizzle this unsafe internal component? `YES: I know what I am doing!`
- In `theme_`, search for code labeled `AL custom` and insert it into freshly swizzle components
  - Use compare feature in VSCode, to ensure all custom code is added
  - In swizzle components, any new code lines from Docusaurus should be kept when applying `AL custom` modifications
- Delete the `theme_` folder

> The `Footer/Copyright`, `Footer/Layout`, `Footer/LinkItem`, `Footer/Links` and `Footer/Logo` themes are left intact and can be safely removed from `src/theme`.

### Tests

#### Build

- `build.bash`
  - New version detection install tech-guides automatically
    - Can be tested by changing the version in `tech-guides/.installed_version.txt` and deleting the file

#### Hotfix and Workaround

##### Workaround

Due to swizzle not working for `@easyops-cn/docusaurus-search-local` a workaround is implemented in the `build.bash` script (see workaround comment).

##### Hotfix

The Search hotfix for `@easyops-cn/docusaurus-search-local v0.32` is removed since `Tech-Guides v1.3.0` from the `build.bash` script.

#### Landing page

- Search
  - Results are working
  - Verify you have a result for the `permissions boundary` search
- Left menu
  - Is present
  - Is well positioned
- Cards
  - Are loading and well positioned
- Theme
  - White and dark themes are displayed properly
- Cards slider
  - If multiple cards are not in use, in `tech-guides/data/cards.json` add a new object in `cards > pages`
  - The position and size of the left and right buttons are well positioned
  - Click on the left and right buttons are working
  - Click on page bullet is working
  - Drag sliding is working
- News
  - Are loading properly when scrolling down
- News bullet indicator
  - Enter in Chrome developer mode (F12) > Application tab > Storage > Cookies > `https://localhost:3000`
  - Update the `news` cookie with a date more in the past
  - A bullet appears when there is a new news
  - Slowly scroll to the news section, the bullet indicator should disappear
- Animated bottom links
  - Stop on mouse hover
  - Links are working

#### Doc item

- Search
  - On the mouse, click the search box is enlarging
  - Results are working
  - Verify you have a result for the `permissions boundary` search
- Mailto link
  - Are working
    - Ensure Chrome is selected in The Windows Control panel Default Email app
    - Chrome settings > Privacy and security > Site settings > Additional permissions > Protocol handler > Remove `mail.google.com` from unauthorized mail handler
    - Go to `mail.google.com`
    - Click on the handler button located at the right in the URL bar and click `authorize`
- Edit this page link
  - Open the correct document in GitLab
- Rating
  - Click on an emoji (`Thank you for your feedback` is displayed)
  - Refresh the page, emoji is still selected
- Footer
  - Has the Air Liquide logo and copyright
  - The size of the Air Liquide logo is correct

#### Responsive

All tests should be executed in desktop and responsive mode

- Desktop, test in standard and large resolution
  - Enter in Chrome developer mode (F12) > Toggle device toolbar (ctrl shift m) and test different screen wide
  - Compare with the live tech-guides website to ensure everything is displayed properly

#### Search

Search results must be tested again in the build done by the pipeline (when working on a branch).

> Verify you have a result for `permissions boundary` search

> Note: In the past we had issues on search on long path slugs

#### Bugfix

When a test fails, some development is required in Tech-Guides in react component and/or CSS.

### Pipeline
#### Service accounts
- `svc_techguides`
  - Have read-write access to the `core` project
  - Is used to create `pipeline triggers` tokens

#### Token
WIP

### Cache

The cache is enabled for the [`public`](#public-folder) (GitLab pages folder).  
The `public` folder cache is shared with all branches.

For core project:
- `yarn` and `node_modules` folders are cached and **separated** per branch

> The option `Use separate caches for protected branches` **must** enabled for the Tech-Guides core project.

For documentation projects:
- `yarn` and `node_modules` folders are cached and **shared** with all branches

> The option `Use separate caches for protected branches` **must** be disabled for all Tech-Guides documentation projects.

### Public folder

For core project:
- `public/` => for the `main` branch
- `public/branch/<branch_name>/` => for any feature branch

For documentation projects:
- `public/` => for the `main` branch
- `public/branch/<branch_name>/` => for any feature branch
- `public/fork/<internal_merge_request_id>-<branch_name>/` => for any fork (only when the creator of the merge_request have write permissions on the documentation project)

For forked projects:
- `public/` => for the `main` branch
- `public/branch/<branch_name>/` => for any feature branch

### Triggered configuration update
WIP

### Development
WIP

### Workflow rules
WIP

#### Resource group

To maintain Tech-Guides consistency, `update:config` and `publish` jobs using a `resource_group`.  
It limits to one the number of parallel jobs.
Once the `resource_group` is created (when the pipeline is run for the first time), it must be configured using GitLab API:
```cmd
curl --request PUT --header "PRIVATE-TOKEN: <your_access_token>" "https://git.apps.airliquide.com/api/v4/projects/<project_id>/resource_groups/publish" --data "process_mode=oldest_first"`
```

> It applies to all Tech-Guides projects.

## New documentation project

### Overview

1. Create a new GitLab project in the [tech-guides group](https://git.apps.airliquide.com/GIO/tech-guides)
   1. [Create initial files](#initial-repository-files)
1. Create a new pipeline [trigger token](#trigger-token)
1. Configure [project settings](#project-configuration)
1. One the Tech-Guides `core` project, create a new issue + branch + merge request
   1. On the [Tech-Guides Core project](https://git.apps.airliquide.com/GIO/tech-guides/core) [create a new entry](#core_configyml) in the `core_config.yml`
   1. [Register the new doc project as a submodule](#add-submodule)
1. [Configure the resource group](#resource-group-configuration)

### Initial repository files

`.gitignore`
```txt
.DS_Store
```

`.gitlab-ci.yml`
```yml
include:
  - project: GIO/tech-guides/core
    ref: main
    file: .ci/client.yml

variables:
  CLIENT_PROJECT_ID: "<PROJECT_ID>"
```

`docs/demo/docs/demo/01-demo.md`
```md
---
displayed_sidebar: null
title: Demo
doc_version: 2022-12-04
---

Demo file : to be deleted.
```

[`static/img/demo/docusaurus.png`](https://git.apps.airliquide.com/GIO/tech-guides/security/-/blob/b8b159d703990c975b54c8fdc51590626d55f21d/static/img/demo/docusaurus.png)

### Trigger Token

Create a new [pipeline trigger token](https://git.apps.airliquide.com/GIO/tech-guides/core/-/settings/ci_cd) on the Tech-Guides `core` project as `svc_techguides`service account.

- Token name: `ProjectID_<PROJECT_ID>`

> The service account `svc_techguides` **must** create this pipeline trigger token.

### Project configuration

- In Settings > General > Visibility, project features, permissions
  - Set the `Project visibility` to public
- In Settings > General > Service Desk
  - Set the Service Desk > Email display name to `Tech-Guides Support Bot`
- In Settings > General > Integrations (optional)
  - Add Google Chat integration (create a new space for the project named `Tech-Guides notifications [<UPPERCASE PROJECT SLUG>]`) with:
    - Issue
    - Confidential issue
    - Pipeline
    - Webhook (fill with the Google Chat incoming webhook, named Tech-Guides, Logo URL `https://raw.githubusercontent.com/facebook/docusaurus/main/website/static/img/docusaurus.png`)
    - Notify only broken pipelines (default branch)
- In Settings > Repository > Protected branches
  - Protect the main branch with:
    - Allowed to merge > Maintainers
    - Allowed to push and merge > No one
    - Allowed to force push > Off
- In Settings > Merge requests
  - Squash commits when merging > Encourage
  - Merge checks
    - [x] Pipelines must succeed
      - [ ] Skipped pipelines are considered successful
    - [ ] All threads must be resolved
- In Settings > CI/CD > General pipelines
  - [x] Public pipelines
  - [x] Auto-cancel redundant pipelines
  - [x] Prevent outdated deployment jobs
  - [ ] Use separate caches for protected branches
- Variables
  - TOKEN_CORE_TRIGGER
    - Value: Token created on the `core` project
    - [ ] Protect variable
    - [x] Mask variable
    - [x] Expand variable reference

### core_config.yml

Create a new entry as follow:
```yml
project_<PROJECT_ID>:
  ref: main
  name: <NAME>
  description: <DESCRIPTION>
  submodule: <SUBMODULE SLUG>
  sidebar:
    type: autogenerated
    level: 1
  enable: true
  cache:
    http_url_to_repo: <HTTP_URL_TO_REPO>
    edit_url: <EDIT_URL>
    service_desk_address: <SERVICE_DESK_ADDRESS>
```

The `ref` will be updated automatically by the next triggered pipeline for this project from `main` to a valid commit SHA.  

> Keep the submodule slug short as it is part of the documentation URL.

### Add submodule

On the Tech-Guides `core` project, add the new documentation project as submodule using the following command:
`git submodule add <DOC_PROJECT_URL> <docs/<SUBMODULE SLUG>`

### Resource group configuration

To maintain Tech-Guides consistency, `update:config` and `publish` jobs using a `resource_group`.  
It limits to one the number of parallel jobs.
Once the `resource_group` is created (when the pipeline is run for the first time), it must be configured using GitLab API:
```cmd
curl --request PUT --header "PRIVATE-TOKEN: <your_access_token>" "https://git.apps.airliquide.com/api/v4/projects/<project_id>/resource_groups/publish" --data "process_mode=oldest_first"`
```

> The pipeline must run successfully at least once before to create resource group.

## Landing Page update

WIP
