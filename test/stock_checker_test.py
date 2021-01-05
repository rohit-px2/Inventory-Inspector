''' Testing the non-GUI elements of the stock checker. This includes the functions in
stock_checker.py and html_parse.py. '''
from testing_aid import *
moveDirToSrcFolder()

from stock_checker import *

class TestStockCheck:
    # Checking remove_newlines
    def test_remove_newlines_one(self):
        normal = ["hello\n", "hi\n", "bonjour\n"]
        assert remove_newlines(normal) == ["hello", "hi", "bonjour"]
    
    def test_remove_newlines_emptylist(self):
        empty = []
        assert remove_newlines(empty) == []
    
    def test_remove_newlines_no_newlines(self):
        no_newlines = ["this", "is", "a", "test"]
        assert remove_newlines(no_newlines) == no_newlines
    


    # Checking get_domain_name (gdn)
    def test_gdn_one(self):
        domain = "http://google.com"
        assert get_domain_name(domain) == "google"
    
    def test_gdn_two(self):
        domain="youtube.com"
        assert get_domain_name(domain) == "youtube"