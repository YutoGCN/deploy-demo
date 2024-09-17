from client_request import SolaClient
import time
import os
from tqdm import tqdm
from logging import getLogger, StreamHandler, DEBUG, INFO, Formatter
import re
import sys
import json

def main(parameters,*,logger):
    try:
        run_id = None
        # add job into the server
        try:
            run_id = SolaClient.request(parameters["material_folder"], parameters["user_name"], parameters["job_name"], json.dumps(parameters))
        except Exception as e:
            logger.error(f"Error ocurred while requesting job, {e}")
            logger.error("Prease retry")
            return
        else:
            logger.info(f"Job requested successfully, run_id: {run_id}")

        while 1:
            status = None
            for _ in range(5):
                try:
                    time.sleep(5)
                    status = SolaClient.get_status(run_id)
                except Exception as e:
                    logger.error("Error ocurred while getting status")
                else:
                    # network ok
                    break
                # network problem occured
            else:
                logger.error("Network error occured")
                return
            
            if "PENDING" == status:
                logger.info("Job is pending")
            else:
                logger.info("Job starts")
                break

        # checking the status of the job
        with tqdm(total=20) as pbar:
            while 1:
                status = None
                for _ in range(5):
                    try:
                        time.sleep(5)
                        status = SolaClient.get_status(run_id)
                    except Exception as e:
                        logger.error("Error ocurred while getting status")
                    else:
                        # network ok
                        break
                    # network problem occured
                else:
                    logger.error("Network error occured")
                    return

                if "RUNNING" in status:
                    numbers = re.search(r'\d+', status)
                    if numbers:
                        progress_i = int(numbers.group())
                        pbar.n = progress_i+1
                        pbar.refresh()
                elif "FINISHED" in status:
                    logger.info("Job finish detected")
                    break
                elif "ERROR" in status:
                    logger.info("Job failed")
                    break
        
        # get movie
        if status == "FINISHED":
            for _ in range(5):
                try:
                    SolaClient.get_movie(run_id, parameters["output_path"])
                except Exception as e:
                    logger.error("Error ocurred while getting movie")
                    logger.debug(f"{e}")
                else:
                    logger.info(f"Movie saved to {parameters['output_path']}")
                    break
            else:
                logger.error("Failed to get movie")
                return
    
    except KeyboardInterrupt:
        if run_id is None:
            logger.info("No job to terminate")
            return
        
        try: 
            SolaClient.terminate(run_id)
        except Exception as e:
            logger.error(f"Error ocurred while terminating job: {e}")
        else:
            logger.info(f"Job with run_id: {run_id} terminated")
        return
    
    except Exception as e:
        logger.error(f"Unexpected error ocurred: {e}")
        return
    
    else:
        logger.info("Job completed successfully")
        return

    

if __name__ == '__main__':
    # logger setting
    logger = getLogger(__name__)
    handler = StreamHandler()
    handler.setLevel(DEBUG)

    formatter = Formatter('[%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s ] %(message)s ')
    handler.setFormatter(formatter)

    logger.setLevel(DEBUG)
    logger.addHandler(handler)
    logger.propagate = False

    # main code parameter: params_comfy.json
    args = sys.argv
    if len(args) != 2:
        logger.error("Invalid arguments, give the parameter file")
        sys.exit(1)
    
    # load parameters
    parameters = None
    try:
        with open(args[1], "r") as f:
            parameters = json.load(f)
    except Exception as e:
        logger.error(f"Error ocurred while loading parameter file: {e}")
        sys.exit(1)

    main(parameters,logger=logger)