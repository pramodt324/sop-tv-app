import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.video import Video
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock

class OfflineSOPPlayer(BoxLayout):
    def __init__(self, **kwargs):
        super(OfflineSOPPlayer, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        self.video_file = None
        self.image_file = None
        self.image_duration = 10  # Seconds to show the image before looping back
        
        self.video_player = None
        self.image_viewer = None
        
        self.find_usb_media()
        
        if self.video_file and self.image_file:
            self.play_video()
            Clock.schedule_interval(self.check_video_status, 1)
        else:
            self.add_widget(Label(
                text="[ OFFLINE SOP SYSTEM ]\n\nERROR: USB Drive Not Detected\nOR Files Missing.\n\nPlease insert USB containing:\n- sop.mp4\n- sop.jpg",
                font_size='22sp', halign='center', color=(1, 0.3, 0.3, 1)
            ))

    def find_usb_media(self):
        possible_usb_roots = ['/storage', '/mnt', '/media', '/mnt/media_rw']
        for root in possible_usb_roots:
            if not os.path.exists(root):
                continue
            for dirpath, _, filenames in os.walk(root):
                if "emulated" in dirpath or "self" in dirpath or "secure" in dirpath:
                    continue
                for filename in filenames:
                    name_lower = filename.lower()
                    full_path = os.path.join(dirpath, filename)
                    if name_lower == "sop.mp4":
                        self.video_file = full_path
                    elif name_lower in ["sop.jpg", "sop.png", "sop.jpeg"]:
                        self.image_file = full_path
                if self.video_file and self.image_file:
                    return

    def play_video(self):
        self.clear_widgets()
        self.video_player = Video(source=self.video_file, state='play', options={'eos': 'stop'})
        self.video_player.bind(state=self.on_video_state_change)
        self.add_widget(self.video_player)

    def on_video_state_change(self, instance, value):
        if value == 'stop':
            self.display_image()

    def check_video_status(self, dt):
        if self.video_player:
            try:
                if self.video_player.position >= self.video_player.duration and self.video_player.duration > 0:
                    self.display_image()
            except Exception:
                pass

    def display_image(self):
        self.clear_widgets()
        if self.video_player:
            self.video_player.unload()
            self.video_player = None
        self.image_viewer = Image(source=self.image_file, allow_stretch=True, keep_ratio=True)
        self.add_widget(self.image_viewer)
        Clock.schedule_once(self.loop_back_to_video, self.image_duration)

    def loop_back_to_video(self, dt):
        self.play_video()

class SOPOfflineApp(App):
    def build(self):
        return OfflineSOPPlayer()

if __name__ == '__main__':
    SOPOfflineApp().run()

