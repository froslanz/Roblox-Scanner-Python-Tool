import os
import sys
import subprocess
import time

os.system('mode con: cols=75 lines=25')

def prepare_environment():
    mods = ["requests", "fade", "rich"]
    missing = [m for m in mods if not __import_util__(m)]
    if missing:
        os.system('cls')
        print("="*60 + "\n [!] MODULE INSTALLER\n" + "="*60)
        if input(f"\n Install {missing}? (y/n): ").lower() == 'y':
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
            os.execv(sys.executable, [sys.executable] + sys.argv)
        sys.exit()

def __import_util__(name):
    try:
        __import__(name)
        return True
    except ImportError:
        return False

prepare_environment()
import requests, fade
from rich.console import Console
from rich.table import Table

console = Console()

def get_id_by_username(username):
    try:
        url = "https://users.roblox.com/v1/usernames/users"
        data = {"usernames": [username], "excludeBannedUsers": False}
        res = requests.post(url, json=data).json()
        if res.get("data"):
            return res["data"][0].get("id")
        return None
    except:
        return None

def get_presence(user_id):
    try:
        url = "https://presence.roblox.com/v1/presence/users"
        data = {"userIds": [int(user_id)]}
        res = requests.post(url, json=data).json()
        presence = res.get("userPresences", [{}])[0]
        status_code = presence.get("userPresenceType", 0)
        status_map = {0: "Offline", 1: "Online", 2: "In a Game", 3: "In Studio", 4: "In Menu"}
        return status_map.get(status_code, "Unknown")
    except:
        return "Error"

def show_banner():
    banner = """
    ╔══════════════════════════════════════════════════════╗
    ║               ROBLOX UNIVERSAL SCANNER               ║
    ╚══════════════════════════════════════════════════════╝"""
    print(fade.purplepink(banner))

def start_scan():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        show_banner()
        
        console.print("\n[bold cyan] >> Enter Username or User ID:[/bold cyan]")
        user_input = input(" > ").strip()

        if not user_input: continue

        # Check if input is ID or Username
        if user_input.isdigit():
            user_id = user_input
        else:
            console.print(f"[dim] [~] Searching ID for: {user_input}...[/dim]")
            user_id = get_id_by_username(user_input)
            if not user_id:
                input("\n [!] User not found. ENTER...")
                continue

        try:
            u_res = requests.get(f"https://users.roblox.com/v1/users/{user_id}").json()
            f_count = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followers/count").json().get('count', 0)
            fing_count = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followings/count").json().get('count', 0)
            fr_count = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/friends/count").json().get('count', 0)
            status = get_presence(user_id)
            
            os.system('cls')
            show_banner()
            
            table = Table(title=f"RESULTS: {u_res.get('name')}", border_style="magenta")
            table.add_column("Category", style="cyan")
            table.add_column("Data", style="white")
            
            table.add_row("Username", u_res.get('name'))
            table.add_row("Display Name", u_res.get('displayName'))
            table.add_row("User ID", str(u_res.get('id')))
            table.add_row("Status", status, style="bold green" if status != "Offline" else "white")
            table.add_row("Friends", str(fr_count))
            table.add_row("Followers", str(f_count))
            table.add_row("Following", str(fing_count))
            
            console.print(table)
            input("\n [✓] ENTER for new search...")
        except:
            input("\n [!] Error fetching data. ENTER...")

if __name__ == "__main__":
    start_scan()