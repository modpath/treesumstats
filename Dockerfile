FROM python:3.12-slim

RUN mkdir /pasteur

# Install treesumstats
RUN cd /usr/local/ && pip3 install --no-cache-dir treesumstats==0.9

# The entrypoint runs treesumstats with command line arguments
ENTRYPOINT ["treesumstats"]