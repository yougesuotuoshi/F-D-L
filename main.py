import os
import requests
import time
import json
import fgourl
import user
import coloredlogs
import logging

userIds = os.environ['userIds'].split(',')
authKeys = os.environ['authKeys'].split(',')
secretKeys = os.environ['secretKeys'].split(',')
fate_region = os.environ['fateRegion']
webhook_discord_url = os.environ['webhookDiscord']
blue_apple_cron = os.environ.get("MAKE_BLUE_APPLE")
idempotency_key_signature = os.environ.get('IDEMPOTENCY_KEY_SIGNATURE_SECRET')
device_info = os.environ.get('DEVICE_INFO_SECRET')
user_agent_2 = os.environ.get('USER_AGENT_SECRET_2')

userNums = len(userIds)
authKeyNums = len(authKeys)
secretKeyNums = len(secretKeys)

logger = logging.getLogger("FGO Daily Login")
coloredlogs.install(fmt='%(asctime)s %(name)s %(levelname)s %(message)s')

def get_latest_verCode():
    endpoint += "https://raw.githubusercontent.com/DNNDHH/FGO-VerCode-extractor/JP/VerCode.json"
    response = requests.get(endpoint).text
    response_data = json.loads(response)

    return response_data['verCode']


def main():
    if userNums == authKeyNums and userNums == secretKeyNums:
        fgourl.set_latest_assets()

        for i in range(userNums):
            try:
                instance = user.user(userIds[i], authKeys[i], secretKeys[i])
                time.sleep(3)
                logger.info('登录账号!')
                time.sleep(1)
                instance.topLogin_s()
                time.sleep(2)
                instance.topHome()
                time.sleep(2)
                instance.lq001()
                instance.lq002()
                time.sleep(2)

                check_blue_apple_cron(instance)
                logger.info('尝试购买蓝苹果!')
                try:
                    instance.buyBlueApple(1)
                    time.sleep(2)
                    for _ in range(3): # 默认购买3个蓝苹果 ，需要 （120AP  3青銅树苗）
                        instance.buyBlueApple(1)
                        time.sleep(2)
                        try:
                            time.sleep(1)
                            instance.topHome()
                            time.sleep(1)
                            logger.info('开始友情点召唤!!')
                            for _ in range(1):  # 可定义每次登录时自动抽几次友情10连 （默认1次） 
                                instance.drawFP()
                                time.sleep(4)
                        except Exception as ex:
                            logger.error(ex)
                except Exception as ex:
                    logger.error(ex)
                    
            except Exception as ex:
                logger.error(ex)

if __name__ == "__main__":
    main()

