FROM ubuntu:20.04

# Sysbench.
RUN apt update && \
    apt -y install curl && \
    curl -s https://packagecloud.io/install/repositories/akopytov/sysbench/script.deb.sh | bash && \
    apt -y install sysbench 

# Actually, we do not need root.
RUN groupadd tv && useradd tv -g tv

# Sysbench directory, so that we don't write into filesystem root.
WORKDIR /sysbench

# Benchmark script.
COPY ./benchmark.sh ./

# Run the benchmark.
CMD "./benchmark.sh"
