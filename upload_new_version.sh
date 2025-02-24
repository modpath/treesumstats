rm -rf bdpn.egg-info build dist
python setup.py sdist bdist_wheel
twine upload dist/* && \
sudo docker build -t evolbioinfo/treesumstats:v0.6 -f Dockerfile . && sudo docker login && sudo docker push evolbioinfo/treesumstats:v0.6