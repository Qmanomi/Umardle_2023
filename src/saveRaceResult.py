import requests
from bs4 import BeautifulSoup
import time
import json
import re


class SaveRaceResult:
    save_path = "./data/raw-data"

    def getRaceUrl(self, race):
        pass

    def getResultList(self, race, soup):
        pass

    def saveRaceResult(self, race):
        url = self.getRaceUrl(race)
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        result_list = self.getResultList(race, soup)

        # jsonファイルに保存
        path = f"{self.save_path}/{race}.json"
        with open(path, "w", encoding="utf-8") as file:
            json.dump(result_list, file, indent=2, ensure_ascii=False)
        print(f"ファイルを保存しました: {path}")


class SaveRaceResultFromJRA(SaveRaceResult):
    save_path = "./data/raw-data/jra"

    def getRaceUrl(self, race):
        return f"https://www.jra.go.jp/datafile/seiseki/g1/{race}/index.html"

    def getResultList(self, race, soup):
        result_rows = soup.find(id="g1_list").find("tbody").find_all("tr")

        result_list = []
        # !CAUTION find_all()による取得がhtmlの上から下=年代の降順かは不確定なので潜在的なバグ
        for row in result_rows:
            year = row.find(class_="year").text.replace("年", "")
            if int(year) < 1983:
                break

            result = {
                "race": race,
            }
            result["year"] = year
            result["name"] = row.find(class_="horse").text
            result_list.append(result)
        return result_list


class SaveRaceResultFromOuma(SaveRaceResult):
    save_path = "./data/raw-data/central"

    def saveRaceResult(self):
        with open("./data/raw-data/races/central.json", "r", encoding="utf-8") as file:
            central_races = json.load(file)

        for race_key, race_info in central_races.items():
            url = f"https://horseicon.web.fc2.com/{race_info['keyword']}.htm"
            response = requests.get(url)
            html = response.content
            soup = BeautifulSoup(html, "html.parser")
            try:
                start = race_info["start"]
                last = race_info["last"]

                table = soup.find(id="table")
                if not table:
                    # 休止重賞などでページレイアウトが古い場合の対処
                    table = soup.find("table", class_="wh")
                result_rows = table.find_all(
                    "tr", class_=["turf", "dirt", "turfdh", "dirtdh"]
                )

                result_list = []
                year = 0
                for row in result_rows:
                    columns = row.find_all("td")
                    # 同着表記の対処
                    if len(columns) < 6:
                        horse = re.search(r"[ァ-ヴー]+", columns[1].text).group()
                    else:
                        year = int(re.search(r"\d{4}", columns[0].text).group())
                        if year < start or last < year:
                            continue
                        horse = re.search(r"[ァ-ヴー]+", columns[3].text).group()

                    result = {
                        "race": race_key,
                        "year": year,
                        "horse": horse,
                    }
                    result_list.append(result)
            except Exception as e:
                print(e)
                print(f"保存中に例外が発生しました: {race_info['name']}")
                continue
            # Downtime to prevent excessive access! Not to be removed!
            time.sleep(1)

            # jsonファイルに保存
            path = f"{self.save_path}/{race_key}.json"
            with open(path, "w", encoding="utf-8") as file:
                json.dump(result_list, file, indent=4, ensure_ascii=False)
            print(f"ファイルを保存しました: {path}")


def main():
    srr_ouma = SaveRaceResultFromOuma()
    srr_ouma.saveRaceResult()


if __name__ == "__main__":
    main()
