from logging import exception

from backend.celery import app
from networks.models import Network, LandingNetwork
from .services.functions import update_pools_apr, update_max_pools_apr, update_eternal_farmings_max_apr, update_eternal_farmings_apr, update_limit_farmings_apr
from .services.landing import update_dex_data, update_bb_data

@app.task()
def update_pools_apr_task():
    for network in Network.objects.all():
        try:
            update_pools_apr(network)
        except Exception as exception_error:
            exception(
                f'~~~~~~~~~~~~~~~\n{exception_error}\n~~~~~~~~~~~~~~~'
            )

@app.task()
def update_max_pools_apr_task():
    for network in Network.objects.all():
        try:
            update_max_pools_apr(network)
        except Exception as exception_error:
            exception(
                f'~~~~~~~~~~~~~~~\n{exception_error}\n~~~~~~~~~~~~~~~'
            )

@app.task()
def update_eternal_farmings_apr_task():
    for network in Network.objects.all():
        try:
            update_eternal_farmings_apr(network)
        except Exception as exception_error:
            exception(
                f'~~~~~~~~~~~~~~~\n{exception_error}\n~~~~~~~~~~~~~~~'
            )

@app.task()
def update_eternal_farmings_max_apr_task():
    for network in Network.objects.all():
        try:
            update_eternal_farmings_max_apr(network)
        except Exception as exception_error:
            exception(
                f'~~~~~~~~~~~~~~~\n{exception_error}\n~~~~~~~~~~~~~~~'
            )


@app.task()
def update_limit_farmings_apr_task():
    for network in Network.objects.all():
        try:
            update_limit_farmings_apr(network)
        except Exception as exception_error:
            exception(
                f'~~~~~~~~~~~~~~~\n{exception_error}\n~~~~~~~~~~~~~~~'
            )

@app.task()
def update_dex_data_task():
    for network in LandingNetwork.objects.all():
        try:
            update_dex_data(network)
        except Exception as exception_error:
            exception(
                f'~~~~~~~~~~~~~~~\n{exception_error}\n~~~~~~~~~~~~~~~'
            )

@app.task()
def update_bb_data_task():
    try:
        update_bb_data()
    except Exception as exception_error:
        exception(
            f'~~~~~~~~~~~~~~~\n{exception_error}\n~~~~~~~~~~~~~~~'
        )