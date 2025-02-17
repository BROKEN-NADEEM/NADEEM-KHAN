import requests
from colorama import Fore, Style, init
import time
import os
import hashlib
import random
from urllib.parse import quote

init(autoreset=True)

def get_unique_id():
    try:
        unique_str = str(os.getuid()) + os.getlogin() if os.name != 'nt' else str(os.getlogin())
        return hashlib.sha256(unique_str.encode()).hexdigest()
    except Exception as e:
        print(f'Error generating unique ID: {e}')
        exit(1)

def print_colored_logo(logo):
    colors = [31, 32, 33, 34, 35, 36]
    for line in logo.split('\n'):
        color = random.choice(colors)
        print(f'\033[1;{color}m{line}\033[0m')
        time.sleep(0.1)

def pre_main():
    logo = '''
     #######  ######## ######## ##       #### ##    ## ######## 
    ##     ## ##       ##       ##        ##  ###   ## ##       
    ##     ## ##       ##       ##        ##  ####  ## ##       
    ##     ## ######   ######   ##        ##  ## ## ## ######   
    ##     ## ##       ##       ##        ##  ##  #### ##       
    ##     ## ##       ##       ##        ##  ##   ### ##       
     #######  ##       ##       ######## #### ##    ## ######## 
    '''
    
    unique_key = get_unique_id()
    os.system('clear')
    print_colored_logo(logo)
    print('•──────────────────────────────────────────────•')
    print('• OWNER-KITTU DON 💕 •')
    print('•──────────────────────────────────────────────•')
    print(f'[🔐] Your Key :: {unique_key}')
    print('•──────────────────────────────────────────────•')
    print(f'{Fore.GREEN}[√] No approval needed. Skipping verification.')

def fetch_ip_info():
    try:
        response = requests.get('http://ip-api.com/json/')
        if response.status_code == 200:
            data = response.json()
            return {
                'ip': data.get('query', 'N/A'),
                'country': data.get('country', 'N/A'),
                'region': data.get('regionName', 'N/A'),
                'city': data.get('city', 'N/A')
            }
    except requests.RequestException as e:
        print(f'{Fore.RED}Error fetching IP info: {e}')

def display_info():
    ip_info = fetch_ip_info()
    if ip_info:
        info = f"\n{Fore.YELLOW}< YOUR INFO >----------------------\n" \
               f"[ IP ADDRESS ]: {ip_info['ip']}\n[ TIME       ]: {time.strftime('%I:%M %p')}\n" \
               f"[ DATE       ]: {time.strftime('%d/%B/%Y')}\n" \
               f"[ COUNTRY    ]: {ip_info['country']}\n[ REGION     ]: {ip_info['region']}\n" \
               f"[ CITY       ]: {ip_info['city']}\n" \
               f"----------------------------------\n"
        print(info)

server_url = 'http://kittu.darkeagle.online/'

def load_from_file(file_path):
    if not os.path.exists(file_path):
        print(f'{Fore.RED}File not found: {file_path}')
        return []
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def send_post_request(url, json_data, retries=3):
    for attempt in range(retries):
        try:
            response = requests.post(url, json=json_data)
            if response.status_code == 200:
                return response
            else:
                print(f'{Fore.RED}Failed (Attempt {attempt + 1}/{retries}): {response.text}')
                time.sleep(1)
        except requests.RequestException as e:
            print(f'{Fore.RED}Error (Attempt {attempt + 1}/{retries}): {e}')
            time.sleep(1)

def start_loader():
    print(f'\n{Fore.YELLOW}--- Start a New Loader ---')
    convo_id = input(f'{Fore.CYAN}Enter Conversation ID: {Style.RESET_ALL}')
    hater_name = input(f'{Fore.CYAN}Enter Hater Name: {Style.RESET_ALL}')
    tokens_file = input(f'{Fore.CYAN}Enter Access Tokens File Path: {Style.RESET_ALL}')
    
    access_tokens = load_from_file(tokens_file)
    if not access_tokens:
        print(f'{Fore.RED}No access tokens found!')
        return

    print(f'{Fore.CYAN}1. Enter Messages Manually')
    print(f'{Fore.CYAN}2. Load Messages from File')
    message_choice = input(f'{Fore.CYAN}Choose an option: {Style.RESET_ALL}')
    
    messages = []
    if message_choice == '1':
        print(f'{Fore.CYAN}Enter messages one per line (type \'END\' to finish):{Style.RESET_ALL}')
        while True:
            message = input()
            if message.upper() == 'END':
                break
            messages.append(message.strip())
    elif message_choice == '2':
        file_path = input(f'{Fore.CYAN}Enter Message File Path: {Style.RESET_ALL}')
        messages = load_from_file(file_path)
    
    if not messages:
        print(f'{Fore.RED}No messages found!')
        return

    try:
        timer = int(input(f'{Fore.CYAN}Enter Timer Interval (in seconds): {Style.RESET_ALL}'))
    except ValueError:
        print(f'{Fore.RED}Invalid timer value! Must be an integer.')
        return

    data = {
        'convo_id': convo_id,
        'tokens': access_tokens,
        'messages': messages,
        'hater_name': hater_name,
        'timer': timer
    }
    print(f'{Fore.BLUE}Sending task to the server...')
    response = send_post_request(f'{server_url}/start_task', data)

    if response and response.status_code == 200:
        print(f'{Fore.GREEN}Loader started successfully!')
    else:
        print(f'{Fore.RED}Failed to start loader.')

def stop_loader():
    print(f'\n{Fore.YELLOW}--- Stop a Loader ---')
    task_id = input(f'{Fore.CYAN}Enter Task ID to stop: {Style.RESET_ALL}')
    print(f'{Fore.BLUE}Stopping loader...')
    response = send_post_request(f'{server_url}/stop_task/{task_id}', {})
    if response and response.status_code == 200:
        print(f'{Fore.GREEN}Loader stopped successfully!')
    else:
        print(f'{Fore.RED}Failed to stop loader.')

def menu():
    display_info()
    while True:
        print(f'\n{Fore.CYAN}< MENU >------------------------')
        print('[1] Start Loader')
        print('[2] Stop Loader')
        print('[3] Exit')
        print('--------------------------------')
        choice = input(f'{Fore.CYAN}Choose an option: {Style.RESET_ALL}')
        
        if choice == '1':
            start_loader()
        elif choice == '2':
            stop_loader()
        elif choice == '3':
            print(f'{Fore.GREEN}Exiting... Goodbye!')
            return
        else:
            print(f'{Fore.RED}Invalid choice! Try again.')

if __name__ == '__main__':
    pre_main()
    menu()
