
## 📦 SolSetup

Automates the installation of essential Solidity and Ethereum development tooling via a shell setup script.

### 🔧 Tools Installed

When you run the setup script (e.g., `./init_setup.sh`), it installs:

* **Node.js** (via nvm) – ensures a compatible JavaScript runtime
* **npm / yarn** – JavaScript package managers
* **Truffle** – Ethereum development framework
* **Hardhat** – Alternative Ethereum development environment
* **Ganache CLI** – Local blockchain simulator
* **Solhint** – Solidity linter
* **Solcover** – Code coverage tool for Solidity
* **Prettier** (with `prettier-plugin-solidity`) – Code formatter
* **TypeChain** – TypeScript bindings for smart contracts
* **Ethers.js** – Ethereum library
* Any additional tools prescribed via plugin system or config file

*(Adjust this list based on your actual requirements – I included the most common tools typically used in Solidity setups.)*

### 🚀 Quick Start

```
git clone https://github.com/DigijEth/SolSetup.git
cd SolSetup
chmod +x install.sh
./install.sh
```

This boots up all listed tools and configures your shell environment (like adding nvm initialization in your `~/.bashrc` or `~/.zshrc`).

---

## 🛠️ How It Works

1. **Checks** your system for necessary prerequisites (e.g. `curl`, `git`).
2. **Installs** missing prerequisites.
3. **Installs Node.js** using nvm (adds a default LTS version).
4. **Installs global packages** like Truffle, Hardhat, etc. via npm/yarn.
5. **Configures** your shell startup file to source nvm and adds helpful aliases, if any.

---

## ➕ Adding New Tools or Dependencies

If you want to **add a new global npm tool**:

1. Open `install.sh`.

2. Add your tool to the global install list:

   ```bash
   GLOBAL_NPM_PACKAGES=(
     truffle
     hardhat
     ganache-cli
     solhint
     solcover
     prettier
     prettier-plugin-solidity
     typechain
     ethers
     your-new-tool-here
   )
   ```

3. Save and rerun the script – your new tool will be installed globally.

---

If your new tool **requires additional setup** (like fetching via `curl`, unpacking, or setting environment variables), add a dedicated install section at the bottom:

```bash
echo "Installing MyTool..."
curl -Lo mytool.tar.gz https://example.com/mytool-v1.2.3.tar.gz
tar -xzf mytool.tar.gz -C /usr/local/bin
```

You can wrap each install in a function if you want modularity:

```bash
install_mytool() {
  echo "Installing MyTool..."
  # commands...
}
```

And then invoke it near the end:

```bash
install_mytool
```

---

## 🧪 Verifying Installation

After the script finishes, verify each installation:

```
node -v
npm -v
truffle version
hardhat --version
ganache-cli --version
solhint --version
prettier --version
typechain --version
```

---

## 🎯 Updating Tools

To update tools globally, re-run:

```bash
npm update -g truffle hardhat ganache-cli solhint typechain your-new-tool
```

Or simply re-run `./install.sh`—if configured with `npm install -g`, it’ll pick up newer versions.

---

## 🧠 Customizing Shell Integration

The installer appends lines to your shell config (e.g., `.bashrc`, `.zshrc`) to load nvm and set useful aliases:

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

To customize aliases or tool versions, edit these sections directly in your shell config.

---

## 📝 README Structure Summary

```md
# SolSetup

## Tools Installed
- node, npm, truffle, hardhat, ganache-cli, solhint, solcover, prettier, typechain, ethers

## Quick Start

## How It Works

## Adding New Tools
(1) Add to GLOBAL_NPM_PACKAGES  
(2) Or write a custom install function  
(3) Re-run install script

## Verifying Installation

## Updating Tools

## Shell Integration & Customization
```
