#!/bin/bash

# Import utils.
source $HERMES_HOME/bash/init.sh

# Main entry point.
main()
{
	log "UPDATING CONFIG"

	cp $PRODIGUER_DIR_TEMPLATES/hermes.json $PRODIGUER_DIR_CONFIG/hermes.json

	if [ $HERMES_MACHINE_TYPE = "dev" ]; then
		cp $PRODIGUER_DIR_TEMPLATES/mq-supervisord.conf $PRODIGUER_DIR_DAEMONS/mq/supervisord.conf
		cp $PRODIGUER_DIR_TEMPLATES/web-supervisord.conf $PRODIGUER_DIR_DAEMONS/web/supervisord.conf
	elif [ $HERMES_MACHINE_TYPE = "mq" ]; then
		cp $PRODIGUER_DIR_TEMPLATES/mq-supervisord.conf $PRODIGUER_DIR_DAEMONS/mq/supervisord.conf
	elif [ $HERMES_MACHINE_TYPE = "web" ]; then
		cp $PRODIGUER_DIR_TEMPLATES/web-supervisord.conf $PRODIGUER_DIR_DAEMONS/web/supervisord.conf
	fi

	log "UPDATED CONFIG"
}

# Invoke entry point.
main