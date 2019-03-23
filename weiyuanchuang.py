import requests
import json
from urllib import parse

server = "http://www.seowyc.com"

#  SEO接口，用于文字或网页内容进行同义词转换
#  @param content 	待转换内容，可以是纯文字，也可以直接是带标签的html内容（转换后格式依然保留）
#  @param ratio 	转换比例，0~100
#  @return 			返回转换后的结果

def getSeoContent( content:str,ratio:int):
    url = server+"/seo/api/wyc.html"
    content = parse.quote(content)
    # param = "content=" + content +"&ratio="+ str(ratio)
    param = {
        'content': content,
        'ratio':  str(ratio)
    }
    result = sendPost(url,param)
    if result == 'ERR': return 'ERR'
    result = parse.unquote(result)
    # print (result)
    return result

    
def sendPost(url:str, param:list):
    headers = {
        'user-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)',
        'accept': '*/*',
        'connection': 'Keep-Alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
    try:
        r = requests.post(url, headers=headers, data=param, timeout=60).text
        temp_list = json.loads(r)
        if temp_list['status'] != '1':
            return temp_list['content']
        return 'ERR'
    except:
        print ('weiyuanchuang server error')
        return 'ERR'


