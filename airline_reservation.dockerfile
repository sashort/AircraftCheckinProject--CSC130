# This is a comment line
FROM ubi7/ubi:7.7 2
LABEL description="This is a custom httpd container image"
MAINTAINER S. Andy Short <essayshort@gmail.com.com>
RUN yum install python3 \
EXPOSE 22 \
ENV LogLevel "info" \
COPY ./ /app/ \
USER sashort \
ENTRYPOINT ["python3", "Main.py"] \
#CMD ["-D", "FOREGROUND"]