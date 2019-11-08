from download import PlenaryMinutesDownloader


def test_scrape_urls_before19():
    urls = PlenaryMinutesDownloader.scrape_urls_before_period19()
    assert(len(urls) == 18)


def test_scrape_urls_19():
    urls = PlenaryMinutesDownloader.scrape_urls_period19()
    assert(len(urls) > 100)
