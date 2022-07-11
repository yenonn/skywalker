FROM skywalker/python:0.1
RUN groupadd -g 999 skywalker && \
    useradd -r -u 999 -g skywalker skywalker
ENV PYTHONPATH /app
RUN mkdir /app
RUN chown -R skywalker:skywalker /app
ADD requirements.txt /install
RUN pip install -r /install/requirements.txt
USER skywalker
