FROM python:3.6

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools pipenv

ADD Pipfile /app/Pipfile
ADD Pipfile.lock /app/Pipfile.lock

RUN pipenv install --deploy --system

ENV PYTHONPATH /app

EXPOSE 5000

CMD ["sleep", "inf"]
# CMD ["python", "-m", "game_of_graphql.server", "--host", "0.0.0.0"]
