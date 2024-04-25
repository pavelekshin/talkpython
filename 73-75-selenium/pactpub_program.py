import re
import os

USER = os.environ.get("PACKT_USER")
PASSWORD = os.environ.get("PACKT_PW")
DOWNLOAD_URL = "https://www.packtpub.com/ebook_download/{nid}/{ebook_format}"
BOOK_FORMATS = "pdf epub mobi"


def get_books(grep, ebook_format, books):
    """Receives a grep regex and book format (epub, pdf, mobi)
    and prints the titles + urls of matching ebooks"""
    grep = grep.lower()
    ebook_format = ebook_format.lower()
    if ebook_format not in BOOK_FORMATS.split():
        raise ValueError(f"Not a valid book format (valid are: {BOOK_FORMATS})")

    for nid, title in books.items():
        if re.search(grep, title.lower()):
            url = DOWNLOAD_URL.format(nid=nid, ebook_format=ebook_format)
            print(title, url)


if __name__ == "__main__":

    login = "https://www.packtpub.com/login"

    driver = webdriver.Chrome()
    driver.get(login)

    driver.find_element_by_id("edit-name").send_keys(USER)
    driver.find_element_by_id("edit-pass").send_keys(PASSWORD + Keys.RETURN)
    driver.find_element_by_link_text("My eBooks").click()
    elements = driver.find_elements_by_class_name("product-line")
    books = {e.get_attribute("nid"): e.get_attribute("title") for e in elements}
    driver.close()
    get_books("Python.*", "PDF", books)
