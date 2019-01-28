from aip import AipSpeech

APP_ID = '15244193'
API_KEY = 'PZGNuLzj5q7bMGGDM4wWbl3F'
SECRET_KEY = 'HMlYtVCYc8nn5g81TnCyShVYPMSlmI8F '

def geneAudio(number):
    f = open("598115920.txt", encoding='utf8')
    j = 0
    lines = f.readlines()
    for i in range(number):
        content = " "
        for line in lines[j:j+4]:
            content = content + line.strip() + " "
        name = "{}_{}".format(j + 1, j + 4)
        print(content)
        text2audio(content,name)
        j = j + 4

def text2audio(content,name):
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis(content, 'zh', 1, {'vol': 5, 'per': 4, 'spd': 5})
    if not isinstance(result, dict):
        with open('asset/audios/{}.mp3'.format(name), 'wb') as f:
            f.write(result)

if __name__ == '__main__':
    geneAudio(120)
