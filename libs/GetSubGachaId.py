import requests
import json
import main

from mytime import GetTimeStamp

def GetGachaSubIdFP():
    response = requests.get(f"https://git.atlasacademy.io/atlasacademy/fgo-game-data/raw/branch/JP/master/mstGachaSub.json");
    main.logger.info(f"Response text: {response.text}") 
    gachaList = json.loads(response.text)
    timeNow = GetTimeStamp()
    main.logger.info(f"{timeNow}")
    priority = 0
    goodGacha = {}

    for gacha in gachaList:
        openedAt = gacha["openedAt"]
        closedAt = gacha["closedAt"]

        main.logger.info(f"openedAt: {goodGacha}")
        main.logger.info(f"closedAt: {goodGacha}")

        # 修正逻辑运算符
        if openedAt <= timeNow and timeNow <= closedAt:
            p = int(gacha["priority"])
            if p > priority:
                priority = p
                goodGacha = gacha

    # 打印 goodGacha 以查看其状态
    main.logger.info(f"Good Gacha: {goodGacha}")

    # 检查是否找到了合适的 gacha
    if not goodGacha:
        main.logger.info("No suitable gacha found")
        return None  # 或者返回一个合适的默认值
    
    # 确认 'id' 键是否存在
    if "id" not in goodGacha:
        main.logger.info("Key 'id' not found in the selected gacha")
        return None  # 或者返回一个合适的默认值

    return str(goodGacha["id"])
