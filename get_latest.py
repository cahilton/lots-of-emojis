from __future__ import print_function
import sys
import os, json
import requests
from subprocess import call

if __name__ == "__main__":
    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        token = ''

    if len(token) > 0:
        url = "https://slack.com/api/emoji.list?token=%s&pretty=1" % token
        try:
            print('saving current json')

            r = requests.get(url)
            r_json = r.json()
            if r_json['ok']:
                with open('current_emojis.json', 'wb') as cur:
                    cur.write(r.content)
            else:
                print('bad request getting current emojis')
        except Exception as e:
            print(e)

    with open('./current_emojis.json') as json_data:
        cur_json = json.load(json_data)
        print('reading current json')

        if cur_json['ok']:
            emoji = cur_json['emoji']
            print('save json list')
            with open('./the_list.json', 'w') as the_list_file:
               the_list_file.write(json.dumps(sorted(emoji.keys()), indent=4))

            n = 0
            for k, v in emoji.items():
                url = v
                if url.startswith('alias'):
                    continue
                r = requests.get(url)

                file_name = k + '.' + v.split('.')[-1]
                with open('./images/{}'.format(file_name), 'wb') as f:
                    f.write(r.content)
                n += 1
                if n % 50 == 0:
                    call(['git', 'add', 'images/.'])
                    call(['git', 'commit', '-m', 'add images'])
                    call(['git', 'push'])
                    print('so far with {}'.format(n))

            call(['git', 'add', 'images/.'])
            call(['git', 'commit', '-m', 'add images'])
            call(['git', 'add', '/the_list.json'])
            call(['git', 'commit', '-m', 'update list file'])
            call(['git', 'push'])
            print('done with '.format(n))

