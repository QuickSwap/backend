from logging import exception

from backend.celery import app
from networks.models import Network, LendingNetwork
from .services.functions import update_pools_apr, update_dex_data, update_max_pools_apr, update_eternal_farmings_max_apr, update_eternal_farmings_apr, update_limit_farmings_apr


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
    for network in LendingNetwork.objects.all():
        try:
            update_dex_data(network)
        except Exception as exception_error:
            exception(
                f'~~~~~~~~~~~~~~~\n{exception_error}\n~~~~~~~~~~~~~~~'
            )