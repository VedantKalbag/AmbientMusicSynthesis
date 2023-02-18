import ambientmusicsynthesis as am
from ambientmusicsynthesis.ambientmusicsynthesis import AmbientMusicSynthesis
import timeit
starttime = timeit.default_timer()
ams = AmbientMusicSynthesis()
ams.generate_audio(90, {0.0:1, 20.3:2, 40.6:3, 60.9:4, 81.2:5, 90:1}, sample_rate=44100)
# print(audio)
# print(audio.realise(44100))
# audio.play()
# ams.export_audio('test_2.wav')
ams.export('test_2.wav', 44100)
print("The time taken is :", timeit.default_timer() - starttime) 