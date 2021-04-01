from bs4 import BeautifulSoup


class HowLongToBeatParser:
    @staticmethod
    def parse_game_list(html: str):
        games = []

        soup = BeautifulSoup(html, "html.parser")
        details = soup.find_all("div", class_="search_list_details")
        for detail in details:
            game_name = detail.h3.a.text.strip()
            game_id = int(detail.h3.a.get("href").split("id=")[-1])
            game = {"name": game_name, "id": game_id}

            game["times"] = {}
            detail_block = (
                detail.find("div", class_="search_list_details_block")
                .find("div")
                .find_all("div")
            )
            current_label = None
            for block in detail_block:
                if current_label:
                    content = block.text.strip()
                    accuracy = 0
                    for block_class in block.get("class"):
                        if block_class.startswith("time_"):
                            accuracy = int(block_class.split("_")[-1])
                    game["times"][current_label] = {
                        "content": content,
                        "accuracy": accuracy,
                    }
                    current_label = None
                else:
                    current_label = block.text.strip()
            games.append(game)

        if len(games) == 0:
            return {"data": [], "pages": None}

        bottom_spans = soup.find("h2").find_all("span")
        page = 1
        for span in bottom_spans:
            if "back_blue" in span.get("class") and span.text != "":
                page = int(span.text)
        total_pages = int(bottom_spans[-1].text)

        return {"data": games, "pages": {"page": page, "total_pages": total_pages}}
