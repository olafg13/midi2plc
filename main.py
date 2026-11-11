### BIBLIOTEKI
import mido
from mido import Message, MidiFile, MidiTrack
from pathlib import Path

### PLIKI
from pc import note, bend, aftertouch, PC

### STAŁE
DEBUG = 1

### SETUP
#directory
SCRIPT_DIR = Path(__file__).resolve().parent
input_path = SCRIPT_DIR / "test.mid"
mid = mido.MidiFile(input_path)
#debug info
if DEBUG == 1:
    print(f"Długość utworu: {mid.length:.2f} s\n")
    for i, track in enumerate(mid.tracks):
        print(f"----- Track: {i} -----")
        for msg in track:
            print(msg)
    print("")

### SORT
PCs = [] # PC(track, id, info)

for track_num, track in enumerate(mid.tracks):
    # setup/track
    time = 0

    for msg in track:

        # time setup
        time = time + msg.time

        # dla komunikatu note_on
        if msg.type == 'note_on' and msg.velocity != 0:
            # PCid setup
            PCid = 0
            active_pcs = []
            for p in PCs:
                if p.track == track_num and p.active_note != -1:
                    active_pcs.append(p.id)
            active_pcs = list(set(active_pcs))
            unactive = 0
            while unactive in active_pcs:
                unactive = unactive + 1
            PCid = unactive

            pc_exists = any(p.track == track_num and p.id == PCid for p in PCs)
            if not pc_exists:
                PCs.append(PC(track_num, PCid))

            # dodanie informacji do PC
            for p in PCs:
                p: PC
                if PCid == p.id and track_num == p.track:
                    p.add_info(msg, time)
                    break

        # dla komunikatów wyłączenia nuty
        elif msg.type == "note_off" or (msg.type == 'note_on' and msg.velocity == 0):
            for p in PCs:
                if p.track == track_num and p.active_note == msg.note:
                    p.add_info(msg, time)
                    break  # POPRAWKA 2: zwalniamy tylko jeden pasujący głos PC

        # dla innych komunikatów (bend, aftertouch, itp.)
        else:
            for p in PCs:
                if p.track == track_num:
                    p.add_info(msg, time)

#debug info
if DEBUG == 1:
    for p in PCs:
        p.display()