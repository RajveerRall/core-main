#!/usr/bin/env bash
ACTION=$1
BUILD=$2
URL=$3
BASE_URL=$4
PRODUCTION=$5
PIPELINE=$6
PROJECT_ID=$7
BRANCH=$8

# Set default values for local build
if [ -z "${ACTION}" ]; then
  ACTION="copy,build"
fi
IFS=',' read -r -a ARR_ACTION <<< "$ACTION"
if [[ "${ARR_ACTION[*]}" =~ "test" ]]; then
  TEST="true"
  # As we want to test update_docs.py script, including production section
  BUILD="production"
else
  TEST="false"
fi
if [[ "${ARR_ACTION[*]}" =~ "install" ]]; then
  INSTALL="true"
else
  INSTALL="false"
fi
if [ -z "${BUILD}" ]; then
  BUILD="preview"
fi
if [ -z "${URL}" ]; then
  URL="http://localhost:3000"
fi
if [ -z "${BASE_URL}" ]; then
  # Leading space needed: parameter handling workaround for Windows, will be trim in python
  BASE_URL=" /"
fi
if [ -z "${PRODUCTION}" ]; then
  PRODUCTION="false"
fi
if [ -z "${PIPELINE}" ]; then
  PIPELINE="false"
fi
if [ -z "${PROJECT_ID}" ]; then
  PROJECT_ID=""
fi
if [ -z "${BRANCH}" ]; then
  BRANCH=""
fi

# Minimum required version
PYTHON_VERSION="3"
NODE_VERSION="16.14"
GIT_VERSION="2.25"

# Version to install
YARN_VERSION="3.4.1"

function version { echo "$@" | awk -F. '{ printf("%d%03d%03d%03d\n", $1,$2,$3,$4); }'; }

if command -v python &>/dev/null; then
  PYTHON=python
elif command -v python3 &>/dev/null; then
  PYTHON=python3
fi


#################
# VERSION CHECK #
#################

TG_PACKAGE_VERSION=$(grep '"version":' ../tech-guides/package.json | cut -d'"' -f4)

if [ -f ../tech-guides/.installed_version.txt ]; then
  TG_INSTALLED_VERSION=$(cat ../tech-guides/.installed_version.txt)
  if [ "$TG_PACKAGE_VERSION" = "$TG_INSTALLED_VERSION" ]; then
    echo "Tech-Guides is up to date: $TG_PACKAGE_VERSION"
  else
    echo "New Tech-Guides version found: $TG_PACKAGE_VERSION != $TG_INSTALLED_VERSION"
    INSTALL="true"
  fi
else
  echo "No Tech-Guides installation found"
  INSTALL="true"
fi


################
# PREREQUISITE #
################

if [[ "${PIPELINE}" == "false" ]] && [[ "${INSTALL}" == "true" ]]; then
  if command -v "${PYTHON}" &>/dev/null; then
    BIN_VERSION=$(${PYTHON} -V | awk '{print $2}' | awk -F. '{print $1"."$2}')
    if [ "$(version "${BIN_VERSION}")" -ge "$(version "${PYTHON_VERSION}")" ]; then
      echo "Python is installed, version ${BIN_VERSION}"
    else
      echo "Error: Python version ${BIN_VERSION} is too low, need 3 or higher"
      exit 1
    fi
  else
    echo "Error: Python is not installed"
    exit 1
  fi

  # Check if pip is installed
  if ! command -v pip &>/dev/null; then
    echo "Error: pip is not installed"
    exit 1
  fi

  # Check if Node.js is installed and its version is 16.14 or higher
  if command -v node &>/dev/null; then
    BIN_VERSION=$(node -v | awk -Fv '{print $2}' | awk -F. '{print $1"."$2}')
    if [ "$(version "${BIN_VERSION}")" -ge "$(version "${NODE_VERSION}")" ]; then
      echo "Node.js is installed, version ${BIN_VERSION}"
    else
      echo "Error: Node.js version ${BIN_VERSION} is too low, need 16.14 or higher"
      exit 1
    fi
  else
    echo "Error: Node.js is not installed"
    exit 1
  fi

  # Check if Git is installed and its version is 2.25 or higher
  if command -v git &>/dev/null; then
    BIN_VERSION=$(git --version | awk '{print $3}' | awk -F. '{print $1"."$2}')
    if [ "$(version "${BIN_VERSION}")" -ge "$(version "${GIT_VERSION}")" ]; then
      echo "Git is installed, version ${BIN_VERSION}"
    else
      echo "Error: Git version ${BIN_VERSION} is too low, need 2.25 or higher"
      exit 1
    fi
  else
    echo "Error: Git is not installed"
    exit 1
  fi
fi


########
# INIT #
########

set -e

if [[ "${INSTALL}" == "true" ]]; then
  # Check if yarn is installed
  if command -v yarn &> /dev/null; then
    echo "Yarn is installed"
  else
    echo "Yarn is not installed. Installing now..."
    npm install --global yarn
  fi

  # Check if all Python requirements are installed
  TEMP_FILE=$(mktemp)
  pip freeze > "${TEMP_FILE}"
  while read -r REQUIREMENT; do
    if ! grep -iq "^${REQUIREMENT}\b" "${TEMP_FILE}"; then
      echo "Installing missing Python requirement: ${REQUIREMENT}"
      pip install ${REQUIREMENT}
    fi
  done < ../scripts/requirements.txt
  rm "${TEMP_FILE}"
  echo "All Python requirements are fulfilled"
fi


###########
# INSTALL #
###########

if [[ "${INSTALL}" == "true" ]]; then
  echo "Performing some cleaning, it may take a while"
  rm -rf "../tech-guides/.docusaurus"
  rm -rf "../tech-guides/build"
  rm -rf "../tech-guides/config"
  rm -rf "../tech-guides/data"
  rm -rf "../tech-guides/node_modules"
  rm -rf "../tech-guides/docs"
  rm -rf "../tech-guides/news"

  # if command -v corepack &>/dev/null; then
  #   echo "Disabling corepack"
  #   corepack disable
  # fi

  cd "../tech-guides/" || exit 1
  if [[ "${PIPELINE}" == "false" ]]; then
    npm config set strict-ssl false
    rm -f .yarnrc.yml
    echo "yarn config set strict-ssl false"
    yarn config set strict-ssl false
    echo "enableStrictSsl: false">>.yarnrc.yml
  fi

  YARN_VERSION=${YARN_VERSION//\"}
  echo "yarn set version ${YARN_VERSION}"
  yarn set version "${YARN_VERSION}"

  echo "nodeLinker: node-modules">>.yarnrc.yml

  if ! grep -Fxq "enableStrictSsl: false" .yarnrc.yml && [[ "${PIPELINE}" == "false" ]]; then
    # On some installation command 'yarn set version' clears '.yarnrc.yml' file
    #   Need to add 'enableStrictSsl: false' again
    echo "enableStrictSsl: false">>.yarnrc.yml
  fi

  # Install Docusaurus
  echo "Docusaurus install"
  if yarn install; then
    echo "Docusaurus installation succeeded"
    echo "${TG_PACKAGE_VERSION}" > ../tech-guides/.installed_version.txt
  else
    echo "Docusaurus installation failed"
    exit 1
  fi

  cd "../tools/" || exit 1
fi


#########
# BUILD #
#########

# Display node and yarn version
cd "../tech-guides/"
echo -n "node version: " && node -v
echo -n "yarn version: " && yarn -v

cd "../tools/"

if [[ "${ARR_ACTION[*]}" =~ "clear" ]] || [[ "${INSTALL}" == "true" ]]; then
  cd "../tech-guides/"
  yarn clear
  cd "../tools/"
fi

if [[ "${ARR_ACTION[*]}" =~ "prepare" ]] || [[ "${INSTALL}" == "true" ]]; then
  echo "Preparing folder structure"
  mkdir -p "../tech-guides/config/"
  mkdir -p "../tech-guides/data/"
  mkdir -p "../tech-guides/docs/"
  mkdir -p "../tech-guides/news/"
  mkdir -p "../tech-guides/work/"

  rm -rf "../tech-guides/config/"*
  rm -rf "../tech-guides/data/"*
  rm -rf "../tech-guides/news/"*

  # Workaround - Start: Replace "yarn swizzle @easyops-cn/docusaurus-search-local"
  echo "Updating SearchBar CSS"
  rm -f "../tech-guides/work/SearchBar.module.css.tmp"
  if [ ! -f "../tech-guides/work/SearchBar.module.css.bak" ]; then
    cp "../tech-guides/node_modules/@easyops-cn/docusaurus-search-local/dist/client/client/theme/SearchBar/SearchBar.module.css" "../tech-guides/work/SearchBar.module.css.bak"
  fi
  cp "../tech-guides/work/SearchBar.module.css.bak" "../tech-guides/work/SearchBar.module.css.tmp"
  cat "../tech-guides/src/css/_searchbar.css" >> "../tech-guides/work/SearchBar.module.css.tmp"
  cp "../tech-guides/work/SearchBar.module.css.tmp" "../tech-guides/node_modules/@easyops-cn/docusaurus-search-local/dist/client/client/theme/SearchBar/SearchBar.module.css"
  rm -f "../tech-guides/work/SearchBar.module.css.tmp"
  # Workaround - End

  echo "Running lp_extract.py [cards.json]"
  ${PYTHON} "../scripts/lp_extract.py" --config-file "../config/lp_config.yml" --element "sections" --keep-root "true" --add-id "true" --destination-file "../tech-guides/data/cards.json"

  echo "Running lp_extract.py [footer.json]"
  ${PYTHON} "../scripts/lp_extract.py" --config-file "../config/lp_config.yml" --element "footer" --keep-root "false" --add-id "true" --destination-file "../tech-guides/data/footer.json"

  echo "Running lp_extract.py [news_cfg.json]"
  ${PYTHON} "../scripts/lp_extract.py" --config-file "../config/lp_config.yml" --element "news" --keep-root "false" --add-id "false" --destination-file "../tech-guides/data/news_cfg.json"

  echo "Running update_config_from_cache.py --get edit_url"
  ${PYTHON} "../scripts/update_config_from_cache.py" --get "edit_url" --config-file "../config/core_config.yml" --destination-folder "../tech-guides/config/" --project-id "${PROJECT_ID}" --branch "${BRANCH}"

  echo "Running update_config_from_cache.py --get service_desk_address"
  ${PYTHON} "../scripts/update_config_from_cache.py" --get "service_desk_address" --config-file "../config/core_config.yml" --destination-folder "../tech-guides/config/"
fi

if [[ "${ARR_ACTION[*]}" =~ "pull" ]] || [[ "${INSTALL}" == "true" ]]; then
  echo "Running configure_submodule.py"
  ${PYTHON} "../scripts/configure_submodule.py" --submodule-path "docs/" --config-file "../config/core_config.yml"
  cat "../.gitmodules"
elif [[ "${ARR_ACTION[*]}" =~ "build" ]] && [[ "${PIPELINE}" == "false" ]]; then
  # Perform submodule init only any non initialized submodule
  for submodule_folder in $(git submodule status | grep "^-" | awk '{print $2}'); do
    git submodule update --init $submodule_folder
  done
fi

if [[ "${ARR_ACTION[*]}" =~ "prepare" ]] || [[ "${INSTALL}" == "true" ]]; then
  # Copying news per clients project
  echo "Copying news"
  for d in ../docs/* ; do
    if [[ -d "${d}/news" ]] && [ "$(ls ${d}/news)" ]; then
      echo -e "\e[39;42;1mCopying custom news for client [${d}]...\e[0m"
      cp -R "${d}/news/"* "../tech-guides/news/"
    fi
  done

  # Copying global news
  if [ "$(ls ../news)" ]; then
    echo -e "\e[39;42;1mCopying news for core...\e[0m"
    cp -R "../news/"* "../tech-guides/news/"
  fi

  echo "Running lp_news.py [news.json]"
  ${PYTHON} "../scripts/lp_news.py" --news-folder "../tech-guides/news/" --url "${URL}" --base-url "${BASE_URL}" --config-file "../config/lp_config.yml" --destination-file "../tech-guides/data/news.json"
fi

if [[ "${ARR_ACTION[*]}" =~ "copy" ]] || [[ "${INSTALL}" == "true" ]]; then
  ${PYTHON} "../scripts/check_docs.py" --submodule-path "docs/" --config-file "../config/core_config.yml" --test "${TEST}"
  ${PYTHON} "../scripts/copy_docs.py" --submodule-path "docs/" --docs-path "tech-guides/docs/" --static-path "tech-guides/static/" --config-file "../config/core_config.yml" --test "${TEST}"
  ${PYTHON} "../scripts/update_docs.py" --docs-path "tech-guides/docs/" --base-url "${BASE_URL}" --config-file "../config/core_config.yml" --build "${BUILD}"
fi

if [[ "${ARR_ACTION[*]}" =~ "build" ]] || [[ "${INSTALL}" == "true" ]]; then
  if [[ "${PIPELINE}" == "false" ]]; then
    echo "Backup docusaurus.config.js"
    if [ ! -f "../tech-guides/work/docusaurus.config.js.bak" ]; then
      cp "../tech-guides/docusaurus.config.js" "../tech-guides/work/docusaurus.config.js.bak"
    fi

    echo "Backup sidebars.js"
    if [ -f "../tech-guides/work/sidebars.js.bak" ]; then
      # Restore sidebars.js if script did not finish last run
      cp "../tech-guides/work/sidebars.js.bak" "../tech-guides/sidebars.js"
      rm -f "../tech-guides/work/sidebars.js.bak"
    fi
    cp "../tech-guides/sidebars.js" "../tech-guides/work/sidebars.js.bak"
  fi

  echo "Running update_docusaurus_config.py"
  ${PYTHON} "../scripts/update_docusaurus_config.py" --url "${URL}" --base-url "${BASE_URL}" --production "${PRODUCTION}" --manifest "../tech-guides/docusaurus.config.js" --test "${TEST}"

  echo "Running update_docusaurus_sidebars.py"
  ${PYTHON} "../scripts/update_docusaurus_sidebars.py" --submodule-path "../docs" --config-file "../config/core_config.yml" --manifest "../tech-guides/sidebars.js" --test "${TEST}"

  # Build docs
  echo "Starting build"
  cd "../tech-guides/"
  yarn build
  cd "../tools/"

  if [[ "${PIPELINE}" == "false" ]]; then
    echo "Restore docusaurus.config.js settings"
    ${PYTHON} "../scripts/update_docusaurus_config.py" --url "${URL}" --base-url "${BASE_URL}" --production "true" --manifest "../tech-guides/docusaurus.config.js" --test "false"

    echo "Restore sidebars.js"
    rm -f "../tech-guides/sidebars.js"
    cp "../tech-guides/work/sidebars.js.bak" "../tech-guides/sidebars.js"
    rm -f "../tech-guides/work/sidebars.js.bak"
  fi
fi
