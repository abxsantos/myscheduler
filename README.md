
<!-- PROJECT LOGO -->
<br />
<p align="center">
  
  <h3 align="center">My Django Q Scheduler</h3>
      <p align="center">
        A very simple django project that helps understanding some concepts about the Django Q implementation. It uses a telegram API to create Clients and make subscriptions via a task management system.
        <br />
        <br />
        <a href="https://github.com/abxsantos/my-djangoq-scheduler/issues">Report Bug</a>
        **·**
        <a href="https://github.com/abxsantos/my-djangoq-scheduler/issues">Request Feature</a>
      </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is a very simple Django to demonstrate how to implement the task manager and scheduler Django Q.

This application also uses the Telegram API to provide an interacting interface with users.

The main logic behind this application is to register a `Client` into the database, using information from the telegram 
context. To register, the person must use the command `/register <provided cpf numbers>` passing in a valid CPF. This
will create a `Client` into the database with a pending cpf validation status.

The CPF will be validated using a Django Q `Task`, that is also created with the `Client`. 
This task, will request the 4devs API sending the registered client CPF and return a message to the user via telegram 
informing the CPF validation status.

A registered `Client` can also subscribe to receive an hourly message containing an activity from the bored API.

This is managed via a Django Q hourly `Scheduler`, that will request the bored API for a new activity 


### Built With

* [Django](https://docs.djangoproject.com/en/3.2/)
* [Django Q](https://django-q.readthedocs.io/en/latest/index.html)
* [python-telegram-bot](https://python-telegram-bot.readthedocs.io/en/stable/)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

To run this project you must either run it using [docker](https://docs.docker.com/get-docker/), or use [python version 3.9.5](https://www.python.org/downloads/) in your local environment.

If you are running locally, you must also provide a [PostgreSQL](https://www.postgresql.org/download/) database!

* Running with `docker`
  ```sh
  docker-compose up --build app
  ```
* Running locally
  ```sh
  pip install poetry
  poetry install
  bash scripts/start.sh
  ```

<!-- USAGE EXAMPLES -->
## Usage

After cloning the repository you need to start the application. 
To do that, you need to run the `start.sh` script.

> If you used docker-compose, when using `docker-compose up --build app` the command will already run the start script

The application interface is on the [telegram app](https://telegram.org/apps). 

1. Add the `@myscheduler_django_bot` in the telegram app.
2. Use the `/register <cpf>` command passing in a CPF number in the `<cpf>` field.
   
    Ex.: `/register 12345678910`
3. Subscribe to receive an hourly message with the `/subscribe` command. 
   For this to work you must have a used a register command.
4. To unsubscribe simply use the `/unsubscribe` command
5. To unregister, simple use the `/unregister` command.

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. 
Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/my_awesome_feature`)
3. Commit your Changes (`git commit -m 'feat: adds some Amazing Feature'`)
4. Push to the Branch (`git push origin feature/my_awesome_feature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Alexandre Xavier - ale.bxsantos@gmail.com

Project Link: [https://github.com/abxsantos/my-djangoq-scheduler](https://github.com/abxsantos/my-djangoq-scheduler)


