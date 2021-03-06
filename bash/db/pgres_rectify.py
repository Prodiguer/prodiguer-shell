# -*- coding: utf-8 -*-

"""
.. module:: monitoring_job_end.py
   :copyright: Copyright "Mar 21, 2015", Institute Pierre Simon Laplace
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: Consumes monitoring job end messages.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import logging

import pika

from hermes import cv
from hermes.db import pgres as db
from hermes.db.pgres import dao_mq
from hermes.utils import logger
from hermes_jobs.mq import metrics
from hermes_jobs.mq import monitoring
from hermes_jobs.mq import supervision
from hermes_jobs.mq.utils import invoke as invoke_handler



# Set logging options.
logging.getLogger("pika").setLevel(logging.ERROR)
logging.getLogger("requests").setLevel(logging.ERROR)

# Map of message types to processing agents.
_AGENTS = {
    u"0000": monitoring.job_start,
    u"1000": monitoring.job_start,
    u"2000": monitoring.job_start,
    u"7010": metrics.conso_project,
    u"8000": supervision.detect_late_job,
    u"8888": monitoring.simulation_delete,
}


def _get_message():
    """Returns a message that previously failed.

    """
    m = db.types.Message

    qry = db.session.query(m)
    qry = qry.filter(m.is_queued_for_reprocessing == True)

    return qry.first()


def _reprocess_message(m, verbose):
    """Reprocesses a message.

    """
    # Set message agent.
    if m.type_id not in _AGENTS:
        raise KeyError("Unsupported message re-processing agent: {}".format(m.type_id))
    agent = _AGENTS[m.type_id]

    # Set message AMPQ properties.
    props = pika.BasicProperties(
        app_id=m.app_id,
        content_type=m.content_type,
        content_encoding=m.content_encoding,
        headers={
            'producer_id': m.producer_id
        },
        message_id=m.uid,
        type=m.type_id,
        user_id=m.user_id
        )

    # Set processing context information.
    ctx = agent.ProcessingContextInfo(props, m.content, validate_props=False)
    ctx.msg = m

    # Invoke processing tasks.
    for task in agent.get_tasks():
        task(ctx)
        if ctx.abort:
            break


def _main(throttle):
    """Main entry point.

    """
    # Initialise cv session.
    cv.session.init()

    # Re-process messages.
    reprocessed = 0
    verbose = throttle > 0
    while True if throttle == 0 else reprocessed < throttle:
        with db.session.create():
            # Dequeue next message to be re-processed.
            m = _get_message()
            if m is None:
                logger.log_mq("reprocessing complete")
                return

            if verbose:
                logger.log_mq("reprocessing message: {} :: {} :: {}".format(m.type_id, m.uid, m.correlation_id_1))

            # Perform message processing.
            try:
                _reprocess_message(m, verbose)
            except Exception as err:
                err = "{} --> {}".format(err.__class__.__name__, err)
                logger.log_mq_error(err)
                db.session.rollback()
                m.processing_error = unicode(err)
            else:
                if verbose:
                    logger.log_mq("message reprocessed: {} :: {}".format(m.uid, m.correlation_id_1))
                m.processing_error = None
            finally:
                m.processing_tries += 1
                m.is_queued_for_reprocessing = False
                db.session.update(m)

            # Increment counter.
            reprocessed += 1


# Main entry point.
if __name__ == '__main__':
    args = argparse.ArgumentParser("Rectifies message processing errors.")
    args.add_argument(
        "-t", "--throttle",
        help="Limit upon number of message to re-process.",
        dest="throttle",
        type=int,
        default=0
        )
    args = args.parse_args()

    _main(args.throttle)
