"""
Entry function
"""

import logging

import azure.functions as func
import azure.durable_functions as df


async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:

    client = df.DurableOrchestrationClient(starter)

    payload = req.get_json()
        
    if payload:

        instance_id = await client.start_new(req.route_params["functionName"], None, payload)
        
        logging.info(f"Started orchestration with ID = '{instance_id}'.")
                        
        return client.create_check_status_response(req, instance_id)

    return client._create_http_response(202, 'no image')