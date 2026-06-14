FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY tests ./tests
COPY projects ./projects

CMD ["python", "projects/jd-resume-ats-matcher/poc.py"]
