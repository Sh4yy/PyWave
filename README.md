# PyWave
A python script for extracting and visualizing sound waves from audio files.

## API
This script is based on the builder pattern which easily lets you customize the settings.

``` python
wave = (
    SoundWave
    .from_url(url='https://some_url/my_music.mp3')
    .with_bar_count(50)
    .with_skip_percent(0.75)
    .using_average()
    .process()
    .visualize(bar_height=50, bar_width=5)
    .delete_file()
).data
```

## Available Methods

### Initializers
You can initialize the SoundWave class using the 3 available class methods,
`from_file`, `from_url`, `from_path` to provide your audio data from a file, direct url, or from a path on your device.

##### with_bar_count(count: int)
change the number of output bars, default is set to 50

##### with_skip_percent(ratio: float)
set a percentage of data to be ignored in order to speed up the process. it is recommended to use 0.5 or higher

##### using_maximum()
use the maximum function when processing the given data

##### using_average()
use the average function when processing the given data

##### visualize(bar_height: int, bar_width: int)
draw the processed sound wave

##### delete_file()
would delete the files after processing them

##### data
calculated property, returns a list of bar heights as int percentage, 100 being the maximum. This is to provide an efficient way to store the data as a blob of UInt8 values. 
