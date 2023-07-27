import json
import os


def formatJsonToJSConst(file_path, save_path, file_name, key_list, constant_name):
    """
    json形式のテキストデータをJavaScriptのconst変数として保存する
    """
    with open(f"{file_path}{file_name}.json", "r", encoding="utf-8") as file:
        raceDataStr = file.read()

    for key in key_list:
        raceDataStr = raceDataStr.replace(f'"{key}"', key)

    raceDataStr = (
        f"const {constant_name} = {raceDataStr}\n\nexport default {constant_name};"
    )

    with open(f"{save_path}{file_name}.js", "w", encoding="utf-8") as file:
        file.write(raceDataStr)
    print(f"ファイルを保存しました：{file_name}")


def formatRaceDataToJSConst(file_name, constant_name):
    """
    レースデータ(開催概要)のjsonファイルを変換・保存する
    """
    file_path = "./data/raw-data/races/"
    save_path = "./data/races/"
    key_list = ["name", "type", "grade", "organize", "start", "last", "keyword"]
    formatJsonToJSConst(
        file_path=file_path,
        save_path=save_path,
        file_name=file_name,
        key_list=key_list,
        constant_name=constant_name,
    )


def formatRaceDirToJSConst():
    """
    racesディレクトリ下のレースデータファイルを変換・保存する
    """
    const_dict = {
        "central": "central_races",
        "local": "local_races",
        "overseas": "ovearseas_races",
    }
    index_txt = ""
    for file_name, constant_name in const_dict.items():
        formatRaceDataToJSConst(file_name=file_name, constant_name=constant_name)

        index_txt += f"import {constant_name} from './data/races/{file_name}.js';\n"

    index_txt += f"\nexport {{{', '.join(const_dict.values())}}};"

    with open(f"./data/races/index.js", "w", encoding="utf-8") as file:
        file.write(index_txt)
    print(f"racesモジュールの保存が完了しました")


def formatRaceResultToJSConst(dir_name, file_name):
    file_path = f"./data/raw-data/{dir_name}/"
    save_path = f"./data/{dir_name}/"
    key_list = ["race", "year", "horse"]
    formatJsonToJSConst(
        file_path=file_path,
        save_path=save_path,
        file_name=file_name,
        key_list=key_list,
        constant_name=file_name,
    )


def formatRaceResultDirToJSConst():
    dir_list = ["central", "local", "overseas"]

    for dir in dir_list:
        directory = f"./data/raw-data/{dir}"
        race_files = os.listdir(directory)
        races = [file_name.replace(".json", "") for file_name in race_files]

        index_txt = ""
        for race in races:
            formatRaceResultToJSConst(dir_name=dir, file_name=race)

            index_txt += f"import {race} from './data/{dir}/{race}.js';\n"

        index_txt += f"\nexport {{{', '.join(races)}}}"

        with open(f"./data/{dir}/index.js", "w", encoding="utf-8") as file:
            file.write(index_txt)
        print(f"レース結果モジュール({dir})の保存が完了しました")


def formatRaceList():
    """
    raceDataからジャンル別にレースキーワードのリストを作成
    """
    # 中央平地重賞 (GIのみ・全重賞)
    central_g1 = []
    central_all = []

    # 地方交流重賞 (GIのみ・全重賞)
    local_g1 = []
    local_all = []

    # 海外重賞 (GIのみ・全重賞)
    overseas_g1 = []
    overseas_all = []

    # 障害重賞 (GIのみ・全重賞)
    jump_g1 = []
    jump_all = []

    with open("./data/raw-data/races/central.json", "r", encoding="utf-8") as file:
        central_races = json.load(file)

    for key, info in central_races.items():
        if info["type"] == "jump":
            jump_all.append(key)
            if info["grade"] == 1:
                jump_g1.append(key)
        else:
            central_all.append(key)
            if info["grade"] == 1:
                central_g1.append(key)

    with open("./data/raw-data/races/local.json", "r", encoding="utf-8") as file:
        local_races = json.load(file)

    for key, info in local_races.items():
        if info["grade"] == 1:
            local_g1.append(key)
        else:
            local_all.append(key)

    with open("./data/raw-data/races/overseas.json", "r", encoding="utf-8") as file:
        overseas_races = json.load(file)

    for key, info in overseas_races.items():
        if info["grade"] == 1:
            overseas_g1.append(key)
        else:
            overseas_all.append(key)

    text = f"""const central_g1 = {central_g1}
const central_all = {central_all}
const local_g1 = {local_g1}
const local_all = {local_all}
const overseas_g1 = {overseas_g1}
const overseas_all = {overseas_all}
const jump_g1 = {jump_g1}
const jump_all = {jump_all}

export {{ central_g1, central_all, local_g1, local_all, overseas_g1, overseas_all, jump_g1, jump_all }}
"""

    path = "data/race-list.js"
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)


def main():
    formatRaceList()
    formatRaceDirToJSConst()
    formatRaceResultDirToJSConst()


if __name__ == "__main__":
    main()
