import os
from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from sqlalchemy import join

__author__ = 'colla69'

class ComputerHelperSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(ComputerHelperSkill, self).__init__(name="TemplateSkill")
        # Initialize working variables used within the skill.
        self.dictation_words = []
        self.read_vocab("UndoKeyword.voc")

    def read_vocab(self, name="DictationKeyword.voc"):
        path = join(dirname(__file__), "vocab", self.lang,
                    name)
        with open(path, 'r') as voc_file:
            for line in voc_file.readlines():
                parts = line.strip().split("|")
                entity = parts[0]
                self.dictation_words.append(entity)
                for alias in parts[1:]:
                    self.dictation_words.append(alias)

    @intent_handler(IntentBuilder("OpenerIntent").require("open"))
    def handle_opener_intent(self, message):
        self.speak_dialog("choose.app", expect_response=True)

    @intent_handler(IntentBuilder("BrowserIntent").require("browser"))
    def handle_opener_intent(self, message):
        cmd = "google-chrome"
        execute(cmd)

    def check_for_intent(self, utterance):
        # check if dictation intent will trigger
        # TODO use https://github.com/MycroftAI/mycroft-core/pull/1351
        for word in self.dictation_words:
            if word in utterance:
                return True
        return False

    def converse(self, utterances, lang="en-us"):
        if self.check_for_intent(utterances[0]):
            return True
        else:
            return False


def execute(cmd):
    os.system(cmd)


def create_skill():
    return ComputerHelperSkill()
