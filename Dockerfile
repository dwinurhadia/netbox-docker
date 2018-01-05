FROM python:3.6-alpine

RUN apk add --no-cache \
      bash \
      build-base \
      ca-certificates \
      cyrus-sasl-dev \
      graphviz \
      jpeg-dev \
      libffi-dev \
      libxml2-dev \
      libxslt-dev \
      openssl-dev \
      postgresql-dev \
      libldap \
      openldap-dev \
      wget

RUN pip install gunicorn

WORKDIR /opt

ARG BRANCH=master
ARG URL=https://github.com/digitalocean/netbox/archive/$BRANCH.tar.gz
RUN wget -q -O - "${URL}" | tar xz \
  && mv netbox* netbox

WORKDIR /opt/netbox
RUN pip install -r requirements.txt

RUN pip install django-auth-ldap

COPY docker/configuration.docker.py /opt/netbox/netbox/netbox/configuration.py
COPY docker/ldap_config.py /opt/netbox/netbox/netbox/ldap_config.py
COPY docker/gunicorn_config.py /opt/netbox/
COPY docker/nginx.conf /etc/netbox-nginx/nginx.conf

WORKDIR /opt/netbox/netbox

COPY docker/docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT [ "/docker-entrypoint.sh" ]

VOLUME ["/etc/netbox-nginx/"]

CMD ["gunicorn", "--log-level debug", "-c /opt/netbox/gunicorn_config.py", "netbox.wsgi"]
