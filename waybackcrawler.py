import re
import requests
from bs4 import BeautifulSoup
import threading
import itertools
import time
import colorama 
from colorama import Fore, Style,init
import os

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    init(autoreset=True)

    banner = """
    ▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨
    $$\      $$\  $$$$$$\ $$\     $$\       $$$$$$$\   $$$$$$\   $$$$$$\  $$\   $$\       $$\   $$\  $$$$$$\  $$\      $$\ $$$$$$$$\ 
    $$ | $\  $$ |$$  __$$\\$$\   $$  |      $$  __$$\ $$  __$$\ $$  __$$\ $$ | $$  |      $$ |  $$ |$$  __$$\ $$$\    $$$ |$$  _____|
    $$ |$$$\ $$ |$$ /  $$ |\$$\ $$  /       $$ |  $$ |$$ /  $$ |$$ /  \__|$$ |$$  /       $$ |  $$ |$$ /  $$ |$$$$\  $$$$ |$$ |      
    $$ $$ $$\$$ |$$$$$$$$ | \$$$$  /        $$$$$$$\ |$$$$$$$$ |$$ |      $$$$$  /        $$$$$$$$ |$$ |  $$ |$$\$$\$$ $$ |$$$$$\    
    $$$$  _$$$$ |$$  __$$ |  \$$  /         $$  __$$\ $$  __$$ |$$ |      $$  $$<         $$  __$$ |$$ |  $$ |$$ \$$$  $$ |$$  __|   
    $$$  / \$$$ |$$ |  $$ |   $$ |          $$ |  $$ |$$ |  $$ |$$ |  $$\ $$ |\$$\        $$ |  $$ |$$ |  $$ |$$ |\$  /$$ |$$ |      
    $$  /   \$$ |$$ |  $$ |   $$ |          $$$$$$$  |$$ |  $$ |\$$$$$$  |$$ | \$$\       $$ |  $$ | $$$$$$  |$$ | \_/ $$ |$$$$$$$$\ 
    \__/     \__|\__|  \__|   \__|          \_______/ \__|  \__| \______/ \__|  \__|      \__|  \__| \______/ \__|     \__|\________|                                                                                                                                                                                                                                                       
    ▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨▨

    """
    print(Fore.GREEN + banner + Style.RESET_ALL)
    print(Fore.GREEN + "A tool to fetch archived URLs from the Wayback Machine based on a given URL and date range." + Style.RESET_ALL)
    print(Fore.GREEN + "Author: Mr Hoodie | GitHub: https://github.com/NotReallySerious")
    print(Fore.GREEN + "Usage: Just run the script and follow the prompts to enter the URL and date range." + Style.RESET_ALL)  
    print(Fore.GREEN + "Version: 1.0" + Style.RESET_ALL)
    print(Fore.RED + "Disclaimer: This tool is for educational purposes only. Use responsibly and ethically." + Style.RESET_ALL)

    def loading_animation(stop_event, message='Fetching'):
        spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        while not stop_event.is_set():
            print(Fore.GREEN + f'\r{next(spinner)} {message}...', end='', flush=True)
            time.sleep(0.1)
        print(Fore.GREEN + f'\r✓ Done!          ', flush=True)

    raw_input = input('Enter the URL to find (with or without https, enter 0 to end): ').strip()
    if raw_input == '0':
        print(Fore.RED + "Exiting the program." + Style.RESET_ALL)
        break
    clean_url = re.sub(r'^https?://', '', raw_input)

    date_from = input('Enter the start date (YYYYMMDD): ').strip()
    date_to = input('Enter the end date (YYYYMMDD): ').strip()

    cdx_url = (
        f'http://web.archive.org/cdx/search/cdx?url={clean_url}/*'
        f'&output=text&fl=timestamp,original&collapse=urlkey'
        f'&from={date_from}&to={date_to}'
    )

    try:
        response = requests.get(cdx_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f'Request failed: {e}')
        exit(1)

    urls = response.text.strip().split('\n')

    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=loading_animation, args=(stop_event, 'Fetching URLs'))
    spinner_thread.start()

    try:
        response = requests.get(cdx_url, timeout=30)
        response.raise_for_status()

        # parse while spinner is still running
        urls = response.text.strip().split('\n')
        urls = [u for u in urls if u]  # filter empty lines

    finally:
        # only stop AFTER fetching and parsing is done
        stop_event.set()
        spinner_thread.join()

    print(f'\n[+] Found {len(urls)} unique URLs for {clean_url}\n')
    for url in urls:
        print(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    link_list = {}
    print(f'\n[+] Found {len(urls)} unique URLs for {clean_url} from {date_from} to {date_to}\n')
    for entry in urls:
        parts = entry.split(' ')
        if len(parts) == 2:
            timestamp, url = parts
            formatted = f'{timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]}'
            print(f'[{formatted}] {url}')
            link_list[url] = formatted

    saved_to_file = input('\nDo you want to save the results to a file? (y/n): ').strip().lower()
    if saved_to_file == 'y':
        filename = f'{clean_url.replace("/", "_")}_wayback_links.txt'
        with open(filename, 'w') as f:
            for url, date in link_list.items():
                f.write(f'[{date}] {url}\n')    