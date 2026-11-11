import mido
from mido import Message, MidiFile, MidiTrack
from pathlib import Path

class note:

    def __init__(self, value, time):
        self.value = value
        self.time = time
        self.pc = None

class bend:

    def __init__(self, value, time):
            self.value = value
            self.time = time
            self.pc = None

class aftertouch:

    def __init__(self, value, time):
            self.value = value
            self.time = time      
            self.pc = None

class PC:

    def __init__(self, track, id):
        self.notes = []
        self.bends = []
        self.aftertouches = []
        self.active_note = -1
        self.id = id
        self.track = track

    def add_note(self, note: note):
        note.pc = self.id
        self.notes.append(note)
    def add_bend(self, bend: bend):
        bend.pc = self.id
        self.bends.append(bend)
    def add_aftertouch(self, aftertouch: aftertouch):
        aftertouch.pc = self.id
        self.aftertouches.append(aftertouch)

    def add_info(self, msg: mido.Message, time):
        if msg.type == 'note_on' and msg.velocity > 0:
            self.add_note(note(msg.note, time))
            self.active_note = msg.note
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            if self.active_note == msg.note:
                self.active_note = -1
        elif msg.type == 'pitchwheel':
            self.add_bend(bend(msg.pitch, time))
        elif msg.type == 'channel_pressure':
            self.add_aftertouch(aftertouch(msg.pressure, time))
        elif msg.type == 'polytouch':
            self.add_aftertouch(aftertouch(msg.value, time))

    def display(self):
        print(f"===== PC{self.id} Track{self.track} =====")
        print("=== notes ===")
        for n in self.notes:
            print(f"Note: {n.value} | Time: {n.time}")
        print("=== bends ===")
        for b in self.bends:
            print(f"Pitch: {b.value} | Time: {b.time}")
        print("=== aftertouch ===")
        for a in self.aftertouches:
                    print(f"Note: {a.value} | Time: {a.time}")