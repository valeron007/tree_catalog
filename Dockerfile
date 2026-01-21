FROM python:3.13.5
USER root
COPY ./ /backend

WORKDIR /backend

RUN pip install pip-tools
RUN pip-compile
RUN pip-sync

EXPOSE 8001

CMD ["python3", "main.py"]
