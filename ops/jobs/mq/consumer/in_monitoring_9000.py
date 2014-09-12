# -*- coding: utf-8 -*-

"""
.. module:: run_in_monitoring_9000.py
   :copyright: Copyright "Apr 26, 2013", Institute Pierre Simon Laplace
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: Consumes monitoring 9000 messages.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
from prodiguer import mq



# MQ exhange to bind to.
MQ_EXCHANGE = mq.constants.EXCHANGE_PRODIGUER_IN

# MQ queue to bind to.
MQ_QUEUE = mq.constants.QUEUE_IN_MONITORING_9000


# Message information wrapper.
class Message(mq.Message):
    """Message information wrapper."""
    def __init__(self, props, body):
        """Constructor."""
        super(Message, self).__init__(props, body, decode=True)

        self.simulation = None
        self.simulation_name = self.content['simuid']


def get_tasks():
    """Returns set of tasks to be executed when processing a message."""
    return _update_simulation_state


def _update_simulation_state(ctx):
    """Updates simulation status."""
    utils.update_simulation_state(ctx.simulation_name,
                                  db.constants.EXECUTION_STATE_ROLLBACK)