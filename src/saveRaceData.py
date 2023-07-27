import requests
from bs4 import BeautifulSoup
import time
import json
import datetime


class SaveRaceDict:
    save_path = "./data/raw-data/races"
    file_name = ""
    race_dict = {}

    # デフォルトの検索範囲
    start = 1984
    last = datetime.datetime.now().year

    def setRaceDict(self, soup):
        pass

    def saveRaceDict(self):
        response = requests.get(self.url)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        self.setRaceDict(soup)

        # jsonファイルに保存
        path = f"{self.save_path}/{self.file_name}.json"
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.race_dict, file, indent=4, ensure_ascii=False)
        print(f"ファイルを保存しました: {path}")


class SaveRaceDictFromJRA(SaveRaceDict):
    file_name = f"central-G1"
    url = "https://www.jra.go.jp/datafile/seiseki/replay/2023/g1.html"

    def setRaceDict(self, soup):
        race_rows = soup.find(id="contentsBody").find("tbody").find_all("tr")
        for row in race_rows:
            race_info = {
                "organize": "central",
                "type": self._getType(row),
                "grade": 1,
            }
            race_td = row.find(class_="race").find("a")
            race_info["name"] = race_td.text
            link_url = race_td.get("href")
            race_key = link_url.split("/")[4]
            self.race_dict[race_key] = race_info
        return self.race_dict

    def _getType(self, race_tr):
        type_char = race_tr.find(class_="course").find(class_="type").text
        if type_char == "芝":
            return "turf"
        elif type_char == "ダ":
            return "dirt"
        elif type_char == "障":
            return "jump"
        else:
            raise Exception("レースタイプを判別できません")


class SaveRaceDictFromOumaIcon(SaveRaceDict):
    url = "https://horseicon.web.fc2.com/jra-grade.htm"
    file_name = "central"

    # デフォルトの主催
    organize = "central"

    # ソース解析から自動登録ができない重賞（setSpecialRaceInfoの対象）
    special_races_dict = {
        "g3-elm-s": {
            "g3_elm_s": {
                "name": "エルムステークス",
                "type": "dirt",
                "grade": 3,
                "start": 1996,
            },
        },
        "g3-keeneland-c": {
            "g3_keeneland_c": {
                "name": "キーンランドカップ",
                "type": "turf",
                "grade": 3,
                "start": 2006,
            },
        },
        "g2-sapporo-kinen": {
            "g3_sapporo_kinen": {
                "name": "札幌記念",
                "type": "turf",
                "grade": 3,
                "last": 1996,
            },
            "g2_sapporo_kinen": {
                "name": "札幌記念",
                "type": "turf",
                "grade": 2,
                "start": 1997,
            },
        },
        "g3-ocean-s": {
            "g3_ocean_s": {
                "name": "オーシャンステークス",
                "type": "turf",
                "grade": 3,
                "start": 2006,
            },
        },
        "g2-yayoi-sho": {
            "g3_yayoi_sho": {
                "name": "弥生賞",
                "type": "turf",
                "grade": 3,
                "last": 1986,
            },
            "g2_yayoi_sho": {
                "name": "弥生賞",
                "type": "turf",
                "grade": 2,
                "start": 1987,
            },
        },
        "g3-flower-c": {
            "g3_flower_c": {
                "name": "フラワーカップ",
                "type": "turf",
                "grade": 3,
                "start": 1987,
            },
        },
        "g3-march-s": {
            "g3_march_s": {
                "name": "マーチステークス",
                "type": "dirt",
                "grade": 3,
                "start": 1994,
            },
        },
        "g2-new-zealand-t": {
            "g3_new_zealand_t": {
                "name": "ニュージーランドトロフィー",
                "type": "turf",
                "grade": 3,
                "last": 1986,
            },
            "g2_new_zealand_t": {
                "name": "ニュージーランドトロフィー",
                "type": "turf",
                "grade": 2,
                "start": 1987,
            },
        },
        "shion-s": {
            "g3_shion_s": {
                "name": "紫苑ステークス",
                "type": "turf",
                "grade": 3,
                "start": 2015,
                "last": 2022,
            },
            # "g2_shion_s": {
            #     "name": "紫苑ステークス",
            #     "type": "turf",
            #     "grade": 2,
            #     "start": 2023,
            # },
        },
        "g2-st-lite-kinen": {
            "g3_st_lite_kinen": {
                "name": "セントライト記念",
                "type": "turf",
                "grade": 3,
                "last": 1986,
            },
            "g2_st_lite_kinen": {
                "name": "セントライト記念",
                "type": "turf",
                "grade": 2,
                "start": 1987,
            },
        },
        "g2-all-comers": {
            "g3_all_comers": {
                "name": "オールカマー",
                "type": "turf",
                "grade": 3,
                "last": 1994,
            },
            "g2_all_comers": {
                "name": "オールカマー",
                "type": "turf",
                "grade": 2,
                "start": 1995,
            },
        },
        "g1-sprinters-s": {
            "g3_sprinters_s": {
                "name": "スプリンターズステークス",
                "type": "turf",
                "grade": 3,
                "last": 1986,
            },
            "g2_sprinters_s": {
                "name": "スプリンターズステークス",
                "type": "turf",
                "grade": 2,
                "start": 1987,
                "last": 1989,
            },
            "g1_sprinters_s": {
                "name": "スプリンターズステークス",
                "type": "turf",
                "grade": 1,
                "start": 1990,
            },
        },
        "g2-stayers-s": {
            "g3_stayers_s": {
                "name": "ステイヤーズステークス",
                "type": "turf",
                "grade": 3,
                "last": 1996,
            },
            "g2_stayers_s": {
                "name": "ステイヤーズステークス",
                "type": "turf",
                "grade": 2,
                "start": 1997,
            },
        },
        "turquoise-s": {
            "g3_turquoise_s": {
                "name": "ターコイズステークス",
                "type": "turf",
                "grade": 3,
                "start": 2015,
            }
        },
        "hopeful-s-jra": {
            "g2_hopeful_s_jra": {
                "name": "ホープフルステークス",
                "type": "turf",
                "grade": 2,
                "start": 2014,
                "last": 2016,
            },
            "g1_hopeful_s_jra": {
                "name": "ホープフルステークス",
                "type": "turf",
                "grade": 1,
                "start": 2017,
            },
        },
        "g3-negishi-s": {
            "g3_negishi_s": {
                "name": "根岸ステークス",
                "type": "dirt",
                "grade": 3,
                "start": 1987,
            },
        },
        "g1-february-s": {
            "g3_february_s": {
                "name": "フェブラリーステークス",
                "type": "dirt",
                "grade": 3,
                "last": 1993,
            },
            "g2_february_s": {
                "name": "フェブラリーステークス",
                "type": "dirt",
                "grade": 2,
                "start": 1994,
                "last": 1996,
            },
            "g1_february_s": {
                "name": "フェブラリーステークス",
                "type": "dirt",
                "grade": 1,
                "start": 1997,
            },
        },
        "g2-aoba-sho": {
            "g3_aoba_sho": {
                "name": "青葉賞",
                "type": "turf",
                "grade": 3,
                "start": 1994,
                "last": 2000,
            },
            "g2_aoba_sho": {
                "name": "青葉賞",
                "type": "turf",
                "grade": 2,
                "start": 2001,
            },
        },
        "saudi-arabia-royal-c": {
            "g3_saudi_arabia_royal_c": {
                "name": "サウジアラビアロイヤルカップ",
                "type": "turf",
                "grade": 3,
                "start": 2015,
            }
        },
        "fuchu-himba-s": {
            "g3_fuchu_himba_s": {
                "name": "府中牝馬ステークス",
                "type": "turf",
                "grade": 3,
                "start": 1984,
                "last": 2010,
            },
            "g2_fuchu_himba_s": {
                "name": "府中牝馬ステークス",
                "type": "turf",
                "grade": 2,
                "start": 2011,
            },
        },
        "g3-musashino-s": {
            "g3_musashino_s": {
                "name": "武蔵野ステークス",
                "type": "dirt",
                "grade": 3,
                "start": 1996,
            },
        },
        "fuji-s": {
            "g3_fuji_s": {
                "name": "富士ステークス",
                "type": "turf",
                "grade": 3,
                "start": 1998,
                "last": 2019,
            },
            "g2_fuji_s": {
                "name": "富士ステークス",
                "type": "turf",
                "grade": 2,
                "start": 2020,
            },
        },
        "tokyo-sports-hai": {
            "g3_tokyo_sports_hai": {
                "name": "東京スポーツ杯2歳ステークス",
                "type": "turf",
                "grade": 3,
                "start": 1996,
                "last": 2020,
            },
            "g2_tokyo_sports_hai": {
                "name": "東京スポーツ杯2歳ステークス",
                "type": "turf",
                "grade": 2,
                "start": 2021,
            },
        },
        "g2-tokai-s.htm": {
            "g3_tokai_s": {
                "name": "東海ステークス",
                "type": "dirt",
                "grade": 3,
                "last": 1996,
            },
            "g2_tokai_s": {
                "name": "東海ステークス",
                "type": "dirt",
                "grade": 2,
                "start": 1997,
            },
        },
        "g2-kinko-sho": {
            "g3_kinko_sho": {
                "name": "金鯱賞",
                "type": "turf",
                "grade": 3,
                "last": 1995,
            },
            "g2_kinko_sho": {
                "name": "金鯱賞",
                "type": "turf",
                "grade": 2,
                "start": 1996,
            },
        },
        "g1-takamatsunomiya": {
            "g2_takamatsunomiya": {
                "name": "高松宮杯",
                "type": "turf",
                "grade": 2,
                "last": 1995,
            },
            "g1_takamatsunomiya": {
                "name": "高松宮記念",
                "type": "turf",
                "grade": 1,
                "start": 1996,
            },
        },
        "g3-cbc-sho": {
            "g3_cbc_sho": {
                "name": "CBC賞",
                "type": "turf",
                "grade": 3,
                "last": 1989,
            },
            "g2_cbc_sho": {
                "name": "CBC賞",
                "type": "turf",
                "grade": 2,
                "start": 1990,
                "last": 2005,
            },
            # TODO 降格重賞の処理を考えてなかったので暫定的に_2として別ファイルに保存
            # できれば同一ファイルに特定の期間（G2期間）が抜けてる形で記載されているのがベスト
            "g3_cbc_sho_2": {
                "name": "CBC賞",
                "type": "turf",
                "grade": 3,
                "start": 2006,
            },
        },
        "g3-procyon-s": {
            "g3_procyon_s": {
                "name": "プロキオンステークス",
                "type": "dirt",
                "grade": 3,
                "start": 1996,
            },
        },
        "g1-jcd": {
            "g1_jcd": {
                "name": "ジャパンカップダート",
                "type": "dirt",
                "grade": 1,
                "start": 2000,
                "last": 2013,
            },
            "g1_champions_cup": {
                "name": "チャンピオンズカップ",
                "type": "dirt",
                "grade": 1,
                "start": 2014,
            },
        },
        "g3-silk-road-s": {
            "g3_silk_road_s": {
                "name": "シルクロードステークス",
                "type": "turf",
                "grade": 3,
                "start": 1996,
            },
        },
        "g3-heian-s": {
            "g3_heian_s": {
                "name": "平安ステークス",
                "type": "dirt",
                "grade": 3,
                "start": 1994,
            },
        },
        "aoi-s": {
            "g3_aoi_s": {
                "name": "葵ステークス",
                "type": "turf",
                "grade": 3,
                "start": 2018,
            }
        },
        "kyoto-2sai-s": {
            "g3_kyoto_2sai_s": {
                "name": "京都2歳ステークス",
                "type": "turf",
                "grade": 3,
                "start": 2014,
            },
        },
        "tulip-sho": {
            "g3_tulip_sho": {
                "name": "チューリップ賞",
                "type": "turf",
                "grade": 3,
                "start": 1994,
                "last": 2017,
            },
            "g2_tulip_sho": {
                "name": "チューリップ賞",
                "type": "turf",
                "grade": 2,
                "start": 2018,
            },
        },
        "osaka-hai": {
            "g2_osaka_hai": {
                "name": "産経大阪杯",
                "type": "turf",
                "grade": 2,
                "last": 2016,
            },
            "g1_osaka_hai": {
                "name": "大阪杯",
                "type": "turf",
                "grade": 1,
                "start": 2017,
            },
        },
        "g2-hanshin-himba-s": {
            "g3_hanshin_himba_s": {
                "name": "阪神牝馬ステークス",
                "type": "turf",
                "grade": 3,
                "last": 1993,
            },
            "g2_hanshin_himba_s": {
                "name": "阪神牝馬ステークス",
                "type": "turf",
                "grade": 2,
                "start": 1994,
            },
        },
        "g3-naruo-kinen": {
            "g2_naruo_kinen": {
                "name": "鳴尾記念",
                "type": "turf",
                "grade": 2,
                "last": 1999,
            },
            "g3_naruo_kinen": {
                "name": "鳴尾記念",
                "type": "turf",
                "grade": 3,
                "start": 2000,
            },
        },
        "g2-centaur-s": {
            "g3_centaur_s": {
                "name": "セントウルステークス",
                "type": "turf",
                "grade": 3,
                "last": 2005,
            },
            "g2_centaur_s": {
                "name": "セントウルステークス",
                "type": "turf",
                "grade": 2,
                "start": 2006,
            },
        },
        "g2-kobe-shimbun-hai": {
            "g3_kobe_shimbun_hai": {
                "name": "神戸新聞杯",
                "type": "turf",
                "grade": 3,
                "last": 1986,
            },
            "g2_kobe_shimbun_hai": {
                "name": "神戸新聞杯",
                "type": "turf",
                "grade": 2,
                "start": 1987,
            },
        },
        "g3-sirius-s": {
            "g3_sirius_s": {
                "name": "シリウスステークス",
                "type": "dirt",
                "grade": 3,
                "start": 1997,
            },
        },
        "g1-hanshin-jf": {
            "g1_hanshin_3sai_s": {
                "name": "阪神3歳ステークス",
                "type": "turf",
                "grade": 1,
                "last": 1990,
            },
            "g1_hanshin_jf": {
                "name": "阪神ジュベナイルフィリーズ",
                "type": "turf",
                "grade": 1,
                "start": 1991,
            },
        },
        # NOTE 参考元サイトが「東京優駿」「優駿牝馬」を併記しているため名称調整のため追記
        "g1-yushun-hinba": {
            "g1_yushun_hinba": {
                "name": "オークス",
                "type": "turf",
                "grade": 1,
            },
        },
        "g1-tokyo-yushun": {
            "g1_tokyo_yushun": {
                "name": "日本ダービー",
                "type": "turf",
                "grade": 1,
            },
        },
        # 休止重賞
        "g3-kabutoyama-kinen": {
            "g3_kabutoyama-_kinen": {
                "name": "カブトヤマ記念",
                "type": "turf",
                "grade": 3,
                "last": 2003,
            },
        },
        "g3-garnet": {
            "g3_garnet": {
                "name": "ガーネットステークス",
                "type": "dirt",
                "grade": 3,
                "start": 1997,
                "last": 2008,
            },
        },
        "g3-crystal-c": {
            "g3_tokyo_sports_hai": {
                "name": "クリスタルカップ",
                "type": "turf",
                "grade": 3,
                "last": 2005,
            },
        },
        "g2-nhk-hai": {
            "g2_nhk_hai": {
                "name": "NHK杯",
                "type": "turf",
                "grade": 2,
                "last": 1995,
            },
        },
        "g3-kyoto-4sai-tokubetsu": {
            "g3_kyoto_4sai_tokubetsu": {
                "name": "京都4歳特別",
                "type": "turf",
                "grade": 3,
                "last": 1999,
            },
        },
        "g3-pegasus-s": {
            "g3_pegasus_s": {
                "name": "ペガサスステークス",
                "type": "turf",
                "grade": 3,
                "start": 1987,
                "last": 1991,
            },
        },
        "g3-sapphire-s": {
            "g3_sapphire_s": {
                "name": "サファイヤステークス",
                "type": "turf",
                "grade": 3,
                "last": 1995,
            },
        },
    }

    def setRaceDict(self, soup):
        race_rows = []
        for td in soup.find("table").find("table").find_all("tr")[2].children:
            if td.find("table") == -1:
                continue
            for tr in td.find("table").find_all("tr"):
                race_rows.append(tr)

        for row in race_rows:
            link_elm = row.find("a")
            if not link_elm:
                continue

            # レースの情報をself.race_dictに保存
            try:
                self.setRaceInfo(link_elm)
            except Exception as e:
                print(e)
                print(f"保存中に例外が発生しました: {link_elm.text}")
                continue

    def setRaceInfo(self, elm):
        link_file = elm.get("href")
        keyword = link_file.replace(".htm", "")

        # 昇格重賞・休止重賞など構文分析が出来ない場合
        def setSpecialRaceInfo(keyword):
            for race_key, race_info in self.special_races_dict[keyword].items():
                # 未入力項目をデフォルト値で更新
                if not race_info.get("organize"):
                    race_info["organize"] = self.organize
                if not race_info.get("start"):
                    race_info["start"] = self.start
                if not race_info.get("last"):
                    race_info["last"] = self.last

                self.race_dict[race_key] = race_info
                race_info["keyword"] = keyword
                print(f"レース情報を登録しました: G{race_info['grade']} {race_info['name']}")

        if keyword in self.special_races_dict.keys():
            setSpecialRaceInfo(keyword)
            return

        splited_text = elm.text.split(" （")
        if len(splited_text) != 2:
            print(f"対象外レースです(グレード記載無し): {elm.text}")
            return
        name, grade_char = splited_text

        # check race grade
        if "GIII" in grade_char:
            grade = 3
        elif "GII" in grade_char:
            grade = 2
        elif "GI" in grade_char:
            grade = 1
        else:
            print(f"対象外レースです(重賞でない): {elm.text}")
            return

        # check race type
        if "J" in grade_char:
            type = "jump"
        else:
            # Downtime to prevent excessive access! Not to be removed!
            time.sleep(2)
            link_url = f"{self.url.rsplit('/', 1)[0]}/{link_file}"
            response = requests.get(link_url)
            html = response.content
            soup = BeautifulSoup(html, "html.parser")
            tbody = soup.find(id="table")
            turf = len(tbody.find_all(class_="turf"))
            dirt = len(tbody.find_all(class_="dirt"))
            if not turf and not dirt:
                raise Exception("レースタイプを判別できません")
            type = "turf" if turf > dirt else "dirt"

        # JavaScriptの変数名として利用するためハイフンをアンダースコアへ変換
        race_key = keyword.replace("-", "_")
        self.race_dict[race_key] = {
            "name": name,
            "type": type,
            "grade": grade,
            "organize": self.organize,
            "start": self.start,
            "last": self.last,
            "keyword": keyword,
        }
        print(f"レース情報を登録しました: G{grade} {name}")


def main():
    srd_ouma = SaveRaceDictFromOumaIcon()
    srd_ouma.saveRaceDict()


if __name__ == "__main__":
    main()
