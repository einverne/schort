#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


class BasicResp:
    code = 0  # 返回错误码
    msg = ''  # 信息
    data = ''  # 数据

    def __init__(self, code=0, msg='', data=''):
        self.code = code
        self.msg = msg
        self.data = data

    def __repr__(self):
        return json.dumps(self.__dict__)
