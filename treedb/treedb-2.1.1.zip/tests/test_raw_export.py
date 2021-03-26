import pytest

from conftest import assert_file_size_between

CHECKSUM = {('v4.1', False): ('strong:sha256:'
                              '1d5a043b6cff9b2adb073e94eb67f5d4'
                              '789b3b8f215c1eb7a3f26d0d1858d90a'),
            ('v4.1', True): ('weak:sha256:'
                             '2380ef917237713ac2d6710c05bb6264'
                             '8f9dafa40024550906674a5135d05e3b'),
            ('v4.1', 'unordered'): ('unordered:sha256:'
                                    'dc6ed1762d47dec12432b09e0d1a1159'
                                    '153f062893bd884e8f21ec6b9e42d6c8'),
            ('v4.2', False): ('strong:sha256:'
                              '413ac7809d1f604a127f94d347f8279e'
                              'cba96ac460c29c20eba139a18bb63aa5'),
            ('v4.2', True): ('weak:sha256:'
                             'a3a5fe9e406b1c63ae3710e3583b191b'
                             'c75ac42fa802d424f71409cd141f4d6c'),
            ('v4.2.1', False): ('strong:sha256:'
                                '03ae265f46c79a5fd9ae44ada3ed5084'
                                '0dbdb897384b7ac57456ba12b6206a71'),
            ('v4.2.1', True): ('weak:sha256:'
                               '9cf661e51d8cd6d8ef1f5e93dbbf4612'
                               'a8a7e06712c56747d7a280b2d83f503b'),
            ('v4.3-treedb-fixes', False):
                ('strong:sha256:'
                 'db13f74ed52884084ab38b9693d42a58'
                 '9ff4ebc033ef1ed62b6463f44ea9320b'),
            ('v4.3-treedb-fixes', True):
                ('weak:sha256:'
                 '1f48d9a546fb99cab53eb171806d6a16'
                 'c5d9affc9c6f49d615692fdbd636c58c')}

RAW_CSV_SHA256 = {'v4.1': ('963163852e7f4ee34b516bc459bdbb90'
                           '8f2f4aab64bda58087a1a23a731921fd'),
                  'v4.2': ('e2ac065f5ce73af2165eb401831b53e0'
                           '494d8b25c4aa360fef879322b46f5f72'),
                  'v4.2.1': ('ab9d4339f3c0fa3acb0faf0f7306dc54'
                             '09640ecd46e451de9a76445519f5157e'),
                  'v4.3-treedb-fixes':
                          ('1ef6923a94d19c708fd0e7ae87b6ee24'
                           'c69d1d82fa9f81b16eaa5067e61ab1b6')}

MB = 2**20


pytestmark = pytest.FLAGS.skip_exclude_raw


def test_print_stats(capsys, treedb_raw):
    assert treedb_raw.print_stats() is None

    out, err = capsys.readouterr()
    assert not err

    assert out.strip()


@pytest.mark.parametrize('weak', [False, True, 'unordered'])
def test_checksum(treedb_raw, weak):
    expected = CHECKSUM.get((pytest.FLAGS.glottolog_tag, weak))

    result = treedb_raw.checksum(weak=weak)

    if expected is None:
        prefix, hash_name, hexdigest = result.split(':')
        assert prefix in ('strong', 'weak', 'unordered')
        assert hash_name == 'sha256'
        assert len(hexdigest) == 64
    else:
        assert result == expected


def test_write_raw_csv(treedb_raw):
    import treedb

    expected = RAW_CSV_SHA256.get(pytest.FLAGS.glottolog_tag)
    suffix = '-memory' if treedb.engine.file is None else ''

    path = treedb_raw.write_raw_csv()

    assert path.name == f'treedb{suffix}.raw.csv.gz'
    assert_file_size_between(path, 1, 100)

    if expected is None:
        pass
    else:
        shasum = treedb.sha256sum(path)
        assert shasum == expected
