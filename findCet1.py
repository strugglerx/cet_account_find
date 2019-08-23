import requests,re,time,json,logging,threading,sys
from bs4 import BeautifulSoup
logging.basicConfig(level=logging.INFO,format="%(asctime)s [line:%(lineno)d]%(levelname)s - %(message)s",datefmt="%m/%d/%Y %I:%M:%S %p")

#忽略ssl证书验证
requests.packages.urllib3.disable_warnings()

'''
@description:学信网 
@param {type} 
@return: 
'''
class Cet:
    def __init__(self,data):
        self.data = data
        self.session = requests.session()
        self.keep_alive = False
        # self.session.get("https://www.chsi.com.cn/cet/index.jsp")

    def headerReq(self):
        headers ={
            "Host": "www.chsi.com.cn",
            # "Connection": "keep-alive",
            # "Content-Length": "51",
            "Cache-Control": "max-age=0",
            "Origin": "https://www.chsi.com.cn",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Referer": "https://www.chsi.com.cn/cet/index.jsp",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        }
        return headers

    def postReq(self):
        html = self.session.post("https://www.chsi.com.cn/cet/query",headers=self.headerReq(),data=self.data)
        # print(html.status_code,html.headers)
        soup = BeautifulSoup(html.text,"lxml")
        res = soup.find("div",class_="m_cnt_m")
        infoList = res.find_all("td",attrs={"colspan":"2"})
        if len(infoList)>0:
            result = []
            for each in infoList:
                try:
                    # print(each.string.strip())
                    result.append(each.string.strip())
                except:
                    # print(each.find("span").string.strip())
                    try:
                        result.append(each.find("span").string.strip())
                    except:
                        print("出错！出现验证码")
            print(result)
        else:
            return False

'''
@description:guowuyuan 
@param {type} 
@return: 
'''
class Cet1:
    def __init__(self,data):
        self.data = data
        self.session = requests.session()
        self.did = "gx6mHwGKiu"
        self.sid = "447fa0c9698b95a425b29f4530cab98129"
    
    def reLoginHeader(self):
        headers ={
            "Accept": "*/*",
            "x-tif-did": self.did,
            "Accept-Language": "zh-cn",
            "Content-Type": "application/json",
            "Content-Length": "87",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.5(0x17000523) NetType/WIFI Language/zh_CN",
            "Referer": "https://servicewechat.com/wx2eec5fb00157a603/56/page-frame.html",
            "Accept-Encoding": "gzip, deflate, br"
        }
        return headers        
    
    def reLogin(self):
        data = {
            "code":"021iddJP1FTsf31z8AIP1PggJP1iddJm",
            "appid":"wx2eec5fb00157a603",
            "paasid":"gss"
            }
        html = self.session.post("https://zwms.gjzwfw.gov.cn/api/mp/login",headers=self.reLoginHeader(),json=data,verify=False)
        soup = BeautifulSoup(html.text,"lxml")
        result = json.loads(soup.find("p").string)
        if(result["errcode"]==0):
            self.sid = result["data"]["session_id"]
            return True
        elif result["errcode"]==1002 or result["errcode"]==12015:
            logging.warning(result["errmsg"])
            return False
        else:
            return False        
        


    def headerReq(self):
        headers ={
            "Host": "zwms.gjzwfw.gov.cn",
            "Accept": "*/*",
            "x-tif-did": self.did,
            "x-yss-page": "jiaoyubu/pages/business/cet/fillInfo/fillInfo",
            "x-yss-city-code": "4400",
            "x-tif-sid": self.sid,
            "Accept-Language": "zh-cn",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Content-Length": "43",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.5(0x17000523) NetType/WIFI Language/zh_CN",
            "Referer": "https://servicewechat.com/wx2eec5fb00157a603/56/page-frame.html",
            "Connection": "keep-alive",
            "dgd-pre-release": "0"
        }
        return headers

    def postReq(self):
        html = self.session.post("https://zwms.gjzwfw.gov.cn/ebus/gss/api/r/jiaoyu/Cxyysljcj",headers=self.headerReq(),json=self.data,verify=False)
        # print(html.status_code,html.headers)
        soup = BeautifulSoup(html.text,"lxml")
        # print(soup)
        result = json.loads(soup.find("p").string)
        if(result["errcode"]==0):
            logging.warning("已找到！学校:{0} 姓名:{1} 考生号:{2} 成绩:{3}".format(result["data"]["xx"],result["data"]["xm"],result["data"]["zkzh"],result["data"]["zf"]))
        elif result["errcode"]==1002:
            logging.warning(result["errmsg"])
            if self.reLogin():
                return False
            else:
                return True
        else:
            return False
'''
@description:http://app.gjzwfw.gov.cn/jimp/jiaoyubu/interfaces/cet.do
@param {type} 
@return: 
'''
class Cet2:
    def __init__(self,data):
        self.data = data
        self.data["name"] = data["xm"]
        self.session = requests.session()
    
    def headerReq(self):
        headers ={
            "Host": "app.gjzwfw.gov.cn",
            "Connection": "keep-alive",
            "Content-Length": "53",
            "Accept": "text/plain, */*; q=0.01",
            "Origin": "http://app.gjzwfw.gov.cn",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "http://app.gjzwfw.gov.cn/jmopen/webapp/html5/jybsljksdccjcx/index.html",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": "wdcid=0592f74adee152b7; wdses=11df73c3f3794aea; wdlast=1566453287",
        }
        return headers

    def postReq(self):
        html = self.session.post("http://app.gjzwfw.gov.cn/jimp/jiaoyubu/interfaces/cet.do",headers=self.headerReq(),data=self.data,verify=False)     
        if( not bool(re.search(r'err',html.text))):
            o = re.sub(r'([a-z]+)',r'"\1"',html.text)
            result = json.loads(re.sub(r'\'',r'"',o))
            logging.warning("已找到！学校:{0} 姓名:{1} 考生号:{2} 成绩:{3}".format(result["x"],result["n"],result["z"],result["s"]))
        elif bool(re.search(r'err',html.text)):
            # logging.warning(html.text)
            return False
        else:
            return False

class threadFind:
    def __init__(self,conf):
        self.conf = conf
        self.room = conf["room"]
        self.roomEnd = 168
        self.ucode = conf["ucode"]
        self.ucodeEnd = conf["ucodeMax"]
        self.zkzh = "{0}191{1}{2}{3}".format(self.conf["code"],self.conf["level"],str(self.room).zfill(3),str(self.ucode+1).zfill(2))
        self.start = time.time()
        self.end = None
        self.unit = 4
        self.average = int((self.roomEnd-self.room)/self.unit)
        self.findStatus = False

    def runFind(self):
        logging.info("开始执行,请等待")
        for i in range(self.roomEnd-self.room):
            for j in range(self.ucodeEnd-self.ucode):
                zkzhList=["{0}191{1}{2}{3}".format(self.conf["code"],self.conf["level"],str(self.room+(self.average*each)).zfill(3),str(self.ucode+1).zfill(2)) for each in range(self.unit)]
                zkzhThread=[threading.Thread(target=self.runReq,args=(zkzh,)) for zkzh in zkzhList]
                for thread in zkzhThread:
                    thread.start()
                for thread in zkzhThread:
                    thread.join()
                if self.findStatus:
                    sys.exit()
                self.ucode = 0  if ((self.ucode+1) == self.conf["ucodeMax"]) else (self.ucode +1)
                logging.info(zkzhList)
                # if self.runReq() == True:
                #     self.end = time.time()
                #     logging.info("执行了 %.2f 秒"%(self.end-self.start))
                #     quit()
                # time.sleep(1)              
            self.room +=1
    def runReq(self,zkzh):
            data = {
                "zkzh": zkzh,
                "xm": self.conf["xm"]
            }
            obj = Cet2(data)
            res = obj.postReq()
            if res!=False:
                self.end = time.time()
                self.findStatus = True
                logging.warning("执行了 %.2f 秒"%(self.end-self.start))
                sys.exit()
                return True
            else:  
                return False 
                
'''
@description: 参数必须填写才能运行 
@param {type} code level xm 
@return: 
'''
if __name__ =="__main__":
    if len(sys.argv)<4:
        logging.warning("参数错误！长度不够")
        sys.exit()
    conf = {
        "code": sys.argv[1], #""前六位
        "room": 1,  #考场
        "ucodeMax":30, #教室最大容量
        "level": sys.argv[2], #1四级 2六级
        "ucode":0, #默认教室号 0
        "xm": sys.argv[3]  #"名字"
    }
    o = threadFind(conf)
    o.runFind()