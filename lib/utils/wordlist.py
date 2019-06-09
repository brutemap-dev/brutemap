#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

import os
import pickle

from lib.compat import file
from lib.compat import next
from lib.exceptions import BrutemapNullValueException

class Wordlist(object):
    """
    Kelas ini berfungsi untuk *mempercepat* proses pengambilan **kata** di file!
    jadi, anda dapat menggunakan file ukuran besar, tanpa harus menunggu lama (proses membaca).
    """

    def __init__(self, filenames):
        assert isinstance(filenames, list)
        self._filenames = filenames
        self._index = 0
        self._newlines = []
        self._fp = None

    def __iter__(self):
        # membuat klon objek, untuk proses bruteforce.
        # supaya, tidak mengurangi isi dari wordlist tersebut.
        return pickle.loads(pickle.dumps(self))

    def next(self):
        self.load()
        try:
            line = next(self._fp).rstrip()
            return line

        except AttributeError:
            return self.next()

        except StopIteration:
            if isinstance(self._fp, file):
                self._fp.close()
            self._fp = None
            return self.next()

    # untuk py3k
    __next__ = next

    def load(self):
        """
        Muat file selanjutnya atau *_newlines* jika tersedia.
        """

        if self._fp is None:
            # cek jika file belum di load semua
            if self._index < len(self._filenames):
                object_ = self._filenames[self._index]
                if os.path.isfile(object_):
                    object_ = open(object_, "r")
                else:
                    object_ = iter([object_])
                self._fp = object_
                # index file selanjutnya
                self._index += 1

            # cek jika file sudah di load semua
            elif self._index >= len(self._filenames) and len(self._newlines) != 0:
                # kemudian, load semua isi *_newlines*.
                self._fp = iter([self._newlines.pop(0)])

            else:
                # reset, jika data sudah di load semua.
                self._index = 0
                # lalu...
                raise BrutemapNullValueException # sebagai gantinya StopIteration
    
    def append(self, line):
        """
        Menambahkan line baru
        """

        self._newlines.append(line)
