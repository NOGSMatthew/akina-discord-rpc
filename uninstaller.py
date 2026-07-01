import tkinter as tk
from tkinter import ttk
import threading
import subprocess
import sys
import os
import shutil
import winreg
from PIL import Image, ImageTk, ImageDraw

BG         = "#0f0f0f"
BG2        = "#161616"
ACCENT     = "#ef4444"
ACCENT2    = "#dc2626"
SUCCESS    = "#22c55e"
TEXT       = "#ffffff"
TEXT2      = "#a1a1aa"
BORDER     = "#27272a"
CONSOLE_BG = "#0a0a0a"

INSTALL_DIR = os.path.join(os.environ["APPDATA"], "AkinaRPC")

def resource(name):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, name)
    return os.path.join(os.path.dirname(__file__), name)

def make_circle_image(path, size=72):
    img = Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    result.paste(img, mask=mask)
    return result


class AkinaUninstaller(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Akina RPC — Desinstaller")
        self.geometry("580x600")
        self.resizable(False, False)
        self.configure(bg=BG)
        self._center()
        self._set_icon()
        self._build_ui()

    def _center(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - 580) // 2
        y = (self.winfo_screenheight() - 600) // 2
        self.geometry(f"580x600+{x}+{y}")

    def _set_icon(self):
        try:
            self.iconbitmap(resource("logo.ico"))
        except Exception:
            pass

    def _build_ui(self):

        # ── BANNIÈRE ──────────────────────────────────────────────────
        try:
            raw = Image.open(resource("banner.png"))
            w, h = raw.size
            nh   = min(int(h * (580 / w)), 180)
            raw  = raw.resize((580, nh), Image.LANCZOS)
            self._banner = ImageTk.PhotoImage(raw)
            tk.Label(self, image=self._banner, bg=BG, bd=0).pack(fill="x")
        except Exception:
            tk.Label(self, text="Akina RPC",
                     font=("Segoe UI", 22, "bold"),
                     bg=BG, fg=ACCENT).pack(pady=16)

        # ── ZONE SCROLLABLE ───────────────────────────────────────────
        outer = tk.Frame(self, bg=BG2)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, bg=BG2, bd=0, highlightthickness=0)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Dark.Vertical.TScrollbar",
            background=BORDER, troughcolor=BG2,
            arrowcolor=TEXT2, borderwidth=0, relief="flat"
        )
        style.configure(
            "Uninstall.Horizontal.TProgressbar",
            troughcolor=BORDER, background=ACCENT,
            thickness=6, borderwidth=0, relief="flat"
        )

        scrollbar = ttk.Scrollbar(outer, orient="vertical",
                                  command=canvas.yview,
                                  style="Dark.Vertical.TScrollbar")
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        body = tk.Frame(canvas, bg=BG2)
        win_id = canvas.create_window((0, 0), window=body, anchor="nw")

        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(win_id, width=e.width))
        body.bind("<Configure>",
                  lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # ── CONTENU ───────────────────────────────────────────────────

        # Logo + titre
        top = tk.Frame(body, bg=BG2)
        top.pack(pady=(22, 6), padx=28, anchor="w")

        try:
            img = make_circle_image(resource("logo.png"), 72)
            self._logo = ImageTk.PhotoImage(img)
            tk.Label(top, image=self._logo, bg=BG2, bd=0).pack(side="left", padx=(0, 16))
        except Exception:
            pass

        col = tk.Frame(top, bg=BG2)
        col.pack(side="left")
        tk.Label(col, text="Desinstaller Akina RPC",
                 font=("Segoe UI", 18, "bold"),
                 bg=BG2, fg=TEXT, anchor="w").pack(anchor="w")
        tk.Label(col, text="Suppression complete de l'application",
                 font=("Segoe UI", 9),
                 bg=BG2, fg=TEXT2).pack(anchor="w", pady=(2, 0))

        # Séparateur
        tk.Frame(body, bg=BORDER, height=1).pack(fill="x", padx=26, pady=(12, 0))

        # Liste suppressions
        items = [
            "Script RPC dans AppData",
            "Entree de demarrage automatique (registre)",
            "Processus AkinaRPC actif en arriere-plan",
        ]
        feats = tk.Frame(body, bg=BG2)
        feats.pack(fill="x", padx=34, pady=(12, 0))
        for label in items:
            row = tk.Frame(feats, bg=BG2)
            row.pack(fill="x", pady=3)
            tk.Label(row, text="✦", font=("Segoe UI", 8),
                     bg=BG2, fg=ACCENT).pack(side="left")
            tk.Label(row, text=f"  {label}", font=("Segoe UI", 9),
                     bg=BG2, fg=TEXT2).pack(side="left")

        # Séparateur
        tk.Frame(body, bg=BORDER, height=1).pack(fill="x", padx=26, pady=(14, 0))

        # ── BOUTON DÉSINSTALLER ───────────────────────────────────────
        self.btn = tk.Button(
            body,
            text="  Desinstaller Akina RPC",
            font=("Segoe UI", 11, "bold"),
            bg=ACCENT, fg=TEXT,
            activebackground=ACCENT2,
            activeforeground=TEXT,
            relief="flat", bd=0,
            cursor="hand2",
            padx=20, pady=12,
            command=self._start_uninstall
        )
        self.btn.pack(fill="x", padx=26, pady=(14, 0))

        # Séparateur
        tk.Frame(body, bg=BORDER, height=1).pack(fill="x", padx=26, pady=(14, 0))

        # Barre de progression
        self.progress = ttk.Progressbar(
            body,
            style="Uninstall.Horizontal.TProgressbar",
            mode="determinate"
        )
        self.progress.pack(fill="x", padx=26, pady=(12, 0))

        self.status_lbl = tk.Label(
            body, text="Pret a desinstaller",
            font=("Segoe UI", 8),
            bg=BG2, fg=TEXT2
        )
        self.status_lbl.pack(anchor="w", padx=27, pady=(4, 0))

        # Console
        cw = tk.Frame(body, bg=CONSOLE_BG,
                      highlightbackground=BORDER, highlightthickness=1)
        cw.pack(fill="x", padx=26, pady=(12, 24))

        tk.Label(cw, text="  Console",
                 font=("Segoe UI", 7, "bold"),
                 bg=CONSOLE_BG, fg=TEXT2, anchor="w").pack(fill="x", pady=(4, 0))

        self.console = tk.Text(
            cw, bg=CONSOLE_BG, fg="#f87171",
            font=("Consolas", 7),
            relief="flat", state="disabled",
            wrap="word", bd=0, height=7
        )
        sb = ttk.Scrollbar(cw, orient="vertical", command=self.console.yview)
        self.console.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.console.pack(fill="x", padx=6, pady=(0, 6))

    # ── Logs ──────────────────────────────────────────────────────────
    def _log(self, msg):
        try:
            self.console.configure(state="normal")
            self.console.insert("end", msg + "\n")
            self.console.see("end")
            self.console.configure(state="disabled")
        except Exception:
            pass

    def _set_status(self, txt, pct):
        try:
            self.status_lbl.configure(text=txt)
            self.progress["value"] = pct
            self.update_idletasks()
        except Exception:
            pass

    # ── Désinstallation ───────────────────────────────────────────────
    def _start_uninstall(self):
        self.btn.configure(state="disabled", text="  Desinstallation en cours...")
        threading.Thread(target=self._uninstall, daemon=True).start()

    def _uninstall(self):
        try:
            # 1 — Tuer processus
            self._set_status("Arret du processus RPC...", 20)
            self._log("[>] Arret des processus Python RPC...")
            for proc in ["python.exe", "pythonw.exe"]:
                subprocess.run(
                    ["taskkill", "/F", "/IM", proc],
                    capture_output=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            self._log("[OK] Processus arretes.")

            # 2 — Registre
            self._set_status("Suppression du registre...", 45)
            self._log("[>] Suppression cle de demarrage...")
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Run",
                    0, winreg.KEY_SET_VALUE
                )
                winreg.DeleteValue(key, "AkinaRPC")
                winreg.CloseKey(key)
                self._log("[OK] Cle registre supprimee.")
            except FileNotFoundError:
                self._log("[OK] Cle deja absente.")
            except Exception as e:
                self._log(f"[!] Registre : {e}")

            # 3 — Dossier
            self._set_status("Suppression des fichiers...", 75)
            self._log(f"[>] Suppression de {INSTALL_DIR}...")
            if os.path.isdir(INSTALL_DIR):
                shutil.rmtree(INSTALL_DIR, ignore_errors=True)
                self._log("[OK] Dossier supprime.")
            else:
                self._log("[OK] Dossier deja absent.")

            self._set_status("Desinstallation terminee !", 100)
            self._log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            self._log("[OK] Akina RPC desinstalle avec succes !")
            self._log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            self.after(0, self._done)

        except Exception as e:
            self._log(f"[X] Erreur : {e}")
            self.after(0, lambda: self.btn.configure(
                state="normal",
                text="  ✖  Erreur — Reessayer",
                bg="#b91c1c", fg=TEXT,
                command=self._start_uninstall
            ))

    def _done(self):
        self.btn.configure(
            state="normal",
            text="  ✔  Termine — Fermer",
            bg=SUCCESS, fg=TEXT,
            command=self.destroy
        )


if __name__ == "__main__":
    app = AkinaUninstaller()
    app.mainloop()
