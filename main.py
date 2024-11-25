from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from plyer import gps, accelerometer
from kivy.clock import Clock
import time

class AnomalyScanner(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)

        # Judul aplikasi
        self.title_label = Label(
            text="[b]Anomali Scanner[/b]", font_size='24sp', size_hint=(1, None), height=40, markup=True
        )
        self.add_widget(self.title_label)

        # Waktu di bawah judul
        self.time_label = Label(
            text=self.get_current_time(), font_size='16sp', size_hint=(1, None), height=30
        )
        self.add_widget(self.time_label)

        # Perbarui waktu setiap detik
        Clock.schedule_interval(self.update_time, 1)

        # Status lokasi
        self.location_label = Label(
            text="Lokasi: Menunggu GPS...", font_size='16sp', size_hint=(1, None), height=40
        )
        self.add_widget(self.location_label)

        # Status sinyal
        self.signal_label = Label(
            text="Status Sinyal: Menunggu sinyal...", font_size='16sp', size_hint=(1, None), height=40
        )
        self.add_widget(self.signal_label)

        # Tombol deteksi anomali
        self.scan_button = Button(
            text="Deteksi Anomali", size_hint=(1, None), height=50, font_size='18sp', background_color=(0.2, 0.6, 1, 1)
        )
        self.scan_button.bind(on_press=self.scan_anomalies)
        self.add_widget(self.scan_button)

        # Hasil deteksi anomali
        self.result_label = Label(
            text="Hasil Deteksi: Belum ada anomali.", font_size='16sp', size_hint=(1, None), height=40
        )
        self.add_widget(self.result_label)

        # Tombol untuk mengaktifkan sensor
        self.activate_sensor_button = Button(
            text="Aktifkan Sensor", size_hint=(1, None), height=50, font_size='16sp', background_color=(0.4, 0.8, 0.4, 1)
        )
        self.activate_sensor_button.bind(on_press=self.activate_sensors)
        self.add_widget(self.activate_sensor_button)

    def get_current_time(self):
        return time.strftime("%H:%M:%S")

    def update_time(self, dt):
        self.time_label.text = self.get_current_time()

    def activate_sensors(self, instance):
        try:
            gps.configure(on_location=self.update_location, on_status=self.update_status)
            gps.start(minTime=1000, minDistance=1)
            self.location_label.text = "GPS diaktifkan, mencari lokasi..."
        except NotImplementedError:
            self.location_label.text = "GPS tidak didukung di perangkat ini."

        try:
            accelerometer.enable()
        except NotImplementedError:
            self.signal_label.text = "Sensor akselerometer tidak didukung di perangkat ini."

    def update_location(self, **kwargs):
        lat = kwargs.get('lat', 'Tidak ada')
        lon = kwargs.get('lon', 'Tidak ada')
        self.location_label.text = f"Lokasi: Lat {lat}, Lon {lon}"

    def update_status(self, stype, status):
        self.signal_label.text = f"Status Sinyal: {status}"

    def scan_anomalies(self, instance):
        try:
            accel_data = accelerometer.acceleration
            x, y, z = accel_data if accel_data else (0, 0, 0)
            anomalies = [axis for axis, value in zip("XYZ", (x, y, z)) if abs(value) > 10]

            if anomalies:
                self.result_label.text = f"Anomali Terdeteksi pada Aksis: {', '.join(anomalies)}"
            else:
                self.result_label.text = "Tidak ada anomali terdeteksi."
        except Exception as e:
            self.result_label.text = f"Kesalahan: {str(e)}"


class AnomalyScannerApp(App):
    def build(self):
        return AnomalyScanner()


if __name__ == "__main__":
    AnomalyScannerApp().run()
