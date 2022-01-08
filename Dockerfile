FROM python:3.8-slim-buster

WORKDIR /app/
RUN echo 'deb http://deb.debian.org/debian testing main' >> /etc/apt/sources.list \
    && apt-get update && apt-get install -y --no-install-recommends -o APT::Immediate-Configure=false gcc g++
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN useradd -U -s /bin/false apprunner
USER apprunner

EXPOSE 5000
COPY api api/
COPY certs certs/

COPY server.py .

CMD ["python", "server.py"]