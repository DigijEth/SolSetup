# path: tests/zero_trust.ts
import { ProgramTestContext } from '@project-serum/anchor/dist/cjs/provider';
import * as anchor from '@coral-xyz/anchor';
import { assert } from 'chai';

describe('zero_trust', () => {
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);
  const program = anchor.workspace.ZeroTrust as anchor.Program;

  it('initialises & updates a record', async () => {
    const owner = provider.wallet.publicKey;
    const [pda] = anchor.web3.PublicKey.findProgramAddressSync(
      [Buffer.from('user'), owner.toBuffer()],
      program.programId
    );

    const hash = new Array(32).fill(1);
    await program.methods.upsertUserData(hash as any, 'ipfs://demo').accounts({ owner, userRecord: pda }).rpc();
    let record = await program.account.userRecord.fetch(pda);
    assert.deepEqual(record.dataHash, Buffer.from(hash));
    assert.equal(record.uri, 'ipfs://demo');

    // update
    const hash2 = new Array(32).fill(2);
    await program.methods.upsertUserData(hash2 as any, 'ipfs://demo2').accounts({ owner, userRecord: pda }).rpc();
    record = await program.account.userRecord.fetch(pda);
    assert.deepEqual(record.dataHash, Buffer.from(hash2));
    assert.equal(record.uri, 'ipfs://demo2');
  });
});
