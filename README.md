# Bitcoin HD Seed

This script assists with dumping
the [HD wallet seed](https://bitcoin.org/en/glossary/hd-wallet-seed) for a
Bitcoin Core [HD wallet](https://bitcoin.org/en/glossary/hd-protocol). HD
wallets were introduced to Core starting
with [Bitcoin Core 0.13.0](https://bitcoin.org/en/release/v0.13.0), released
August 23, 2016. This tool works by calling the `dumpwallet` JSON-RPC method,
and extracting the master seed from its output. For more information about HD
wallets,
see [BIP32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki).

In principle, the master seed is the *only* thing you need to back up if you are
using an HD wallet; all subsequent keys used by the wallet are generated
deterministically from the HD seed. You can use a tool
like [bip32utils](https://github.com/prusnak/bip32utils) to experiment with
these derived keys.

## Installation

From the git checkout:

```bash
# Optional: create and activate a virtualenv
mkvirtualenv -p python3 bitcoin-hd-seed
workon bitcoin-hd-seed

# Install get-hd-seed
pip install -r requirements.txt
python setup.py install
```

This will install a command called `get-hd-seed`.

## Usage

Just run `get-hd-seed`, and the seed will be dumped to stdout.

If your wallet is locked, you will be prompted for a wallet passphrase. If you
don't feel comfortable typing your passphrase this way, manually unlock the
wallet (e.g. `bitcoin-cli -stdin walletpassphrase`) and then enter a blank
passphrase at the prompt.
