# candidatos-query

El microservicio candidatos-query permite consultar y listar información de candidatos...


## API 

|                     | Método | Ruta                         | Params | Headers | Body |   
|---------------------|--------|------------------------------|--------|---------|------|
| Consultar Candidato | GET    | /candidates-query/{id}/tests | id: identificador del candidato | Authorization: Bearer token |  |  
| Health Check        | GET    | /candidates-query/ping       |        |         |      |  


## Pruebas 

1. Pruebas unitarias locales
```
cd offers
python -m unittest discover -s tests -v
```

2. Pruebas unitarias locales con coverage sobre el 80%
```
cd offers
pipenv run pytest --cov=. -v -s --cov-fail-under=80
```

3. Pipeline pruebas unitarias con coverage sobre el 80%

El archivo **ci_pipeline.yml** ubicado en la ruta github\workflows contiene el pipeline que ejecuta las pruebas y valida el coverage cuando se realiza un pull request para integrar en **main** la rama **develop** 
