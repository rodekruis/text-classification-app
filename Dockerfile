# python base image in the container from Docker Hub
FROM tensorflow/tensorflow:latest-gpu

#set up environment
RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y curl
RUN apt-get install unzip

# copy files to the /app folder in the container
COPY ./main.py /app/main.py

# set the working directory in the container to be /app
WORKDIR /app

# install the packages
RUN pip install fastapi uvicorn transformers sentencepiece python-dotenv

# expose the port that uvicorn will run the app on
ENV PORT=8000
EXPOSE 8000

# define the model that will be loaded
ENV MODEL_ORG="MoritzLaurer"
ENV MODEL_NAME="DeBERTa-v3-base-mnli-fever-anli"

# execute the command python main.py (in the WORKDIR) to start the app
CMD ["python", "main.py"]