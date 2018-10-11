FROM i3thuan5/tai5-uan5_gian5-gi2_kang1-ku7:latest
MAINTAINER Singhong

WORKDIR /opt/
EXPOSE 5000
RUN pip3 install Flask gunicorn
COPY docker.csv .
COPY lm.arpa.gz .
RUN gzip -d lm.arpa.gz
COPY tngsu.py .

CMD gunicorn -w 2 -b 0.0.0.0:5000 -t 120 --log-level debug tngsu:app