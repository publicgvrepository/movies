from __future__ import absolute_import, unicode_literals

from celery import shared_task

from django.db import transaction
import csv
import pandas as pd
from re import sub, fullmatch, IGNORECASE
from math import isnan
from decimal import Decimal

from .models import Movie

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


def valid_money_string(money):
    if fullmatch(r"[\D]{1,3} [\d]+(\.[\d]+)?", money, flags=IGNORECASE):
        return True
    else:
        return False


def money_value(money):
    if type(money) is float:
        if isnan(money):
            money = 0
    elif type(money) is str:
        if valid_money_string(money):
            money = Decimal(sub(r'[^\d\.]+', '', money))
        else:
            money = 0
    else:
        money = 0
    return money


def money_currency(currency):
    if (type(currency) is str) and valid_money_string(currency):
        return sub(r"[\d \.]+", "", currency, flags=0)
    else:
        return ""


@shared_task()
def task_validating_csv(name: str):
    df = pd.read_csv(name)
    df = df[['imdb_title_id', 'title', 'country', 'budget']]
    df['currency'] = df.apply(
        lambda row: money_currency(row['budget']), axis=1)
    df['budget'] = df['budget'].apply(money_value)
    df.to_csv(name)
    logger.info(f"csv tested :) ----------------> {name}")


@shared_task()
def task_transaction_test(name: str):
    """
    """
    with open(name, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        with transaction.atomic():
            for row in csv_reader:
                logger.info(f'saving: {row}\n')
                Movie.objects.create(
                    imdb_title_id=row['imdb_title_id'],
                    title=row['title'],
                    country=row['country'],
                    budget=row['budget'],
                    currency=row['currency']
                )
        logger.info(f"movies loaded :) {name}")
