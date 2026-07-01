import pypresence
import time
import os
import sys
from pypresence import Presence

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#          CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CLIENT_ID = "1509568054303002786"

STATE       = "Serveur +10 000 membres"
DETAILS     = "Akina"
LARGE_IMAGE = "banner"
LARGE_TEXT  = "Akina"
SMALL_IMAGE = "logo"
SMALL_TEXT  = "Akina Community"

# ⚠️ IMPORTANT : Utilise le lien complet avec https://
BUTTON_LABEL = "Rejoindre le serveur"
BUTTON_URL   = "https://discord.gg/akina"   # <-- https:// obligatoire

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def connect():
    while True:
        try:
            print("[✔] Connexion à Discord RPC...")
            RPC = Presence(CLIENT_ID)
            RPC.connect()
            print("[✔] Connecté avec succès !")

            start_time = time.time()

            while True:
                try:
                    RPC.update(
                        state       = STATE,
                        details     = DETAILS,
                        large_image = LARGE_IMAGE,
                        large_text  = LARGE_TEXT,
                        small_image = SMALL_IMAGE,
                        small_text  = SMALL_TEXT,
                        start       = int(start_time),
                        buttons     = [
                            {
                                "label": BUTTON_LABEL,
                                "url"  : BUTTON_URL
                            }
                        ]
                    )
                    print(f"[✔] Activité mise à jour - {time.strftime('%H:%M:%S')}")

                except Exception as e:
                    print(f"[⚠] Erreur update: {e}")
                    print("[⚠] Tentative sans bouton...")

                    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    # Si le bouton échoue, on réessaie avec
                    # une URL alternative
                    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    try:
                        RPC.update(
                            state       = STATE,
                            details     = DETAILS,
                            large_image = LARGE_IMAGE,
                            large_text  = LARGE_TEXT,
                            small_image = SMALL_IMAGE,
                            small_text  = SMALL_TEXT,
                            start       = int(start_time),
                            buttons     = [
                                {
                                    "label": BUTTON_LABEL,
                                    # Lien de secours avec redirect
                                    "url"  : "https://discord.com/invite/akina"
                                }
                            ]
                        )
                        print("[✔] Activité mise à jour avec lien alternatif !")

                    except Exception as e2:
                        print(f"[✖] Erreur bouton: {e2}")

                time.sleep(15)

        except pypresence.exceptions.DiscordNotFound:
            print("[✖] Discord n'est pas ouvert. Nouvelle tentative dans 30s...")
            time.sleep(30)

        except pypresence.exceptions.InvalidID:
            print("[✖] CLIENT_ID invalide ! Vérifie ton ID dans le code.")
            input("Appuie sur Entrée pour quitter...")
            sys.exit(1)

        except KeyboardInterrupt:
            print("\n[✔] Arrêt du programme.")
            try:
                RPC.close()
            except:
                pass
            sys.exit(0)

        except Exception as e:
            print(f"[✖] Erreur: {e} - Reconnexion dans 30s...")
            time.sleep(30)

if __name__ == "__main__":
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("     Discord Rich Presence      ")
    print("          Akina                 ")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    connect()
