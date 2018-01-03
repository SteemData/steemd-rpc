# -*- coding: utf-8 -*-
FROM phusion/baseimage:latest

ARG STEEM_STATIC_BUILD=ON
ENV STEEM_STATIC_BUILD ${STEEM_STATIC_BUILD}

ENV LANG=en_US.UTF-8

RUN \
    apt-get update && \
    apt-get install -y \
        autoconf \
        automake \
        autotools-dev \
        bsdmainutils \
        build-essential \
        cmake \
        doxygen \
        git \
        libboost-all-dev \
        libreadline-dev \
        libssl-dev \
        libtool \
        ncurses-dev \
        pbzip2 \
        pkg-config \
        python3 \
        python3-dev \
        python3-jinja2 \
        python3-pip \
        wget \
        gdb \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    pip3 install gcovr


ENV BUILDBASE /r
ENV BUILDROOT $BUILDBASE/build
ENV FILESROOT $BUILDBASE/files

RUN mkdir -p $BUILDROOT $FILESROOT

ENV STEEM_VERSION 0.19.2
ENV STEEM_RELEASE v$STEEM_VERSION

RUN cd $BUILDROOT && \
    ( \
        git clone https://github.com/steemit/steem.git steem &&\
        cd steem ;\
        ( \
            git checkout $STEEM_RELEASE &&\
            git submodule update --init --recursive &&\
            cmake \
                -DCMAKE_BUILD_TYPE=Release \
                -DLOW_MEMORY_NODE=OFF -DCLEAR_VOTES=OFF -DSKIP_BY_TX_ID=ON \
                -DSTEEM_STATIC_BUILD=${STEEM_STATIC_BUILD} \
                -DCMAKE_INSTALL_PREFIX=/usr/local \
                CMakeLists.txt &&\
            make -j 8 install \
        ) \
    ) &&\
    ( \
        rm -Rf $BUILDROOT/steem \
    )

RUN \
    apt-get remove -y \
        automake \
        autotools-dev \
        bsdmainutils \
        build-essential \
        cmake \
        doxygen \
        dpkg-dev \
        git \
        libboost-all-dev \
        libc6-dev \
        libexpat1-dev \
        libgcc-5-dev \
        libhwloc-dev \
        libibverbs-dev \
        libicu-dev \
        libltdl-dev \
        libncurses5-dev \
        libnuma-dev \
        libopenmpi-dev \
        libpython-dev \
        libpython2.7-dev \
        libreadline-dev \
        libreadline6-dev \
        libssl-dev \
        libstdc++-5-dev \
        libtinfo-dev \
        libtool \
        linux-libc-dev \
        m4 \
        make \
        manpages \
        manpages-dev \
        mpi-default-dev \
        python-dev \
        python2.7-dev \
        python3-dev \
    && \
    apt-get autoremove -y && \
    rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /var/cache/* \
        /usr/include \
        /usr/local/include

RUN mkdir -p /witness_node_data_dir &&\
    touch /witness_node_data_dir/.default_dir

ADD fullnode.config.ini /witness_node_data_dir/config.ini

ENV STEEMD_EXEC="/usr/local/bin/steemd"
ENV STEEMD_ARGS=""
# --replay-blockchain

ADD run-steemd.sh /usr/local/bin
RUN chmod +x /usr/local/bin/run-steemd.sh

EXPOSE 2001
EXPOSE 8090

VOLUME ["/witness_node_data_dir"]

CMD ["/usr/local/bin/run-steemd.sh"]