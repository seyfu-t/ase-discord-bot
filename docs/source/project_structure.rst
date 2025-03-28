Project Structure
=================

The repository is organized as follows:

.. code-block:: text

   .
   ├── assets/              # Static assets (images, JSON data from the TMDB API for languages and genres)
   ├── docker/              # Docker and compose files
   ├── docs/                # Sphinx documentation source files
   ├── scripts/             # Utility scripts for building, testing, dockerizing etc.
   ├── src/                 # Source code for the Discord bot
   │   └── ase_discord_bot/
   │       ├── ai/         # AI module for summarization
   │       ├── api_util/    # API utilities and data models for recommendations
   │       ├── bot/        # Bot commands and message formatting utilities
   │       ├── config.py   # Core configuration settings
   │       ├── config_registry.py  # Registry for environment-specific settings
   │       └── main.py     # Application entry point
   └── test/                # Tests
