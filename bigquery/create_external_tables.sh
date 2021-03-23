bq mkdef \
  --autodetect \
  --source_format=NEWLINE_DELIMITED_JSON \
  --hive_partitioning_mode=AUTO \
  --hive_partitioning_source_uri_prefix=gs://warehouse-ticket-data/groups/ \
  gs://warehouse-ticket-data/groups/ingest_date=*/groups.json > groups.json

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
  --require_hive_partition_filter=True \
  gs://warehouse-ticket-data/tickets/ingest_date=*/tickets.json > tickets.json

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
  --require_hive_partition_filter=True \
  gs://warehouse-ticket-data/organizations/*json > organizations.json

bq rm -f -t \
 warehouse-302911:stream.organizations

bq mk \
  --external_table_definition=organizations.json \
  stream.organizations
