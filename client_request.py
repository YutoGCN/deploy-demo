#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    File name: client_request.py
    Objectives: control ComfyUI in the execute instance
    Author: Yuto Noguchi (Love Machine Inc.)
    Date created: 7/26/2024
'''

import os
import shutil
import requests
import time
from endpoint import BASE_URL

class SolaClient:
    def check_folder_structure(folder:str):
        check_folders = ['COLOR','LINE','vector1-64-8']

        # check folder name
        for check_folder in check_folders:
            if os.path.exists(os.path.join(folder, check_folder)) == False:
                raise ValueError(f'{os.path.join(folder, check_folder)} is not found')

        # check file count
        file_count_tmp = -1
        for check_folder in check_folders:
            file_count = len(os.listdir(os.path.join(folder, check_folder)))
            if file_count == 0:
                raise ValueError(f'{os.path.join(folder, check_folder)} is empty')
            if file_count_tmp == -1:
                file_count_tmp = file_count
            elif file_count_tmp != file_count:
                raise ValueError(f'{os.path.join(folder, check_folder)} has different file count')
            
    def count_files(folder:str):
        return len(os.listdir(os.path.join(folder)))

    def compress_materials(material_folder, output_path):
        shutil.make_archive(output_path.replace(".zip","") , 'zip', material_folder)

    def request(folder, user_name, lora_option, scale_option):
        """
        @brief Request a job to the server
        @param folder The name of the folder containing the materials
        @param user_name The name of the user, set free text
        @param lora_option The option for the lora, 'man' or 'woman'
        @param scale_option The option for the scale, 'upper' or 'whole'
        @return The run_id of the job
        """
        # check lora_option
        if lora_option not in ['man','woman']:
            raise ValueError(f'lora_option "{lora_option}" is invalid, please select "man" or "woman".')
        
        # check scale_option
        if scale_option not in ["upper","whole"]:
            raise ValueError(f'scale_option "{scale_option}" is invalid, please select "upper" or "whole".')
        
        # check folder structure
        SolaClient.check_folder_structure(folder)
        
        # count files in tmp dir
        files = SolaClient.count_files(folder)

        # compress materials
        SolaClient.compress_materials(folder, f'tmp/{folder}.zip')

        # send request to server
        url = f"{BASE_URL}/request"
        files = {'file': open(f'tmp/{folder}.zip', 'rb')}
        params = {'user_name': user_name,'lora_option': lora_option, 'scale_option': scale_option, }
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
    
    def get_movie(run_id, output_path):
        """
        @brief get movie function
        @param run_id: run_id
        @param output_path: movie path you want to save
        @return output_path: movie path, if failed return None
        """
        status = SolaClient.get_status(run_id)
        if status != 'FINISHED':
            return None

        url = f"{BASE_URL}/get_movie"
        params = {'run_id': run_id}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise ValueError(f'Request failed with status code {response.status_code}, message: {response.json()}')
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return output_path