#!/bin/bash

# Nightly maintenance script
# Add to the crontab as
#
#    0 0 * * * /path/to/script/nightly.sh

DATABASE = "../data/database.db"

sqlite3 $DATABASE "UPDATE Prescriptions SET cur_dose=0;"

