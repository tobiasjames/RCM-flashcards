# -*- coding: utf-8 -*-
"""
Created on Thu May 14 09:19:50 2020

@author: Tobias James
"""
import genanki as gn
import subprocess, os

w = 8
dh = 6
h = 4
q = 2
e = 1

alphabet = [w, dh, h, q, e] #rhyhtmic variables
measure = [] #measuresure
measures = [] #list of measuresures

def enum(alphabet, measure, measures, meter):
    def complete(measure):
        return sum(measure) == meter
    
    def incomplete(measure):
        return sum(measure) < meter
    
    def onesOk(measure):
        #return True
        ones = 0
        for letter in measure:
            if letter == 1:
                ones += 1
            elif ones % 2 == 1:  # got odd number of 1s before this non-1
                return False
            else:
                ones = 0
                
        return True
                
            
    for letter in alphabet:   #loops thru rhythmic alphabet
        measure.append( letter )    # append letter and test if ok

        if complete(measure): # measure complete so ... 
            if onesOk(measure): # append only measures with even 1s
                measures.append(measure.copy())
             
        elif incomplete(measure):   # measure still has room for more so ...
            enum(alphabet, measure, measures, meter)
                

        measure.pop(len(measure) - 1)

# generate all our measures
enum(alphabet, measure, measures, 8)
measure = []
enum(alphabet, measure, measures, 6)


######################## generate audio ###################################################3
os.chdir('C:/Users/Tobias James/Documents/rcm prep rhythm')
s = 0
for i in measures: #creates synthesized wav with SoX
    s += 1
    sox = 'sox -n rhythm.wav '
    if sum(i) == 8:
        sox2 = 'sox commontime.wav rhythm.wav rcmPr{}.wav'.format(str(s))
    else:
        sox2 = 'sox threefourtime.wav rhythm.wav rcmPr{}.wav'.format(str(s))
    for j in i:
        sox += ' synth {} pl C :'.format(str(j/2))
    sox = sox[:-1]
    sox += ''
    f = subprocess.run(sox)
    f = subprocess.run(sox2)
    
    
    

################################### generate score #############################################

s = 0
lilyDict = {'1':'8', '2':'4', '4':'2', '6':'2.', '8':'1'}

for i in measures:
    s += 1
    if sum(i) == 6:
        ly = '\\version \"2.20.0\" \n #(set-default-paper-size "a8") \n { \\time 3/4'
    else:
        ly = '\\version \"2.20.0\" \n #(set-default-paper-size "a8") \n {'
    for j in i:
        ly += " c\'{} ".format(lilyDict[str(j)])
    ly += '}'
    f = open('rcmPr{}.ly'.format(str(s)), 'w')
    f.write(ly)
    f.close()
    subprocess.run('lilypond -fpng rcmPr{}.ly'.format(str(s)))
    os.remove('C:/Users/Tobias James/Documents/rcm prep rhythm/rcmPr{}.ly'.format(str(s)))
        
################################## add anki notes ###########################################


my_model = gn.Model(75232843, name = 'rcm_guitar_rhythm_prep', 
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



my_deck = gn.Deck(deck_id = 12345678, name = 'RCM Prep Clapback')

my_package = gn.Package(my_deck)

os.chdir('C:/Users/Tobias James/Documents/rcm prep rhythm')

for n in range(len(measures)):
    my_package.media_files.append('C:/Users/Tobias James/Documents/rcm prep rhythm/rcmPr' + str(n+1) + '.wav')
    my_package.media_files.append('C:/Users/Tobias James/Documents/rcm prep rhythm/rcmPr' + str(n+1) + '.png')
    my_note = gn.Note(my_model,
                      fields = [
                          '[sound:rcmPr' + str(n+1) + '.wav]', 
                          '<img src={}>'.format('"rcmPr' + str(n+1) + '.png"'),
        ],
        sort_field = n
        )
    
    my_deck.add_note(my_note)

my_package.write_to_file('rcm_guitar_rhythm_prep.apkg')




