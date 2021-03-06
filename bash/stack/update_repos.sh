#!/bin/bash

# Import utils.
source $HERMES_HOME/bash/utils.sh

# Installs a git repo.
_install_repo()
{
	log "Installing repo: $1"

	rm -rf $HERMES_DIR_REPOS/$1
	git clone -q $HERMES_GITHUB/$1.git $HERMES_DIR_REPOS/$1
}

# Updates a git repo.
_update_repo()
{
	log "Updating repo: $1"

	set_working_dir $HERMES_DIR_REPOS/$1
	git pull -q
	remove_files "*.pyc"
	set_working_dir
}

# Main entry point.
main()
{
	log "UPDATING REPOS"

	for repo in "${HERMES_REPOS[@]}"
	do
		if [ -d "$HERMES_DIR_REPOS/$repo" ]; then
			_update_repo $repo
		else
			_install_repo $repo
		fi
	done

	log "UPDATED REPOS"
}

# Invoke entry point.
main
