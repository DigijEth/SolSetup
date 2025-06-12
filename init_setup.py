#!/usr/bin/env python3
import os
import sys
import subprocess

# --- Prerequisite Checks: Rust and Node.js ---
# Check if Rust (cargo) is installed, if not, install it (for Anchor, Seahorse, etc.)
def ensure_rust_install():
    try:
        subprocess.run(["cargo", "--version"], check=True, stdout=subprocess.DEVNULL)
        print("Rust is already installed.")
    except subprocess.CalledProcessError:
        print("Rust/Cargo not found. Installing Rust toolchain (via rustup)...")
        # Install Rust using rustup (non-interactively)
        subprocess.run("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y",
                       shell=True, check=True)
        # Source the cargo environment to use in this script
        cargo_env = os.path.expanduser("~/.cargo/env")
        if os.path.exists(cargo_env):
            subprocess.run(f". {cargo_env}", shell=True, executable="/bin/bash")
        # Also update PATH for current session
        os.environ["PATH"] = os.path.expanduser("~/.cargo/bin") + ":" + os.environ.get("PATH", "")
        print("Rust/Cargo has been installed.")

# Check if Node.js is installed (for tools that need npm)
def check_node_install():
    node_installed = True
    try:
        subprocess.run(["node", "--version"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        node_installed = False
    try:
        subprocess.run(["npm", "--version"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        node_installed = False
    if not node_installed:
        print("Warning: Node.js/npm not detected. Some tools (e.g. Metaplex CLI) require Node 16+.")
    return node_installed

# Ensure Rust is installed (needed for several tools below)
ensure_rust_install()
node_available = check_node_install()

# --- Tool Definitions ---
tools = [
    # name, description, install_func or command, recommended (True/False), installable (True if script can install)
    {"name": "Solana CLI", 
     "desc": "Solana command-line tool (solana CLI and test validator)",
     "install": lambda: subprocess.run(
         'sh -c "$(curl -sSfL https://release.solana.com/stable/install)"', 
         shell=True, check=True),
     "recommended": True, "installable": True},
    {"name": "Anchor CLI", 
     "desc": "Anchor framework CLI for Solana development",
     # Install via Cargo
     "install": lambda: subprocess.run(
         ["cargo", "install", "--git", "https://github.com/solana-foundation/anchor", 
          "anchor-cli", "--locked"], check=True),
     "recommended": True, "installable": True},
    {"name": "Metaplex CLI (mplx)", 
     "desc": "Metaplex CLI for NFTs, tokens, and more",
     "install": lambda: subprocess.run(
         ["npm", "install", "-g", "@metaplex-foundation/cli"], check=True) 
         if node_available else print("Skipped Metaplex CLI (Node.js not available)"),
     "recommended": True, "installable": True},
    {"name": "AnchorPy (Python SDK)", 
     "desc": "Python client library for Anchor programs",
     "install": lambda: subprocess.run([sys.executable, "-m", "pip", "install", "anchorpy"], check=True),
     "recommended": False, "installable": True},
    {"name": "Shank (IDL generator)", 
     "desc": "CLI to generate IDL from Rust code",
     "install": lambda: subprocess.run(["cargo", "install", "shank-cli"], check=True),
     "recommended": False, "installable": True},
    {"name": "Seahorse (Python framework)", 
     "desc": "Write Solana programs in Python (Seahorse Lang)",
     "install": lambda: subprocess.run(["cargo", "install", "seahorse-dev"], check=True),
     "recommended": False, "installable": True},
    {"name": "Metaboss (NFT tool)", 
     "desc": "Metaplex NFT Swiss Army Knife CLI",
     "install": lambda: subprocess.run(["cargo", "install", "metaboss"], check=True),
     "recommended": False, "installable": True},
    # Tools that require extra setup or manual install will have installable=False.
    {"name": "Solana NextJS Scaffold", 
     "desc": "Next.js dApp starter project (clone from GitHub)",
     "install": None, "recommended": False, "installable": False},
    {"name": "Oxylana Scaffold", 
     "desc": "Rust program scaffold (clone from GitHub)",
     "install": None, "recommended": False, "installable": False},
    {"name": "Amman (Local test toolkit)", 
     "desc": "Testing toolkit for Solana (add via npm to your project)",
     "install": None, "recommended": False, "installable": False},
    {"name": "Solita (IDL TypeScript codegen)", 
     "desc": "TS code generator from IDL (add as dev dependency in project)",
     "install": None, "recommended": False, "installable": False},
    {"name": "Underdog API", 
     "desc": "API for dynamic NFTs (requires account setup)",
     "install": None, "recommended": False, "installable": False},
    {"name": "Concise Labs GraphQL API", 
     "desc": "GraphQL API for Solana data (requires account setup)",
     "install": None, "recommended": False, "installable": False},
    {"name": "Clockwork (Automation)", 
     "desc": "On-chain automation engine (requires integration/Docker setup)",
     "install": None, "recommended": False, "installable": False},
    {"name": "Solana Wallet Adapter", 
     "desc": "Wallet integration library for dApps (add via npm/yarn)",
     "install": None, "recommended": False, "installable": False},
    {"name": "Solana Wallet Names", 
     "desc": "Name service resolution library (integration via API/SDK)",
     "install": None, "recommended": False, "installable": False},
    {"name": "Solana Unity SDK", 
     "desc": "Unity SDK for Solana (import into Unity project)",
     "install": None, "recommended": False, "installable": False},
    {"name": "SolNet (.NET SDK)", 
     "desc": ".NET library for Solana (install via NuGet in project)",
     "install": None, "recommended": False, "installable": False},
    {"name": "Sol4k (Kotlin SDK)", 
     "desc": "Kotlin/JVM library for Solana (add via Gradle/Maven)",
     "install": None, "recommended": False, "installable": False},
    {"name": "Elusiv SDK", 
     "desc": "Privacy SDK for Solana (install via npm, requires integration)",
     "install": None, "recommended": False, "installable": False},
    {"name": "Nonci (Nonce Queue API)", 
     "desc": "API/SDK for queued transactions (requires integration)",
     "install": None, "recommended": False, "installable": False},
    {"name": "QuickNode RPC", 
     "desc": "Hosted RPC service (sign up on website)",
     "install": None, "recommended": False, "installable": False},
    {"name": "Chainstack RPC", 
     "desc": "Managed blockchain infrastructure (sign up on website)",
     "install": None, "recommended": False, "installable": False},
    {"name": "Helius API", 
     "desc": "Solana APIs, webhooks, indexer (sign up on website)",
     "install": None, "recommended": False, "installable": False},
    {"name": "Phantom Wallet (GUI)", 
     "desc": "Browser wallet for Solana (install extension manually)",
     "install": None, "recommended": False, "installable": False}
]

# Prepare menu display
print("\nSolana Development Tools Setup")
print("================================")
print("Select which tools to install or setup:")
for idx, tool in enumerate(tools, start=1):
    status = "(Recommended)" if tool["recommended"] else "(Optional)"
    # Mark non-installable tools in the prompt to indicate manual setup
    if not tool["installable"]:
        status += " [Manual setup]"
    print(f"{idx}. {tool['name']} - {tool['desc']} {status}")

print("A. All recommended    B. All (installable) tools    0. Exit")

# User selection input
choice = input("Enter the number(s) of tools to install (comma or space-separated), or choose an option (A/B/0): ").strip()

if not choice or choice.lower() == '0':
    print("No tools selected. Exiting setup.")
    sys.exit(0)

# Determine selection set
choice = choice.lower()
install_indices = []
if choice == 'a' or choice == 'all recommended':
    # Select all recommended tools
    install_indices = [i for i, t in enumerate(tools, start=1) if t["recommended"] and t["installable"]]
elif choice == 'b' or choice == 'all':
    # Select all installable tools (exclude manual-only ones)
    install_indices = [i for i, t in enumerate(tools, start=1) if t["installable"]]
else:
    # Parse specific numbers
    # Allow comma or space separated list of indices
    separators = "," if "," in choice else " "
    parts = [p for p in choice.replace(",", " ").split() if p.isdigit()]
    for p in parts:
        idx = int(p)
        if 1 <= idx <= len(tools):
            if tools[idx-1]["installable"]:
                install_indices.append(idx)
            else:
                # If a chosen tool is manual, we won't "install" it, but we can note it
                print(f"Note: {tools[idx-1]['name']} requires manual setup and will not be installed by this script.")
        else:
            print(f"Invalid selection: {p} (skipped)")
    # Remove duplicates and sort
    install_indices = sorted(set(install_indices))

# Execute installations for selected tools
if install_indices:
    print("\nInstalling selected tools...\n")
    for idx in install_indices:
        tool = tools[idx - 1]
        print(f"*** Installing {tool['name']} ***")
        try:
            if tool["install"]:
                tool["install"]()  # call the install lambda/function
                print(f"{tool['name']} installation completed.\n")
            else:
                # This case would only happen if a non-installable tool sneaked into list, which we handled above.
                print(f"{tool['name']} cannot be installed via script. Skipping.\n")
        except Exception as e:
            print(f"Error installing {tool['name']}: {e}\n")
else:
    print("No valid installable tools selected.")

# List tools that must be installed or set up manually (not handled by script)
manual_tools = [tool["name"] for tool in tools if not tool["installable"]]
if manual_tools:
    print("\nNOTE: The following tools were *not* installed by this script and require manual setup or installation:")
    for name in manual_tools:
        print(f" - {name}")
    print("Refer to the documentation for each of these tools for guidance on how to set them up.")
