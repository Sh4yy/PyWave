import requests
from uuid import uuid4
import os
from pydub import AudioSegment
import numpy as np
import shutil
from PIL import Image, ImageDraw


class SoundWave:

    bar_count = 50
    skip_count = 5

    def __init__(self, file):
        """
        initialize sound wave from file
        :param file:
        """
        self._file = file
        self._audio = AudioSegment.from_file(file.name)
        self._frame_rate = self._audio.frame_rate
        self._bar_count = self.bar_count
        self._skip_count = self.skip_count
        self._data = None
        self._process_func = max

    @classmethod
    def from_file(cls, file):
        """
        initialize SoundWave from sound file
        :param file: file instance
        :return: SoundWave
        """
        return cls(file)

    @classmethod
    def from_path(cls, path):
        """
        initialize SoundWave from sound path
        :param path: sound path
        :return: SoundWave
        """
        return cls(open(path, 'rb'))

    @classmethod
    def from_url(cls, url):
        """
        initialize SoundWave from sound url
        :param url: sound url
        :return: SoundWave
        """
        uid = f'downloads/{uuid4().hex}.mp3'
        with requests.get(url, stream=True) as stream:
            with open(uid, 'wb') as file:
                shutil.copyfileobj(stream.raw, file)

        return cls(open(uid, 'rb'))

    def with_bar_count(self, count):
        """
        change bar count
        :param count: new bar count
        :return: self
        """
        self._bar_count = count
        return self

    def with_skip_percent(self, ratio):
        """
        percentage of the data to ignore
        :param ratio: ignore ratio
        :return:
        """
        if ratio >= 1:
            self._skip_count = 1
        elif ratio >= 0:
            self._skip_count = int(1 / (1 - ratio))
        else:
            raise Exception('invalid skip percentage')
        return self

    def using_maximum(self):
        """
        use maximum function
        :return: self
        """
        self._process_func = max
        return self

    def using_average(self):
        """
        use average function
        :return: self
        """
        def avg(lst):
            lst = list(lst)
            return sum(lst) / len(lst)
        self._process_func = avg
        return self

    def process(self):
        """
        start processing the data
        :return:
        """

        data = np.fromstring(self._audio._data, np.int16)
        data = data[::self._skip_count]
        height_list = []
        max_height = 0

        def chunks(l, n):
            for i in range(0, len(l), n):
                yield l[i:i + n]

        for segment in chunks(data, int(len(data) / self._bar_count)):
            height = self._process_func(map(lambda x: abs(x), segment))
            height_list.append(height)
            if max_height < height:
                max_height = height

        self._data = list(map(lambda x: int(x / max_height * 100), height_list))
        return self

    def visualize(self, bar_height, bar_width):
        """
        visualize this soundwave
        :param bar_height: max height of the bars
        :param bar_width: width of each bar
        :return: self
        """

        image = Image.new('RGBA', (self._bar_count * bar_width, bar_height), (255, 255, 255, 1))
        draw = ImageDraw.Draw(image)

        current_x = 1
        for segment in self.data:
            seg_height = segment / 100 * bar_height
            current_y = (bar_height - seg_height) / 2
            draw.line((current_x, current_y, current_x, current_y + seg_height), fill=(169, 171, 172), width=4)
            current_x = current_x + bar_width

        image.show()
        return self

    @property
    def data(self):
        """ get processed data """
        return self._data

    def delete_file(self):
        """ delete file after processing """
        os.remove(self._file.name)
        return self

