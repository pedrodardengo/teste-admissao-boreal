FROM python:3.9 AS build-image
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc git musl-dev python3-dev libffi-dev g++

# Activating VENV
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install all deps in VENV
RUN pip install --upgrade pip && pip install --upgrade setuptools && pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry export --without-hashes > requirements.txt && pip install -r requirements.txt


# Use fresh image to run the app
FROM python:3.9-slim
# Copy VENV and assign it to PATH
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY --from=build-image $VIRTUAL_ENV $VIRTUAL_ENV
# Copy app
WORKDIR /app
COPY src/ ./src
# Run it!
EXPOSE 8000
ENTRYPOINT ["uvicorn", "src.main:app"]
CMD ["--host", "0.0.0.0", "--workers", "3"]
