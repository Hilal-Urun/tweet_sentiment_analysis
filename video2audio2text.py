import pytube #pip install pytube3
import subprocess
import speech_recognition as sr
import zeyrek

analyzer = zeyrek.MorphAnalyzer()
#download
url = 'https://www.youtube.com/watch?v=ITYVXUvMtHI'
youtube = pytube.YouTube(url)
video = youtube.streams.first()
video.download('./videos', filename="asd")
#audio converter
filename = "./videos/asd.mp4"
outputname = "./audios/asd"

#Kullanımı için ffmpeg yüklü olması gereklidir
command = "ffmpeg -i "+filename+" -ab 160k -ac 2 -ar 44100 -vn "+outputname+".wav"
subprocess.call(command, shell=True)
#toText
r = sr.Recognizer()
asd = sr.AudioFile('./audios/asd.wav')
with asd as source:
    audio = r.record(source)
    #print(r.recognize_sphinx(audio))
    text = r.recognize_google(audio, language='tr-TR')
    print(text)
    analysis = analyzer.analyze(text)

print(analysis)
print(analyzer.lemmatize('hedeflenmektedir'))


# FOR NORMAL LINKS
'''import urllib.request

url = ""
name = "dsd"
name = name+".mp4"

try:
    urllib.request.urlretrieve(url, name)
    print(urllib.request.urlretrieve(url, name))
except Exception as e:
    print(e)'''
