bq mkdef \
  --autodetect \
  --source_format=NEWLINE_DELIMITED_JSON \
  --hive_partitioning_mode=AUTO \
  --hive_partitioning_source_uri_prefix=gs://warehouse-ticket-data/groups/ \
  gs://warehouse-ticket-data/groups/*/groups.json > groups.json

bq rm -f -t \
 warehouse-302911:stream.groups

bq mk \
  --external_table_definition=groups.json \
  stream.groups


bq mkdef \
  --autodetect \
  --source_format=NEWLINE_DELIMITED_JSON \
  --hive_partitioning_mode=AUTO \
  --hive_partitioning_source_uri_prefix=gs://warehouse-ticket-data/tickets/ \
  gs://warehouse-ticket-data/tickets/*/tickets.json > tickets.json

bq rm -f -t \
 warehouse-302911:stream.tickets

bq mk \
  --external_table_definition=tickets.json \
  stream.tickets

bq mkdef \
  --autodetect \
  --source_format=NEWLINE_DELIMITED_JSON \
  --hive_partitioning_mode=AUTO \
  --hive_partitioning_source_uri_prefix=gs://warehouse-ticket-data/organizations/ \
  gs://warehouse-ticket-data/organizations/*/organizations.json > organizations.json

bq rm -f -t \
 warehouse-302911:stream.organizations

bq mk \
  --external_table_definition=organizations.json \
  stream.organizations

bq mkdef -i \
  --source_format=NEWLINE_DELIMITED_JSON \
  --hive_partitioning_mode=AUTO \
  --hive_partitioning_source_uri_prefix=gs://warehouse-ticket-data/organizations/ \
  gs://warehouse-ticket-data/users/*/users.json \
  id:INTEGER,url:STRING,name:STRING,email:STRING,created_at:STRING,updated_at:STRING,time_zone:STRING,iana_time_zone:STRING,phone:STRING,shared_phone_number:BOOLEAN,locale_id:INTEGER,locale:STRING,organization_id:INTEGER,role:STRING,verified:BOOLEAN,external_id:INTEGER,alias:STRING,active:BOOLEAN,shared:BOOLEAN,shared_agent:BOOLEAN,last_login_at:STRING,two_factor_auth_enabled:BOOLEAN,signature:STRING,details:STRING,notes:STRING,role_type:INTEGER,custom_role_id:INTEGER,moderator:BOOLEAN,ticket_restriction:STRING,only_private_comments:BOOLEAN,restricted_agent:BOOLEAN,suspended:BOOLEAN,chat_only:BOOLEAN,default_group_id:INTEGER,report_csv:BOOLEAN > users.json

bq rm -f -t \
 warehouse-302911:stream.users

bq mk \
  --external_table_definition=users.json \
  stream.users

