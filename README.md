# Streamfinity's Prototype

A repository that contains the Streamfinity's prototype REST API that go with [a Medium article called Streamfinity's API Makeover - Embracing Python and FastAPI](https://medium.com/itnext/streamfinitys-api-makeover-embracing-python-and-fastapi-93df4dc237aa)


Here are the steps to install and run the prototype.

## Requirements

- Docker
- Python 3.11
- Pip3

## Installation Steps

1. Install the Python requirements:

    ```bash
    pip3 install -r requirements.txt
    ```

2. Start the database:

    ```bash
    docker compose up
    ```

3. In another terminal, navigate to the `app` folder and start the application by:

    ```bash
    cd app
    uvicorn main:app
    ```

During the startup of the application a selection of movies and their actors will be entered in the database.

## Restart with clean database

If you need to reset the database, follow these steps:

1. Stop docker compose:

    ```bash
    docker compose down
    ```

2. Run the cleanup script:

    ```bash
    python3 clear_db_folders.py
    ```

3. Restart the database:

    ```bash
    docker compose up
    ```

4. Navigate to the `app` folder and start the application:

    ```bash
    cd app
    uvicorn main:app
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

* This project is part of the journey of Streamfinity to improve its server operations by segregating read and write operations. 

## Support

If you're having any problem, please raise an issue on GitHub.

