# Docker version

Here are the high-level steps to create a Docker container:

Write a Dockerfile that defines the image. The Dockerfile should start with a base image (e.g. Ubuntu, Alpine) and then add the necessary dependencies and files to run the `manual.py` file.
Build the Docker image using the Dockerfile.
Run the Docker container from the image.

This Dockerfile uses the official Python 3.8 slim-buster image as the base image, creates a working directory `/app`, copies the `manual.py` file to the working directory, and installs the necessary dependencies using pip. Finally, it sets the default command to run `python manual.py` when the container is started.

To build the Docker image, navigate to the directory where the Dockerfile and `manual.py` file are located, and run the following command:

```bash
docker build -t manual-bot .
```

This command builds a Docker image and tags it with the name `manual-bot`.

To run the Docker container, use the following command:

```bash
docker run -it --rm manual-bot
```

This command starts a new container using the `manual-bot` image and attaches the terminal to it (`-it` option). The `--rm` option removes the container and its data when the container is stopped.

To load the Docker image, you will first need to have the Docker engine installed on your machine. You can download the Docker engine from the official Docker website (<https://www.docker.com/products/docker-desktop>).

Once you have Docker installed, you can load the Docker image using the following command:

```bash
docker load -i manual-bot.tar.gz
```

This command loads the Docker image from the `manual-bot.tar.gz` file. You will need to replace `manual-bot.tar.gz` with the name of the tar file that contains the Docker image.

Alternatively, if you have the Docker image ID, you can load the Docker image using the following command:

```bash
docker load -i <image_id>.tar.gz
```

This command loads the Docker image with the specified image ID from the tar file. You will need to replace `<image_id>` with the actual image ID of the Docker image.

After the Docker image is loaded, you can run the Docker container using the following command:

```bash
docker run -it --rm manual-bot
```

This command starts a new container using the `manual-bot` image and attaches the terminal to it (`-it` option). The `--rm` option removes the container and its data when the container is stopped.

First, make sure that you have Docker installed on your remote server. You can use the following command to install Docker on your server:

```bash
sudo apt-get update
sudo apt-get install docker.io
```

Once you have Docker installed, you can load the Docker image into the server using the following command:

```bash
docker load -i manual-bot.tar.gz
```

This command loads the Docker image from the manual-bot.tar.gz file. You will need to replace manual-bot.tar.gz with the name of the tar file that contains the Docker image.

After the Docker image is loaded, you can run the Docker container using the following command:

```bash
docker run -it --rm manual-bot
```

This command starts a new container using the manual-bot image and attaches the terminal to it (-it option). The --rm option removes the container and its data when the container is stopped.

To run the Docker container in the background, you can use the following command:

```bash
docker run -d --name manual-bot-container manual-bot
```

This command starts a new container using the manual-bot image and runs it in detached mode (-d option). It also gives the container a name (--name manual-bot-container) for easy reference.

You can then access the running container using Termius by SSHing into your remote server and running the following command:

```bash
docker exec -it manual-bot-container bash
```

This command starts an interactive terminal (-it option) inside the running container and runs the bash shell. From there, you can interact with the running manual.py script as needed.
