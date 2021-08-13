FROM alpine:latest
WORKDIR /tests
COPY tests/requirements.txt /tests/
COPY /tests/*.py /tests/
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip -r /tests/requirements.txt
ENTRYPOINT ["pytest", "/tests"]