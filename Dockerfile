FROM python:3.8

WORKDIR /app/

RUN pip install --upgrade pip

RUN echo "alias l='ls -lahF --color=auto'" >> /root/.bashrc
RUN echo "python -m pytest" >> /root/.bash_history

COPY requirements-test.txt /app/

RUN pip install -r requirements-test.txt

COPY . /app/
