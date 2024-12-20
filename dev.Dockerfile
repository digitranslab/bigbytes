FROM python:3.10-bookworm
LABEL description="Bigbytes data management platform"
ARG PIP=pip3
USER root

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

## System Packages
RUN \
  curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
  curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
  curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
  NODE_MAJOR=20 && \
  echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list && \
  apt-get update -y && \
  ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
  # Node
  nodejs \
  # NFS dependencies
  nfs-common \
  # odbc dependencies
  msodbcsql18 \
  unixodbc-dev \
  # postgres dependencies \
  postgresql-client && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

RUN apt-get update -y && \
  apt-get install -y --no-install-recommends graphviz && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

## Node Packages
RUN npm install --global yarn && yarn global add next

## Python Packages
RUN \
  pip3 install --no-cache-dir sparkmagic && \
  mkdir ~/.sparkmagic && \
  curl https://raw.githubusercontent.com/jupyter-incubator/sparkmagic/master/sparkmagic/example_config.json > ~/.sparkmagic/config.json && \
  sed -i 's/localhost:8998/host.docker.internal:9999/g' ~/.sparkmagic/config.json && \
  jupyter-kernelspec install --user "$(pip3 show sparkmagic | grep Location | cut -d' ' -f2)/sparkmagic/kernels/pysparkkernel"
 \
    RUN \
  pip3 install --no-cache-dir "git+https://github.com/wbond/oscrypto.git@d5f3437ed24257895ae1edd9e503cfb352e635a8" && \
  pip3 install --no-cache-dir "git+https://github.com/dremio-hub/arrow-flight-client-examples.git#egg=dremio-flight&subdirectory=python/dremio-flight" && \
  pip3 install --no-cache-dir "git+https://github.com/mage-ai/singer-python.git#egg=singer-python" && \
  pip3 install --no-cache-dir "git+https://github.com/mage-ai/dbt-mysql.git#egg=dbt-mysql" && \
  pip3 install --no-cache-dir "git+https://github.com/mage-ai/sqlglot#egg=sqlglot" && \
  pip3 install --no-cache-dir faster-fifo && \
  pip3 install --no-cache-dir "git+https://github.com/mage-ai/dbt-synapse.git#egg=dbt-synapse"

COPY bigbytes_integrations /tmp/bigbytes_integrations

RUN \
  pip3 install --no-cache-dir /tmp/bigbytes_integrations && \
  rm -rf /tmp/bigbytes_integrations
# Bigbytes Dependencies
COPY requirements.txt /tmp/requirements.txt
RUN \
  pip3 install --no-cache-dir -r /tmp/requirements.txt && \
  rm /tmp/requirements.txt

## Bigbytes Frontend
COPY ./bigbytes /home/src/bigbytes
WORKDIR /home/src/bigbytes/frontend
RUN yarn install && yarn cache clean

ENV PYTHONPATH="${PYTHONPATH}:/home/src"
WORKDIR /home/src
