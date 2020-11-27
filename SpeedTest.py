#Aleks4920
import kivy
kivy.require('1.6.0')
from kivy.config import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import BoundedNumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from os.path import join, dirname, abspath
from kivy.uix.slider import Slider
import pyspeedtest

class Gauge(Widget):
    unit = NumericProperty(1.8)
    value = BoundedNumericProperty(0, min=0, max=100, errorvalue=0)
    path = dirname(abspath(__file__))
    file_gauge = StringProperty(join(path, "cadran1.png"))
    file_needle = StringProperty(join(path, "needle1.png"))
    size_gauge = BoundedNumericProperty(128, min=128, max=256, errorvalue=128)
    size_text = NumericProperty(10)

    def __init__(self, **kwargs):
        super(Gauge, self).__init__(**kwargs)

        self._gauge = Scatter(
            size=(self.size_gauge, self.size_gauge),
            do_rotation=False,
            do_scale=False,
            do_translation=False
        )

        _img_gauge = Image(
            source=self.file_gauge,
            size=(self.size_gauge, self.size_gauge),
            pos=self.pos

        )

        self._needle = Scatter(
            size=(self.size_gauge, self.size_gauge),
            do_rotation=False,
            do_scale=False,
            do_translation=False
        )

        _img_needle = Image(
            source=self.file_needle,
            size=(self.size_gauge, self.size_gauge)
        )

        self._glab = Label(font_size=self.size_text, markup=True)
        self.Text = Label(text="Download", font_size=self.size_text, markup=True, bold=True)
        self._progress = ProgressBar(max=100, height=20, value=self.value)

        self._gauge.add_widget(_img_gauge)
        self._needle.add_widget(_img_needle)

        self.add_widget(self._gauge)
        self.add_widget(self._needle)
        self.add_widget(self._glab)
        self.add_widget(self.Text)
        self.add_widget(self._progress)

        self.bind(pos=self._update)
        self.bind(size=self._update)
        self.bind(value=self._turn)

    #update needle postion and sizing of widgets
    def _update(self, *args):
        self._gauge.pos = self.pos
        self._needle.pos = (self.x, self.y)
        self._needle.center = self._gauge.center
        self._glab.center_x = self._gauge.center_x
        self._glab.center_y = self._gauge.center_y + (self.size_gauge / 4)
        self.Text.center_x = self._gauge.center_x
        self.Text.center_y = self._gauge.center_y + (self.size_gauge / 1.5)
        self._progress.x = self._gauge.x
        self._progress.y = self._gauge.y + (self.size_gauge / 4)
        self._progress.width = self.size_gauge

    #set needle to 50 and updat 1 for every value
    def _turn(self, *args):
        self._needle.center_x = self._gauge.center_x
        self._needle.center_y = self._gauge.center_y
        self._needle.rotation = (50 * self.unit) - (self.value * self.unit)
        self._glab.text = "[b]{0:.0f}[/b]".format(self.value)
        self._progress.value = self.value


#this allows app to run a loop till close
if __name__ == '__main__':






    
    class GaugeApp(App):

        def build(self):
            box = BoxLayout(orientation='vertical', padding=5, pos_hint={'x': .33, 'y': .4})
            self.gauge = Gauge(value=50, size_gauge=256, size_text=25)

            box.add_widget(self.gauge)
            Clock.schedule_interval(lambda *t: self.gauge_increment(), 0.1)

            return box

        def gauge_increment(self):
            st=pyspeedtest.SpeedTest("www.google.com")
            self.gauge.value =  int(st.download()/10000)

    GaugeApp().run()
box.add_widget(self.gauge)
