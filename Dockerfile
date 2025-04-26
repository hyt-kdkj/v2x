FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# パッケージインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    clang \
    gdb \
    bison \
    flex \
    perl \
    python3 \
    python3-pip \
    python3-venv \
    libpython3-dev \
    qtbase5-dev \
    qtchooser \
    qt5-qmake \
    qtbase5-dev-tools \
    libqt5opengl5-dev \
    libxml2-dev \
    zlib1g-dev \
    doxygen \
    graphviz \
    libwebkit2gtk-4.1-0 \
    xdg-utils \
    libdw-dev \
    wget \
    curl \
    git \
    nano \
    vim \
    cmake \
    openmpi-bin \
    software-properties-common \
    gnupg2 \
    unzip \
 && rm -rf /var/lib/apt/lists/*

# シンボリックリンク
RUN ln -sf /usr/bin/python3 /usr/bin/python && ln -sf /usr/bin/pip3 /usr/bin/pip

# SUMOインストール
RUN add-apt-repository ppa:sumo/stable -y && \
    apt-get update && \
    apt-get install -y sumo sumo-tools sumo-doc && \
    rm -rf /var/lib/apt/lists/*
ENV SUMO_HOME=/usr/share/sumo

# 作業ディレクトリ
WORKDIR /workspace

# Python仮想環境の作成と依存関係
RUN python -m venv venv
COPY requirements.txt .
RUN . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

# README, sampleディレクトリ
COPY README.md .
RUN mkdir -p /workspace/sumo
RUN mkdir -p /workspace/sumo/sample
COPY sample/ /workspace/sumo/sample/

# OMNeT++ 6.0.3 のインストール
RUN wget https://github.com/omnetpp/omnetpp/releases/download/omnetpp-6.0.3/omnetpp-6.0.3-linux-x86_64.tgz && \
    tar xvf omnetpp-6.0.3-linux-x86_64.tgz && \
    echo "WITH_QTENV=no" >> /workspace/omnetpp-6.0.3/configure.user && \
    echo "WITH_OSG=no" >> /workspace/omnetpp-6.0.3/configure.user && \
    rm omnetpp-6.0.3-linux-x86_64.tgz

# Veins 5.2 をダウンロード・解凍・ビルド
RUN wget https://veins.car2x.org/download/veins-5.2.zip && \
    unzip veins-5.2.zip && rm veins-5.2.zip

# 環境変数を有効化した状態で起動
ENV PATH="/workspace/omnetpp-6.0.3/bin:$PATH"
ENV LD_LIBRARY_PATH="/workspace/omnetpp-6.0.3/lib"

# デフォルト起動はbash
CMD ["/bin/bash"]
