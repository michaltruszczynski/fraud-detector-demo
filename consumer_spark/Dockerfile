FROM bitnami/spark:3.5

USER root

# Skopiuj kod i model
COPY consumer_spark/consumer_spark.py /app/consumer_spark.py
COPY model/model.pkl /model/model.pkl

# Pobierz JAR-y potrzebne do Spark + Kafka
ENV SPARK_VERSION=3.5.0
ENV SCALA_VERSION=2.12

RUN mkdir -p /opt/bitnami/spark/jars && \
    curl -L -o /opt/bitnami/spark/jars/spark-sql-kafka.jar \
      https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.0/spark-sql-kafka-0-10_2.12-3.5.0.jar && \
    curl -L -o /opt/bitnami/spark/jars/kafka-clients.jar \
      https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.7.0/kafka-clients-3.7.0.jar && \
    curl -L -o /opt/bitnami/spark/jars/spark-token-provider-kafka.jar \
      https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.5.0/spark-token-provider-kafka-0-10_2.12-3.5.0.jar && \
    curl -L -o /opt/bitnami/spark/jars/commons-pool2.jar \
      https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar

# Python + joblib
RUN install_packages python3 python3-pip && \
    pip3 install joblib pandas scikit-learn requests

WORKDIR /app
CMD ["spark-submit", "consumer_spark.py"]