#!/bin/bash
DOCKERNAME="Inventory-Backend"
REPONAME="new_inventory"
CLONELINK="https://github.com/shubhamm033/new_inventory"
RUNSCRIPT=$REPONAME/run.py

docker exec -d $DOCKERNAME /bin/sh -c "pkill -SIGINT python;rm -rf "$REPONAME"/;git clone "$CLONELINK";echo "$PWD";python3.5 "$RUNSCRIPT