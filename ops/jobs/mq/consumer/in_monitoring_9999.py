# -*- coding: utf-8 -*-

"""
.. module:: run_in_monitoring_9999.py
   :copyright: Copyright "Apr 26, 2013", Institute Pierre Simon Laplace
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: Consumes monitoring 9999 messages.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from prodiguer import mq
from prodiguer.db import pgres as db

import utils



# MQ exhange to bind to.
MQ_EXCHANGE = mq.constants.EXCHANGE_PRODIGUER_IN

# MQ queue to bind to.
MQ_QUEUE = mq.constants.QUEUE_IN_MONITORING_9999


def get_tasks():
    """Returns set of tasks to be executed when processing a message.

    """
    return (
        _unpack_message_content,
        _persist_simulation_updates,
        _notify_api
        )


class ProcessingContextInfo(mq.Message):
    """Message processing context information.

    """
    def __init__(self, props, body, decode=True):
        """Object constructor.

        """
        super(ProcessingContextInfo, self).__init__(
            props, body, decode=decode)

        self.notify_api = False
        self.simulation_uid = None


def _unpack_message_content(ctx):
    """Unpacks message being processed.

    """
    ctx.simulation_uid = ctx.content['simuid']


def _persist_simulation_updates(ctx):
    """Persists simulation updates to db.

    """
    simulation = db.dao_monitoring.persist_simulation_02(
        ctx.msg.timestamp,
        True,
        ctx.simulation_uid
        )

    ctx.notify_api = simulation.name is not None


def _notify_api(ctx):
    """Dispatches API notification.

    """
    if not ctx.notify_api:
        return

    data = {
        "event_type": u"simulation_error",
        "simulation_uid": unicode(ctx.simulation_uid)
    }

    utils.dispatch_message(data, mq.constants.TYPE_GENERAL_API)

