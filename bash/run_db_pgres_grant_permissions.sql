/* Grant schema permissions */
GRANT USAGE ON SCHEMA monitoring, mq, shared TO prodiguer_db_user;

/* Grant table permissions */
GRANT INSERT, UPDATE, DELETE, SELECT ON ALL TABLES IN SCHEMA monitoring TO prodiguer_db_user;
GRANT INSERT, UPDATE, DELETE, SELECT ON ALL TABLES IN SCHEMA mq TO prodiguer_db_user;
GRANT INSERT, UPDATE, DELETE, SELECT ON ALL TABLES IN SCHEMA shared TO prodiguer_db_user;

/* Grant sequence permissions */
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA monitoring TO prodiguer_db_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA mq TO prodiguer_db_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA shared TO prodiguer_db_user;