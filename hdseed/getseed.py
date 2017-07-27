# Copyright 2017, Evan Klitzke <evan@eklitzke.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import getpass
import os
import re
import sys
import tempfile

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

RPCUSER = re.compile(r'^\s*rpcuser\s*=\s*(.*)$')
RPCPASS = re.compile(r'^\s*rpcpassword\s*=\s*(.*)$')
MASTERKEY = re.compile(r'^# extended private masterkey: (\S+)$')


def get_connection(bitcoin_conf, rpc_addr):
    """Get a Bitcoin RPC connection."""
    rpc_user, rpc_pass = None, None
    with open(bitcoin_conf) as f:
        for line in f:
            m = RPCUSER.match(line)
            if m:
                rpc_user, = m.groups()
                continue
            m = RPCPASS.match(line)
            if m:
                rpc_pass, = m.groups()

    if rpc_user is None:
        raise ValueError('Missing rpcuser from bitcoin.conf')
    elif rpc_pass is None:
        raise ValueError('Missing rpcpassword from bitcoin.conf')
    url = 'http://{}:{}@{}'.format(rpc_user, rpc_pass, rpc_addr)
    return AuthServiceProxy(url)


def temp_dir():
    """Try to get a secure temporary directory."""
    home_dir = os.path.expanduser('~')
    priv_dir = os.path.join(home_dir, 'Private')
    if os.path.exists(priv_dir):
        return priv_dir
    return home_dir


def dumpwallet(conn, path, do_prompt=True, unlock_secs=5):
    """Dump the wallet, prompting for a passphrase if necessary."""
    try:
        conn.dumpwallet(path)
    except JSONRPCException:
        if not do_prompt:
            sys.exit('Please unlock your wallet and try again.')
        passphrase = getpass.getpass(
            'Wallet was locked; enter your passphrase here: ').strip()
        if passphrase:
            # The user can manually unlock the wallet and then give us an empty
            # password to bypass the unlock here.
            conn.walletpassphrase(passphrase, unlock_secs)
        conn.dumpwallet(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        default=os.path.expanduser('~/.bitcoin/bitcoin.conf'),
        help='Path to bitcoin.conf')
    parser.add_argument(
        '--rpc-addr', default='127.0.0.1:8332', help='RPC address')
    parser.add_argument(
        '--no-prompt',
        dest='do_prompt',
        default=True,
        action='store_false',
        help='Disable password prompt')
    args = parser.parse_args()

    conn = get_connection(args.config, args.rpc_addr)

    fd, temp_name = tempfile.mkstemp(
        prefix="tmp-wallet-", suffix=".txt", dir=temp_dir())
    os.fchmod(fd, 0o600)  # set permissions rw-------
    os.close(fd)

    try:
        dumpwallet(conn, temp_name, do_prompt=args.do_prompt)
        with open(temp_name) as f:
            for line in f:
                m = MASTERKEY.match(line)
                if m:
                    print(m.groups()[0])
                    break
    finally:
        os.unlink(temp_name)
