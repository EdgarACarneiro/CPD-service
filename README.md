# CPD-service

A microservice to run the Coherent Point Drift (CPD) method.

## Example request

Example of a request to this microservice:
```shell
curl -d '{"X": [[10, 10],[10, 11],[11, 11],[11, 10]], "Y": [[0, 0],[0, 1],[1, 1],[1, 0]]}' -H "Content-Type: application/json" -X POST http://localhost:5000/cpd
```
* __X__: represents the target point set
* __Y__: represents the moving point set (the one to be altered)

The respective response, in json:
```json
{
    "rotation": 0.0,
    "scale": 0.002487577505966565,
    "translation": [10.498756211247015, 10.498756211247013]
}
```

## Running Instructions

* Using Docker:
```shell
docker build -t cpd-service . --no-cache
docker run -p 5000:5000 cpd-service
```

* Using command line:
```
python -m venv venv
. venv/bin activate
sh init.sh
```