import requests
import re
import redis
import time

def get_ipa(word):
    headers =  {
            'Content-Type': 'application/x-www-form-urlencoded' ,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' ,
            'Referer': 'https://tophonetics.com/' ,
            'Accept-Encoding': 'gzip, deflate, br' ,
    }

    resp = requests.post(
        'https://tophonetics.com/',
        headers=headers,
        data='text_to_transcribe={}&submit=Show+transcription&output_dialect=am&output_style=only_tr&preBracket=&postBracket=&speech_support=1'.format(word),
    )

    pattern = '<div id="transcr_output"><span class="transcribed_word">(.*)</span><br /></div>'
    m = re.search(pattern, resp.content)
    return  None if m is None else m.group(1)

with open('words', 'r') as f:
    lines = [line for line in f.read().splitlines() if line != '']

rclient = redis.Redis(host='localhost', port=6379, db=0)
# rclient.set('foo', 'bar')
# print rclien.get('foo')

with open('words.ipa', 'a') as f:
    while True:
        word = rclient.rpop('wordslist')
        print 'getting pronunciation for', word,
        if word is None: break
        pronunciation = get_ipa(word)
        print pronunciation
        f.write('{} {}\n'.format(word, pronunciation))
        f.flush()

