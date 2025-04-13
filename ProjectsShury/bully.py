import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import numpy as np
import numpy
import re

from tensorflow.python.keras.layers import Dense, recurrent, Input,  Dropout, Embedding
from tensorflow.python.keras.models import Sequential
from keras._tf_keras.keras.preprocessing.text import Tokenizer, text_to_word_sequence
from keras._tf_keras.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.engine import data_adapter

from telethon.sync import TelegramClient
import csv
from telethon.tl.functions.messages import GetHistoryRequest
import asyncio

def begin():
    api_id, api_hash, api_phone=[i.replace('/n', '') for i in open('data.txt')]
    if api_id=='' or api_hash=='' or api_phone=='':
        return 'Error'
    print(int(api_id), api_hash, api_phone)
    asyncio.set_event_loop(asyncio.new_event_loop())
    client=TelegramClient(api_phone, int(api_id), api_hash, system_version='4.16.30-vxCUSTOM')
    return client


def parse():
    asyncio.set_event_loop(asyncio.new_event_loop())
    try:
        client = begin()
        client.start()
        grops=[]

        for chat in client.get_dialogs():
            if chat.is_group:
                grops.append(chat)

        for dialog in client.iter_dialogs():
            if dialog.id>0:
                grops.append(dialog)
    finally:
        client.disconnect()
        return grops

def parse_print():
    grop=parse()
    i=0
    lst=''
    for g in grop:
        lst+=f'||{str(i)} - {g.title}||\n'
        i+=1
    return lst

d=[i.replace('\n', '') for i in open('data.txt')]
print(d)

def parse_group():
    asyncio.set_event_loop(asyncio.new_event_loop())
    try:
        grp = parse()
        client=begin()
        client.start()
        g_index=0
        for i in open('number.txt'):
            g_index=int(i)
        target_group=grp[int(g_index)]
        if target_group.is_group:
            print('Get know user...')
            all_participants=[]
            all_participants=client.get_participants(target_group)

            print('Save data in file...')
            with open('members.csv', "w", encoding='UTF-16') as f:
                writer=csv.writer(f, delimiter=",", lineterminator="\n")
                writer.writerow(['username', 'name', 'group'])
                for user in all_participants:
                    if user.username:
                        username=user.username
                    else:
                        username=""
                    if user.first_name:
                        first_name=user.first_name
                    else:
                        first_name=""
                    if user.last_name:
                        last_name=user.last_name
                    else:
                        last_name=""
                    name=(first_name+' '+last_name).strip()
                    writer.writerow([username, name, target_group.title])
            print('Parsing users group complete successfully.')

            all_messages=[]
            offset_id=0
            limit=100

            while True:
                history=client(GetHistoryRequest(
                    peer=target_group,
                    offset_id=offset_id,
                    offset_date=None,
                    add_offset=0,
                    limit=limit,
                    max_id=0,
                    min_id=0,
                    hash=0
                ))
                if not history.messages:
                    break
                messages=history.messages
                for message in messages:
                    all_messages.append(message.message)
                if len(all_messages)==100:
                    break
            print('Save data in file...')

            with open('chats.csv', "w", encoding='UTF-16') as f:
                writer=csv.writer(f, delimiter=',', lineterminator="\n")
                writer.writerow(["message"])
                for message in all_messages:
                    writer.writerow([message])
        else:
            all_message = []
            for message in client.iter_messages(target_group):
                all_message.append(message.message)
            print('Save data in file...')

            with open('chats.csv', "w", encoding='UTF-16') as f:
                writer=csv.writer(f, delimiter=',', lineterminator="\n")
                writer.writerow(['ID', 'name', "message"])
                for msg in all_message:
                    writer.writerow([target_group.id, client.get_entity(target_group.id).first_name, msg])
    finally:
        client.disconnect()
        return 'OK'

