FROM python:3.10

# Locale.
RUN apt-get update -y && apt-get install -y locales alien \
    && localedef -i en_US -c -f UTF-8 -A \/usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

# Environment.
COPY ./requirements.txt /tmp
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --root-user-action ignore -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# Actually, we do not need root.
RUN groupadd tv && useradd tv -g tv

# App.
WORKDIR /app

# Source.
COPY ./src ./src
COPY ./config ./config

# Run.
USER tv
