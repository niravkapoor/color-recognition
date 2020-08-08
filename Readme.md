# Overview

* Project is all about detecting the name of the fruit from the uploaded image.
* User uploads the image and later cron job execute certain operation and update the name of the fruit.
* User can confirm whether the name processed is same as the fruit.

## Project Structure
Detect Fruit is having following:
1. detect_fruit : it contains the settings required to run the Django application.
2. opencv: contains the api, required to process the image.

## Technology Used

* **Python** : Python 3
* **Django Framework** : Django 3.0
* **PostgreSQL** : Database to store the infromation related to the uploaded images.
  * **psycopg2** : Version 2.8.5 , Package to connect to PostgreSQL.
* **Kafka** : Path of the uploaded image is stored in Kafka Queue. Later cron job process the images from the queue and save the name of the fruit detected in the image.
  * **kafka-python** : Version 2.0.1 , to connect to the kafka queue.
* **OpenCV** : OpenCV to process the image and detect the fruit's name from the image.
  **opencv-python**: Version 3.4.2, to use the open cv operation with python.
* **django-crontab**: Version 0.7.1, to register the cron job in crontab.

## Setup
* **Python3** : brew install python
* **module.txt** : File in root directory consist of packages required.
* **pip3 install -r module.txt** : To install all the packages
* **Kafka** : brew install kafka
* **PostgreSQL**: brew install postgresql

## Run
* **PostgreSQL**:  **brew services start postgresql** to start the Psql
* **Kafka** :
  * Start zookeeper : 
  ```bash
  /usr/local/bin/zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties.
  ```
  * Generally zookeeper.properties files exist under /usr/local/etc/kafka/ path
  * Start Kafka : 
  ```bash
  /usr/local/Cellar/kafka/2.5.0/libexec/bin/kafka-server-start.sh /usr/local/etc/kafka/server.properties
  ```
  * Depending on the version of the Kafka installed the path will get change accordingly.
* **Cron Job** : 
  * Register cron job : python3 [manage.py](manage.py) crontab add , will add the cron job.
  * File **[Cron.py](/opencv/cron.py)** -> **cron_job** process the kafka queue
  * **[Settings.py](/detect_fruit/settings.py)** , consist of  **CRONJOBS** setting. Currently it runs the job on every 10th minute. It will write the logs in **/var/log/cron.log** file.
  * **python3 [manage.py](manage.py) crontab show** : to list all the register jobs
  * **python3 [manage.py](manage.py) crontab remove** : to remove all the jobs
* **Run the server** : python3 [manage.py](manage.py) runserver. Open **http://127.0.0.1:8000/opencv**

## Fruit Detection Algo:
1. **Start** function in **InitDetect** class resize and crop the uploaded image.
2. App is using **L*a*b** color space to detect the fruit name.
3. **Find** function in **DetectColor** class converts the image from RGB to LAB.
4. Image is process by **label** function of **ColorLabeler** class.
5. **ColorLabeler** class consist of major color Dictionary with their fruit/color name.
6. **Euclidean** algorithm is used to find the minimum distance between mean color of the image and with each values of the color dictionary. One with min distance is returned as the name of the fruit in the image.

## Points
* **DEBUG = True** , in settings.py for development mode.
* **/opencv/run_job** : api endpoint to manually process the kafka queue

## Database
* Create a database with name **test**
* Run command to create table :
  * ```sql
    CREATE TABLE uploads
    (
        user_id bigint NOT NULL,
        is_verified boolean,
        id integer NOT NULL DEFAULT nextval('uploads_id_seq'::regclass),
        url character varying(1000),
        fruit_name character varying(500),
        ext character varying(10),
        CONSTRAINT uploads_pkey PRIMARY KEY (id)
    )
    ```
  * ```sql
    CREATE TABLE users
    (
        user_id integer NOT NULL DEFAULT nextval('users_user_id_seq'::regclass),
        phone bigint,
        name character varying,
        CONSTRAINT users_pkey PRIMARY KEY (user_id)
    )
    ```