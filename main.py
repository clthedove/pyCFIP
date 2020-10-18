# -*- coding: utf-8 -*-
"""
pyCFIP
A tool helps you to find some usable Cloudflare IP.
"""
__author__ = "clthedove"

import collections as _collections
import json as _json
import os as _os
import random as _random
import sys as _sys

from IPy import IP as _IP

from lib import CloudflareSpeedTest

ips_json = 'ips.json'
ranges_json = 'ranges.json'


def _test(
        _ips_list: list,
        _test_times: int,
        _dload_time,
        _dload_chunk_siz: int,
        _dload_timeout,
        _test_thread_amt: int,
        _test_ip_amt: int,
        _on_prog: _collections.Callable
) -> list:
    _random.shuffle(_ips_list)
    return CloudflareSpeedTest(
        _test_times,
        _dload_time,
        _dload_chunk_siz,
        _dload_timeout,
        _test_thread_amt
    ).test(
        _ips_list[:_test_ip_amt],
        _on_prog
    )


def _input_valid_number(
        _hint: str,
        _def,
        _val_typ,
        _min_val=-_sys.maxsize,
        _max_val=_sys.maxsize
):
    while True:
        try:
            _input = input(_hint)
            if _input == "":
                _input = _def
            if type(_input) != _val_typ:
                _input = _val_typ(_input)
            if _input in range(_min_val, _max_val + 1):
                return _input
            else:
                _error('not in valid range')
        except ValueError:
            _error('not a valid number')


def _input_valid_filepath(_hint: str, _def) -> str:
    while True:
        _input = input(_hint)
        if _input == "":
            _input = _def
        if _os.path.exists(_input):
            return _def
        else:
            _error('file not exist.')


def _get_term_width() -> int:
    try:
        return _os.get_terminal_size()[0]
    except OSError:
        return 80


def _show_prog(_p):
    """
    A function to show the progress bar.
    """
    print(
        '\r%s%8s' % (
            (
                    '#' * int(_p * (_get_term_width() - 8))
            ).ljust(_get_term_width() - 8),
            "%.2f%%" % (
                    _p * 100
            )
        ),
        end='\n' if _p == 1 else ''
    )


def _print(_pipe, _lines, _end: str = '\n'):
    _pipe.writelines([''.join(_lines), _end])


def _info(_value: str, _start: str = 'info: ', _end: str = '\n'):
    _print(_sys.stdout, [_start, _value], _end)


def _warn(_value: str, _start: str = 'warn: ', _end: str = '\n'):
    _print(_sys.stderr, [_start, _value], _end)


def _error(_value: str, _start: str = 'error: ', _end: str = '\n'):
    _print(_sys.stderr, [_start, _value], _end)


def main():
    """
    The main function of the program.
    """
    try:
        _info('pyCFIP <https://github.com/clthedove/pyCFIP>')
        if _os.path.exists(ips_json):
            with open(ips_json, 'r') as _f:
                _ips_list = _json.loads(_f.read())
            _info('using %s' % ips_json)
        else:
            if _os.path.exists(ranges_json):
                _info('using %s' % ranges_json)
                _f = open(ranges_json, 'r')
            else :
                _f = open(
                    _input_valid_filepath(
                        'enter ip ranges filepath[%s]: ' % ranges_json,
                        ranges_json
                    ), 'r')
            _ip_ranges = _json.loads(_f.read())
            _f.close()
            _ips = set()
            _j = len(_ip_ranges)
            _info('generating %s...' % ips_json)
            _show_prog(0)
            for _i in range(_j):
                _show_prog((_i + 1) / _j)
                _ip_range = _ip_ranges[_i]
                if not _ip_range.strip():
                    continue
                try:
                    _ips_ = _IP(_ip_range)
                except ValueError:
                    continue
                for _ip_ in _ips_:
                    _ips.add(str(_ip_))
            _ips_list = list(_ips)
            with open(ips_json, 'w') as _f_:
                _f_.write(_json.dumps(_ips_list))
        _test_times = _input_valid_number(
            'enter test times(1-N)[5]: ',
            5, int, 1)
        _dload_time = _input_valid_number(
            'enter download time(1-N)[10]: ',
            10, int, 1)
        _dload_chunk_siz = _input_valid_number(
            'enter download chunk size(1-N)[16384]: ',
            16384, int, 1)
        _dload_timeout = _input_valid_number(
            'enter download timeout(1-N)[2]: ',
            2, int, 1)
        _test_thread_amt = _input_valid_number(
            'enter test thread amount(1-N)[5]: ',
            5, int, 1)
        _test_ip_amt = _input_valid_number(
            'enter test ip amount(1-N)[100]: ',
            100, int, 1)
        while True:
            _info('starting test...')
            _valid_ips = _test(
                _ips_list.copy(),
                _test_times,
                _dload_time,
                _dload_chunk_siz,
                _dload_timeout,
                _test_thread_amt,
                _test_ip_amt,
                _show_prog
            )
            if _valid_ips:
                break
            else:
                _warn('nothing found, retrying')
        _len = len(_valid_ips)
        _info('found %d valid ips:' % _len)
        for _l in range(_len):
            (
                _max_dl_sped,
                _max_elapsed,
                _avg_dl_sped,
                _avg_elapsed,
                _min_dl_sped,
                _min_elapsed,
                _ip
            ) = _valid_ips[_l]
            print('%-24s\t%-24s\t%.2f-%.2f(%.2f)MiB/s' % (
                "[%d] %s" % (
                    _l + 1,
                    _ip
                ),
                "%d-%d(%d)MS" % (
                    _min_elapsed * 1000,
                    _max_elapsed * 1000,
                    _avg_elapsed * 1000
                ),
                _min_dl_sped / 1048576,
                _max_dl_sped / 1048576,
                _avg_dl_sped / 1048576
            ))
    except KeyboardInterrupt:
        _warn('terminated')
        _sys.exit()


if __name__ == '__main__':
    main()  # Run
