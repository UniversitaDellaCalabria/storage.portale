Ricerca Unical
--------------

![CI build](https://travis-ci.org/UniversitaDellaCalabria/Ricerca.svg?branch=master)
![Python version](https://img.shields.io/badge/license-Apache%202-blue.svg)
![License](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7%203.8%203.9-blue.svg)

Servizio di interoperabilità dei dati.


#### OpenAPI v3

https://teamdigitale.github.io/api-oas-checker/?url=https://thaturl/openapi?format=openapi-json


#### OpenAPI v3 AGID

````
python manage.py generateschema --format openapi_agid --generator_class rest_framework.schemas.openapi_agid.AgidSchemaGenerator | head -n 23
````

url: https://thaturl/openapi?format=openapi-json


#### Risorse

 - https://github.com/teamdigitale/api-oas-checker
 - https://docs.italia.it/italia/piano-triennale-ict/lg-modellointeroperabilita-docs/it/bozza/doc/profili-di-interazione/regole-comuni-rest-soap.html#definire-format-quando-si-usano-i-tipi-number-ed-integer
 - https://www.agid.gov.it/it/infrastrutture/sistema-pubblico-connettivita/il-nuovo-modello-interoperabilita
 - https://columbia-it-django-jsonapi-training.readthedocs.io/en/latest/documenting-api.html#why-an-oas-3-0-schema
 - https://djangoadventures.com/django-rest-framework-openapi-3-support/
 - https://github.com/tfranzel/drf-spectacular
