from SoundWave import SoundWave

path = 'downloads/show-137.mp3'
wave = (
    SoundWave
    .from_path(path)
    .with_bar_count(50)
    .with_skip_count(25)
    .process()
    .visualize(60, 5)
).data

wave2 = (
    SoundWave
    .from_url(url='google.mp3')
    .with_bar_count(50)
    .with_skip_count(25)
    .process()
    .visualize(50, 5)
    .delete_file()
).data

