FROM python:3.9.10

WORKDIR /home/spm_pj
COPY . /home/spm_pj

RUN ["pip","install","-r","requirement.txt"]

ENTRYPOINT ["python","manage.py","runserver" , "0.0.0.0:8000"]

EXPOSE 8000