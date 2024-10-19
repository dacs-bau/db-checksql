# checksql service

Python service to check SQL statements against expected results.

## Build container

~~~sh
buildah unshare ./build-container.sh
~~~

## Run server locally 

~~~sh
pip install -e .
python -m checksql --host=127.0.0.1 --port=8080 --check demo/check.py
~~~

## Check with cURL

~~~sh
curl 'http://localhost:8080/api/v1/check-answer?pset=36-ansichten&pid=1&query=SELECT%0A++japanese_title+AS+%22Japanischer+Titel%22%2C%0A++english_title+AS+%22Englischer+Titel%22%0AFROM%0A++views%3B'
~~~

Other interesting queries:

~~~sh
curl 'http://localhost:8080/health-check'
curl 'http://localhost:8080/api/v1/known-checks'
~~~
