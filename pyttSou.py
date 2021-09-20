
import pyttsx3
# engine = pyttsx3.init()
# rate = engine.getProperty('rate')
# engine.setProperty('rate', rate-100)
# engine.say('The quick brown fox jumped over the lazy dog.')
# engine.runAndWait()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
  engine.setProperty('voice', voice.id)
  print(voice.id)
  engine.say('中文呢啊么')
  engine.runAndWait()


# com.apple.speech.synthesis.voice.mei-jia
# com.apple.speech.synthesis.voice.ting-ting.premium
#

