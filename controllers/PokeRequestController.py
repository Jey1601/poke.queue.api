import json
import logging


from fastapi import HTTPException
from models.PokeRequest import PokeRequest
from utils.database import execute_query_json
from utils.AQueue import AQueue

#Configuración del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def select_pokemon_request(id : int) :
    try:  
        query = "select * from pokequeue.requests where id = ?"
        params = (id,)
        result = await execute_query_json(query, params)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        logger.error(f"Error updating Pokemon request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



async def update_pokemon_request(poke_request: PokeRequest) -> dict:
    try:  
        query = "exec pokequeue.update_poke_request ?, ?, ?"

        if not poke_request.url:
            poke_request.url = "";

        params = (poke_request.id, poke_request.status, poke_request.url, )
        result = await execute_query_json(query, params, True)
        result_dict = json.loads(result)
        

        return result_dict
    except Exception as e:
        logger.error(f"Error updating Pokemon request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



async def insert_pokemon_request(poke_request: PokeRequest) -> dict:
    try:  
        query = "exec pokequeue.create_poke_request ? "
        params = (poke_request.pokemon_type,)
        result = await execute_query_json(query, params, True)
        result_dict = json.loads(result)
        
        await AQueue().insert_message_on_queue(result)

        return result_dict
    except Exception as e:
        logger.error(f"Error inserting Pokemon request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def get_all_request() -> dict:
    query = """
        select 
            r.id as ReportId
            , s.description as Status
            , r.type as PokemonType
            , r.url 
            , r.created 
            , r.updated
        from pokequeue.requests r 
        inner join pokequeue.status s 
        on r.id_status = s.id 
    """
    result = await execute_query_json( query  )
    result_dict = json.loads(result)
    blob = ABlob()
    for record in result_dict:
        id = record['ReportId']
        record['url'] = f"{record['url']}?{blob.generate_sas(id)}"
    return result_dict

