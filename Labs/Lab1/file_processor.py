import os
import shutil
import json

def read_config_file(config_path):
    f = open(config_path, 'r')
    data = json.load(f)
    return data

def write_log(message, log_file='app.log'):
    f = open(log_file, 'a')
    f.write(message + '\n')

def copy_file(source, destination):
    try:
        shutil.copy(source, destination)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def delete_old_files(directory, days=30):
    import time
    current_time = time.time()

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > (days * 86400):
                os.remove(file_path)

def read_sensitive_data(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    return data

def backup_files(source_dir, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    for item in os.listdir(source_dir):
        source = os.path.join(source_dir, item)
        destination = os.path.join(backup_dir, item)

        if os.path.isfile(source):
            shutil.copy2(source, destination)

def process_batch_files(file_list):
    results = []
    for file in file_list:
        try:
            data = read_config_file(file)
            results.append(data)
        except:
            pass
    return results

def clean_temp_files():
    temp_dir = '/tmp'
    for file in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except:
            pass
