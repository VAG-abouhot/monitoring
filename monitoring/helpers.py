# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Valind&GO
http://www.validandgo.com/
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import calendar
import datetime
import decimal
import json
import sys
import warnings

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote


PY2 = (sys.version_info[0] == 2)


def deprecated(func):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used.
    """

    def newFunc(*args, **kwargs):
        warnings.warn('Call to deprecated function %s.' % func.__name__,
                      category=DeprecationWarning)
        return func(*args, **kwargs)

    newFunc.__name__ = func.__name__
    newFunc.__doc__ = func.__doc__
    newFunc.__dict__.update(func.__dict__)
    return newFunc


def encode(e):
    """Unicode helper for Python 2.x"""
    if PY2 and isinstance(e, unicode):
        e = e.encode('utf-8')
    return e


def safe(e):
    """Returns a safe string for URL."""
    if PY2 and isinstance(e, unicode):
        return quote(e.encode('utf-8'), safe='')
    else:
        return quote(str(e), safe='')


def urlify(e):
    """Return dict/list/value that can be used as URL parameters."""
    if isinstance(e, dict):
        try:
            iteritems = e.iteritems()
        except AttributeError:
            iteritems = e.items()

        return dict((k, urlify(v)) for k, v in iteritems)
    elif isinstance(e, (list, tuple)):
        return json.dumps(e, cls=CustomJSONEncoder)
    elif isinstance(e, bool):
        return 'true' if e else 'false'
    else:
        return encode(e)

def endpoint(path, *args):
    # type: (str, Optional[Union[str, int]]) -> str

    arguments = []
    for arg in args:
        if not sys.version_info >= (3, 0) and isinstance(arg, unicode):
            arguments.append(
                quote(arg.encode('utf-8'), safe='')
            )  # pragma: no cover
        else:
            arguments.append(quote(str(arg), safe=''))  # pragma: no cover

    return getattr(path, 'format')(*arguments)

def rotate(l, n=1):
    """
    Return the list rotated n times.
        rotate([1, 2, 3], 2) => [3, 1, 2]
    """
    return l[n:] + l[:n]

    
def get_items(dictionary=None):
    # type: (Optional[dict]) -> Iterable

    if dictionary is None:
        items = []  # type: Iterable
    elif sys.version_info >= (3, 0):
        items = dictionary.items()
    else:
        items = dictionary.iteritems()  # pragma: no cover

    return items
    
    
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, datetime.datetime):
            try:
                return int(calendar.timegm(obj.utctimetuple()))
            except:
                return 0

        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            if PY2:
                return unicode(obj)
            else:
                return str(obj)


class MonitoringException(Exception):
    """Exception launched by Monitoring Client when an error occured."""