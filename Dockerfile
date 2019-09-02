FROM python:3.6
ENV PYTHONUNBUFFERED 1

# Install node 8 and yarn globally.
#RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
#RUN apt-get update && apt-get install -y nodejs
#RUN npm install -g yarn

RUN mkdir /code
WORKDIR /code
EXPOSE 8000

COPY requirements.txt /code/
RUN pip install -r requirements.txt
#RUN yarn install
COPY . /code/
