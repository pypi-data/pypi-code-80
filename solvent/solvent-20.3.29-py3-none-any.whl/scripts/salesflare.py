import pomace

from . import Script


class Salesflare(Script):

    URL = "https://integrations.salesflare.com/s/tortii"

    def run(self, page) -> pomace.Page:
        pomace.log.info("Launching form")
        page = page.click_request_this_listing(wait=0)
        page.fill_email(pomace.fake.email)
        page.fill_company(pomace.fake.company)

        pomace.log.info("Submitting form")
        page = page.click_submit(wait=1)
        return page

    def check(self, page) -> bool:
        success = "Thank you for your request" in page
        page.click_close(wait=0.1)
        return success
