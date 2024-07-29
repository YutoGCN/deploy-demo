from client_request import SolaClient
import time

def main():
    run_ids = []
    
    # Request to server
    run_id = SolaClient.request('test_man', 'user-demo-1', 'man', 'upper')
    run_ids.append(run_id)

    while True:
        time.sleep(5)
        for run_id in run_ids:
            status = SolaClient.get_status(run_id)
            print(f'run_id: {run_id}, status: {status}')

            if status == 'FINISHED':
                SolaClient.get_movie(run_id, f'tmp\\{run_id}.mp4')
                run_ids.remove(run_id)
            elif status == 'ERROR':
                run_ids.remove(run_id)
                
        if len(run_ids) == 0:
            break

    print('All jobs are finished')

if __name__ == '__main__':
    main()