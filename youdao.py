# -*- coding: utf-8 -*-

import os
import shutil
import webbrowser

import requests
from wox import Wox

NODE_ICO_PATH = r'img\node'

QUERY_API = 'http://fanyi.youdao.com/openapi.do?keyfrom=WoxYoudaoPlugin&key=315576122&type=data&doctype=json&version=1.1&q='

class Main(Wox):
  
  def query(self, param):
    response = requests.get(QUERY_API + param.strip()).json()

    return result

  def open_url(self, url):
    webbrowser.open(url)

  def __get_proxies(self):
    proxies = {}
    if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
        proxies["http"] = "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port"))
        proxies["https"] = "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port"))
    return proxies


if __name__ == '__main__':
    Main()
