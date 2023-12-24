# Youtube Watch History Analyzer

Django project that allows you to upload your YouTube watch history in json format.

After file being processed, you can visualize your watch history.

Insights about your interests and how they have changed over the years.


## Contents
- [Run Locally](#run-locally)
    - [Run Tests](#run-tests)
    - [.env File](#env-file)
- [Get json YouTube History](#get-json-youtube-history)
- [Porject Architecture](#project-architecture)
    - [Technologies](#technologies)
    - [Project Logic](#project-logic)
    - [Databases](#databases)
       - [PostgreSQL](#postgresql)
       - [MongoDB](#mongodb)
    - [Docker](#docker)
    - [Visualization](#visualization)
- [Project Future](#project-future)
- [Lessons Learned](#lessons-learned)
- [References](#references)

## Run Locally
You can run this project locally using docker compose.
    
1. Have pre-installed docker.
2. Clone this repository.
3. Open project directory.
4. Fill .env file according to .env.example.
   1. Django secret key can be generated using secret.py script.
      ```bash
      python secret.py
      ```
   2. YouTube API you can get from [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
       Step-by-step guide: [Get API key Guide link](docs%2Fget-youtube-api-guide%2Fget-yb-api-guide.md)
5. Amazing! Now you can run this project using docker compose.
    ```bash
    docker compose up --build
    ```
6. Open http://localhost:8000/ in your browser.

## .env File
You can fill .env file according to .env.example

| Variable name          | Description                                                                                                                                                                                                   |
|------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DJANGO_SECRET_KEY      | Django secret key can be generated using secret.py script. <br>```python secret.py```                                                                                                                         |
| API_KEY                | YouTube API you can get from [Google Cloud Console](https://console.cloud.google.com/apis/credentials). <br> Step-by-step guide: [Get API key Guide link](docs%2Fget-youtube-api-guide%2Fget-yb-api-guide.md) |
| Postgres Variables     |                                                                                                                                                                                                               |
| MongoDB Variables      |                                                                                                                                                                                                               |

### Run Tests
If you want to run tests without docker:
1. Have running PostgreSQL database.
2. Fill .env file according to .env.example. (No need to fill YouTube API key)
3. Run tests
    ```bash
    python manage.py test
    ```

## Get json YouTube History
Handy step-by-step guide how to get json YouTube history you can find here:
[History Export Guide link](docs%2Fhistory-export-guide%2Fexport-guide.md)

## Project Architecture

### Technologies
* Django 
* PostgreSQL, MongoDB
* RabbitMQ, Celery
* Docker, Docker Compose
* Plotly
* Bootstrap

### Project Logic
![project_logic.png](docs%2Fproject_logic.png)

### Databases
#### PostgreSQL
Is used as main database. Stores processed data.

DB designed in way that info about video is stored independently of user. 
This allows us to not gather the same data each time.

| Model                         | Description                                                   |
|-------------------------------|---------------------------------------------------------------|
| *WatchRecord model*           | 'User watched some video at some time'                        |
| *UserProfile (Or File) model* | 'Uploaded file in mongodb'. <br/>Relates to website user.     |
| *Video model*                 | 'YouTube video'                                               |
| *Channel model*               | 'YouTube channel'                                             |
| *Category model*              | 'YouTube video category'. <br/>Predefined list of categories. |


*Image doesn't contain django generated default tables.*
![postgresql.png](docs%2Fpostgresql.png)

#### MongoDB
Is used as history object storage from Json.
- *File* - 'Uploaded file'.
    - status: True each video's status is True (Proceeded).
- *Video* - 'Watch Record json object'.
    - host: Relates to File.
    - status: True if video is proceeded.

![mongodb.png](docs%2Fmongodb.png)

### Docker
For this project was used docker compose to run web, postgres, mongodb, rabbitmq and celery containers.
Dockerfiles and entrypoint scripts was used for better container management and automation.
For better configurability was used environment variables.
Helpful guide for docker compose [1].

### Visualization
Different charts are used to visualize our processed data.
Using plotly on backend we generate charts and send them to frontend.
Useful article about watch history analysis [2], [3].

## Project Future
What to improve:
* Better UI.
* Use another YouTube API to get more info for analysis.
* Add more charts.

## Lessons Learned
This project had a big impact on my knowledge of Django and Docker.

App and databases architecture design practice.

Learned how to use workers (RabbitMQ and Celery).

Run server on virtual machine using OpenStack.
    
## References

References
* [1] Saúl Buentello. Explore your activity on youtube with r: How to analyze and visualize
your personal data history. online. [cit. 2023–12–24] https://towardsdatascience.com/explore-your-activity-on-youtube-with-r-how-to-analyze-and-visualize-your-personal-data-histo
* [2] neerajb22. My youtube history analysis. online. [cit. 2023–12–24] https://jovian.com/neerajb22/my-youtube-history-analysis.
* [3] Jan Žižka. My youtube history analysis. online, 1415. [cit. 2020–02–09] http://zizka.trocnov/husiti/conspiration.pdf.