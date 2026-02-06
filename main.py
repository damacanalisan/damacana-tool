#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import time

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    
    BLUE = "\033[34m"
    RESET = "\033[0m"

    print(BLUE + r"""
                              ...                           
                         .:=====:.                         
                         .=+++++=..                        
                         .+=.::==:.                        
                         :+=.::+=:                         
                       ..-+=:..=+-..                       
                    ....:---=++=--:....                    
                 ..:.....:=+++++=-.....:...                
                .-+*+-:..::------==+++=++=..               
               .:+=--:.............:::.::+:.               
               .=+:++-:::--=======++++==---.               
               .=---:..............:::.:-:=.               
               .==:-:..................:-:=.               
               .:=.-:..................:---.               
               .:+-+=-:::::.....:::-----===.               
               .=*.--:................::-==.               
               .+=-+=:...:::...::::---:---+.               
               .==--:.. ...............:--=.               
               .-=.-:..................:--=.               
               .:=.=:.....:::..........:---..              
               .:=.-::---==----------:.::--..              
               .:=.-:=++*+====+++***+=-::--..              
               .:+:=.::.:::.......:::---:=-..              
               .-*:=:-=++++====++++++-:--==..              
               .+*:--:....:::::::::::::--=+..              
               .++.---:::::::::::--:::--:=+..              
               .=*+=-:...:::::::::::::--=+=.               
               .:=++=------------=======+=:.               
                 ...::-::::----------::...                 
                          ...                              

                     ███ DAMACANA TOOL ███
    """ + RESET)
    print("        Damacana-Tool | Terminal Security Toolkit")
    print("        Educational & Defensive Use Only")
    print("                   ~ damacanalisan ~\n")

def pause():
    input("\nDevam etmek için ENTER...")

# ================== MODÜLLER (ŞİMDİLİK BOŞ) ==================

# Başta ekle
from colorama import init, Fore, Style
init(autoreset=True)
import time

# OSINT Ana Menü
def osint_module():
    while True:
        clear()
        banner()
        print(Fore.CYAN + "[ OSINT MODULE ]\n")
        print(Fore.YELLOW + "[1] Domain OSINT")
        print(Fore.YELLOW + "[2] Username OSINT")
        print(Fore.YELLOW + "[3] IP Lookup\n")
        print(Fore.YELLOW + "[0] Geri\n")

        choice = input(Fore.GREEN + "Seçiminiz >> ").strip()

        if choice == "1":
            domain_osint()
        elif choice == "2":
            username_osint()
        elif choice == "3":
         ip_lookup()  # artık IP Lookup aktif olarak çalışacak
        elif choice == "0":
            return
        else:
            print(Fore.RED + "Geçersiz seçim!")
            time.sleep(1)

# -------------------- DOMAIN OSINT --------------------
def domain_osint():
    import socket
    import ssl

    clear()
    banner()
    print(Fore.CYAN + "[ Domain OSINT ]\n")

    domain = input(Fore.GREEN + "Domain (ör: google.com): ").strip().lower()

    if not domain or "." not in domain:
        print(Fore.RED + "[!] Geçersiz domain!")
        pause()
        return

    print(Fore.GREEN + "\n[+] Domain formatı geçerli.")
    time.sleep(0.5)

    # IP çözümleme
    try:
        ip = socket.gethostbyname(domain)
        print(Fore.CYAN + f"[+] IP Adresi: {ip}")
    except socket.gaierror:
        print(Fore.RED + "[!] IP çözümlenemedi.")
        pause()
        return

    # IP tipi
    if ip.startswith(("10.", "192.168.", "172.")):
        print(Fore.YELLOW + "[+] IP Türü: Private IP")
    else:
        print(Fore.YELLOW + "[+] IP Türü: Public IP")

    # HTTPS / SSL kontrolü
    print(Fore.GREEN + "\n[+] HTTPS kontrolü yapılıyor...")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=3) as sock:
            with context.wrap_socket(sock, server_hostname=domain):
                print(Fore.GREEN + "[+] HTTPS: AKTİF")
                https_ok = True
    except:
        print(Fore.RED + "[!] HTTPS: YOK / ERİŞİLEMEDİ")
        https_ok = False

    # Subdomain kontrol (offline)
    print(Fore.GREEN + "\n[+] Subdomain kontrolü (offline)...")
    common_subs = ["www", "mail", "ftp", "dev", "test"]
    found_subs = []

    for sub in common_subs:
        test_domain = f"{sub}.{domain}"
        try:
            socket.gethostbyname(test_domain)
            found_subs.append(test_domain)
        except:
            pass

    if found_subs:
        for s in found_subs:
            print(Fore.CYAN + f"[+] Bulunan subdomain: {s}")
    else:
        print(Fore.RED + "[-] Yaygın subdomain bulunamadı")

    # Risk analizi
    print(Fore.GREEN + "\n[+] Risk analizi yapılıyor...")
    time.sleep(1)

    risk_score = 0
    if domain.count("-") >= 2:
        risk_score += 1
    if any(char.isdigit() for char in domain):
        risk_score += 1
    if domain.startswith("xn--"):
        risk_score += 2
    if not https_ok:
        risk_score += 1

    if risk_score <= 1:
        risk = "LOW"
    elif risk_score == 2:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    print(Fore.MAGENTA + f"[+] Risk Seviyesi: {risk}")
    print(Fore.GREEN + "\n[✓] Domain OSINT tamamlandı.")
    pause()

# -------------------- USERNAME OSINT --------------------
def username_osint():
    import requests

    clear()
    banner()
    print("[ Username OSINT ]\n")  # Başlık sadece Username OSINT

    username = input("Kullanıcı adı: ").strip()

    if not username:
        print("[!] Geçersiz kullanıcı adı!")
        pause()
        return

    print("\n[+] Kontrol ediliyor (var/yok)...\n")

    platforms = {
        "GitHub": f"https://github.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "Reddit": f"https://www.reddit.com/user/{username}/",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Facebook": f"https://www.facebook.com/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "Medium": f"https://medium.com/@{username}",
        "LinkedIn": f"https://www.linkedin.com/in/{username}/",
        "Steam": f"https://steamcommunity.com/id/{username}/",
        "YouTube": f"https://www.youtube.com/{username}"
    }

    for platform, url in platforms.items():
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                print(f"[+] {platform}: Var ({url})")
            else:
                print(f"[-] {platform}: Yok ({url})")
        except requests.RequestException:
            print(f"[-] {platform}: Yok ({url})")

    print("\n[✓] Username OSINT tamamlandı.")
    pause()

import socket
import requests
from colorama import init, Fore, Style

init(autoreset=True)

import socket
import requests
from colorama import Fore, init

init(autoreset=True)

def ip_lookup():
    clear()
    banner()
    print(Fore.CYAN + "[ IP LOOKUP ]\n")
    
    target = input("IP veya Domain girin: ").strip()
    if not target:
        print(Fore.RED + "[!] Geçersiz giriş!")
        pause()
        return
    
    # IP çözümleme
    try:
        ip = socket.gethostbyname(target)
        print(Fore.GREEN + f"[+] IP Adresi: {ip}")
    except:
        print(Fore.RED + "[!] IP çözümlenemedi")
        pause()
        return
    
    # IP tipi
    if ip.startswith(("10.", "192.168.", "172.")):
        print(Fore.YELLOW + "[+] IP Türü: Private IP")
    else:
        print(Fore.YELLOW + "[+] IP Türü: Public IP")
    
    # IP konumu
    try:
        res = requests.get(f"https://ipapi.co/{ip}/json/").json()
        print(Fore.MAGENTA + f"[+] Ülke: {res.get('country_name', 'Bilinmiyor')}")
        print(Fore.MAGENTA + f"[+] Şehir: {res.get('city', 'Bilinmiyor')}")
        print(Fore.MAGENTA + f"[+] ISP: {res.get('org', 'Bilinmiyor')}")
    except:
        print(Fore.RED + "[!] Konum bilgisi alınamadı")
    
    pause()

import re
from colorama import init, Fore, Style
init(autoreset=True)

import os
import time
from collections import Counter

# Terminal renkleri
class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPress Enter to continue...")



def log_analyzer():
    clear()
    banner()

    log_file = input(f"{Colors.OKBLUE}Analiz edilecek log dosyası (örn: access.log): {Colors.ENDC}").strip()

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        print(f"\n{Colors.OKGREEN}[+] Toplam satır sayısı: {len(lines)}{Colors.ENDC}\n")

        # IP adresleri sayısı
        ip_list = []
        for line in lines:
            parts = line.split()
            if len(parts) > 0:
                ip_list.append(parts[0])
        ip_counts = Counter(ip_list)

        print(f"{Colors.OKCYAN}[+] IP Dağılımı:{Colors.ENDC}")
        for ip, count in ip_counts.most_common(10):  # en çok 10 IP göster
            print(f"{Colors.WARNING}{ip}{Colors.ENDC} → {Colors.OKGREEN}{count} kez{Colors.ENDC}")

        # Basit hata analizi
        errors = [line for line in lines if "error" in line.lower()]
        print(f"\n{Colors.FAIL}[+] Hata sayısı: {len(errors)}{Colors.ENDC}")

    except FileNotFoundError:
        print(f"\n{Colors.FAIL}[!] Dosya bulunamadı: {log_file}{Colors.ENDC}")

    pause()

def phishing_module():
    import socket
    import time
    from urllib.parse import urlparse

    clear()
    banner()
    print("[ PHISHING URL CHECKER ]\n")

    url = input("Analiz edilecek URL: ").strip()

    if not url.startswith(("http://", "https://")):
        print("\n[!] URL http:// veya https:// ile başlamalı")
        pause()
        return

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    print(f"\n[+] Domain: {domain}")
    time.sleep(0.5)

    risk = 0

    # HTTPS kontrolü
    if url.startswith("https://"):
        print("[✓] HTTPS: VAR")
    else:
        print("[!] HTTPS: YOK")
        risk += 1

    # IP ile erişim kontrolü
    try:
        socket.inet_aton(domain)
        print("[!] Domain yerine IP kullanılıyor")
        risk += 2
    except:
        print("[✓] IP yerine domain kullanılıyor")

    # Şüpheli karakterler
    if domain.count("-") >= 2:
        print("[!] Fazla '-' karakteri")
        risk += 1

    if any(char.isdigit() for char in domain):
        print("[!] Domain içinde rakam var")
        risk += 1

    # Marka taklidi kontrolü
    brands = ["paypal", "google", "facebook", "instagram", "apple", "microsoft"]
    for brand in brands:
        if brand in domain and not domain.endswith(f"{brand}.com"):
            print(f"[!] Marka taklidi şüphesi: {brand}")
            risk += 2

    # Sonuç
    print("\n[ SONUÇ ]")
    if risk <= 1:
        print("[✓] LOW RISK")
    elif risk <= 3:
        print("[!] MEDIUM RISK")
    else:
        print("[✗] HIGH RISK – PHISHING OLABİLİR")

    pause()

def password_module():
    import re
    import random
    import string

    clear()
    banner()
    print("[ PASSWORD STRENGTH TESTER ]\n")

    password = input("Test edilecek şifre: ").strip()

    score = 0
    feedback = []

    # Uzunluk
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("• Şifre çok kısa (min 8-12 karakter)")

    # Büyük harf
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("• Büyük harf yok")

    # Küçük harf
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("• Küçük harf yok")

    # Rakam
    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("• Rakam yok")

    # Özel karakter
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 2
    else:
        feedback.append("• Özel karakter yok")

    print("\n[ ANALİZ SONUCU ]")

    if score <= 3:
        print("[✗] ZAYIF ŞİFRE")
    elif score <= 6:
        print("[!] ORTA SEVİYE ŞİFRE")
    else:
        print("[✓] GÜÇLÜ ŞİFRE")

    if feedback:
        print("\n[ GELİŞTİRME ÖNERİLERİ ]")
        for f in feedback:
            print(f)

    # Güçlü şifre önerisi
    print("\n[ ÖRNEK GÜÇLÜ ŞİFRE ]")
    strong_password = generate_strong_password()
    print(strong_password)

    pause()


def generate_strong_password(length=16):
    import random
    import string

    chars = (
        string.ascii_lowercase +
        string.ascii_uppercase +
        string.digits +
        "!@#$%^&*()-_=+[]{}"
    )

    return "".join(random.choice(chars) for _ in range(length))

# ================== ANA MENÜ ==================

def main_menu():
    while True:
        clear()
        banner()
        print("[1] OSINT - Domain Analyzer")
        print("[2] Log Analyzer")
        print("[3] Phishing URL Checker")
        print("[4] Password Strength Tester")
        print("[0] Exit\n")

        choice = input("Seçiminiz >> ").strip()

        if choice == "1":
            osint_module()
        elif choice == "2":
            log_analyzer()
        elif choice == "3":
            phishing_module()
        elif choice == "4":
            password_module()
        elif choice == "0":
            clear()
            print("Çıkılıyor... 👋")
            time.sleep(1)
            sys.exit()
        else:
            print("\nGeçersiz seçim!")
            time.sleep(1)

# ================== START ==================

if __name__ == "__main__":
    main_menu()