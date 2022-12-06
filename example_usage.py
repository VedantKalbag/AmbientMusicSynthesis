import ambientmusicsynthesis.ambientmusicsynthesis as ams

a = ams.AmbientMusicSynthesis()
a.generate_audio(90, {0.0:1, 20.3:2, 40.6:3, 60.9:4, 81.2:5, 90:1}, sample_rate=44100)
a.export_audio('test_n.wav')