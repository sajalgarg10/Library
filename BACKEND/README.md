# Library Management 
    Welcome to Library-
        It is an application that allows user to request books from the admin 

# Features
    * User Authentication
    * Create, Edit and Delete the Section
    * Create, Edit and Delete the Book
    * Request book from the admin
    * Daily reminder
    * Caching


# Installation
    * make a copy of the backend and then run the wsl in windows
    * run the python app
        ```sh
            python main.py

    * run the redis server
        ```sh
            redis-server

    * run the celery worker
        ```sh
            celery -A app.jobs.celery worker --loglevel=info

    * run the celery beat
        ```sh
            celery -A app.jobs.celery beat --loglevel=info

    * Finally run mailhog
        ```sh
            install it from browser
            then run it.


