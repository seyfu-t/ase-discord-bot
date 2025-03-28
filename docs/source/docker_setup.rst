Docker Setup
============

For containerized deployments, follow these steps:

Build the Docker Image:

.. code-block:: bash

   bash scripts/dockerize.sh

Run the container using Docker Compose:

.. code-block:: bash

   docker compose --file docker/docker-compose.yml up -d

Note: The compose files have the required environment variables commented out. You must add them before running.
