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
