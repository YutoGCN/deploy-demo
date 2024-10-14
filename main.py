from client_request import SolaClient
import time
import os
from tqdm import tqdm
from logging import getLogger, StreamHandler, DEBUG, INFO, Formatter
import re
import sys
import json
import argparse

def main(parameters, run_id, no_request, *, logger):
    try:
        # If not using --no_request, request a new job
        if not no_request:
            # Add a new job to the server
            try:
                run_id = SolaClient.request(
                    parameters["material_folder"],
                    parameters["user_name"],
                    parameters["job_name"],
                    json.dumps(parameters)
                )
            except Exception as e:
                logger.error(f"Error occurred while requesting the job: {e}")
                logger.error("Please retry.")
                return
            else:
                logger.info(f"Job requested successfully. run_id: {run_id}")
        else:
            if run_id is None:
                # If --run_id is not provided, prompt the user to input it
                run_id = input("Please enter the existing job's run_id: ").strip()
                if not run_id:
                    logger.error("No run_id was entered. Exiting the program.")
                    return
            logger.info(f"Using existing run_id: {run_id}")

        while True:
            status = None
            for _ in range(5):
                try:
                    time.sleep(5)
                    status = SolaClient.get_status(run_id)
                except Exception as e:
                    logger.error("Error occurred while fetching the status.")
                else:
                    # Network is okay
                    break
                # Network problem occurred
            else:
                logger.error("Network error occurred.")
                return

            if status in ["PENDING", "UPLOADING", "INSTANCE_INIT"]:
                logger.info("Job is pending.")
            elif "TERMINATED" in status:
                logger.info("Job has been terminated.")
                return
            elif "ERROR" in status:
                logger.error("Job failed.")
                return
            elif "FINISHED" in status:
                logger.info("Job has already finished.")
                break
            elif "RUNNING" in status:
                logger.info("Job is running.")
                break
            else:
                logger.error("Unknown status, please report: {status}")
                return

        # Check the job status
        with tqdm(total=20) as pbar:
            while True:
                status = None
                for _ in range(5):
                    try:
                        time.sleep(5)
                        status = SolaClient.get_status(run_id)
                    except Exception as e:
                        logger.error("Error occurred while fetching the status.")
                    else:
                        # Network is okay
                        break
                    # Network problem occurred
                else:
                    logger.error("Network error occurred.")
                    return

                if "RUNNING" in status:
                    numbers = re.search(r'\d+', status)
                    if numbers:
                        progress_i = int(numbers.group())
                        if progress_i < pbar.total:
                            pbar.n = progress_i + 1
                            pbar.refresh()
                elif "FINISHED" in status:
                    logger.info("Job completion detected.")
                    break
                elif "ERROR" in status:
                    logger.info("Job failed.")
                    break

        # Retrieve the movie
        if status == "FINISHED":
            for _ in range(5):
                try:
                    SolaClient.get_movie(run_id, parameters["output_path"])
                except Exception as e:
                    logger.error("Error occurred while retrieving the movie.")
                    logger.debug(f"Details: {e}")
                else:
                    logger.info(f"Movie saved to: {parameters['output_path']}")
                    break
            else:
                logger.error("Failed to retrieve the movie.")
                return

    # except KeyboardInterrupt:
    #     if run_id is None:
    #         logger.info("No job to terminate.")
    #         return

    #     try:
    #         SolaClient.terminate(run_id)
    #     except Exception as e:
    #         logger.error(f"Error occurred while terminating the job: {e}")
    #     else:
    #         logger.info(f"Job terminated successfully. run_id={run_id}")
    #     return

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return

    else:
        logger.info("Job completed successfully.")
        return

if __name__ == '__main__':
    # Logger setup
    logger = getLogger(__name__)
    handler = StreamHandler()
    handler.setLevel(DEBUG)

    formatter = Formatter('[%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s] %(message)s')
    handler.setFormatter(formatter)

    logger.setLevel(DEBUG)
    logger.addHandler(handler)
    logger.propagate = False

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        usage="%(prog)s parameter_file [-h] [--no_request] [--run_id RUN_ID]",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "parameter_file",
        help="JSON file containing job parameters"
    )
    parser.add_argument(
        "--no_request",
        action="store_true",
        help="Do not request a new job; only perform status checks and download"
    )
    parser.add_argument(
        "--run_id",
        help="Specify the run_id of an existing job (used with --no_request)"
    )

    args = parser.parse_args()

    # Load parameters from the JSON file
    parameters = None
    try:
        with open(args.parameter_file, "r") as f:
            parameters = json.load(f)
    except Exception as e:
        logger.error(f"Error occurred while loading the parameter file: {e}")
        sys.exit(1)

    # If --no_request is used and --run_id is not provided, prompt the user for run_id
    if args.no_request and not args.run_id:
        try:
            run_id_input = input("--no_request option is used, but --run_id was not provided.\nPlease enter the existing job's run_id: ").strip()
            if not run_id_input:
                logger.error("No run_id was entered. Exiting the program.")
                sys.exit(1)
            args.run_id = run_id_input
        except EOFError:
            logger.error("Input for run_id was interrupted. Exiting the program.")
            sys.exit(1)

    # Execute the main function
    main(parameters, run_id=args.run_id, no_request=args.no_request, logger=logger)
