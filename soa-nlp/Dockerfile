# Downloads the slim version of python-base-3.9 from HUB
#FROM sit1-dtr.anthem.com/core/python-base-3.9:1.0.0
FROM quay.apps.lz-np2.ent-ocp4-useast1.aws.internal.das/openshift-base-images/python-3.9-image-with-certs:latest

USER root
# Let's create directories to store source-code, packages etc.
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/vmt-nlp-api

# RUN echo "sslverify=false" >> /etc/yum.conf
# Let's download and install the required packages
RUN pip install --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org spacy==3.2.4 \
      && CURL_CA_BUNDLE="" python -m spacy download en_core_web_md

# Let's copy the requirement.txt into the specified working dir
COPY requirements.txt /opt/app/requirements.txt

# Let's copy the application code into the specified working dir
COPY . /opt/app/vmt-nlp-api/

# Let's set the working directory for any RUN, COPY, ADD etc that follow it in the Dockerfile.
WORKDIR /opt/app/vmt-nlp-api/


# Let's install the required python packages using pip
RUN pip install --upgrade --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Let's install some nltk related packages like stopwords, punkt etc
RUN python -c "import ssl; ssl._create_default_https_context = ssl._create_unverified_context; import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"

# Let's expose the specified port for running the application
EXPOSE 8080/tcp

# Let's run the server using the below command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]