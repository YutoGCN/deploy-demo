from client_request import SolaClient
from logging import getLogger, StreamHandler, DEBUG, Formatter
import sys
import json
import argparse
from datetime import datetime

def main(parameters, mode, run_id, *, logger, param_file_path):
    """
    Main function to execute the specified mode of operation.

    Args:
        parameters (dict): Configuration parameters loaded from JSON.
        mode (str or None): Mode of operation specified via command-line or interactively.
        run_id (str or None): run_id specified via command-line.
        logger (Logger): Logger instance for logging messages.
        param_file_path (str): Path to the parameter JSON file.
    """
    # Mapping of mode inputs to internal mode names
    mode_mapping = {
        '1': 'request',
        '2': 'list',
        '3': 'status',
        '4': 'download',
        '5': 'terminate',
        'request': 'request',
        'list': 'list',
        'status': 'status',
        'download': 'download',
        'terminate': 'terminate'
    }

    internal_mode = None

    if mode:
        internal_mode = mode_mapping.get(mode.lower())
        if internal_mode is None:
            logger.error("Invalid mode specified.")
            sys.exit(1)
    else:
        # Prompt the user interactively to enter the mode
        while True:
            user_input = input('Enter mode (1: request, 2: list, 3: status, 4: download, 5: terminate): ').strip()
            internal_mode = mode_mapping.get(user_input)
            if internal_mode:
                break
            else:
                logger.error("Invalid mode entered. Please try again.")

    # Load parameters from the JSON configuration
    try:
        material_folder = parameters["material_folder"]
        USER_NAME = parameters["user_name"]
        job_name = parameters["job_name"]
        output_path = parameters["output_path"]
        params_comfy_path = json.dumps(parameters)
    except KeyError as e:
        logger.error(f"Missing required parameter: {e}")
        sys.exit(1)

    # Execute the operation based on the selected mode
    if internal_mode == 'request':
        try:
            run_id = SolaClient.request(material_folder, USER_NAME, job_name, params_comfy_path)
        except ValueError as e:
            logger.error("An error occurred while requesting the job.")
            logger.error("Please try again.")
        else:
            logger.info("Job requested successfully.")
            logger.info(f"run_id: {run_id}")
    elif internal_mode == 'list':
        try:
            jobs = SolaClient.list_all_jobs()
        except ValueError as e:
            logger.error(f"An error occurred while retrieving the job list, {e}")
            logger.error("Please try again.")
        else:
            if not jobs:
                logger.info("No jobs found.")
            else:
                formatted_jobs = format_jobs_table(jobs)
                logger.info(f"\n{formatted_jobs}")
    elif internal_mode in ['status', 'download', 'terminate']:
        # Retrieve run_id from command-line argument or prompt
        if run_id:
            selected_run_id = run_id
        else:
            # Prompt the user interactively
            selected_run_id = input('Please enter run_id: ').strip()
            if not selected_run_id:
                logger.error("No run_id provided. Exiting.")
                sys.exit(1)
        # Execute based on the mode
        if internal_mode == 'status':
            try:
                status = SolaClient.get_status(selected_run_id)
            except ValueError as e:
                logger.error("An error occurred while retrieving the job status.")
                logger.error("Please try again.")
            else:
                logger.info(f"Status: {status}")
        elif internal_mode == 'download':
            try:
                downloaded_path = SolaClient.get_movie(selected_run_id, output_path)
            except Exception as e:
                logger.error(f"An error occurred while downloading the movie, {e}")
                logger.error("Please try again.")
            else:
                if downloaded_path is None:
                    logger.info("The job is not finished yet or has failed.")
                    return
                logger.info(f"Movie downloaded to: {downloaded_path}")
        elif internal_mode == 'terminate':
            try:
                SolaClient.terminate(selected_run_id)
            except ValueError as e:
                logger.error("An error occurred while terminating the job.")
                logger.error("Please try again.")
            else:
                logger.info("Job terminated successfully.")
    else:
        logger.error("Invalid mode selected.")
        sys.exit(1)

def format_jobs_table(jobs):
    """
    Formats the list of jobs into a table-like string.

    Args:
        jobs (list of lists): List containing job details.

    Returns:
        str: Formatted table as a string.
    """
    if not jobs:
        return "No jobs available."

    # Define headers based on the job data structure
    headers = ["run_id", "user_name", "job_name", "status", "run_time(s)"]

    # Determine the width of each column
    column_widths = [len(header) for header in headers]
    for job in jobs:
        for idx, item in enumerate(job):
            item_length = len(str(item))
            if item_length > column_widths[idx]:
                column_widths[idx] = item_length

    # Create a horizontal separator
    separator = ' | '.join(['-' * width for width in column_widths])

    # Format headers
    header_row = ' | '.join([headers[i].ljust(column_widths[i]) for i in range(len(headers))])

    # Format each job row
    job_rows = []
    for job in jobs:
        row = ' | '.join([str(job[i]).ljust(column_widths[i]) for i in range(len(job))])
        job_rows.append(row)

    # Combine all parts into the final table
    table = f"{header_row}\n{separator}\n" + "\n".join(job_rows)
    return table

def print_custom_usage():
    """
    Prints custom usage information.
    Note: This function is optional as argparse handles --help automatically.
    """
    usage_text = """
    Usage:
        python script.py param_file.json [--mode MODE] [--run_id RUN_ID]

    Options:
        --mode MODE      Specify the mode of operation. Modes can be:
                            1/request, 2/list, 3/status, 4/download, 5/terminate
        --run_id RUN_ID  Specify the run_id for operations that require it (status, download, terminate)
        --help           Show this help message and exit.

    If --mode is not provided, the script will prompt for it interactively.
    If --run_id is not provided for modes that require it, the script will prompt
    the user to enter it interactively.
    """
    print(usage_text)

if __name__ == '__main__':
    # Configure the logger
    logger = getLogger(__name__)
    handler = StreamHandler()
    handler.setLevel(DEBUG)

    formatter = Formatter('[%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s] %(message)s')
    handler.setFormatter(formatter)

    logger.setLevel(DEBUG)
    logger.addHandler(handler)
    logger.propagate = False

    # Set up argparse for command-line argument parsing
    parser = argparse.ArgumentParser(
        description='SolaClient Operation Script',
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False  # Disable default help to add custom usage if needed
    )
    parser.add_argument('param_file', help='Path to the JSON file containing parameters')
    parser.add_argument('--mode', help='Operation mode: 1/request, 2/list, 3/status, 4/download, 5/terminate')
    parser.add_argument('--run_id', help='Specify the run_id for operations that require it')

    # Add custom help
    parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')

    # Parse the arguments
    args = parser.parse_args()

    # Handle custom help
    if args.help:
        print_custom_usage()
        sys.exit(0)

    # Load the parameters from the specified JSON file
    param_file_path = args.param_file
    try:
        with open(param_file_path, "r", encoding='utf-8') as f:
            parameters = json.load(f)
    except FileNotFoundError:
        logger.error(f"Parameter file not found: {param_file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON parameter file: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error while loading parameter file: {e}")
        sys.exit(1)

    # Execute the main function with the provided parameters, mode, and run_id
    main(parameters, args.mode, args.run_id, logger=logger, param_file_path=param_file_path)
