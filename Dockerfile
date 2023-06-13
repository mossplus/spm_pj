FROM python:3.9
ENV PYTHONUNBUFFERED=1
RUN mkdir -p /home/spm_pj
COPY . /home/spm_pj
WORKDIR /home/spm_pj
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple