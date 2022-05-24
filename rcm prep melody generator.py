# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 20:22:48 2020

@author: Tobias James
"""


from music21 import scale as sc
from music21 import note as n
from music21 import stream as s
from music21 import key
import os
import subprocess
import genanki as gn

c_major = sc.MajorScale('C')
g_major = sc.MajorScale('G')
a_minor = sc.MinorScale('A')

cRange = c_major.getPitches('C4', 'G4')
gRange = g_major.getPitches('G3', 'D4')
aRange = a_minor.getPitches('A3', 'E4')

keys = [cRange, gRange, aRange]

melodies = []

melody = s.Measure()
for i in keys:
    for n1 in i:
        for n2 in i:
            for n3 in i:
                if i == gRange:
                    melody.keySignature = key.Key('G', 'major')
                elif i == cRange:
                    melody.keySignature = key.Key('C', 'major')
                elif i == aRange:
                    melody.keySignature = key.Key('A', 'minor')
                melody.append(n.Note(i[0]))
                melody.append(n.Note(n1))
                melody.append(n.Note(n2))
                melody.append(n.Note(n3))
                melodies.append(melody)
                melody = s.Measure()
                
for i in keys:
    for n1 in i:
        for n2 in i:
            for n3 in i:
                if i == gRange:
                    melody.keySignature = key.Key('G', 'major')
                elif i == cRange:
                    melody.keySignature = key.Key('C', 'major')
                elif i == aRange:
                    melody.keySignature = key.Key('A', 'minor')
                melody.append(n.Note(i[4]))
                melody.append(n.Note(n1))
                melody.append(n.Note(n2))
                melody.append(n.Note(n3))
                melodies.append(melody)
                melody = s.Measure()



os.chdir('C:/Users/Tobias James/Documents/rcm lev1 melody')
count = 0
for i in melodies:
    count += 1
    lily = open('rcmL1m{}.ly'.format(count), 'a')
    lily.write('\\version "2.20.0" \n #(set-default-paper-size "a10landscape") \n \n { \\clef "treble_8" ')
    synth = ' -n melody.wav '
    if i.keySignature == key.Key('C', 'major'):
        lily.write('\\key c \\major ')
    elif i.keySignature == key.Key('G', 'major'):
        lily.write('\\key g \\major ')
    elif i.keySignature == key.Key('A', 'minor'):
        lily.write('\\key a \\minor ')
    for j in i[1:]:
        txt = j.nameWithOctave
        synth += ' synth 1 pl {} vol 0.5 :'.format(j.nameWithOctave)
        txt = txt.replace("2", ", ")
        txt = txt.replace("3", " ")
        txt = txt.replace("4", "\' ")
        txt = txt.replace("5", "\'\' ")
        txt = txt.lower()
        lily.write(txt)
    synth = synth[0:-1]
    lily.write('}')
    lily.close()
    subprocess.run('lilypond -fpng rcmL1m{}.ly'.format(count))
    os.remove('C:/Users/Tobias James/Documents/rcm prep melody/rcmL1m{}.ly'.format(count))
    subprocess.run('sox' + synth)
    if i.keySignature == key.Key('C', 'major'):
        final_synth = ' guitarCmajor.wav melody.wav rcmL1m{}.wav'.format(count)
    elif i.keySignature == key.Key('G', 'major'):
        final_synth = ' guitarGmajor.wav melody.wav rcmL1m{}.wav'.format(count)
    elif i.keySignature == key.Key('A', 'minor'):
        final_synth = ' guitarAminor.wav melody.wav rcmL1m{}.wav'.format(count)
    subprocess.run('sox' + final_synth)
    synth = ''
    final_synth = ''
    

my_model = gn.Model(75232843, name = 'rcm_guitar_melody_lev1', 
                    fields = [
                        {'name':'audio'},
                        {'name':'score'}
                        ], 
                    templates = [
                        {'name':'ear training',
                         'qfmt':'{{audio}}',
                         'afmt': '{{audio}}<hr id = "answer"> \n <div>{{score}}</div>'
                         }
                        ]
                    )



my_deck = gn.Deck(deck_id = 12345678, name = 'RCM Lev1 Playback')

my_package = gn.Package(my_deck)

os.chdir('C:/Users/Tobias James/Documents/rcm prep melody')

for i in range(len(melodies)):
    my_package.media_files.append('C:/Users/Tobias James/Documents/rcm lev1 melody/rcmL1m' + str(i+1) + '.wav')
    my_package.media_files.append('C:/Users/Tobias James/Documents/rcm lev1 melody/rcmL1m' + str(i+1) + '.png')
    if melodies[i].keySignature == key.Key('C', 'major'):
        ks = ['CM']
    elif melodies[i].keySignature == key.Key('G', 'major'):
        ks = ['GM']
    elif melodies[i].keySignature == key.Key('A', 'minor'):
        ks = ['am']
    my_note = gn.Note(my_model,
                      fields = [
                          '[sound:rcmL1m' + str(i+1) + '.wav]', 
                          '<img src={}>'.format('"rcmL1m' + str(i+1) + '.png"'),
        ],
        sort_field = i,
        tags = ks
        )
    
    my_deck.add_note(my_note)

my_package.write_to_file('rcm_guitar_melody_lev1.apkg')


    







