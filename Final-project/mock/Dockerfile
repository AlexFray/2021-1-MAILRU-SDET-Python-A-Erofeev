FROM python:3.8

ADD /requirements.txt requirements.txt
RUN pip3.8 install -r requirements.txt

ADD /main.py main.py

CMD ["python3", "main.py"]