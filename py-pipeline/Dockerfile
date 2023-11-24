FROM rockylinux:8
COPY . .
RUN yum -y install python39
RUN /usr/bin/python3 -m venv appvenv
RUN source appvenv/bin/activate
RUN /usr/bin/pip3 install -r requirements.txt
CMD python3 main.py
# Failed docker images should be deleted.


