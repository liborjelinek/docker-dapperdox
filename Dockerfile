FROM golang:1.8
ENV VER 1.1.1

# install unzip utility
RUN apt-get -y update && apt-get -y install zip

# download and unzip Dapperdox sources
RUN cd /go/src/ && \
    curl -L -o dapperdox.zip https://github.com/DapperDox/dapperdox/archive/v${VER}.zip && \
    unzip dapperdox.zip && \
    rm dapperdox.zip

# compile
WORKDIR /go/src/dapperdox-${VER}
RUN go-wrapper download         # "go get -d -v ./..."
RUN go-wrapper install          # "go install -v ./..."

# script to convert specs in YAML to JSON (Dapperdox supports JSON only)
RUN apt-get install -y python3 python3-pip
RUN pip3 install pyaml
COPY yaml_to_json.py /usr/local/bin

# default Dapperdox configuration
ENV DAPPERDOX_ROOT /dapperdox
ENV SPEC_DIR $DAPPERDOX_ROOT/specs
ENV ASSETS_DIR $DAPPERDOX_ROOT/assets
ENV THEME sectionbar
# listen on ALL interfaces
ENV BIND_ADDR 0.0.0.0:3123
EXPOSE 3123

# run Dapperdox
CMD ["go-wrapper", "run"]       # ["app"]