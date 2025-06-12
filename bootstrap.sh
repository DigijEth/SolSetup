# create and enter the project
npm create svelte@latest pedophile‑ai‑client
cd pedophile‑ai‑client

# add dependencies
npm install --save \
    @solana/web3.js            \
    @solana/wallet-adapter-base \
    @solana/wallet-adapter-svelte \
    @solana/wallet-adapter-wallets \
    tweetnacl tweetnacl-util      \
    @tailwindcss/forms postcss autoprefixer \
    zod                           # runtime schema validation
