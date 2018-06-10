#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest, appdirs, tempfile,  os, shutil, subprocess, sys
subprocess      # shut up spyder!
appdirs         # shut up spyder!

from unittest import mock

def test_makedirs_fail(monkeypatch, caplog):

    from unittest.mock import patch

    with patch('pydna._os.path.isdir') as pid, patch('pydna._os.makedirs') as pmd:
        pmd.side_effect = OSError()
        pid.return_value = True
        with pytest.raises(OSError):
            import pydna
            from importlib import reload
            reload(pydna)
        #assert pmd.called == True
        
    with patch('pydna._os.path.isdir') as pid, patch('pydna._os.makedirs') as pmd:
        pmd.side_effect = IOError() #OSError()
        pid.return_value = False
        with pytest.raises(IOError):
            import pydna
            from importlib import reload
            reload(pydna)

def test_default_env(monkeypatch):
    
    pydna_base_dir = os.path.join( tempfile.gettempdir(), "pydna_test")
    
    try:
        shutil.rmtree(pydna_base_dir)
    except FileNotFoundError:
        pass
    
    def pydna_config_dir_name(x):
        return pydna_base_dir
                                
    def pydna_data_dir_name(x):
        return pydna_base_dir            
    
    def pydna_log_dir_name(x):
        return pydna_base_dir
    
    monkeypatch.delenv("pydna_loglevel", raising=False)
    monkeypatch.delenv("pydna_email", raising=False)
    monkeypatch.delenv("pydna_cached_funcs", raising=False)
    monkeypatch.delenv("pydna_ape", raising=False)
    monkeypatch.delenv("pydna_primers", raising=False)
    monkeypatch.delenv("pydna_enzymes", raising=False)
    monkeypatch.delenv("pydna_config_dir", raising=False)
    monkeypatch.delenv("pydna_data_dir", raising=False)
    monkeypatch.delenv("pydna_log_dir", raising=False)
    
    monkeypatch.setattr("appdirs.user_config_dir", pydna_config_dir_name)
    monkeypatch.setattr("appdirs.user_data_dir",   pydna_data_dir_name)
    monkeypatch.setattr("appdirs.user_log_dir",    pydna_log_dir_name)
    
    import pydna
    from importlib import reload
    reload(pydna)
    assert( os.getenv("pydna_config_dir") == pydna_base_dir )
    assert( os.getenv("pydna_data_dir")   == pydna_base_dir )
    assert( os.getenv("pydna_config_dir") == pydna_base_dir )
    pydnaenv = pydna.get_env()
    with open("getenv.txt", "rt", encoding="utf-8") as f:
        saved_env = f.read()
    assert pydnaenv in saved_env

    subp = mock.MagicMock()
    monkeypatch.setattr("sys.platform", "linux")
    monkeypatch.setattr("subprocess.run", subp)

    pydna.open_current_folder()
    subp.assert_called_with(['xdg-open', os.getcwd() ])
    pydna.open_cache_folder()
    subp.assert_called_with(['xdg-open', pydna_base_dir   ])
    pydna.open_config_folder()
    subp.assert_called_with(['xdg-open', pydna_base_dir ])
    pydna.open_log_folder()
    subp.assert_called_with(['xdg-open', pydna_base_dir ])
    monkeypatch.setattr("sys.platform", "win32")
    pydna.open_current_folder()
    subp.assert_called_with(['start', os.getcwd() ], shell=True)
    monkeypatch.setattr("sys.platform", "darwin")
    pydna.open_current_folder()
    subp.assert_called_with(['open', os.getcwd() ])
    
def test_read_ini_file():
    import pydna

    
def test_scipy_missing(monkeypatch):
    import pydna
    import copy
    fakesysmodules = copy.copy(sys.modules)
    fakesysmodules["scipy"] = None
    monkeypatch.delitem(sys.modules,"scipy")
    monkeypatch.setattr("sys.modules", fakesysmodules)
    from importlib import reload
    reload(pydna)


def test_numpy_missing(monkeypatch):
    import pydna
    import copy
    fakesysmodules = copy.copy(sys.modules)
    fakesysmodules["numpy"] = None
    monkeypatch.delitem(sys.modules,"numpy")
    monkeypatch.setattr("sys.modules", fakesysmodules)
    from importlib import reload
    reload(pydna)
    assert "numpy" in pydna._missing_modules_for_gel
    
    
def test_matplotlib_missing(monkeypatch):
    import pydna
    import copy
    fakesysmodules = copy.copy(sys.modules)
    fakesysmodules["matplotlib"] = None
    monkeypatch.delitem(sys.modules,"matplotlib")
    monkeypatch.setattr("sys.modules", fakesysmodules)
    from importlib import reload
    reload(pydna)
    assert "matplotlib" in pydna._missing_modules_for_gel 
    
    
def test_mpldatacursor_missing(monkeypatch):
    import pydna
    import copy
    fakesysmodules = copy.copy(sys.modules)
    fakesysmodules["mpldatacursor"] = None
    monkeypatch.delitem(sys.modules,"mpldatacursor")
    monkeypatch.setattr("sys.modules", fakesysmodules)
    from importlib import reload
    reload(pydna)
    assert "mpldatacursor" in pydna._missing_modules_for_gel
    
    
def test_pint_missing(monkeypatch):
    import pydna
    import copy
    fakesysmodules = copy.copy(sys.modules)
    fakesysmodules["pint"] = None
    monkeypatch.delitem(sys.modules,"pint")
    monkeypatch.setattr("sys.modules", fakesysmodules)
    from importlib import reload
    reload(pydna)
    assert "pint" in pydna._missing_modules_for_gel
       
#def test_open_folders(monkeypatch):
#    subp = mock.MagicMock()
#    monkeypatch.setattr("sys.platform", "linux")
#    monkeypatch.setattr("subprocess.run", subp)
#    import pydna
#    import appdirs
#    pydna.open_current_folder()
#    subp.assert_called_with(['xdg-open', os.getcwd() ])
#    pydna.open_cache_folder()
#    subp.assert_called_with(['xdg-open', appdirs.user_data_dir("pydna")   ])
#    pydna.open_config_folder()
#    subp.assert_called_with(['xdg-open', appdirs.user_config_dir("pydna") ])
#    pydna.open_log_folder()
#    subp.assert_called_with(['xdg-open', appdirs.user_log_dir("pydna") ])
#    monkeypatch.setattr("sys.platform", "win32")
#    pydna.open_current_folder()
#    subp.assert_called_with(['start', os.getcwd() ], shell=True)
#    monkeypatch.setattr("sys.platform", "darwin")
#    pydna.open_current_folder()
#    subp.assert_called_with(['open', os.getcwd() ])
    
def test_no_xdg_open(monkeypatch):
    subp = mock.MagicMock( side_effect=OSError(['xdg-open', os.getcwd() ]) )
    monkeypatch.setattr("sys.platform", "linux")
    monkeypatch.setattr("subprocess.run", subp)
    import pydna
    pydna.open_current_folder()
    subp.assert_called_with(['xdg-open', os.getcwd() ])
   
def test_logo():
    import pydna
    assert pydna.logo() == str("                 _             \n"       
                               "                | |            \n"            
                               " ____  _   _  __| |___   __ ___\n"
                               "|  _ \| | | |/ _  |  _ \(____ |\n"
                               "| |_| | |_| ( (_| | | | / ___ |\n"
                               "|  __/ \__  |\____|_| |_\_____|\n"
                               "|_|   (____/                   \n")

if __name__ == '__main__':
    pytest.main([__file__, "-vv", "-s", "--cov=pydna","--cov-report=html"])