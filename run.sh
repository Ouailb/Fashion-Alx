#!/bin/bash
./stop_all.sh
echo "Try to run api..."
HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=ecom_db python3   -m api.api > /dev/null 2>&1 &

sleep 1
echo "Try to run app.py..."
python3 app.py  > /dev/null 2>&1 &
sleep 1
echo "done!"
