# Building prod image.
FROM python:3-buster AS prod

RUN pip install pipenv

COPY ./api /api
WORKDIR /api

RUN pipenv install --system --deploy 

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

# Building dev image with dev dependencies
FROM prod as dev

RUN pipenv install --system --deploy --dev
