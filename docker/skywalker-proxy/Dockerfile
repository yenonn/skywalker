FROM python
ENV PYTHONPATH /app
RUN mkdir /app /install
ADD requirements.txt /install
RUN pip install -r /install/requirements.txt
EXPOSE 5000
ENTRYPOINT python /app/web.py
