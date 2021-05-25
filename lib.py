# -*- coding: utf-8 -*-
"""
The pyCFIP's library.
"""

import collections as _collections
import datetime as _datatime

import numpy as _numpy
import requests as _requests
import threadpool as _threadpool


class CloudflareSpeedTest(object):
    def __init__(
            self,
            _test_url: str,
            _test_host: str,
            _test_times: int,
            _dload_time,
            _dload_chunk_siz: int,
            _dload_timeout,
            _test_thread_amt: int
    ):
        self._test_times = _test_times
        self._dload_time = _dload_time
        self._dload_chunk_siz = _dload_chunk_siz
        self._dload_timeout = _dload_timeout
        self._test_thread_amt = _test_thread_amt
        self._req = _requests.session()
        self._headers = {'Host': _test_host}
        self._test_url = _test_url
        self._results = list()

    def _test(self, _ip: str):
        _dl_sped = list()
        _elapsed = list()
        for _t in range(self._test_times):
            try:
                _resp = self._req.get(
                    self._test_url.format(_ip),
                    headers=self._headers,
                    stream=True,
                    timeout=self._dload_timeout
                )
                if _resp.status_code != _requests.codes.ok:
                    raise _requests.exceptions.HTTPError
                _elapsed.append(_resp.elapsed.total_seconds())
                _dl = 0
                _start = _datatime.datetime.now()
                for _data in _resp.iter_content(
                        chunk_size=self._dload_chunk_siz
                ):
                    _dl += len(_data)
                    if (_datatime.datetime.now() - _start).seconds > \
                            self._dload_time:
                        _dl_sped.append(_dl / self._dload_time)
                        break
                self._prog += 1
                self._on_prog(self._prog / self._all)
            except (
                    _requests.exceptions.ConnectionError,
                    _requests.exceptions.ReadTimeout,
                    _requests.exceptions.ChunkedEncodingError,
                    _requests.exceptions.HTTPError
            ):
                self._prog += self._test_times - _t
                self._on_prog(self._prog / self._all)
                return
        self._results.append((
            _numpy.max(_dl_sped),
            _numpy.max(_elapsed),
            _numpy.mean(_dl_sped),
            _numpy.mean(_elapsed),
            _numpy.min(_dl_sped),
            _numpy.min(_elapsed),
            _ip
        ))

    def test(
            self,
            _ips: list,
            _on_prog: _collections.Callable
    ) -> list:
        self._on_prog = _on_prog
        self._results.clear()
        self._prog = 0
        self._all = len(_ips) * self._test_times
        _pool = _threadpool.ThreadPool(self._test_thread_amt)
        _tasks = _threadpool.makeRequests(self._test, _ips)
        _on_prog(0)
        [_pool.putRequest(_task) for _task in _tasks]
        _pool.wait()
        self._results.sort(
            key=lambda _item: (
                _item[0],
                # _item[1],
                _item[2],
                # _item[3],
                _item[4],
                # _item[5]
            ),
            reverse=True
        )
        return self._results
