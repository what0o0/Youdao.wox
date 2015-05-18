# -*- coding: utf-8 -*-

import os
import shutil
import webbrowser

import requests
from wox import Wox

QUERY_API = 'http://fanyi.youdao.com/openapi.do?keyfrom=WoxYoudaoPlugin&key=315576122&type=data&doctype=json&version=1.1&q='
EMPTY_RESULT = {
  'Title': 'Start to translate between Chinese and English',
  'SubTitle': 'Powered by youdao api',
  'IcoPath': 'Img\\youdao.ico'
}

class Main(Wox):
  
  def query(self, param):
    result = []
    if param.strip() == '':
      result.append(EMPTY_RESULT)
    else:
      response = requests.get(QUERY_API + param.strip(), proxies = self.__get_proxies()).json()
      if response and response['errorCode'] == 0:
        if 'translation' in response and response['translation'] != []:
          result.append({
            'Title': ','.join(response['translation']),
            'SubTitle': '有道翻译',
            'IcoPath': 'Img\\youdao.ico',
            'JsonRPCAction': {
              'method': 'open_url',
              'parameters': [param.strip()]
            }
          })
        if 'basic' in response and response['basic'] != {}:
          for i in response['basic']['explains']:
            result.append({
              'Title': i,
              'SubTitle': '{} - 基本词典'.format(response['query'].encode('utf-8')),
              'IcoPath': 'Img\\youdao.ico',
              'JsonRPCAction': {
                'method': 'open_url',
                'parameters': [param.strip()]
              }
            })
        if 'web' in response and response['web'] != []:
          for i in response['web']:
            result.append({
              'Title': ','.join(i['value']),
              'SubTitle': '{} - 网络释义'.format(i['key'].encode('utf-8')),
              'IcoPath': 'Img\\youdao.ico',
              'JsonRPCAction': {
                'method': 'open_url',
                'parameters': [param.strip()]
              }
            })
      elif response:
        errCode = response['errorCode']
        errMsg = '未知错误'
        if errCode == 20:
          errMsg = '要翻译的文本过长'
        elif errCode == 30:
          errMsg = '无法进行有效的翻译'
        elif errCode == 40:
          errMsg = '不支持的语言类型'
        elif errCode == 50:
          errMsg = '无效的key'
        elif errCode == 60:
          errMsg = '无词典结果'
        result.append({
          'Title': errMsg,
          'SubTitle': 'errorCode=%d' % errCode,
          'IcoPath': 'Img\\youdao.ico'
        })
      else:
        result.append(EMPTY_RESULT)
    return result

  def open_url(self, query):
    webbrowser.open('http://dict.youdao.com/search?q=' + query)

  def __get_proxies(self):
    proxies = {}
    if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
        proxies["http"] = "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port"))
        proxies["https"] = "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port"))
    return proxies


if __name__ == '__main__':
    Main()
