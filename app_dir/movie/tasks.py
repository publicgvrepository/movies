from __future__ import absolute_import, unicode_literals

import csv
from decimal import Decimal
from re import IGNORECASE, fullmatch, sub

import pandas as pd
from app_dir.movie.models import Movie
from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import IntegrityError, transaction

logger = get_task_logger(__name__)


def valid_money_string(money):
    if fullmatch(r"[\D]{1,3} [\d]+(\.[\d]+)?", money, flags=IGNORECASE):
        return True
    else:
        return False


def money_value(money) -> Decimal:
    money = Decimal(0)
    if type(money) is str:
        if valid_money_string(money):
            money = Decimal(sub(r'[^\d\.]+', '', money))
    return money


def money_currency(currency):
    if (type(currency) is str) and valid_money_string(currency):
        return sub(r"[\d \.]+", "", currency, flags=0)
    else:
        return ""


@shared_task(bind=True)
def task_validating_csv(self, name: str):
    logger.info(f"CVS validator: {name}")
    try:
        df = pd.read_csv(name)
        df = df[['imdb_title_id', 'title', 'country', 'budget']]
        df['currency'] = df.apply(
            lambda row: money_currency(row['budget']), axis=1)
        df['budget'] = df['budget'].apply(money_value)
        df.to_csv(name)
    except Exception as e:
        logger.error(f"CVS validator: Reason  {str(e)}")
        raise Exception("Error on csv validation")


@shared_task
def task_transaction_test(name: str):
    """
    """
    try:
        with open(name, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            with transaction.atomic():
                for row in csv_reader:
                    logger.info(
                        f"Saving: {row['imdb_title_id']} {row['title']}\n")
                    Movie.objects.create(
                        imdb_title_id=row['imdb_title_id'],
                        title=row['title'],
                        country=row['country'],
                        budget=row['budget'],
                        currency=row['currency']
                    )
            logger.info(f"Movies on {name} loaded")
    except IntegrityError as e:
        logger.error(f"CVS loader: IntegrityError  {str(e)}")
        raise Exception("Error loadding movies")
    except Exception as e:
        logger.error(f"CVS loader: Reason  {str(e)}")
        raise Exception("Error loadding movies")


@shared_task
def error_handler(request, exc, traceback):
    logger.error(
        "--\n\nRAISED EXCEPTION: {0} {1} {2}".format(request.id, exc, traceback))
