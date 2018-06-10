#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import io
import pytest
import requests_mock as rm_module

@pytest.fixture
def requests_mock(request):
    m = rm_module.Mocker()
    m.start()
    request.addfinalizer(m.stop)
    return m
    
def test_web(requests_mock, monkeypatch):
    
    from pydna.download import download_text
    
    monkeypatch.setenv("pydna_cached_funcs", "")
       
    flo = io.BytesIO(b"some text data")
    
    requests_mock.get("http://www.fake.com/hej.txt", 
                  headers={'last-modified'  : 'Mon, 01 Jan 2001 00:00:00 GMT', #978307200
                           'content-length' : "100"}, 
                  body = flo)
    
    tx = download_text("http://www.fake.com/hej.txt")    
    
    assert tx=="some text data"

if __name__ == '__main__':
    pytest.main([__file__, "-v", "-s", "--cov=pydna","--cov-report=html"])
    

    