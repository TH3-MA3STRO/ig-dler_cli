from login import login
from profiledler import ProfileDler
from storydler import StoryDler
from progress.bar import *
from requests import Session
import argparse
import pickle
import os
import glob
parser = argparse.ArgumentParser(prog='ig-dler_cli')
parser.add_argument('--login',action='store_true',default=None)
args = parser.parse_args()
ext_options = ''
new_session = Session()

if args.login:
    ext_options = '''\n[3] Download Stories [4] Download Highlights'''

    if not os.path.exists('cookies'):
        os.mkdir('cookies')
    
    files = glob.glob('cookies/*')
    permit = 'N'

    if len(files) != 0:
        permit = input('Old login credentials found!\nDo you want to use them?[y/N]: ')

        if permit.lower()=='y' or permit.lower() == 'yes' or permit=='':
            for opt_num,acc_name in enumerate(files):
                acc_name = acc_name.split('/')[-1]
                print(f'[{opt_num+1}] {acc_name}')

            while True:
                try:
                    cookiefile = int(input('Enter the file no. which you wish to use: '))
                    cookiefile = files[int(cookiefile)-1]
                except ValueError or IndexError:
                    print('Please enter one of the specified numbers!')
                    continue

            print(f"Using {cookiefile.split('/')[-1]}'s cookies'")

            with open(cookiefile, 'rb') as in_cookies:
                new_session.cookies.update(pickle.load(in_cookies))

    if permit.lower()=='n' or permit.lower() == 'no':
        print('Enter Instagram login credentials:')
        username = input('Username: ')
        password = input('Password: ')
        a = login(username,password)
        if a:
            print('Login succesful:)')
        else:
            print('Login unsuccessful:(\nPlease try again after sometime!')
            exit()


target = input('Enter target profile: ')

print(f'Select the option which you wish to use:\n[1] Download DP [2] Download Post{ext_options}')
option = input(': ')

os.system('clear')

if option == '1':
    ProfileDler(target,new_session).execute()
elif option == '2':
    print(
'''Enter the post\'s shortcode if you want to download that particular post
e.g. POST's LINK: https://www.instagram.com/p/BucMXT-hu4X/
     SHORTCODE: BucMXT-hu4X
[NOTE: Leave empty if you want to download all the posts]
(*CASE SENSITIVE*)''')

    _filter = input(': ')
    ProfileDler(target,new_session,_filter=_filter).profile_iterator()
elif option == '3':
    StoryDler(target,new_session).download_stories()
elif option == '4':
    print(
'''Enter the Highlight\'s name if you want to download that particular Highlight
[NOTE: Leave empty if you want to download all the highlights]
(*NOT CASE SENSITIVE*)'''
    )

    _filter = input(': ')
    StoryDler(target,new_session, _filter_title=_filter).getHighlightId()
