FROM python:3-alpine
WORKDIR /tests
COPY tests/requirements.txt /tests/
COPY /tests/*.py /tests/
RUN pip3 install --no-cache --upgrade pip -r /tests/requirements.txt
ENTRYPOINT ["pytest", "/tests"]