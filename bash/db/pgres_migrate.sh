source $HERMES_HOME/bash/init.sh

log "DB : migrating postgres db ..."

psql -U hermes_db_admin -d $HERMES_DB_PGRES_NAME -q -f $HERMES_HOME/bash/db/sql/pgres_migrate-1-0-2-3-0.sql
psql -U hermes_db_admin -d $HERMES_DB_PGRES_NAME -q -f $HERMES_HOME/bash/db/sql/pgres_migrate-1-0-2-3-1.sql

log "DB : migrated postgres db"
