import os
from os.path import dirname, join
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
import pynput
from alsaaudio import Mixer, mixers as alsa_mixers
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


class ComputerHelperSkill(MycroftSkill):

    def __init__(self):
        super(ComputerHelperSkill, self).__init__(name="TemplateSkill")
        # Initialize working variables used within the skill.
        self.dictation_words = []
        try:
            # If there are only 1 mixer use that one
            mixers = alsa_mixers()
            if len(mixers) == 1:
                self.mixer = Mixer(mixers[0])
            else:  # Try using the default mixer
                self.mixer = Mixer()
        except Exception:
            # Retry instanciating the mixer
            try:
                self.mixer = Mixer()
            except Exception as e:
                self.log.error('Couldn\'t allocate mixer, {}'.format(repr(e)))

    def initialize(self):
        beamer_intent = IntentBuilder("BeamerIntent").require("BeamerKeyword").build()
        self.register_intent(beamer_intent, self.handle_beamer_intent)
        table_intent = IntentBuilder("TableIntent").require("TableKeyword").build()
        self.register_intent(table_intent,self.handle_table_intent)
        self.add_event('recognizer_loop:record_begin', self.handle_listener_started)
        self.add_event('recognizer_loop:record_end', self.handle_listener_stopped)

    def read_vocab(self, name=""):
        path = join(dirname(__file__), "vocab", self.lang, name)
        LOG.info(path)
        with open(path, 'r') as voc_file:
            for line in voc_file.readlines():
                parts = line.strip().split("|")
                entity = parts[0]
                self.dictation_words.append(entity)
                for alias in parts[1:]:
                    self.dictation_words.append(alias)

    ######################################################################
    # audio ducking

    def handle_listener_started(self, message):
        vol = self.mixer.getvolume()[0]
        vol = (vol//3)*2
        self.mixer.setvolume(vol)

    def handle_listener_stopped(self, message):
        vol = self.mixer.getvolume()[0]
        vol = (vol // 2) * 3
        self.mixer.setvolume(vol)

    ######################################################################
    # intents

    def handle_beamer_intent(self, message):
        beamer_screen()
        self.speak_dialog("changes.done")

    def handle_table_intent(self, message):
        table_screen()
        self.speak_dialog("changes.done")

    @intent_handler(IntentBuilder("BrowserIntent").require("browser"))
    def handle_browser_intent(self, message):
        execute(browserCMD)

    @intent_handler(IntentBuilder("StackIntent").require("all"))
    def handle_stack_intent(self, message):
        execute(allCMD)

    @intent_handler(IntentBuilder("PyCharmsIntent").require("open").require("pycharm"))
    def handle_pycharms_intent(self, message):
        execute(pyCharmCMD)

    @intent_handler(IntentBuilder("IdeaIntent").require("idea"))
    def handle_idea_intent(self, message):
        execute(ideaCMD)

    @intent_handler(IntentBuilder("RefreshIntent").require("refresh"))
    def handle_refresh_intent(self, message):
        keyboard.press(pynput.keyboard.Key.f5)
        keyboard.release(pynput.keyboard.Key.f5)

    def check_for_intent(self, utterance):
        # check if dictation intent will trigger
        # TODO use https://github.com/MycroftAI/mycroft-core/pull/1351
        for word in self.dictation_words:
            if word in utterance:
                return True
        return False

    def converse(self, utterances, lang="en-us"):
        # contains all triggerwords for second layer Intents
        LOG.info(self.dictation_words)
        ####
        return False

    def stop(self):
        pass


def execute(cmd):
    os.system(cmd)


def create_skill():
    return ComputerHelperSkill()
