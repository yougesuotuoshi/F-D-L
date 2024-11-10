# coding: utf-8
import msgpack
import uuid
import hashlib
import base64
import fgourl
import mytime
import gacha
import webhook
import main
import logging
import json
import os
import subprocess
import re
import sys
import binascii
import random
import time
import requests
import shutil

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from urllib.parse import quote_plus
from libs.GetSubGachaId import GetGachaSubIdFP

class ParameterBuilder:
    def __init__(self, uid: str, auth_key: str, secret_key: str):
        self.uid_ = uid
        self.auth_key_ = auth_key
        self.secret_key_ = secret_key
        self.content_ = ''
        self.idempotency_key_ = str(uuid.uuid4()) 
        self.parameter_list_ = [
            ('appVer', fgourl.app_ver_),
            ('authKey', self.auth_key_),
            ('dataVer', str(fgourl.data_ver_)),
            ('dateVer', str(fgourl.date_ver_)),
            ('idempotencyKey', self.idempotency_key_), 
            ('lastAccessTime', str(mytime.GetTimeStamp())),
            ('userId', self.uid_),
            ('verCode', fgourl.ver_code_),
        ]

    def get_idempotency_key(self):
        return self.idempotency_key_

    def AddParameter(self, key: str, value: str):
        self.parameter_list_.append((key, value))
        

    def Build(self) -> str:
        self.parameter_list_.sort(key=lambda tup: tup[0])
        temp = ''
        for first, second in self.parameter_list_:
            if temp:
                temp += '&'
                self.content_ += '&'
            escaped_key = quote_plus(first)
            if not second:
                temp += first + '='
                self.content_ += escaped_key + '='
            else:
                escaped_value = quote_plus(second)
                temp += first + '=' + second
                self.content_ += escaped_key + '=' + escaped_value

        temp += ':' + self.secret_key_
        self.content_ += '&authCode=' + \
            quote_plus(base64.b64encode(
                hashlib.sha1(temp.encode('utf-8')).digest()))

        return self.content_

    def Clean(self):
        self.content_ = ''
        self.parameter_list_ = [
            ('appVer', fgourl.app_ver_),
            ('authKey', self.auth_key_),
            ('dataVer', str(fgourl.data_ver_)),
            ('dateVer', str(fgourl.date_ver_)),
            ('idempotencyKey', str(uuid.uuid4())),
            ('lastAccessTime', str(mytime.GetTimeStamp())),
            ('userId', self.uid_),
            ('verCode', fgourl.ver_code_),
        ]


class Rewards:
    def __init__(self, stone, level, ticket, goldenfruit, silverfruit, bronzefruit, bluebronzesapling, bluebronzefruit, pureprism, sqf01, holygrail):
        self.stone = stone
        self.level = level
        self.ticket = ticket
        self.goldenfruit = goldenfruit
        self.silverfruit = silverfruit
        self.bronzefruit = bronzefruit
        self.bluebronzesapling = bluebronzesapling
        self.bluebronzefruit = bluebronzefruit
        self.pureprism = pureprism
        self.sqf01 = sqf01
        self.holygrail = holygrail


class Login:
    def __init__(self, name, login_days, total_days, act_max, act_recover_at, now_act, add_fp, total_fp, name1, fpids1, remaining_ap):
        self.name = name
        self.login_days = login_days
        self.total_days = total_days
        self.act_max = act_max
        self.act_recover_at = act_recover_at
        self.now_act = now_act
        self.add_fp = add_fp
        self.total_fp = total_fp
        self.name1 = name1
        self.fpids1 = fpids1
        self.remaining_ap = remaining_ap



class Bonus:
    def __init__(self, message, items, bonus_name, bonus_detail, bonus_camp_items):
        self.message = message
        self.items = items
        self.bonus_name = bonus_name
        self.bonus_detail = bonus_detail
        self.bonus_camp_items = bonus_camp_items


class user:
    def __init__(self, user_id: str, auth_key: str, secret_key: str):
        self.name_ = ''
        self.user_id_ = (int)(user_id)
        self.s_ = fgourl.NewSession()
        self.builder_ = ParameterBuilder(user_id, auth_key, secret_key)

    def Post(self, url):
        res = fgourl.PostReq(self.s_, url, self.builder_.Build())
        self.builder_.Clean()
        return res

    def topLogin(self):
        DataWebhook = []  
        device_info = os.environ.get('DEVICE_INFO_SECRET')
        
        private_key_pem = """
-----BEGIN RSA PRIVATE KEY-----
MIICWAIBAAKBgLkG1MbGaKzsCnfEz/v5Pv0mSffavUujhNKjmAAUdlBuE6v+uxMH
ezdep9kH1FZRZHtYRjN1M6oeqckKVMhK82DMkoRxjCjwyknnM6VKO8uMbI3jbZwE
jEv7yyNjxNIF7jVq5ifJujc13uainCQw2Y2UyJD3pmSgZp7xkt9vM9lVAgMBAAEC
gYAdGhn1edeU+ztaQzaDZ1yk7JTNyzXi48FMcDbELHO/itDFSLeb8p1KxDSaSkT3
nq2zSNsh1NlfdJs358wWBNPqrSBOEQGrcwUqob59mLQysxddE8HKN0kN7ZfLiebp
y1xHxTqV1VEBmTlon9sMyYa5wbjJ8teSBQnvXP5JCnw2sQJAytZc/rIxKSazx2is
os89qJFkzIEK4QhopCvSiDWarsYRi79KIxizrL0PCK0qAu6OXFsy5F2Ei+YXw++I
Hhgx2wJA6YVwCKnGybW5hDKy7+XdFPpy0mhLxcGMWo9LQKCCSTKXqj6IOH3HOvnc
iXN7NUf/TwN6mFzrsBHzyKrXJhAAjwJAnNIhMfW41nUKt9hw6KtLo4FNqmL2c0da
B9utuQugnRGbzSzG992IRLwi3HVtLrkbrcIA1diLutHZe+48ke/o0wJANVdPogr1
53llKPdTvEyrVXFn7Pv54vA1GTKGI/sGB6ZQ0oh6IT1J1wTgBV2llSQfA3Nt+4Ou
KofPQdUUVBNvrQJAeFeVPpvWJTiMWCN2NMmJXqqdva8J1XIT047x5fdg72LcPOU+
xCGlz9vV3+AAQ31C2phoyd/QhvpL85p39n6Ibg==
-----END RSA PRIVATE KEY-----
        """
        loaded_private_key = serialization.load_pem_private_key(
            private_key_pem.encode('utf-8'), password=None, backend=default_backend())
            
        def sign(uuid):
            signature = loaded_private_key.sign(
                bytes(uuid, 'utf-8'),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return base64.b64encode(signature).decode('utf-8')
            
        userid = self.user_id_
        idk = self.builder_.get_idempotency_key()
        input_string = f"{userid}{idk}"
        idempotencyKeySignature = sign(input_string)
        
        lastAccessTime = self.builder_.parameter_list_[5][1]
        
        userState = (-int(lastAccessTime) >>
                     2) ^ self.user_id_ & fgourl.data_server_folder_crc_

        self.builder_.AddParameter(
            'assetbundleFolder', fgourl.asset_bundle_folder_)
        self.builder_.AddParameter('idempotencyKeySignature', idempotencyKeySignature)
        self.builder_.AddParameter('deviceInfo', device_info)
        self.builder_.AddParameter('isTerminalLogin', '1')
        self.builder_.AddParameter('userState', str(userState))

        data = self.Post(
            f'{fgourl.server_addr_}/login/top?_userId={self.user_id_}')

        responses = data['response']
        
        with open('login.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        self.name_ = hashlib.md5(
            data['cache']['replaced']['userGame'][0]['name'].encode('utf-8')).hexdigest()
        stone = data['cache']['replaced']['userGame'][0]['stone']
        lv = data['cache']['replaced']['userGame'][0]['lv']
        ticket = 0
        goldenfruit = 0
        silverfruit = 0
        bronzefruit = 0
        bluebronzesapling = 0
        bluebronzefruit = 0
        pureprism = 0
        sqf01 = 0
        holygrail = 0

        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 4001:
                ticket = item['num']
                break
        
        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 100:
                goldenfruit = item['num']
                break

        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 101:
                silverfruit = item['num']
                break

        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 102:
                bronzefruit = item['num']
                break

        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 103:
                bluebronzesapling = item['num']
                break

        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 104:
                bluebronzefruit = item['num']
                break

        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 46:
                pureprism = item['num']
                break

        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 16:
                sqf01 = item['num']
                break

        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 7999:
                holygrail = item['num']
                break

        
        rewards = Rewards(stone, lv, ticket, goldenfruit, silverfruit, bronzefruit, bluebronzesapling, bluebronzefruit, pureprism, sqf01, holygrail)

        DataWebhook.append(rewards)

        login_days = data['cache']['updated']['userLogin'][0]['seqLoginCount']
        total_days = data['cache']['updated']['userLogin'][0]['totalLoginCount']
        name1 = data['cache']['replaced']['userGame'][0]['name']
        fpids1 = data['cache']['replaced']['userGame'][0]['friendCode']

        act_max = data['cache']['replaced']['userGame'][0]['actMax']
        act_recover_at = data['cache']['replaced']['userGame'][0]['actRecoverAt']
        carryOverActPoint = data['cache']['replaced']['userGame'][0]['carryOverActPoint']
        serverTime = data['cache']['serverTime']
        ap_points = act_recover_at - serverTime
        remaining_ap = 0
        
        if ap_points > 0:
            lost_ap_point = (ap_points + 299) // 300
            if act_max >= lost_ap_point:
                remaining_ap_int = act_max - lost_ap_point
                remaining_ap = int(remaining_ap_int)
        else:
            remaining_ap = act_max + carryOverActPoint
        
        now_act = (act_max - (act_recover_at - mytime.GetTimeStamp()) / 300)

        add_fp = data['response'][0]['success']['addFriendPoint']
        total_fp = data['cache']['replaced']['tblUserGame'][0]['friendPoint']

        login = Login(
            self.name_,
            login_days,
            total_days,
            act_max, act_recover_at,
            now_act,
            add_fp,
            total_fp,
            name1,
            fpids1,
            remaining_ap
        )

        DataWebhook.append(login)

        if 'seqLoginBonus' in data['response'][0]['success']:
            bonus_message = data['response'][0]['success']['seqLoginBonus'][0]['message']

            items = []
            items_camp_bonus = []

            for i in data['response'][0]['success']['seqLoginBonus'][0]['items']:
                items.append(f'{i["name"]} x{i["num"]}')

            if 'campaignbonus' in data['response'][0]['success']:
                bonus_name = data['response'][0]['success']['campaignbonus'][0]['name']
                bonus_detail = data['response'][0]['success']['campaignbonus'][0]['detail']

                for i in data['response'][0]['success']['campaignbonus'][0]['items']:
                    items_camp_bonus.append(f'{i["name"]} x{i["num"]}')
            else:
                bonus_name = None
                bonus_detail = None

            bonus = Bonus(bonus_message, items, bonus_name,
                          bonus_detail, items_camp_bonus)
            DataWebhook.append(bonus)
        else:
            DataWebhook.append("No Bonus")

        webhook.topLogin(DataWebhook)
        

    def buyBlueApple(self):
        with open('login.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

            actRecoverAt = data['cache']['replaced']['userGame'][0]['actRecoverAt']
            actMax = data['cache']['replaced']['userGame'][0]['actMax']
            carryOverActPoint = data['cache']['replaced']['userGame'][0]['carryOverActPoint']
            serverTime = data['cache']['serverTime']
        
            bluebronzesapling = 0 
            for item in data['cache']['replaced']['userItem']:
                if item['itemId'] == 103:
                    bluebronzesapling = item['num']
                    break
                
            ap_points = actRecoverAt - serverTime
            remaining_ap = 0
        
            if ap_points > 0:
               lost_ap_point = (ap_points + 299) // 300
               if actMax >= lost_ap_point:
                   remaining_ap = actMax - lost_ap_point
                   remaining_ap_int = int(remaining_ap)
            else:
                remaining_ap = actMax + carryOverActPoint
                remaining_ap_int = int(remaining_ap)

            if bluebronzesapling > 0:
                quantity = remaining_ap_int // 40
                if quantity == 0:
                    main.logger.info(f"\n {'=' * 40} \n [+] APが40未満の場合は購入できません (´･ω･`)? \n {'=' * 40} ")
                    return
                
                if bluebronzesapling < quantity:
                    num_to_purchase = bluebronzesapling
                else:
                    num_to_purchase = quantity

                self.builder_.AddParameter('id', '13000000')
                self.builder_.AddParameter('num', str(num_to_purchase))

                data = self.Post(f'{fgourl.server_addr_}/shop/purchase?_userId={self.user_id_}')
                responses = data['response']

                for response in responses:
                    resCode = response['resCode']
                    resSuccess = response['success']
                    nid = response["nid"]

                    if (resCode != "00"):
                        continue

                    if nid == "purchase":
                        if "purchaseName" in resSuccess and "purchaseNum" in resSuccess:
                            purchaseName = resSuccess['purchaseName']
                            purchaseNum = resSuccess['purchaseNum']

                            main.logger.info(f"\n{'=' * 40}\n[+] {purchaseName} x{purchaseNum} 购买成功\n{'=' * 40}")
                            webhook.shop(purchaseName, purchaseNum)
            else:
                main.logger.info(f"\n {'=' * 40} \n [+] ＞︿＜ 青銅の苗木が足りないヽ (*。>Д<)o゜ \n {'=' * 40} " )





    def LTO_Gacha(self):
        # 10/16 【期間限定】「岸波白野ピックアップフレンドポイント召喚」！

        nowAt = mytime.GetTimeStamp()
        closedAt = 1730865599
        
        if nowAt > closedAt:
            main.logger.info(f"\n {'=' * 40} \n [+] 期間限定召喚 已结束，当前时间：{nowAt} \n {'=' * 40} ")
            return

        with open('login.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        user_svt_list = data.get('cache', {}).get('replaced', {}).get('userSvt', [])

        found_svt = False 

        for svt in user_svt_list:
            svtId = svt.get('svtId')
            if svtId in [2300800, 2300700]:  #岸波白野的SvtID
                found_svt = True 
                
                gachaId = 3  #这个限定卡池有两个ID【 2 / 3 】懒得写判定，如果报错就用2
                gachaSubId = 417  #这个限定卡池有两个ID【 416 / 417 】懒得写判定，如果报错就用416

                self.builder_.AddParameter('storyAdjustIds', '[]')
                self.builder_.AddParameter('selectBonusList', '')
                self.builder_.AddParameter('gachaId', str(gachaId))
                self.builder_.AddParameter('num', '10')
                self.builder_.AddParameter('ticketItemId', '0')
                self.builder_.AddParameter('shopIdIndex', '1')
                self.builder_.AddParameter('gachaSubId', str(gachaSubId))
                
                main.logger.info(f"\n {'=' * 40} \n [+] 期間限定召喚 GachaId：{gachaId} SubId：{gachaSubId} \n {'=' * 40} ")
                data = self.Post(f'{fgourl.server_addr_}/gacha/draw?_userId={self.user_id_}')
                
                responses = data['response']

                servantArray = []
                missionArray = []

                for response in responses:
                    resCode = response['resCode']
                    resSuccess = response['success']

                    if (resCode != "00"):
                        continue

                    if "gachaInfos" in resSuccess:
                        for info in resSuccess['gachaInfos']:
                            servantArray.append(
                                gacha.gachaInfoServant(
                                    info['objectId']
                                )
                            )

                webhook.LTO_Gacha(servantArray)
                return

        if not found_svt:
            main.logger.info(f"\n {'=' * 40} \n [+] 不满足活动条件..不能参加限定召唤 \n {'=' * 40} ")
            return 

    def drawFP(self):
        #SubID判定有点不准了.偶尔错误抽卡失败...等哪天闲暇再修
        gachaSubId = GetGachaSubIdFP()

        if gachaSubId is None:
           gachaSubId = 0
            
        self.builder_.AddParameter('storyAdjustIds', '[]')
        self.builder_.AddParameter('selectBonusList', '')
        self.builder_.AddParameter('gachaId', '1')
        self.builder_.AddParameter('num', '10')
        self.builder_.AddParameter('ticketItemId', '0')
        self.builder_.AddParameter('shopIdIndex', '1')
        self.builder_.AddParameter('gachaSubId', gachaSubId)

        main.logger.info(f"\n {'=' * 40} \n [+] 友情卡池ID : {gachaSubId}\n {'=' * 40} " )
        data = self.Post(f'{fgourl.server_addr_}/gacha/draw?_userId={self.user_id_}')
        responses = data['response']

        servantArray = []
        missionArray = []

        for response in responses:
            resCode = response['resCode']
            resSuccess = response['success']

            if (resCode != "00"):
                continue

            if "gachaInfos" in resSuccess:
                for info in resSuccess['gachaInfos']:
                    servantArray.append(
                        gacha.gachaInfoServant(
                            info['objectId']
                        )
                    )

            if "eventMissionAnnounce" in resSuccess:
                for mission in resSuccess["eventMissionAnnounce"]:
                    missionArray.append(
                        gacha.EventMission(
                            mission['message'], mission['progressFrom'], mission['progressTo'], mission['condition']
                        )
                    )

        webhook.drawFP(servantArray, missionArray)

    def topHome(self):
        self.Post(f'{fgourl.server_addr_}/home/top?_userId={self.user_id_}')


    def lq001(self):
         # https://game.fate-go.jp/present/list?
          
        data = self.Post(
            f'{fgourl.server_addr_}/present/list?_userId={self.user_id_}')
        
        responses = data['response']
        
        with open('present.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            
        main.logger.info(f"\n {'=' * 40} \n [+] 获得礼物盒数据 \n {'=' * 40} " )

    def lq002(self):
         # https://game.fate-go.jp/present/receive?
        with open('login.json', 'r', encoding='utf-8')as f:
            data = json.load(f)

        present_ids = []
        for item in data['cache']['replaced']['userPresentBox']:
            if item['objectId'] in [2, 6, 11, 16, 3, 46, 18, 48, 4001, 100, 101, 102, 103, 104, 1, 4, 7998, 7999, 1000, 2000, 6999, 9570400, 9670400]: #添加你需要领取的物品 Id 或者 baseSvtId 进入筛选列表
                present_ids.append(str(item['presentId']))

        with open('JJM.json', 'w') as f:
            json.dump(present_ids, f, ensure_ascii=False, indent=4)
            
        time.sleep(1)

        if os.path.exists('JJM.json'):
            with open('JJM.json', 'r', encoding='utf-8') as file:
                datas = json.load(file)

            msgpack_data = msgpack.packb(datas)

            base64_encoded_data = base64.b64encode(msgpack_data).decode()

            self.builder_.AddParameter('presentIds', base64_encoded_data)
            self.builder_.AddParameter('itemSelectIdx', '0')
            self.builder_.AddParameter('itemSelectNum', '0')

            data = self.Post(
                f'{fgourl.server_addr_}/present/receive?_userId={self.user_id_}')
    
            responses = data['response']

            main.logger.info(f"\n {'=' * 40} \n [+] 领取成功 \n {'=' * 40} " )

    def lq003(self):
        url = 'https://git.atlasacademy.io/atlasacademy/fgo-game-data/raw/branch/JP/master/mstShop.json'
        response = requests.get(url)
        Purchase_data = response.json()
    
        # 获取每月兑换物品信息
        monthly_shop_id, monthly_limit, monthly_price = None, None, None
        for item in Purchase_data:
            if 4001 in item.get('targetIds', []) and item.get('flag') == 4096:
                monthly_shop_id = item.get('baseShopId')
                monthly_limit = item.get('limitNum')
                monthly_price = item.get('prices')[0]
                break
    
        if monthly_shop_id is None:
            main.logger.info("未找到符合条件的每月兑换呼符信息")
            return
    
        with open('login.json', 'r', encoding='utf-8') as file:
            login_data = json.load(file)

        # 获取用户的魔力棱镜数量
        mana = login_data['cache']['replaced']['userGame'][0]['mana']
        monthly_num_value = next((item.get('num') for item in login_data.get('cache', {}).get('updated', {}).get('userShop', []) if item.get('shopId') == monthly_shop_id), 0)
        
        # 计算可兑换的数量
        monthly_num_ok = monthly_limit - monthly_num_value
        mana_s = mana // monthly_price
        num = min(monthly_num_ok, mana_s)
    
        # 检查兑换条件
        if mana_s == 0:
            main.logger.info("魔力棱镜不足，无法兑换")
            return
        elif monthly_num_value > 0 and monthly_num_ok == 0:
            main.logger.info("你已经兑换完所有每月呼符")
            return
        else:
            self.builder_.AddParameter('id', str(monthly_shop_id))
            self.builder_.AddParameter('num', str(num))
    
            data = self.Post(f'{fgourl.server_addr_}/shop/purchase?_userId={self.user_id_}')
            if 'response' in data:
                main.logger.info(f"已兑换 {num} 呼符（每月）")
                namegift = "呼符（每月）"
                name = "呼符"
                object_id_count = num
                webhook.Present(name, namegift, object_id_count)
    
        # 获取当前时间戳
        response_time = mytime.GetTimeStamp()
    
        # 获取活动兑换物品信息
        S_base_shop_id, S_base_limit, S_base_price, S_base_name = None, None, None, None
        for item in Purchase_data:
            if 4001 in item.get('targetIds', []) and item.get('flag') == 2048 and response_time < item.get('closedAt'):
                S_base_shop_id = item.get('baseShopId')
                S_base_limit = item.get('limitNum')
                S_base_price = item.get('prices')[0]
                match = re.search(r'【(.*?)】', item.get('detail'))
                S_base_name = match.group(1) if match else "活动"
                break
    
        if S_base_shop_id is None:
            main.logger.info("目前没有绿方块活动(´･ω･`)")
            return
    
        # 获取活动物品已兑换数量
        S_num_value = next((item.get('num') for item in login_data.get('cache', {}).get('updated', {}).get('userShop', []) if item.get('shopId') == S_base_shop_id), 0)
    
        # 计算可兑换的数量
        S_num_ok = S_base_limit - S_num_value
        S_mana_s = mana // S_base_price
        S_num = min(S_num_ok, S_mana_s)
    
        if S_mana_s == 0:
            main.logger.info("魔力棱镜不足，无法兑换")
            return
        elif S_num_value > 0 and S_num_ok == 0:
            main.logger.info(f"你已经兑换完所有 {S_base_name} 呼符")
            return
        else:
            self.builder_.AddParameter('id', str(S_base_shop_id))
            self.builder_.AddParameter('num', str(S_num))
    
            data = self.Post(f'{fgourl.server_addr_}/shop/purchase?_userId={self.user_id_}')
            if 'response' in data:
                main.logger.info(f"已兑换 {S_num} 呼符 // {S_base_name}")
                name = "呼符"
                namegift = S_base_name
                object_id_count = S_num
                webhook.Present(name, namegift, object_id_count)

    
    def Present(self):
        #素材交換券
        response = requests.get("https://api.atlasacademy.io/export/JP/nice_item.json")
        if response.status_code == 200:
            with open("nice_item.json", 'wb') as f:
                f.write(response.content)
                
        with open('present.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        user_present_box = data.get('cache', {}).get('replaced', {}).get('userPresentBox', [])
        
        first_object_id = None
        object_id_count = 0
        object_ids = []
        presentIds = []

        for item in user_present_box:
            if item.get('giftType') == 2:
                object_id = item.get('objectId')
                presentId = item.get('presentId')
    
                if object_id and 10000 <= object_id <= 20000:
                    if first_object_id is None:
                        first_object_id = object_id
                        
                if object_id == first_object_id:
                    object_id_count += 1
                    object_ids.append(str(object_id))
                    presentIds.append(str(presentId))

                    datajs = [int(present_id) for present_id in presentIds]

                    with open('Ticket.json', 'w') as f:
                        json.dump(datajs, f, ensure_ascii=False)
                else:
                    continue

        if first_object_id is not None:
           
           with open('nice_item.json', 'r', encoding='utf-8') as file:
               itemdata = json.load(file)
    
           item_data = next((item for item in itemdata if item.get('id') == first_object_id), None)
    
           if item_data:
               name = item_data.get('name', 'None')
               item_selects = item_data.get('itemSelects', [])
            
               if item_selects:
                   random_item = random.choice(item_selects)
                   idxs = random_item.get('idx')
                   gifts = random_item.get('gifts', [])
                
                   for gift in gifts:
                       object_id = gift.get('objectId')
                       
                   item_name = next((item for item in itemdata if item.get('id') == object_id), None)
                   namegift = item_name.get('originalName', 'None')

                   with open('Ticket.json', 'r', encoding='utf-8') as file:
                       presentdata = json.load(file)

                   msgpack_data = msgpack.packb(presentdata)

                   base64_encoded_data = base64.b64encode(msgpack_data).decode()
                   
                   self.builder_.AddParameter('presentIds', base64_encoded_data)
                   self.builder_.AddParameter('itemSelectIdx', str(idxs))
                   self.builder_.AddParameter('itemSelectNum', str(object_id_count))

                   data = self.Post(
                       f'{fgourl.server_addr_}/present/receive?_userId={self.user_id_}')
    
                   responses = data['response']

                   main.logger.info(f"\n {'=' * 40} \n [+] {name} 兑换成功 \n {'=' * 40} " )
        
                   webhook.Present(name, namegift, object_id_count)
                   
        else:
            main.logger.info(f"\n {'=' * 40} \n [+] 礼物盒中交換券なし(´･ω･`) \n {'=' * 40} ")















