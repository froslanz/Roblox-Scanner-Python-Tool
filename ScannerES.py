import os
import sys
import subprocess
import time

os.system('mode con: cols=75 lines=25')

def preparar_entorno():
    modulos = ["requests", "fade", "rich"]
    faltantes = [m for m in modulos if not __import_util__(m)]
    if faltantes:
        os.system('cls')
        print("="*60 + "\n [!] INSTALADOR DE MODULOS\n" + "="*60)
        if input(f"\n Instalar {faltantes}? (s/n): ").lower() == 's':
            subprocess.check_call([sys.executable, "-m", "pip", "install", *faltantes])
            os.execv(sys.executable, [sys.executable] + sys.argv)
        sys.exit()

def __import_util__(name):
    try:
        __import__(name)
        return True
    except ImportError:
        return False

preparar_entorno()
import requests, fade
from rich.console import Console
from rich.table import Table

console = Console()

def obtener_id_por_nombre(username):
    try:
        url = "https://users.roblox.com/v1/usernames/users"
        data = {"usernames": [username], "excludeBannedUsers": False}
        res = requests.post(url, json=data).json()
        if res.get("data"):
            return res["data"][0].get("id")
        return None
    except:
        return None

def obtener_presencia(user_id):
    try:
        url = "https://presence.roblox.com/v1/presence/users"
        data = {"userIds": [int(user_id)]}
        res = requests.post(url, json=data).json()
        presencia = res.get("userPresences", [{}])[0]
        estado_code = presencia.get("userPresenceType", 0)
        estados = {0: "Offline", 1: "Online", 2: "En un Juego", 3: "En Studio", 4: "En el Menu"}
        return estados.get(estado_code, "Desconocido")
    except:
        return "Error"

def mostrar_banner():
    banner = """
    ╔══════════════════════════════════════════════════════╗
    ║               ROBLOX UNIVERSAL SCANNER               ║
    ╚══════════════════════════════════════════════════════╝"""
    print(fade.purplepink(banner))

def iniciar_escaneo():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        mostrar_banner()
        
        console.print("\n[bold cyan] >> Ingrese Nombre de Usuario o ID:[/bold cyan]")
        entrada = input(" > ").strip()

        if not entrada: continue

        # Determinar si es ID o Username
        if entrada.isdigit():
            user_id = entrada
        else:
            console.print(f"[dim] [~] Buscando ID para: {entrada}...[/dim]")
            user_id = obtener_id_por_nombre(entrada)
            if not user_id:
                input("\n [!] Usuario no encontrado. ENTER...")
                continue

        try:
            # Peticiones de datos
            u_res = requests.get(f"https://users.roblox.com/v1/users/{user_id}").json()
            f_count = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followers/count").json().get('count', 0)
            fing_count = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followings/count").json().get('count', 0)
            fr_count = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/friends/count").json().get('count', 0)
            estado = obtener_presencia(user_id)
            
            os.system('cls')
            mostrar_banner()
            
            table = Table(title=f"RESULTADOS: {u_res.get('name')}", border_style="magenta")
            table.add_column("Categoria", style="cyan")
            table.add_column("Dato", style="white")
            
            table.add_row("Username", u_res.get('name'))
            table.add_row("Display Name", u_res.get('displayName'))
            table.add_row("User ID", str(u_res.get('id')))
            table.add_row("Estado", estado, style="bold green" if estado != "Offline" else "white")
            table.add_row("Amigos", str(fr_count))
            table.add_row("Seguidores", str(f_count))
            table.add_row("Siguiendo", str(fing_count))
            
            console.print(table)
            input("\n [✓] ENTER para nueva busqueda...")
        except:
            input("\n [!] Error al obtener datos. ENTER...")

if __name__ == "__main__":
    iniciar_escaneo()