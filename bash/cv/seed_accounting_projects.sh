#!/bin/bash

# Import utils.
source $HERMES_HOME/bash/init.sh

# Main entry point.
main()
{
	log "Seeding cv termset: accounting project ..."
	activate_venv server
	python $HERMES_DIR_JOBS/cv/run_seed_accounting_projects.py
}

# Invoke entry point.
main