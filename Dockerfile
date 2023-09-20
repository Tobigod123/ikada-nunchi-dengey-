# Base Image 
FROM fedora:37

# Setup home directory, non interactive shell and timezone
RUN mkdir /bot /tgenc && chmod 777 /bot
WORKDIR /bot
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Africa/Lagos

# Install Dependencies
RUN dnf -qq -y update && dnf -qq -y install git aria2 bash xz wget curl pv jq python3-pip mediainfo procps-ng && python3 -m pip install --upgrade pip

# Install latest ffmpeg
RUN wget https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n6.0-latest-linux64-gpl-6.0.tar.xz && tar -xvf *xz && cp *6.0/bin/* /usr/bin && rm -rf *xz && rm -rf *6.0

# Copy files from repo to home directory
COPY . .

# Install python3 requirements
RUN pip3 install -r requirements.txt

# Start bot
CMD ["bash","start.sh"]
