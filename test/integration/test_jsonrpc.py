import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from kyand import KyanDaemon
from kyan_config import KyanConfig


def test_kyand():
    config_text = KyanConfig.slurp_config_file(config.kyan_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000551e93eb0749d40dfafd54b092e78d6612b47bd40de8d099818f65f53c1'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'000000313693c8b25165dbdc8498b8c0084fa24ffea6a02765733700fbcf7467'

    creds = KyanConfig.get_rpc_creds(config_text, network)
    kyand = KyanDaemon(**creds)
    assert kyand.rpc_command is not None

    assert hasattr(kyand, 'rpc_connection')

    # Kyan testnet block 0 hash == 000000313693c8b25165dbdc8498b8c0084fa24ffea6a02765733700fbcf7467
    # test commands without arguments
    info = kyand.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert kyand.rpc_command('getblockhash', 0) == genesis_hash
