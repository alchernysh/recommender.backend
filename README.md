# Recommender training

This repo is part of recommender project. It contains code for backend service.

## Requirements

- Ubuntu >= 18.04
- Python >= 3.8

## Installation

If you are using *pip* run command below to install python dependencies.

```shell
pip3 install -r requirements.txt
```

If you are using *Pipenv* you can install dependencies by command:

```shell
 pipenv install
```

You need install PostgreSQL server:

```
sudo apt install postgresql postgresql-contrib
```

Besides you need install redisai server for serving model.

## Usage

Firstly you need download [model](https://drive.google.com/file/d/1DfnrxVJDIA5ZaWliYFjI90NwfSXhvRLE/view?usp=sharing) and [embeddings file](https://drive.google.com/file/d/1SlsGTj3B6DfdIrJT3ViJLtK-DlUy8KpG/view?usp=sharing) and place them to folder `resources`. Besides you need download [Bert weights](http://files.deeppavlov.ai/deeppavlov_data/bert/sentence_ru_cased_L-12_H-768_A-12_pt.tar.gz) for russian language and place it to folder `resources`.

Also you need apply migrations:

```shell
python3 manage.py migrate
```


After this you need load ONNX model to redisai. To do this run command:

```shell
python3 load_model.py
```

Besides you need run scheduler for loading of new articles to database.

```shell
python manage.py runapscheduler
```

After all of this you can start django server:

```shell
python manage.py runserver
```
