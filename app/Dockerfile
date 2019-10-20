FROM frolvlad/alpine-python3

WORKDIR /usr/src/app

COPY requirements.txt .

RUN \
 apk add postgresql-libs && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev python3-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

# Copy and Install application
COPY .  .
RUN pip3 install .

# Set environ vars
ENV CACHE_REDIS_HOST 'legalist-test-devops-chintal-redis'
ENV CACHE_REDIS_PORT 6379
ENV CACHE_REDIS_PASSWORD 'kFfZyXP8BmyZbIBPcL/khBZcd5r42jOpvuMGl8xABGTVFqPAcfld9Qmw3H+m1JmmH1HHG6LsEHlolf13'

ENV DATABASE_HOST 'legalist-test-devops-chintal-postgres'
ENV DATABASE_PORT 5432
ENV DATABASE_USER 'legalist'
ENV DATABASE_PASS 'legalist'
ENV DATABASE_DB 'legalist'

# Expose port
EXPOSE 8080

# Command to run on start
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "3", "chintal.app:app"]
