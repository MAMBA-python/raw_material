# Cleaning WhatsApp log
import os
import re
import pandas as pd
import numpy as np
import zipfile
import glob


def read_whatsapp(whatsapp_file):

    if whatsapp_file.endswith('.zip'):
        whatsapp_txt = unzip_whatsapp_file(whatsapp_file)
    else:
        whatsapp_txt = whatsapp_file

    # find usernames
    user_names = []
    with open(whatsapp_txt, 'r', encoding="utf8") as fo:
        for line in fo:
            if line.startswith('[') and ':' in line[23:]:
                user_name = line[23:].split(':')[0]
                if user_name not in user_names:
                    user_names.append(user_name)

    # create dataframe with time, user and text
    datetime_list = []
    user_list = []
    text_list = []
    with open(whatsapp_txt, 'r', encoding="utf8") as fo:
        for line in fo:
            if line.startswith('['):
                for user_name in user_names:
                    if line[23:].startswith(user_name):
                        user_list.append(user_name)
                        text_list.append(line[len(user_name) + 25:])
                        datetime_list.append(line[1:21])
            else:
                # this is necesary for using messages with multiple lines
                text_list[-1] = text_list[-1] + line

    time_user_df = pd.DataFrame(data={'user': user_list,
                                      'text': text_list,
                                      'message': [1] * len(user_list)},
                                index=pd.to_datetime(datetime_list, dayfirst=True))
    time_user_df[['user', 'message']].to_csv(r'data\_chat_df.csv')

    return time_user_df

def unzip_whatsapp_file(whatsapp_file):

    zip_ref = zipfile.ZipFile(whatsapp_file, 'r')
    zip_ref.extractall(os.path.split(whatsapp_file)[0])
    zip_ref.close()

    zip_dir = os.path.split(whatsapp_file)[0]

    return os.path.join(zip_dir, '_chat.txt')