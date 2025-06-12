# path: clients/cli/src/encrypt_upload.ts
import { create } from 'ipfs-http-client';
import { randomBytes } from '@noble/ciphers/utils';
import { x25519, aes256ctr, hmac } from '@noble/ciphers';
import { sha256 } from '@noble/hashes/sha256';
import { Keypair, Connection, PublicKey } from '@solana/web3.js';
import { Program, AnchorProvider, IdlAccounts, utils } from '@coral-xyz/anchor';
import idl from '../../../target/idl/zero_trust.json' assert { type: 'json' };

const ipfs = create({ url: 'https://ipfs.infura.io:5001/api/v0' });
const connection = new Connection('http://localhost:8899');
const wallet = Keypair.fromSecretKey(
  Uint8Array.from(JSON.parse(require('fs').readFileSync(process.env.HOME + '/.config/solana/id.json')))
);
const provider = new AnchorProvider(connection, {
  publicKey: wallet.publicKey,
  signAllTransactions: async txs => {
    txs.forEach(tx => tx.partialSign(wallet));
    return txs;
  },
  signTransaction: async tx => {
    tx.partialSign(wallet);
    return tx;
  }
}, {});

// eslint-disable-next-line @typescript-eslint/consistent-type-definitions
type UserRecord = IdlAccounts<typeof idl>['userRecord'];

async function encryptAndUpload(filePath: string) {
  const plaintext = require('fs').readFileSync(filePath);
  // derive shared secret from wallet keypair -> simple self‑encryption
  const shared = x25519.getSharedSecret(wallet.secretKey.slice(0, 32), wallet.publicKey.toBytes());
  const iv = randomBytes(16);
  const cipher = aes256ctr(shared.slice(0, 32), iv);
  const ciphertext = cipher.encrypt(plaintext);
  const cid = await ipfs.add(Buffer.concat([iv, Uint8Array.from(ciphertext)]));

  const dataHash = sha256(ciphertext);
  const program = new Program(idl as any, new PublicKey(idl.metadata.address), provider);

  const [pda] = PublicKey.findProgramAddressSync(
    [Buffer.from('user'), wallet.publicKey.toBuffer()],
    program.programId
  );

  await program.methods
    .upsertUserData(Array.from(dataHash) as any, cid.path)
    .accounts({ owner: wallet.publicKey, userRecord: pda })
    .rpc();

  console.log('Stored metadata on chain. PDA:', pda.toBase58());
  console.log('IPFS CID:', cid.path);
}

encryptAndUpload(process.argv[2] || 'secret.pdf').catch(console.error);
