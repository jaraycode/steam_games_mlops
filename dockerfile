FROM python:3.10-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirement.txt .
RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate"
RUN pip install -r requirement.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn","app:app","--reload","--host","0.0.0.0","--port","8000"]