''' Testing the non-GUI elements of the stock checker. This includes the functions in
stock_checker.py and html_parse.py. '''
import testing_aid
testing_aid.moveDirToSrcFolder()
import stock_checker


class TestStockCheck:

    # Checking remove_newlines
    def test_remove_newlines_one(self):
        normal = ["hello\n", "hi\n", "bonjour\n"]
        assert stock_checker.remove_newlines(normal) == ["hello", "hi", "bonjour"]

    def test_remove_newlines_emptylist(self):
        empty = []
        assert stock_checker.remove_newlines(empty) == []

    def test_remove_newlines_no_newlines(self):
        no_newlines = ["this", "is", "a", "test"]
        assert stock_checker.remove_newlines(no_newlines) == no_newlines

    # Checking get_domain_name (gdn)
    def test_gdn_one(self):
        domain = "http://google.com"
        assert stock_checker.get_domain_name(domain) == "google"

    def test_gdn_two(self):
        domain = "youtube.com"
        assert stock_checker.get_domain_name(domain) == "youtube"

    # Checking get_relevant_dict (grd)
    def test_grd_one(self):
        cc = {
            "classCode": "pi-prod-availability",
            "messages": [
                "Not Available Online"
            ]
        }
        assert stock_checker.get_relevant_dict("canadacomputers") == cc

    def test_grd_two(self):
        mx = {
            "classCode": "c-capr-inventory-store",
            "messages": [
                "Out of Stock"
            ]
        }
        assert stock_checker.get_relevant_dict("memoryexpress") == mx

    # Checking fetch_content (fc)
    def test_fc_one(self):
        assert b"Python is a programming language" in stock_checker.fetch_content("http://python.org").content
