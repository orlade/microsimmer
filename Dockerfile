FROM python:2.7.8-onbuild

MAINTAINER Oliver Lade <oliver@runsimmer.com>

EXPOSE 5000

CMD ["python", "./serve.py"]
