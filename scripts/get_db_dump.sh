#!/bin/bash
set -ev

LOCAL_ENV_LOCATION=$PWD/.env
echo $LOCAL_ENV_LOCATION
source $LOCAL_ENV_LOCATION

mongoexport -h $DB_URL:$DB_PORT -d $DB_NAME -c $STUD_16_COLL -u $DB_USER -p $DB_PASS -o $OUTPUT_DIR/$STUD_16_COLL.json --jsonArray --pretty

mongoexport -h $DB_URL:$DB_PORT -d $DB_NAME -c $STUD_17_COLL -u $DB_USER -p $DB_PASS -o $OUTPUT_DIR/$STUD_17_COLL.json --jsonArray --pretty

mongoexport -h $DB_URL:$DB_PORT -d $DB_NAME -c $TABLE_COLL -u $DB_USER -p $DB_PASS -o $OUTPUT_DIR/$TABLE_COLL.json --jsonArray --pretty
