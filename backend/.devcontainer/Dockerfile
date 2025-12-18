FROM mcr.microsoft.com/devcontainers/python:3.13

ARG USERNAME
ARG USER_UID
ARG USER_GID

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV TZ=Asia/Tokyo \
	LANG=ja_JP.UTF-8 \
	LANGUAGE=ja_JP:jp \
	LC_ALL=ja_JP.UTF-8 \
	DEVCONTAINER=true \
	DEBIAN_FRONTEND=noninteractive

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
	locales \
	tzdata \
	unzip \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* \
	&& locale-gen ja_JP.UTF-8 \
	&& localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

USER ${USERNAME}

# hadolint ignore=SC2016
RUN curl -fsSL https://bun.sh/install | bash \
	&& echo 'export BUN_INSTALL="$HOME/.bun"' >> ~/.bashrc \
	&& echo 'export PATH="$BUN_INSTALL/bin:$PATH"' >> ~/.bashrc

WORKDIR /workspace
