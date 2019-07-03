import os
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler, intent_file_handler
from mycroft.util.log import LOG
import pynput
from alsaaudio import Mixer, mixers as alsa_mixers
from mycroft.skills.audioservice import AudioService

keyboard = pynput.keyboard.Controller()


__author__ = 'colla69'


browserCMD = "sensible-browser"
allCMD = "sensible-browser & skypeforlinux & whatsie &"
pyCharmCMD = "env BAMF_DESKTOP_FILE_HINT=/var/lib/snapd/desktop/applications/pycharm-professional_pycharm" \
             "-professional.desktop /snap/bin/pycharm-professional  & "
ideaCMD = "env BAMF_DESKTOP_FILE_HINT=/var/lib/snapd/desktop/applications/intellij-idea-ultimate_intellij-idea" \
          "-ultimate.desktop /snap/bin/intellij-idea-ultimate  & "
raiunoCMD = "firefox 'http://webtvhd.com/rai-uno-live.php' "


def beamer_screen():
    os.system("xrandr --output DVI-I-2 --mode 1920x1080 --output  DVI-I-3 --off --output HDMI-0 --mode 1920x1080")


def table_screen():
    os.system("xrandr --output DVI-I-2 --mode 1920x1080 --output DVI-I-3 --mode 1920x1080  --right-of DVI-I-2 "
              "--output HDMI-0 --off")


def turn_off_screens():
    os.system("xset dpms force off")


class ComputerHelperSkill(MycroftSkill):
    def __init__(self):
        super(ComputerHelperSkill, self).__init__(name="TemplateSkill")
        # mixers = alsa_mixers()
        self.mixer = Mixer('Master')
        # self.audioservice = AudioService(self._bus)
        # Initialize working variables used within the skill.

    def initialize(self):
        #beamer_intent = IntentBuilder("BeamerIntent").require("BeamerKeyword").build()
        #self.register_intent(beamer_intent, self.handle_beamer_intent)
        #table_intent = IntentBuilder("TableIntent").require("TableKeyword").build()
        #self.register_intent(table_intent,self.handle_table_intent)

        self.add_event('recognizer_loop:record_begin', self.handle_listener_started)
        self.add_event('recognizer_loop:record_end', self.handle_listener_stopped)

        # self.add_event('recognizer_loop:audio_output_start', self.handle_audio_start)
        # self.add_event('recognizer_loop:audio_output_end', self.handle_audio_stop)
        # self.audioservice.play("http://plex.colarietitosti.info:32400/library/parts/15480/1557728134/file.mp3?download=1&X-Plex-Token=y9pLd6uPWXpwbw14sRYf")

    ######################################################################
    # audio ducking
    def handle_listener_started(self, message):
        vol = Mixer('Master').getvolume()[0]
        vol = (vol//3)*2
        Mixer('Master').setvolume(vol)

    def handle_listener_stopped(self, message):
        vol = Mixer('Master').getvolume()[0]
        vol = (vol // 2) * 3
        if vol > 100:
            vol = 100
        Mixer('Master').setvolume(vol)

    def handle_audio_start(self, event):
        vol = Mixer('Master').getvolume()[0]
        vol = (vol // 3) * 2
        Mixer('Master').setvolume(vol)

    def handle_audio_stop(self, event):
        vol = Mixer('Master').getvolume()[0]
        vol = (vol // 2) * 3
        if vol > 100:
            vol = 100
        Mixer('Master').setvolume(vol)

    ######################################################################
    # intents
    """
        def handle_beamer_intent(self, message):
            beamer_screen()
            self.speak_dialog("changes.done")
    
        def handle_table_intent(self, message):
            table_screen()
            self.speak_dialog("changes.done")
    """

    @intent_file_handler("turn.off.screens.intent")
    def handle_night_intent(self, message):
        turn_off_screens()

    @intent_handler(IntentBuilder("BrowserIntent").require("browser"))
    def handle_browser_intent(self, message):
        os.system(browserCMD)

    @intent_handler(IntentBuilder("StackIntent").require("all"))
    def handle_stack_intent(self, message):
        os.system(allCMD)

    @intent_handler(IntentBuilder("PyCharmsIntent").require("open").require("pycharm"))
    def handle_pycharms_intent(self, message):
        os.system(pyCharmCMD)

    @intent_handler(IntentBuilder("IdeaIntent").require("idea"))
    def handle_idea_intent(self, message):
        os.system(ideaCMD)

    @intent_handler(IntentBuilder("RefreshIntent").require("refresh"))
    def handle_refresh_intent(self, message):
        keyboard.press(pynput.keyboard.Key.f5)
        keyboard.release(pynput.keyboard.Key.f5)

    def converse(self, utterances, lang="en-us"):
        # contains all triggerwords for second layer Intents
        return False

    def stop(self):
        pass



def create_skill():
    return ComputerHelperSkill()
