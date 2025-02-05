FROM python:3.9-slim

RUN mkdir /pasteur

# Install treesumstats
RUN cd /usr/local/ && pip3 install --no-cache-dir treesumstats==0.1

# The entrypoint runs treesumstats with command line arguments
ENTRYPOINT ["treesumstats"]