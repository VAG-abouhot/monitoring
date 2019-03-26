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

class Model(object):
    """
    Contains all the functions related to one model.
    >>> model = application.create_model('myModelName', 'modelDescription','modelVersion')
    """
    
    def __init__(self, model_name, model_description, model_version):
        self.model_name = model_name
        self.model_description = model_description
        self.model_version = model_version
        self._request_path = '/applications/%s' % safe(self.model_name)

    def __repr__(self):
        return u'<Model: %r>' % self.model_name