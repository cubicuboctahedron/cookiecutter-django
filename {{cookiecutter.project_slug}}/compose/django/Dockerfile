{% if cookiecutter.use_python3 == 'y' -%}
FROM python:3.5
{% else %}
FROM python:2.7
{%- endif %}
ENV PYTHONUNBUFFERED 1

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements

RUN pip install --no-cache-dir -r /requirements/production.txt

# adding node+npm
RUN curl -sL https://deb.nodesource.com/setup_4.x | bash - && apt-get install -y nodejs && apt-get clean && npm install -g grunt-cli bower

RUN groupadd -r django && useradd -r -g django django

RUN mkdir -p /node
ADD package.json /node/package.json
RUN cd /node && npm install && npm cache clean

RUN mkdir -p /bower
ADD bower.json /bower/bower.json
RUN cd /bower && bower --allow-root install && bower --allow-root cache clean

COPY . /app
RUN cp -a /node/node_modules /app/
RUN cp -a /bower/bower_components /app/{{ cookiecutter.project_slug }}/static/components
RUN chown -R django /app

WORKDIR /app

RUN grunt build

COPY ./compose/django/gunicorn.sh /gunicorn.sh
COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh \
    && sed -i 's/\r//' /gunicorn.sh \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh \
    && chmod +x /gunicorn.sh \
    && chown django /gunicorn.sh

ENTRYPOINT ["/entrypoint.sh"]
