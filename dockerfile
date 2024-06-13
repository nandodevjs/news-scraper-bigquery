FROM gcr.io/dataflow-templates-base/python310-template-launcher-base:latest

ARG WORKDIR=/dataflow/template
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

COPY . ${WORKDIR}

ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="${WORKDIR}/requirements.txt"
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/main.py"
ENV FLEX_TEMPLATE_PYTHON_SETUP_FILE="${WORKDIR}/setup.py"

RUN apt-get -y update

RUN pip install apache-beam[gcp]==2.55.0
RUN pip install apache-beam==2.53.0
RUN pip install google-cloud-secret-manager

RUN pip install -U -r ${WORKDIR}/requirements.txt