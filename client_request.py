#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    File name: client_request.py
    Objectives: control ComfyUI in the execute instance
    Author: Yuto Noguchi (Love Machine Inc.)
    Date created: 7/26/2024
'''

import os
import zipfile
import requests
import time
from endpoint import BASE_URL
import json
import io

class SolaClient:
    def check_folder_structure(folder:str):
        check_folders = ['COLOR', 'LINE', 'vector1-64-8']

        # check folder name
        for check_folder in check_folders:
            if not os.path.exists(os.path.join(folder, check_folder)):
                raise ValueError(f'{os.path.join(folder, check_folder)} is not found')

        # check file count
        file_count_tmp = -1
        for check_folder in check_folders:
            png_files = [f for f in os.listdir(os.path.join(folder, check_folder)) if f.endswith('.png')]
            file_count = len(png_files)
            if file_count == 0:
                raise ValueError(f'{os.path.join(folder, check_folder)} is empty')
            if file_count_tmp == -1:
                file_count_tmp = file_count
            elif file_count_tmp != file_count:
                raise ValueError(f'{os.path.join(folder, check_folder)} has different file count')
            
    def count_files(folder:str):
        return len(os.listdir(os.path.join(folder)))

    def compress_materials(material_folder, output_path):
        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))
        with zipfile.ZipFile(output_path, 'w') as zipf:
            for root, dirs, files in os.walk(material_folder):
                for file in files:
                    if file.endswith('.png'):
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, material_folder)  # material_folderからの相対パス
                        zipf.write(file_path, arcname)

    def validate_json(json_str):
        data = json.loads(json_str)
        parameters = json.loads(json.dumps(data['parameters']))
        workflow_name = data['workflow_name']

        workflow_list = ['dafault','by_character','PartialCN-Chara']

        if workflow_name not in workflow_list:
            raise ValueError(f"Invalid value for workflow_name: {workflow_name}, must be one of {workflow_list}")

        if workflow_name == 'dafault':
            lora_names = [f"PARAM_LORA_{i}_NAME" for i in range(1, 4)]
            valid_keys = lora_names + [
                "PARAM_BASEMODEL",
                "PARAM_UPSCALE",
                "PARAM_PROMPT",
                "PARAM_DENOISE",
                "PARAM_CONTROLNET_1_STRENGTH",
                "PARAM_CONTROLNET_2_STRENGTH",
                "PARAM_CONTROLNET_3_STRENGTH"
            ]

            allowed_lora_names = [
                "angel\\\\angel_man_test00.safetensors",
                "angel\\\\angel_woman_test01-000120.safetensors"
            ]

            allowed_base_models = [
                "animelike25D_animelike25DV11Pruned.safetensors",
                "cetusMix_Whalefall2.safetensors"
            ]

            for key, value in parameters.items():
                if key in lora_names:
                    if value not in allowed_lora_names:
                        raise ValueError(f"Invalid value for {key}: {value}, must be one of {allowed_lora_names}")
                elif key == "PARAM_BASEMODEL":
                    if value not in allowed_base_models:
                        raise ValueError(f"Invalid value for {key}: {value}, must be one of {allowed_base_models}")
                elif key == "PARAM_UPSCALE":
                    if not (0.7 <= value <= 1):
                        raise ValueError(f"Invalid value for {key}: {value}, must be in [0.7, 1]")
                elif key.startswith("PARAM_") and key.endswith("_STRENGTH"):
                    if not (0 <= value <= 1):
                        raise ValueError(f"Invalid value for {key}: {value}, must be in [0, 1]")
                elif key not in valid_keys:
                    raise ValueError(f"Unknown key: {key}")

        elif workflow_name == 'by_character':
            lora_names = [f"PARAM_LORA_{i}_NAME" for i in range(1, 2)]
            valid_keys = lora_names + [
                "PARAM_BASEMODEL",
                "PARAM_UPSCALE",
                "PARAM_PROMPT",
                "PARAM_DENOISE",
                "PARAM_CONTROLNET_1_STRENGTH",
                "PARAM_CONTROLNET_2_STRENGTH",
                "PARAM_CONTROLNET_3_STRENGTH"
            ]

            allowed_lora_names = [
                "angel\\\\angel_man_test00.safetensors",
                "angel\\\\angel_woman_test01-000120.safetensors"
            ]

            allowed_base_models = [
                "animelike25D_animelike25DV11Pruned.safetensors",
                "cetusMix_Whalefall2.safetensors"
            ]

            for key, value in parameters.items():
                if key in lora_names:
                    if value not in allowed_lora_names:
                        raise ValueError(f"Invalid value for {key}: {value}, must be one of {allowed_lora_names}")
                elif key == "PARAM_BASEMODEL":
                    if value not in allowed_base_models:
                        raise ValueError(f"Invalid value for {key}: {value}, must be one of {allowed_base_models}")
                elif key == "PARAM_UPSCALE":
                    if not (0.7 <= value <= 1):
                        raise ValueError(f"Invalid value for {key}: {value}, must be in [0.7, 1]")
                elif key.startswith("PARAM_") and key.endswith("_STRENGTH"):
                    if not (0 <= value <= 1):
                        raise ValueError(f"Invalid value for {key}: {value}, must be in [0, 1]")
                elif key not in valid_keys:
                    raise ValueError(f"Unknown key: {key}")
                
        elif workflow_name == 'PartialCN-Chara':
            lora_names = [f"PARAM_LORA_{i}_NAME" for i in range(1, 2)]
            valid_keys = lora_names + [
                "PARAM_BASEMODEL",
                "PARAM_UPSCALE",
                "PARAM_PROMPT",
                "PARAM_MASK_PROMPT",
                "PARAM_MASK_OBJECT_PROMPT",
                "PARAM_DENOISE",
                "PARAM_CONTROLNET_LINEART_WITH_MASK_STRENGTH",
                "PARAM_CONTROLNET_LINEART_OUT_MASK_STRENGTH",
                "PARAM_CONTROLNET_LIGHTBASEDPICTURE_STRENGTH",
                "PARAM_CONTROLNET_TILE_WITH_MASK_STRENGTH",
                "PARAM_CONTROLNET_TILE_OUT_MASK_STRENGTH"
            ]

            allowed_lora_names = [
                "angel\\\\angel_man_test00.safetensors",
                "angel\\\\angel_woman_test01-000120.safetensors"
            ]

            allowed_base_models = [
                "animelike25D_animelike25DV11Pruned.safetensors",
                "cetusMix_Whalefall2.safetensors"
            ]

            for key, value in parameters.items():
                if key in lora_names:
                    if value not in allowed_lora_names:
                        raise ValueError(f"Invalid value for {key}: {value}, must be one of {allowed_lora_names}")
                elif key == "PARAM_BASEMODEL":
                    if value not in allowed_base_models:
                        raise ValueError(f"Invalid value for {key}: {value}, must be one of {allowed_base_models}")
                elif key == "PARAM_UPSCALE":
                    if not (0.7 <= value <= 1):
                        raise ValueError(f"Invalid value for {key}: {value}, must be in [0.7, 1]")
                elif key.startswith("PARAM_") and key.endswith("_STRENGTH"):
                    if not (0 <= value <= 1):
                        raise ValueError(f"Invalid value for {key}: {value}, must be in [0, 1]")
                elif key not in valid_keys:
                    raise ValueError(f"Unknown key: {key}")



    def request(folder, user_name, job_name, params_comfy):
        """
        @brief Request a job to the server
        @param folder The name of the folder containing the materials
        @param user_name The name of the user, set free text
        @param lora_option The option for the lora, 'man' or 'woman'
        @param scale_option The option for the scale, 'upper' or 'whole'
        @return The run_id of the job
        """

        SolaClient.validate_json(params_comfy)
        
        # check folder structure
        SolaClient.check_folder_structure(folder)
        
        # count files in tmp dir
        files = SolaClient.count_files(folder)

        # compress materials
        SolaClient.compress_materials(folder, f'tmp/{folder}.zip')

        # send request to server
        url = f"{BASE_URL}/request"
        files = {'file': open(f'tmp/{folder}.zip', 'rb')}
        params = {'user_name': user_name, 'job_name': job_name, 'params_comfy': params_comfy}
        response = requests.post(url, files=files, params=params)

        if response.status_code != 200:
            raise ValueError(f'Request failed with status code {response.status_code}, message: {response.json()}')

        return response.json().get('run_id')
    
    def get_status(run_id):
        """
        @brief Get the status of the job with the given run_id
        @param run_id The run_id of the job
        @return The status of the job: 'PENDING', 'RUNNING', 'FINISHED', 'ERROR'
        """
        url = f"{BASE_URL}/status"
        params = {'run_id': run_id}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise ValueError(f'Request failed with status code {response.status_code}, message: {response.json()}')
        
        return response.json().get('status')[0]
    
    def get_movie(run_id, output_dir):
        """
        @brief get movie function
        @param run_id: run_id
        @param output_dir: directory to extract the movie
        @return output_dir: directory path with extracted movie, if failed return None
        """
        status = SolaClient.get_status(run_id)
        if status != 'FINISHED':
            return None

        url = f"{BASE_URL}/get_movie"
        params = {'run_id': run_id}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise ValueError(f'Request failed with status code {response.status_code}, message: {response.json()}')
        
        # make output directory
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            # extract zip file
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                z.extractall(output_dir)
        except zipfile.BadZipFile:
            raise ValueError('Response content is not a valid zip file')

        return output_dir
    
    def terminate(run_id):
        """
        @brief Terminate the job
        @param run_id The run_id of the job
        @return The status of the termination
        """
        url = f"{BASE_URL}/terminate"
        params = {'run_id': run_id}
        response = requests.post(url, params=params)

        if response.status_code != 200:
            raise ValueError(f'Request failed with status code {response.status_code}, message: {response.json()}')
        
    def list_jobs_by_user(user_name):
        """
        @brief List the jobs of the given user
        @param user_name The name of the user
        @return The list of jobs
        """
        url = f"{BASE_URL}/job_list_by_user"
        params = {'user_name': user_name}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise ValueError(f'Request failed with status code {response.status_code}, message: {response.json()}')
        
        return response.json().get('jobs')
    
    def list_all_jobs():
        """
        @brief List all jobs
        @return The list of jobs
        """
        url = f"{BASE_URL}/job_list_all"
        response = requests.get(url)

        if response.status_code != 200:
            raise ValueError(f'Request failed with status code {response.status_code}, message: {response.json()}')
        
        return response.json().get('jobs')
