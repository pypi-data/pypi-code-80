import pomace


def main():
    pomace.freeze()

    page = pomace.visit("https://integrations.salesflare.com/s/tortii")

    attempted = completed = failed = 0
    while failed < 10:
        attempted += 1

        page = page.click_request_this_listing(wait=0)
        page.fill_email(pomace.fake.email)
        page.fill_company(pomace.fake.company)

        page = page.click_submit(wait=1)

        if "Thank you for your request" in page:
            page = page.click_close(wait=0)
            completed += 1
            failed = 0
        else:
            failed += 1

        pomace.log.info(f"Iterations: {attempted=} {completed=} {failed=}")
