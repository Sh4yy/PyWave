from SoundWave import SoundWave

wave = (
    SoundWave
    .from_url(url='https://my_url.com/my_file.mp3')
    .with_bar_count(50)
    .with_skip_percent(0.75)
    .using_average()
    .process()
    .visualize(bar_height=50, bar_width=5)
    .delete_file()
).data

print(wave)
