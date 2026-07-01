import tkinter as tk
from tkinter import ttk
import threading
import subprocess
import sys
import os
import shutil
import winreg
import webbrowser
import urllib.request
from PIL import Image, ImageTk, ImageDraw

BG         = "#0f0f0f"
BG2        = "#161616"
ACCENT     = "#7c3aed"
ACCENT2    = "#6d28d9"
SUCCESS    = "#22c55e"
TEXT       = "#ffffff"
TEXT2      = "#a1a1aa"
BORDER     = "#27272a"
CONSOLE_BG = "#0a0a0a"

INSTALL_DIR = os.path.join(os.environ["APPDATA"], "AkinaRPC")
SCRIPT_DST  = os.path.join(INSTALL_DIR, "rpc_script.py")
VBS_DST     = os.path.join(INSTALL_DIR, "launch.vbs")
SITE_URL    = "https://donuts-club.com/akina.php"
PYTHON_URL  = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
PYTHON_INST = os.path.join(os.environ["TEMP"], "python_installer.exe")

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


class AkinaInstaller(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Akina RPC — Installer")
        self.geometry("620x640")
        self.resizable(False, False)
        self.configure(bg=BG)
        self._center()
        self._set_icon()
        self._build_ui()

    def _center(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - 620) // 2
        y = (self.winfo_screenheight() - 640) // 2
        self.geometry(f"620x640+{x}+{y}")

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
            nh   = min(int(h * (620 / w)), 180)
            raw  = raw.resize((620, nh), Image.LANCZOS)
            self._banner = ImageTk.PhotoImage(raw)
            tk.Label(self, image=self._banner, bg=BG, bd=0).pack(fill="x")
        except Exception:
            tk.Label(self, text="Akina RPC",
                     font=("Segoe UI", 22, "bold"),
                     bg=BG, fg=ACCENT).pack(pady=16)

        outer = tk.Frame(self, bg=BG2)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, bg=BG2, bd=0, highlightthickness=0)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.Vertical.TScrollbar",
                        background=BORDER, troughcolor=BG2,
                        arrowcolor=TEXT2, borderwidth=0, relief="flat")
        style.configure("Akina.Horizontal.TProgressbar",
                        troughcolor=BORDER, background=ACCENT,
                        thickness=6, borderwidth=0, relief="flat")

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

        # Logo + titre
        top = tk.Frame(body, bg=BG2)
        top.pack(pady=(22, 6), padx=30, anchor="w")

        try:
            img = make_circle_image(resource("logo.png"), 72)
            self._logo = ImageTk.PhotoImage(img)
            tk.Label(top, image=self._logo, bg=BG2, bd=0).pack(side="left", padx=(0, 16))
        except Exception:
            tk.Label(top, text="A", font=("Segoe UI", 36, "bold"),
                     bg=BG2, fg=ACCENT).pack(side="left", padx=(0, 16))

        col = tk.Frame(top, bg=BG2)
        col.pack(side="left")
        tk.Label(col, text="Akina RPC",
                 font=("Segoe UI", 20, "bold"),
                 bg=BG2, fg=TEXT).pack(anchor="w")
        tk.Label(col, text="Discord Rich Presence  •  v1.0",
                 font=("Segoe UI", 9),
                 bg=BG2, fg=TEXT2).pack(anchor="w", pady=(2, 0))

        tk.Frame(body, bg=BORDER, height=1).pack(fill="x", padx=26, pady=(12, 0))

        feats = tk.Frame(body, bg=BG2)
        feats.pack(fill="x", padx=34, pady=(12, 0))
        for label in [
            "Serveur +10 000 membres",
            "Fait partie de l'elite de Akina",
            "App fiable et code source disponible",
            "Affiche ton statut Discord personnalise",
        ]:
            row = tk.Frame(feats, bg=BG2)
            row.pack(fill="x", pady=3)
            tk.Label(row, text="✦", font=("Segoe UI", 8),
                     bg=BG2, fg=ACCENT).pack(side="left")
            tk.Label(row, text=f"  {label}", font=("Segoe UI", 9),
                     bg=BG2, fg=TEXT2).pack(side="left")

        tk.Frame(body, bg=BORDER, height=1).pack(fill="x", padx=26, pady=(14, 0))

        self.btn = tk.Button(
            body,
            text="  Installer Akina RPC",
            font=("Segoe UI", 11, "bold"),
            bg=ACCENT, fg=TEXT,
            activebackground=ACCENT2, activeforeground=TEXT,
            relief="flat", bd=0, cursor="hand2",
            padx=20, pady=12,
            command=self._start_install
        )
        self.btn.pack(fill="x", padx=26, pady=(14, 0))

        tk.Frame(body, bg=BORDER, height=1).pack(fill="x", padx=26, pady=(14, 0))

        self.progress = ttk.Progressbar(body,
                                        style="Akina.Horizontal.TProgressbar",
                                        mode="determinate")
        self.progress.pack(fill="x", padx=26, pady=(12, 0))

        self.status_lbl = tk.Label(body, text="Pret a installer",
                                   font=("Segoe UI", 8), bg=BG2, fg=TEXT2)
        self.status_lbl.pack(anchor="w", padx=27, pady=(4, 0))

        cw = tk.Frame(body, bg=CONSOLE_BG,
                      highlightbackground=BORDER, highlightthickness=1)
        cw.pack(fill="x", padx=26, pady=(12, 24))

        tk.Label(cw, text="  Console", font=("Segoe UI", 7, "bold"),
                 bg=CONSOLE_BG, fg=TEXT2, anchor="w").pack(fill="x", pady=(4, 0))

        self.console = tk.Text(cw, bg=CONSOLE_BG, fg="#a3e635",
                               font=("Consolas", 7), relief="flat",
                               state="disabled", wrap="word", bd=0, height=7)
        sb = ttk.Scrollbar(cw, orient="vertical", command=self.console.yview)
        self.console.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.console.pack(fill="x", padx=6, pady=(0, 6))

    # ── Logs (thread-safe) ────────────────────────────────────────────
    def _log(self, msg):
        def _do():
            try:
                self.console.configure(state="normal")
                self.console.insert("end", msg + "\n")
                self.console.see("end")
                self.console.configure(state="disabled")
            except Exception:
                pass
        self.after(0, _do)

    def _set_status(self, txt, pct):
        def _do():
            try:
                self.status_lbl.configure(text=txt)
                self.progress["value"] = pct
            except Exception:
                pass
        self.after(0, _do)

    # ── Installation ──────────────────────────────────────────────────
    def _start_install(self):
        self.btn.configure(state="disabled", text="  Installation en cours...")
        threading.Thread(target=self._install, daemon=True).start()

    def _install(self):
        try:
            # 1 — Python
            self._set_status("Verification de Python...", 8)
            self._log("[>] Verification de Python...")
            py = self._find_python()

            if not py:
                self._log("[>] Python absent — telechargement en cours...")
                self._log(f"[>] URL : {PYTHON_URL}")
                self._download_python()
                self._set_status("Installation de Python 3.11...", 28)
                self._log("[>] Lancement de l'installateur Python...")
                self._log("[>] Cela peut prendre 1 a 2 minutes...")
                self._install_python()
                self._log("[>] Verification post-installation...")
                py = self._find_python()
                if not py:
                    self._error("Python introuvable apres installation.")
                    return
                self._log(f"[OK] Python installe : {py}")
            else:
                self._log(f"[OK] Python detecte : {py}")

            # 2 — pypresence
            self._set_status("Installation de pypresence...", 42)
            self._log("[>] Installation de pypresence...")
            result = subprocess.run(
                [py, "-m", "pip", "install", "pypresence"],
                capture_output=True, text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            for line in (result.stdout + result.stderr).splitlines():
                line = line.strip()
                if line:
                    self._log(f"    {line}")
            if result.returncode != 0:
                raise RuntimeError(f"pip exit code {result.returncode}")
            self._log("[OK] pypresence installe.")

            # 3 — Copie script
            self._set_status("Copie des fichiers...", 62)
            self._log("[>] Copie du script RPC...")
            os.makedirs(INSTALL_DIR, exist_ok=True)
            shutil.copy(resource("rpc_script.py"), SCRIPT_DST)
            self._log(f"[OK] Script -> {SCRIPT_DST}")

            # 4 — Création du .vbs lanceur
            self._log("[>] Creation du lanceur VBS...")
            self._write_vbs(py)
            self._log(f"[OK] VBS -> {VBS_DST}")

            # 5 — Démarrage via VBS
            self._set_status("Configuration du demarrage...", 78)
            self._log("[>] Ajout du VBS au demarrage Windows...")
            self._add_startup_vbs()
            self._log("[OK] Demarrage automatique configure.")

            # 6 — Lancement immédiat via VBS
            self._set_status("Lancement du RPC...", 92)
            self._log("[>] Lancement silencieux via VBS...")
            self._launch_vbs()
            self._log("[OK] RPC actif en arriere-plan.")

            # 7 — Terminé
            self._set_status("Installation terminee !", 100)
            self._log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            self._log("[OK] Akina RPC installe avec succes !")
            self._log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            self.after(0, self._done)

        except Exception as e:
            self._log(f"[X] Erreur fatale : {e}")
            self._error(str(e))

    # ── VBS ───────────────────────────────────────────────────────────
    def _write_vbs(self, py):
        """
        Crée launch.vbs qui lance pythonw.exe rpc_script.py sans aucune fenêtre.
        pythonw.exe = python sans console, chemin absolu garanti.
        """
        py_abs    = os.path.abspath(py)
        # pythonw.exe est dans le même dossier que python.exe
        pythonw   = os.path.join(os.path.dirname(py_abs), "pythonw.exe")
        if not os.path.isfile(pythonw):
            # fallback : python.exe avec fenêtre cachée
            pythonw = py_abs

        vbs = (
            'Set objShell = CreateObject("WScript.Shell")\n'
            f'objShell.Run Chr(34) & "{pythonw}" & Chr(34) & " " & '
            f'Chr(34) & "{SCRIPT_DST}" & Chr(34), 0, False\n'
        )
        os.makedirs(INSTALL_DIR, exist_ok=True)
        with open(VBS_DST, "w", encoding="utf-8") as f:
            f.write(vbs)

    def _add_startup_vbs(self):
        """
        Double méthode de démarrage :
        1. Clé Run du registre (avec chemin complet wscript.exe)
        2. Dossier Startup Windows (fallback garanti)
        """
        wscript = os.path.join(
            os.environ.get("SystemRoot", r"C:\Windows"),
            "System32", "wscript.exe"
        )
        cmd = f'"{wscript}" "{VBS_DST}"'

        # — Méthode 1 : Registre Run ──────────────────────────────────
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, "AkinaRPC", 0, winreg.REG_SZ, cmd)
            winreg.CloseKey(key)
            self._log(f"[OK] Registre Run : {cmd}")
        except Exception as e:
            self._log(f"[!] Registre : {e}")

        # — Méthode 2 : Dossier Startup ───────────────────────────────
        try:
            startup_dir = os.path.join(
                os.environ["APPDATA"],
                r"Microsoft\Windows\Start Menu\Programs\Startup"
            )
            shortcut_vbs = os.path.join(startup_dir, "AkinaRPC.vbs")
            # Copie directement le .vbs dans Startup
            shutil.copy(VBS_DST, shortcut_vbs)
            self._log(f"[OK] Startup folder : {shortcut_vbs}")
        except Exception as e:
            self._log(f"[!] Startup folder : {e}")


    def _launch_vbs(self):
        """Lance immédiatement le VBS (sans attendre)."""
        subprocess.Popen(
            ["wscript.exe", VBS_DST],
            creationflags=subprocess.CREATE_NO_WINDOW
        )

    # ── Helpers Python ────────────────────────────────────────────────
    def _is_stub(self, path):
        if not path:
            return True
        if "windowsapps" in path.replace("\\", "/").lower():
            return True
        try:
            r = subprocess.run(
                [path, "-m", "pip", "--version"],
                capture_output=True, text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=10
            )
            return r.returncode != 0
        except Exception:
            return True

    def _find_python(self):
        candidates = []
        local = os.environ.get("LOCALAPPDATA", "")
        for ver in ["313", "312", "311", "310", "39"]:
            p = os.path.join(local, "Programs", "Python", f"Python{ver}", "python.exe")
            if os.path.isfile(p):
                candidates.append(p)

        for cmd in ["python", "python3"]:
            found = shutil.which(cmd)
            if found:
                candidates.append(found)

        for root_hive in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
            for sub in [r"SOFTWARE\Python\PythonCore",
                        r"SOFTWARE\WOW6432Node\Python\PythonCore"]:
                try:
                    key = winreg.OpenKey(root_hive, sub)
                    i = 0
                    while True:
                        try:
                            ver = winreg.EnumKey(key, i)
                            try:
                                ikey = winreg.OpenKey(key, rf"{ver}\InstallPath")
                                try:
                                    exe = winreg.QueryValueEx(ikey, "ExecutablePath")[0]
                                except Exception:
                                    base = winreg.QueryValueEx(ikey, "")[0]
                                    exe  = os.path.join(base, "python.exe")
                                if os.path.isfile(exe):
                                    candidates.append(exe)
                            except Exception:
                                pass
                            i += 1
                        except OSError:
                            break
                except Exception:
                    pass

        for c in candidates:
            if self._is_stub(c):
                self._log(f"[!] Stub ignore : {c}")
                continue
            try:
                r = subprocess.run(
                    [c, "--version"],
                    capture_output=True, text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    timeout=10
                )
                if r.returncode == 0 and "Python" in (r.stdout + r.stderr):
                    return c
            except Exception:
                continue
        return None

    def _download_python(self):
        last_pct = [-1]
        def hook(count, block, total):
            if total > 0:
                pct = min(int(count * block * 100 / total), 100)
                if pct != last_pct[0]:
                    last_pct[0] = pct
                    mb_done  = round(count * block / 1_048_576, 1)
                    mb_total = round(total / 1_048_576, 1)
                    self._set_status(
                        f"Telechargement Python 3.11... {pct}%  ({mb_done}/{mb_total} MB)",
                        12 + int(pct * 0.15)
                    )
                    self._log(f"[↓] Python {pct}% — {mb_done}/{mb_total} MB")
        self._log(f"[>] Destination : {PYTHON_INST}")
        urllib.request.urlretrieve(PYTHON_URL, PYTHON_INST, hook)
        self._log("[OK] Telechargement termine.")

    def _install_python(self):
        import time
        self._log("[>] Commande : python_installer.exe /quiet PrependPath=1 ...")

        proc = subprocess.Popen(
            [
                PYTHON_INST, "/quiet",
                "InstallAllUsers=0", "PrependPath=1",
                "Include_pip=1", "Include_launcher=0",
            ],
            creationflags=subprocess.CREATE_NO_WINDOW
            # PAS de stdout=PIPE — l'installateur MSI ne produit rien
        )

        steps = [
            "Installation Python — preparation...",
            "Installation Python — copie des fichiers...",
            "Installation Python — copie des fichiers...",
            "Installation Python — copie des fichiers...",
            "Installation Python — configuration...",
            "Installation Python — configuration...",
            "Installation Python — finalisation...",
            "Installation Python — finalisation...",
        ]
        step_idx = 0
        # On anime de 28% → 54% pendant que l'installateur tourne
        pct = 28

        while proc.poll() is None:
            label = steps[step_idx % len(steps)]
            self._set_status(label, min(pct, 54))
            if step_idx % 4 == 0:          # log toutes les 2s
                self._log(f"[...] {label}")
            pct       += 1
            step_idx  += 1
            time.sleep(0.5)

        rc = proc.returncode
        # L'installateur Python retourne 0 OU 1641/3010 (reboot requis) = OK
        if rc not in (0, 1641, 3010):
            raise RuntimeError(f"Installateur Python exit code {rc}")

        self._log(f"[OK] Installateur Python termine (code {rc}).")

        new_path = os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            "Programs", "Python", "Python311"
        )
        os.environ["PATH"] = (
            new_path + os.pathsep +
            os.path.join(new_path, "Scripts") + os.pathsep +
            os.environ["PATH"]
        )
        self._log(f"[OK] PATH mis a jour : {new_path}")

    def _done(self):
        self.btn.configure(
            state="normal",
            text="  ✔  Termine — Fermer",
            bg=SUCCESS, fg=TEXT,
            command=self.destroy
        )
        webbrowser.open(SITE_URL)

    def _error(self, msg):
        self.after(0, lambda: self.btn.configure(
            state="normal",
            text="  ✖  Erreur — Reessayer",
            bg="#ef4444", fg=TEXT,
            command=self._start_install
        ))
        self.after(0, lambda: self._set_status(f"Erreur : {msg}", 0))


if __name__ == "__main__":
    app = AkinaInstaller()
    app.mainloop()
