FROM python:3.11-slim

RUN useradd -m -u 1000 runner
USER runner
WORKDIR /code

# No extra packages needed — pure stdlib Python
