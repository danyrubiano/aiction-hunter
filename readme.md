![VERSION](https://img.shields.io/badge/Version-0.0.1-blue?style=for-the-badge) ![LICENSE](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge) ![MAINTAINED](https://img.shields.io/badge/Maintained-yes-green?style=for-the-badge) ![COVERAGE](https://img.shields.io/badge/Coverage-0%25-red?style=for-the-badge)


# Personalized substitution

Repo for personalized substitution experimentation

## 1. Local usage (if needed)

Run something for clone and run 

```
git clone https://gecgithub01.walmart.com/cl-omnilab/personalized-substitution.git
cd personalized-substitution
```
then run
```
pip install -r requirements.txt
```
and then
```
streamlit run app.py
```

## 2. Deploy on GCP

You need:
- A project on GCP with acces to Cloud Run, Container Registry and Bigquery.
- Docker installed in your local machine

For configure the GCP credentials on Docker
```
gcloud auth configure-docker
```
Then make docker login
```
docker login gcr.io/<your_gcp_project>
```
For docker-build
```
docker build -t eu.gcr.io/<your_gcp_project>/<your_project_name>:v1 .   
```
For docker run and pass the environment variables saved into an env file
```
docker run --rm -p 8080:8080 --env-file ./config/.env eu.gcr.io/<your_gcp_project>/<your_project_name>:v1 
```
Then make docker push
```
docker push  eu.gcr.io/<your_gcp_project>/<your_project_name>:v1     
```
After that, you will be able to see the image inside the Container Registry on GCP

And to raise it in Cloud Run you can follow the following [instructions](https://cloud.google.com/run/docs/quickstarts/deploy-container)
