#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'LotteWong'

'''
    该脚本用于提醒微信私聊和群聊撤回的消息，作用机理是缓存每条消息，再判断撤回后按索引返回撤回消息的内容。
'''

import itchat
from itchat.content import *
import re
import time

msg_info = {}

#缓存私聊消息
@itchat.msg_register([TEXT, CARD, FRIENDS, PICTURE, RECORDING, VIDEO, ATTACHMENT, SHARING, MAP, NOTE, SYSTEM], isFriendChat=True)
def handle_download_friendchat(msg):
    msg_recv_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    msg_cret_time = msg['CreateTime']
    msg_from = itchat.search_friends(userName=msg['FromUserName'])['NickName']
    msg_to = itchat.search_friends()['NickName']
    msg_id = msg['MsgId']
    msg_content = None
    msg_url = None

    if msg['Type'] == 'Text':
        msg_content = msg['Text']
        print(msg_content)

    if msg['Type'] == 'Picture' or msg['Type'] == 'Recording' or msg['Type'] == 'Video' or msg['Type'] == 'Attachment':
        msg_content = msg['FileName']
        #print(type(msg_content)
        msg['Text'](str(msg_content))
        print(str(msg_content))

    if msg['Type'] == 'Card':
        msg_content = msg['RecommendInfo']['NickName']
        if msg['RecommendInfo']['Sex'] == 1:
            msg_content += ' 性别为男'
        else:
            msg_content += ' 性别为女'
        print(msg_content)

    if msg['Type'] == 'Friends':
        msg_content = msg['Text']
        print(msg_content)

    if msg['Type'] == 'Sharing':
        msg_content = msg['Text']
        msg_url = msg['Url']
        print(msg_content + '->' + msg_url)

    if msg['Type'] == 'Map':
        x, y, location = re.search('<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*', msg['OriContent']).group(1, 2, 3)
        if location is None:
            msg_content = r'纬度->' + x.__str__() + '经度->' + y.__str__()
        else:
            msg_content = r'' + location
        print(msg_content)

    msg_info.update(
        {
            msg_id:
                {
                    'msg_recv_time':msg_recv_time, 'msg_cret_time':msg_cret_time,
                    'msg_from':msg_from, 'msg_to':msg_to,
                    'msg_content':msg_content, 'msg_url':msg_url,
                    'msg_type':msg['Type']
                }
        }
    )

#判断私聊的撤回
@itchat.msg_register(NOTE, isFriendChat=True)
def handle_friendchat(msg):
    if '撤回了一条消息' in msg['Content']:
        old_msg_id = re.search('\<msgid\>(.*?)\<\/msgid\>', msg['Content']).group(1)
        old_msg = msg_info[old_msg_id]
        print(old_msg_id)
        print(old_msg)

        itchat.send_msg('%s撤回了一条%s消息[%s]，内容为：%s' % (old_msg['msg_from'], old_msg['msg_type'], old_msg['msg_recv_time'], old_msg['msg_content']), toUserName='filehelper')

        if old_msg['msg_type'] == ' Sharing':
            itchat.send_msg(msg='->%s' % old_msg['msg_url'], toUserName='filehelper')

        if old_msg['msg_type'] == 'Recording' or old_msg['msg_type'] == 'Attachment':
            itchat.send_file(old_msg['msg_content'], toUserName='filehelper')

        if old_msg['msg_type'] == 'Picture':
            itchat.send_image(old_msg['msg_content'], toUserName='filehelper')

        if old_msg['msg_type'] == 'Video':
            itchat.send_video(old_msg['msg_content'], toUserName='filehelper')

        msg_info.pop(old_msg_id)

#缓存群聊消息
@itchat.msg_register([TEXT, CARD, FRIENDS, PICTURE, RECORDING, VIDEO, ATTACHMENT, SHARING, MAP, NOTE, SYSTEM], isGroupChat=True)
def handle_download_groupchat(msg):
    msg_recv_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    msg_cret_time = msg['CreateTime']
    msg_from = itchat.update_chatroom(userName=msg['FromUserName'])['NickName']
    msg_to = itchat.search_friends()['NickName']
    msg_id = msg['MsgId']
    msg_content = None
    msg_url = None

    if msg['Type'] == 'Text':
        msg_content = msg['Text']
        print(msg_content)

    if msg['Type'] == 'Picture' or msg['Type'] == 'Recording' or msg['Type'] == 'Video' or msg['Type'] == 'Attachment':
        msg_content = msg['FileName']
        #print(type(msg_content)
        msg['Text'](str(msg_content))
        print(str(msg_content))

    if msg['Type'] == 'Card':
        msg_content = msg['RecommendInfo']['NickName']
        if msg['RecommendInfo']['Sex'] == 1:
            msg_content += ' 性别为男'
        else:
            msg_content += ' 性别为女'
        print(msg_content)

    if msg['Type'] == 'Friends':
        msg_content = msg['Text']
        print(msg_content)

    if msg['Type'] == 'Sharing':
        msg_content = msg['Text']
        msg_url = msg['Url']
        print(msg_content + '->' + msg_url)

    if msg['Type'] == 'Map':
        x, y, location = re.search('<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*', msg['OriContent']).group(1, 2, 3)
        if location is None:
            msg_content = r'纬度->' + x.__str__() + '经度->' + y.__str__()
        else:
            msg_content = r'' + location
        print(msg_content)

    msg_info.update(
        {
            msg_id:
                {
                    'msg_recv_time':msg_recv_time, 'msg_cret_time':msg_cret_time,
                    'msg_from':msg_from, 'msg_to':msg_to,
                    'msg_content':msg_content, 'msg_url':msg_url,
                    'msg_type':msg['Type']
                }
        }
    )

#判断群聊的撤回
@itchat.msg_register(NOTE, isGroupChat=True)
def handle_groupchat(msg):
    if '撤回了一条消息' in msg['Content']:
        old_msg_id = re.search('\<msgid\>(.*?)\<\/msgid\>', msg['Content']).group(1)
        old_msg = msg_info[old_msg_id]
        print(old_msg_id, old_msg)

        itchat.send_msg('%s撤回了一条%s消息[%s]，内容为：%s' % (
        old_msg['msg_from'], old_msg['msg_type'], old_msg['msg_recv_time'], old_msg['msg_content']), toUserName='filehelper')

        if old_msg['msg_type'] == ' Sharing':
            itchat.send_msg(msg='->%s' % old_msg['msg_url'], toUserName='filehelper')

        if old_msg['msg_type'] == 'Recording' or old_msg['msg_type'] == 'Attachment':
            itchat.send_file(old_msg['msg_content'], toUserName='filehelper')

        if old_msg['msg_type'] == 'Picture':
            itchat.send_image(old_msg['msg_content'], toUserName='filehelper')

        if old_msg['msg_type'] == 'Video':
            itchat.send_video(old_msg['msg_content'], toUserName='filehelper')

        msg_info.pop(old_msg_id)

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()