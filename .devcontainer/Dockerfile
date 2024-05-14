# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.224.3/containers/javascript-node/.devcontainer/base.Dockerfile

# [Choice] Node.js version (use -bullseye variants on local arm64/Apple Silicon): 16, 14, 12, 16-bullseye, 14-bullseye, 12-bullseye, 16-buster, 14-buster, 12-buster
ARG VARIANT="16-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/javascript-node:0-${VARIANT}

# Install Zscaler root CA in the trust store
COPY cert/cazscaler-root.crt /tmp/cazscaler-root.crt
RUN cp tmp/cazscaler-root.crt /usr/local/share/ca-certificates/
COPY cert/cazscaler-root.pem /tmp/cazscaler-root.pem
RUN cp tmp/cazscaler-root.pem /usr/local/share/ca-certificates/
RUN if [ $? -ne 0 ]; then echo "*** ERROR *** during copy cazscaler-root.crt"; exit 1; fi
RUN update-ca-certificates
RUN npm config set cafile /etc/ssl/certs/ca-certificates.crt

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# [Optional] Uncomment if you want to install an additional version of node using nvm
# ARG EXTRA_NODE_VERSION=10
# RUN su node -c "source /usr/local/share/nvm/nvm.sh && nvm install ${EXTRA_NODE_VERSION}"

# [Optional] Uncomment if you want to install more global node modules
#RUN su node -c "npm install -g yarn"
RUN curl https://stedolan.github.io/jq/download/linux64/jq -v > /usr/bin/jq && chmod +x /usr/bin/jq

