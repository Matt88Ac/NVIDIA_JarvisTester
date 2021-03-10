# NVIDIA Jarvis

> NVIDIA released Jarvis 1.0 Beta which includes an end-to-end workflow for building and deploying real-time conversational AI apps, such as transcription, virtual assistants and chatbots. Jarvis is a flexible application framework for multimodal conversational AI services that delivers real-time performance on NVIDIA GPUs.

![](https://developer-blogs.nvidia.com/news/wp-content/uploads/sites/3/2021/02/Jarvis-Beta-Featured-Image.png)

In this repo, built a Q&A chatbot application using Jarvis application framework.

# Quick Start: Creating Jarvis Flask server.

> Following instrauctions can be found on [Jarvis Speech Skills Quick Start Guide](https://docs.nvidia.com/deeplearning/jarvis/user-guide/docs/quick-start-guide.html)

Prerequisites:
1.  You have access and are logged into NVIDIA GPU Cloud (NGC). You must have an API key and NGC CLI to run this example. Instructions of how to get them can be found [here](https://ngc.nvidia.com/setup/installers/cli)  
3.  You have access to a Volta, Turing, or an NVIDIA Ampere arcitecture-based A100 GPU.
4.  You have Docker installed with support for NVIDIA GPUs. [Installing Docker](https://docs.docker.com/engine/install/)
 
## Step 1 - Download the scripts.


(After you got the the API key and filled the credentials on the NGC CLI)
Run:
> `$ ngc registry resource download-version nvidia/jarvis/jarvis_quickstart:1.0.0-b.2`
 
This step will download the scripts that will download and start the Jarvis containers.

## Step 2 - Initialize and start Jarvis.

The start script launches the server. Within the quickstart directory, modify the config.sh file with your preferred configuration. Options include which models to retrieve from NGC, where to store them, and which GPU to use if more than one is installed in your system.

> `$  cd jarvis_quickstart_v1.0.0-b.2`

> `$  bash jarvis_init.sh`

> `$  bash jarvis_start.sh`

**This process may take quite a while depending on the speed of your Internet connection and number of models deployed. Each model is individually optimized for the target GPU after download.**

## Step 3 - Start a container with sample clients for each service.

This step should log you in the container.
> `$  bash jarvis_start_client.sh`

## Step 4 - (Optional) - Launch example notebooks provided

Optional step, the notebooks provided in the container are examples of usage of different services in Jarvis.
Within the container, Run:
> `$  jupyter notebook --ip=0.0.0.0 --allow-root --notebook-dir=/work/notebooks`

## Step 5 - Before Running the application.

Within the container install the following python modules:

> `$ pip install flask`

> `$ pip install wikipedia`

In a new terminal (not in the container) copy the **app.py** file to the container.

> `docker cp app.py <containerID>:path/of/working/dir/app.py`

* Get the containerID using `docker ps` and copy the id of the **jarvis-client** client
* path/of/working/dir/ can be for example: /work/app.py

## Step 6 - Run the application.

Within the container run:

> `$ python3 app.py`

The application will receive POST requests sent from the `main.py` script.
The request contains the sample rate and the audio sample recorded.

**Note: If you do deploy the flask server on cloud (AWS instance etc.) make sure u have the public IP of the instance for the `main.py` script**

## Step 7 - Test our applciation.

1.  install following modules:

> `$ pip install soundfile`

> `$ pip install sounddevice `

2.  run main.py - The scripts records a vocal question and sends it to the application.
**NOTE: Make sure before running the script that you have changed the *SERVER_IP* to yours.**

> `$ python main.py`

Example Output:

## TODO:
-Presentation.
-Quick start instruction
-Add requirments.txt
-screenshots of examples
