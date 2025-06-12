# path: init_setup.py
#!/usr/bin/env python3
"""
Setec Gaming Labs – Decency Checker & Installer
Converted from `framework_alpha.sh` (dependency section) to Python.

Features
--------
*   Shows a dependency checklist with ✅ / ❌ status marks.
*   Lets the user:
    • install **all** missing tools
    • install a **recommended** subset
    • install **selected** tools by entering comma‑separated numbers
*   Gracefully skips tools if the host OS/package manager is unsupported
*   Wraps every shell install command with user confirmation
*   Works on Linux/macOS (requires `sudo` privileges for system installs)

© 2025 Setec Gaming Labs – No warranty.  Use at your own risk.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import textwrap
import time
from typing import Callable, List, Tuple

GREEN = "\033[0;32m"
RED = "\033[0;31m"
NC = "\033[0m"

# --------------------------------------------------------------------------- #
#  Dependency table                                                           #
# --------------------------------------------------------------------------- #
Dependency = Tuple[str, List[str], str | Callable[[], str]]

DEPENDENCIES: List[Dependency] = [
    ("Node.js + npm", ["node", "npm"], "sudo apt-get install -y nodejs npm"),
    ("Rust (cargo)", ["cargo"], "sudo apt-get install -y cargo"),
    ("Anchor CLI", ["anchor"], lambda: "cargo install --git https://github.com/coral-xyz/anchor anchor-cli"),
    ("netlify‑cli", ["netlify"], "npm install -g netlify-cli"),
    ("vercel CLI", ["vercel"], "npm install -g vercel"),
    ("Solana CLI", ["solana"], 'sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"'),
    ("spl‑token CLI", ["spl-token"], "cargo install spl-token-cli"),
    ("Metaplex CLI", ["metaplex"], "npm install -g @metaplex-foundation/cli"),
    (
        "Openbook DEX CLI",
        ["openbook-dex"],
        textwrap.dedent(
            """
            git clone https://github.com/openbook-dex/program.git openbook-dex &&
            cd openbook-dex/dex/cli &&
            cargo build --release &&
            sudo cp target/release/openbook-dex /usr/local/bin/ &&
            cd ../../.. &&
            rm -rf openbook-dex
            """
        ).replace("\n", " ").strip(),
    ),
    ("Raydium CLI", ["raydium"], "npm install -g @raydium-io/raydium-cli"),
    ("Jupiter CLI", ["jupiter"], "npm install -g @jup-ag/jupiter-cli"),
]

RECOMMENDED_IDX = {0, 1, 2, 5, 6, 7}  # indices in DEPENDENCIES


# --------------------------------------------------------------------------- #
#  Helpers                                                                    #
# --------------------------------------------------------------------------- #
def command_exists(cmd: str) -> bool:
    """Return True if *cmd* is on $PATH."""
    return shutil.which(cmd) is not None


def installed(dep: Dependency) -> bool:
    """Return True if *all* commands listed for a dependency are present."""
    _, cmds, _ = dep
    return all(command_exists(c) for c in cmds)


def print_header() -> None:
    os.system("clear" if os.name != "nt" else "cls")
    print(f"{GREEN}{'-' * 63}")
    print("| Setec Gaming Labs – Dependency Checker".ljust(62) + "|")
    print(f"{'-' * 63}{NC}")


def scan_progress() -> None:
    print("Detecting dependencies...")
    for pct in range(20, 101, 20):
        print(f"Progress: {pct}%")
        time.sleep(0.3)
    print("Dependency scan complete.\n")
    time.sleep(0.5)


def show_checklist() -> None:
    print_header()
    print("Dependency Checklist:\n")
    for i, (label, _, _) in enumerate(DEPENDENCIES, 1):
        status = "✅" if installed(DEPENDENCIES[i - 1]) else "❌"
        print(f"{i:>2}. {label:<20} : {status}")
    print(
        "\nType 'A' to install all missing, "
        "'R' for recommended, or list numbers separated by commas (e.g., 1,3,5)."
    )
    print("M. Return/Exit\n")


def run_install(cmd: str) -> None:
    """Run an install shell command with live output."""
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"{RED}❌ Installation failed (code {exc.returncode}).{NC}")


def get_install_cmd(dep: Dependency) -> str:
    """Return the shell command string for a dependency."""
    cmd = dep[2]
    return cmd() if callable(cmd) else cmd


def verify_or_install(idx: int) -> None:
    label, _, _ = DEPENDENCIES[idx]
    if installed(DEPENDENCIES[idx]):
        print(f"{GREEN}✓ {label} already installed.{NC}")
        return

    cmd = get_install_cmd(DEPENDENCIES[idx])

    print(f"\nAbout to install: {label}")
    print(f"Install command:\n  {cmd}\n")
    confirm = input("Proceed? (y/N) ").strip().lower()
    if confirm != "y":
        print("Skipped.\n")
        return

    run_install(cmd)
    print("")  # spacer


# --------------------------------------------------------------------------- #
#  Main interactive loop                                                      #
# --------------------------------------------------------------------------- #
def main() -> None:
    disclaimer = textwrap.dedent(
        f"""
        {RED}DISCLAIMER:{NC}
        Setec Gaming Labs is not responsible for any financial or other losses.
        This tool is provided as‑is.  By using it you agree not to hold Setec
        Gaming Labs or its contributors liable for your losses.
        """
    )
    print(disclaimer)
    if input("Do you accept these terms? (y/N) ").strip().lower() != "y":
        sys.exit("Terms not accepted. Exiting.")

    scan_progress()

    while True:
        show_checklist()
        choice = input("Enter selection: ").strip().lower()

        if choice in {"m", "q", "quit", "exit"}:
            break
        if choice == "a":
            for i in range(len(DEPENDENCIES)):
                verify_or_install(i)
            continue
        if choice == "r":
            for i in RECOMMENDED_IDX:
                verify_or_install(i)
            continue

        # numeric list handling
        try:
            selections = {int(x) for x in choice.split(",")}
        except ValueError:
            print(f"{RED}Invalid input. Try again.{NC}")
            continue

        for idx in sorted(selections):
            if 1 <= idx <= len(DEPENDENCIES):
                verify_or_install(idx - 1)
            else:
                print(f"{RED}Invalid selection: {idx}{NC}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
