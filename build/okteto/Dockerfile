FROM python

WORKDIR /skywalker

RUN apt-get update && apt-get install -y zip git tmux vim
RUN mkdir /install
ADD requirements.txt /install
RUN pip install -r /install/requirements.txt


CMD ["bash"]
