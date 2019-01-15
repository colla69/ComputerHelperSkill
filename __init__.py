import os
from os.path import dirname, join
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

__author__ = 'colla69'

browserCMD = "sensible-browser"
allCMD = "sensible-browser & skypeforlinux & whatsie &"
pyCharmCMD = "env BAMF_DESKTOP_FILE_HINT=/var/lib/snapd/desktop/applications/pycharm-professional_pycharm-professional.desktop /snap/bin/pycharm-professional  &"
ideaCMD = "env BAMF_DESKTOP_FILE_HINT=/var/lib/snapd/desktop/applications/intellij-idea-ultimate_intellij-idea-ultimate.desktop /snap/bin/intellij-idea-ultimate  &"
raiunoCMD = "sensible-browser 'http://webtvhd.com/rai-uno-live.php' "

class ComputerHelperSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(ComputerHelperSkill, self).__init__(name="TemplateSkill")
        # Initialize working variables used within the skill.
        self.dictation_words = []
        self.read_vocab("browser.voc")
        self.read_vocab("pycharm.voc")
        self.read_vocab("all.voc")
        self.read_vocab("raiuno.voc")


    def read_vocab(self, name=""):
        path = join(dirname(__file__), "vocab", self.lang,
                    name)
        LOG.info(path)
        with open(path, 'r') as voc_file:
            for line in voc_file.readlines():
                parts = line.strip().split("|")
                entity = parts[0]
                self.dictation_words.append(entity)
                for alias in parts[1:]:
                    self.dictation_words.append(alias)

    @intent_handler(IntentBuilder("OpenerIntent").require("OpenKeyword"))
    def handle_opener_intent(self, message):
        self.speak_dialog("choose.app", expect_response=True)

    @intent_handler(IntentBuilder("BrowserIntent").require("browser"))
    def handle_browser_intent(self, message):
        execute(browserCMD)

    @intent_handler(IntentBuilder("StackIntent").require("all"))
    def handle_stack_intent(self, message):
        execute(allCMD)

    @intent_handler(IntentBuilder("PyCharmsIntent").require("pycharm"))
    def handle_pycharms_intent(self, message):
        execute(pycharmCMD)

    @intent_handler(IntentBuilder("IdeaIntent").require("idea"))
    def handle_idea_intent(self, message):
        execute(ideaCMD)

    @intent_handler(IntentBuilder("RaiUnoIntent").require("raiuno"))
    def handle_raiuno_intent(self, message):
        execute(raiunoCMD)

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
