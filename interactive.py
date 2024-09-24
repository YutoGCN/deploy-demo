from client_request import SolaClient
from logging import getLogger, StreamHandler, DEBUG, INFO, Formatter
import time
import os
import sys
import json

# USER_NAME = 'lvm_ngc'

def main(parameters,*,logger):
    mode = input('Enter mode (1: request, 2: list, 3: status, 4: download, 5: terminate): ')
    
    # load parameter from json file
    material_folder = parameters["material_folder"]
    USER_NAME = parameters["user_name"]
    job_name = parameters["job_name"]
    output_path = parameters["output_path"]
    params_comfy_path = json.dumps(parameters)
    

    if mode == '1':
        try:
            run_id = SolaClient.request(material_folder, USER_NAME, job_name, params_comfy_path)
        except ValueError as e:
            logger.error("Error ocurred while requesting job")
            logger.error("Prease retry")
        else:
            logger.info("Job requested successfully")
            logger.info(f"run_id: {run_id}")
    elif mode == '2':
        try:
            jobs = SolaClient.list_jobs_by_user(USER_NAME)
        except ValueError as e:
            logger.error("Error ocurred while getting job list")
            logger.error("Prease retry")
        else:
            logger.info(f"Jobs: {jobs}")
    elif mode == '3':
        run_id = input('Enter run_id: ')
        try:
            status = SolaClient.get_status(run_id)
        except ValueError as e:
            logger.error("Error ocurred while getting status")
            logger.error("Prease retry")
        else:
            logger.info(f"Status: {status}")
    elif mode == '4':
        run_id = input('Enter run_id: ')
        try:
            output_path = SolaClient.get_movie(run_id, output_path)
        except ValueError as e:
            logger.error("Error ocurred while downloading movie")
            logger.error("Prease retry")
        else:
            if output_path is None:
                logger.info("Job is not finished yet or failed")
                return
            logger.info(f"Movie downloaded to {output_path}")
    elif mode == '5':
        run_id = input('Enter run_id: ')
        try:
            SolaClient.terminate(run_id)
        except ValueError as e:
            logger.error("Error ocurred while terminating job")
            logger.error("Prease retry")
        else:
            logger.info("Job terminated successfully")
    else:
        logger.error("Invalid mode")

if __name__ == '__main__':
    logger = getLogger(__name__)
    handler = StreamHandler()
    handler.setLevel(DEBUG)

    formatter = Formatter('[%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s ] %(message)s ')
    handler.setFormatter(formatter)

    logger.setLevel(DEBUG)
    logger.addHandler(handler)
    logger.propagate = False

    args = sys.argv
    if len(args) != 2:
        logger.error("Invalid arguments")
        sys.exit(1)

    # load parameters
    parameters = None
    try:
        with open(args[1], "r") as f:
            parameters = json.load(f)
    except Exception as e:
        logger.error(f"Error ocurred while loading parameter file: {e}")
        sys.exit(1)

    main(parameters,logger = logger)