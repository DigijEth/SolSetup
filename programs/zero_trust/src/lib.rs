# path: programs/zero_trust/src/lib.rs
use anchor_lang::prelude::*;

declare_id!("ZrTrst1zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz");

#[program]
pub mod zero_trust {
    use super::*;

    /// Creates (or overwrites) a PDA‑backed record that stores the
    /// SHA‑256 hash of the user‑encrypted payload and a content URI.
    pub fn upsert_user_data(
        ctx: Context<UpsertUserData>,
        data_hash: [u8; 32],
        uri: String,
    ) -> Result<()> {
        let record = &mut ctx.accounts.user_record;
        record.owner = ctx.accounts.owner.key();
        record.data_hash = data_hash;
        record.uri = uri;
        record.bump = *ctx.bumps.get("user_record").unwrap();
        Ok(())
    }

    /// Allows the owner to close (delete) their record.
    pub fn delete_user_data(ctx: Context<DeleteUserData>) -> Result<()> {
        let record = &mut ctx.accounts.user_record;
        record.close(ctx.accounts.owner.to_account_info())?;
        Ok(())
    }
}

#[derive(Accounts)]
#[instruction(data_hash: [u8; 32], uri: String)]
pub struct UpsertUserData<'info> {
    #[account(mut)]
    pub owner: Signer<'info>,

    /// PDA: seeds = [b"user", owner], space = 8 + 32 + 4 + uri.len()
    #[account(
        init_if_needed,
        seeds = [b"user", owner.key().as_ref()],
        bump,
        payer = owner,
        space = 8 + 32 + 4 + uri.len()
    )]
    pub user_record: Account<'info, UserRecord>,

    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct DeleteUserData<'info> {
    #[account(mut)]
    pub owner: Signer<'info>,

    #[account(
        mut,
        seeds = [b"user", owner.key().as_ref()],
        bump = user_record.bump,
        close = owner
    )]
    pub user_record: Account<'info, UserRecord>,
}

#[account]
pub struct UserRecord {
    pub owner: Pubkey,
    pub data_hash: [u8; 32],
    pub uri: String,
    pub bump: u8,
}
