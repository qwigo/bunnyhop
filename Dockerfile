FROM capless/capless-docker:2
ADD . /code
RUN poetry install
