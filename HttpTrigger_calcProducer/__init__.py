import logging
import random
import datetime
import json
import requests
import os

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    base = int(req.params.get('base'))
    exp = int(req.params.get('exp'))

    run_id = random.randint(1, 999999)

    results = []
    
    for num in range(2, exp+1):
        event_id = random.randint(1, 999999)
        event= {
            "id": event_id,
            "eventType": "recordInserted",
            "subject": "demo/calc/exp",
            "eventTime": f"{datetime.datetime.now()}",
            "data": { 
                "base": base, 
                "exp": num, 
                "total": exp-1,
                "runId": run_id
            },
            "dataVersion": "1.0"
        }

        eg_endpoint = os.environ.get("eghost")
        eg_key =  os.environ.get("egkey")
        
        event_str = "[" + json.dumps(event) + "]"

        logging.warn(event_str)
        r = requests.post(eg_endpoint, data=event_str, headers={"aeg-sas-key": eg_key})
        result = {
            "requestId": event_id,
            "event": event_str,
            "responseCode": r.status_code
        }
        results.append(result)

    return(json.dumps(results))