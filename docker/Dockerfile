FROM debian:11

LABEL org.opencontainers.image.authors="steffen@volkmann.com"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update 
RUN apt-get install -y apt-utils 2>&1 | grep -v "debconf: delaying package configuration, since apt-utils is not installed" 
RUN apt-get install -y procps 

RUN apt-get install -y subversion \
    rsync \
    git \
    wget \
    python3-pip \
    imagemagick \
    build-essential \
    unzip \
    p7zip-full 

COPY policy.xml /etc/ImageMagick-6/policy.xml

# install FreeImage
RUN wget --no-verbose --show-progress --progress=bar:force:noscroll \
    "https://sourceforge.net/projects/freeimage/files/Source Distribution/3.18.0/FreeImage3180.zip"

RUN unzip FreeImage3180.zip \
 &&  cd FreeImage \
 &&  make -j 8 \
 &&  make install 

# install imgkap
RUN git clone https://github.com/stevo01/imgkap
RUN cd imgkap \
 && make \
 && make install

USER root
COPY requirements.txt /
RUN pip3 install -r /requirements.txt 

RUN apt install -y locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Start running
USER root
COPY run.sh /
RUN chmod +x /run.sh
ENTRYPOINT ["/run.sh"]
CMD []
EXPOSE 2022
