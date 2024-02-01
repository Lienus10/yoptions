from yoptions import yoptions as yo


def test_url_fetch_no_url_encoding_required():
    data = yo.url_fetch("AAPL")
    assert data != []


def test_url_fetch_url_encoding_required():
    data = yo.url_fetch("^SPX")
    assert data != []
