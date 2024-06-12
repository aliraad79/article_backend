FROM python:3.12.3

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100
ENV PATH="$POETRY_HOME/bin:$PATH"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY requirements.txt /code/

# Project initialization:
RUN pip install -r requirements.txt

# Copy the Django project files
COPY . articles/
WORKDIR /code/articles

EXPOSE 8000
# start server
CMD ["sh", "entrypoint.sh"]