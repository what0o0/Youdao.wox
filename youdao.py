# -*- coding: utf-8 -*-

import os
import shutil
import random
import hashlib
import webbrowser

import requests
from wox import Wox
from urllib import urlencode

APP_KEY = ''
APP_SECRET = ''
QUERY_API = 'https://openapi.youdao.com/api?q=%s&form=auto&to=auto&appKey=%s&salt=%s&sign=%s'
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
      salt = str(random.randint(0, 10000))
      q = param.strip().encode('utf8')
      sign = hashlib.md5(APP_KEY + q + salt + APP_SECRET).hexdigest().upper()
      response = requests.get(QUERY_API % (q, APP_KEY, salt, sign), proxies = self.__get_proxies()).json()
      if response and response['errorCode'] == '0':
        if 'translation' in response and response['translation'] != []:
          result.append({
            'Title': ','.join(response['translation']),
            'SubTitle': '有道翻译',
            'IcoPath': 'Img\\youdao.ico',
            'JsonRPCAction': {
              'method': 'open_url',
              'parameters': [q]
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
                'parameters': [q]
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
                'parameters': [q]
              }
            })
      elif response:
        errCode = response['errorCode']
        errMsg = '未知错误'
        if errCode == '101':
          errMsg = '缺少必填的参数'
        elif errCode == '102':
          errMsg = '不支持的语言类型'
        elif errCode == '103':
          errMsg = '翻译文本过长'
        elif errCode == '104':
          errMsg = '不支持的API类型'
        elif errCode == '105':
          errMsg = '不支持的签名类型'
        elif errCode == '106':
          errMsg = '不支持的响应类型'
        elif errCode == '107':
          errMsg = '不支持的传输加密类型'
        elif errCode == '108':
          errMsg = 'appKey无效'
        elif errCode == '109':
          errMsg = 'batchLog格式不正确'
        elif errCode == '110':
          errMsg = '无相关服务的有效实例'
        elif errCode == '111':
          errMsg = '开发者账号无效，可能是账号为欠费状态'
        elif errCode == '201':
          errMsg = '解密失败，可能为DES,BASE64,URLDecode的错误'
        elif errCode == '202':
          errMsg = '签名检验失败'
        elif errCode == '203':
          errMsg = '访问IP地址不在可访问IP列表'
        elif errCode == '301':
          errMsg = '辞典查询失败'
        elif errCode == '302':
          errMsg = '翻译查询失败'
        elif errCode == '303':
          errMsg = '服务端的其它异常'
        elif errCode == '401':
          errMsg = '账户已经欠费停'
        result.append({
          'Title': errMsg,
          'SubTitle': 'errorCode=%s' % errCode,
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
