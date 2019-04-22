#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
import random
from random import shuffle
from functools import partial
import time
import sys
import os

class SetCard(object):
    def __init__(self,numshapes,typeshapes,shading,color):
        self.numshapes = numshapes
        self.typeshapes = typeshapes
        self.shading = shading
        self.color = color

    def gif_file(self):
        return '{}_{}_{}_{}.gif'.format(self.numshapes,self.typeshapes,self.shading,self.color)

    def longname(self):
        return '\t\t\t{:1s}\t{:<15s}\t{:<15s}\t{:<15s}'.format(self.numshapes,self.typeshapes,self.shading,self.color)
            
    def shortname(self):
        return '{}{}{}{}'.format(self.numshapes[0],self.typeshapes[0],self.shading[0],self.color[0])

    def show(self):
        return '{} {} {} {}'.format(self.numshapes,self.typeshapes,self.shading,self.color)
               
        
class SetDeck(object):
    numshapes=['1','2','3']
    typeshapes=['oval','diamond','squiggle']
    shading=['clear','lined','solid']
    color=['red','green','purple']

    def __init__(self):
        self.cards = []
        self.build()

    def show(self):
        for card in self.cards:
            card.show()

    def build(self):
        for n in self.numshapes:
                for t in self.typeshapes:
                    for s in self.shading:
                        for c in self.color:
                            self.cards.append(SetCard(n,t,s,c))
                            
    def shuffle(self, num=1):
        num_cards=len(self.cards)
        for _ in range(num):
            # This is the fisher yates shuffle algorithm
            for i in range(num_cards-1, 0, -1):
                randi = random.randint(0, i)
                if i == randi:
                    continue
                self.cards[i], self.cards[randi] = self.cards[randi], self.cards[i]

    def deal(self):
        return self.cards.pop()

    def return_to_deck(self, return_card):
        self.cards.append(return_card)

    def insert_in_deck(self, return_card):
        self.cards.insert(0, return_card)


def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

# compare features on 3 cards for all the same or all different
def match(card1, card2, card3):
    for s in (0,1,2,3):
        if (not((card1[s]==card2[s] and card1[s]==card3[s]) or (card1[s]!=card2[s] and card1[s]!=card3[s] and card2[s]!=card3[s]))):
            return False
    return True

class SetGame(object):
    def __init__(self):
        self.hand = []
        self.setname = []
        self.my_set = []
        self.SETS={}
        self.NumSets=0
        self.SETS_picked={}
        self.attempts=0
        self.PickList=[]
        self.MasterList=[]
        self.StartNewGame=0
        self.TotalTrys=0
        self.TotalSets=0
        self.NumErrs=0
                
    def showhand(self):
        return "{}".format(self.set_hand)
        return self

    # Draw n number of cards from a deck
    # Returns true in n cards are drawn, false if less then that
    def draw(self, deck, num=1):
        for _ in range(num):
            card = deck.deal()
            if card:
                self.hand.append(card)
            else: 
                return False
        return True

    # if no SET present in 12 cards drawn, swap out a card in our hand for a new one from the deck until we have a SET
    def swap_out_card(self):
        if len(mydeck.cards)>0:
            while (self.NumSets == 0):
                return_card=self.hand.pop(-1)
                draw_card=self.draw(mydeck,1)
                mydeck.insert_in_deck(return_card)
                #print('No SETS found, returned {} and drew {}'.format(return_card.shortname(), self.hand[-1].shortname()))
                self.findsets(self.hand)
                if self.NumSets > 0 :
                    break
        else:
            my_string=("Game Over - You cleared the deck in {:.2f} minutes".format(total_time))
            score_label=Label(display_frame,text=my_string, bg='aquamarine').grid(row=score_row+1, column=0,columnspan=4,sticky='nsew')

    # examine our hand of 12 cards for SETs and populate the SETS dictionary with them
    def findsets(self, hand):
        self.SetNames=('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
        self.hand = hand
        self.NumSets=0
        self.SETS={}
        self.SETS_picked={}
                
        for i in list(range(12)):
            for j in list(range(12)):
                if (j==i):
                    next
                else:
                    for k in list(range(12)):
                        if (k==j or k==i):
                            next
                        else:
                            card1=self.hand[i].shortname()
                            card2=self.hand[j].shortname()
                            card3=self.hand[k].shortname()
                            if match(card1,card2,card3):
                                GROUP=[ card1,card2,card3 ]
                                GROUP.sort()
                                NEWSET={self.SetNames[self.NumSets] : GROUP}
                                if (GROUP not in self.SETS.values()):
                                    self.SETS.update(NEWSET)
                                    self.NumSets=self.NumSets+1
                                        
    def paint_screen(self, hand):
        self.image_ref=[]
        self.image_count=0
        self.Button_Dict={}

        for r in range(3):
            Grid.rowconfigure(display_frame,r, weight=2)
            for c in range(4):
                Grid.columnconfigure(display_frame, c, weight=2)
                display_card=self.hand[self.image_count]
                img=PhotoImage(file=str(display_card.gif_file()))
                self.image_ref.append(img)
                callback_with_arg=partial(mygame.pickcard, display_card.shortname())
                my_button=Button(display_frame, image=img, relief=RAISED, bd=5, command=callback_with_arg)
                my_button.grid(row=r, column=c,sticky='nsew')
                button_name=display_card.shortname()
                NEW_BUTTON={ button_name : my_button }
                self.Button_Dict.update(NEW_BUTTON)
                self.image_count+=1
                
        Grid.rowconfigure(display_frame,score_row, weight=1)
        Grid.columnconfigure(display_frame,0,weight=1)

        score_info=('SETS: {}'.format(self.NumSets))
        score_lblc1=Label(display_frame,text=score_info).grid(row=score_row,column=0,sticky="nsew")

        score_infoc0=('SETS: {}'.format(self.NumSets))
        score_lblc0=Label(display_frame,text=score_infoc0).grid(row=score_row,column=0, sticky="nsew")
        score_infoc1=('Total SETS Found: {}'.format(self.TotalSets))
        score_lblc1=Label(display_frame,text=score_infoc1).grid(row=score_row,column=1, sticky="nsew")
        score_infoc2=('Hints/Misses: {}'.format(self.NumErrs))
        score_lblc2=Label(display_frame,text=score_infoc2).grid(row=score_row,column=2, sticky="nsew")

    # callback for button pressed (card selected). We stack three of them, then call the check_this_set() method.
    # we use the Button 'relief' attribute as a selection toggle - unfortunately, this doesn't display correctly on Mac
    def pickcard(self,card_shortname):
        self.card_shortname=card_shortname
        if mygame.Button_Dict[self.card_shortname].cget('relief') == 'raised':
            mygame.Button_Dict[self.card_shortname].config(relief='sunken')
            if (len(self.my_set)<3):
                self.my_set.append(card_shortname)
        else:
            mygame.Button_Dict[self.card_shortname].config(relief='raised')
            self.my_set.pop(-1)

        if (len(self.my_set)==3):
            self.check_this_set(self.my_set)

    def restore_relief(self):
        for button in mygame.Button_Dict.values():
            button.config(bg='white')
        self.paint_screen(self.hand)

          
    def show_hint(self, found_set):
        self.NumErrs+=1
        self.found_set = found_set
       
        for cards in sorted(self.SETS.values()):
            if cards in sorted(self.SETS_picked.values()):
                next
            else:
                break
            
        for card in cards:
            self.Button_Dict[card].config(bg='tomato')
            self.Button_Dict[card].after(1000, self.restore_relief)
                
               
    # check if 3 chosen cards form a SET
    def check_this_set(self, my_set):
        self.chk_set=my_set
        self.my_set=[]
        self.attempts=self.attempts+1
        self.MasterList=[]
        self.PickList=[]
        self.LabelRef=[]
        self.BadSet=[]
        global pickref
        global time_started
        global total_time

        for button in mygame.Button_Dict.values():
            button.config(relief=RAISED)

        err_label1=Label(display_frame,text='').grid(row=score_row+1, column=0, columnspan=4,sticky='nsew')
        err_label2=Label(display_frame,text='').grid(row=score_row+2, column=0, columnspan=4,sticky='nsew')
        err_label3=Label(display_frame,text='').grid(row=score_row+3, column=0, columnspan=4,sticky='nsew')
        err_label4=Label(display_frame,text='').grid(row=score_row+4, column=0, columnspan=4,sticky='nsew')
        err_label5=Label(display_frame,text='').grid(row=score_row+5, column=0, columnspan=4,sticky='nsew')


        self.TotalTrys+=1
        GRP=[self.chk_set[0],self.chk_set[1],self.chk_set[2]]
        GRP.sort()
        if (GRP in self.SETS.values()):
            PickedSet={self.SetNames[len(self.SETS_picked)] : GRP }
            if (GRP not in self.SETS_picked.values()):
                self.TotalSets+=1
                score_infoc1=('Total SETS Found: {}'.format(self.TotalSets))
                score_lblc1=Label(display_frame,text=score_infoc1).grid(row=score_row,column=1, sticky="nsew")
                self.SETS_picked.update(PickedSet)
                # draw widgets for previous SETs picked using smaller sized image files - place them to the right of our current SET hand
                if len(self.SETS_picked) > 0:
                    past_picks_row=len(self.SETS_picked)-1
                    past_picks_col=5
                for card in self.hand:
                    if card.shortname() in GRP:
                        pick_img=PhotoImage(file='./resized/'+card.gif_file())
                        pickref.append(pick_img)
                        sets_found=Label(score_frame,image=pick_img).grid(row=past_picks_row,column=past_picks_col,sticky="nw")
                        past_picks_col+=1
                self.LabelRef.append(sets_found)
            else:
                self.NumErrs+=1
                score_label=Label(display_frame, text='You already found that SET!', bg='tomato').grid(row=score_row+1,column=0,columnspan=4,sticky='nsew')
                score_infoc2=('Total Misses: {}'.format(self.NumErrs))
                score_lblc2=Label(display_frame,text=score_infoc2).grid(row=score_row,column=2, sticky="nsew")

        else:
            for card in GRP:
                for Xcard in self.hand:
                    if Xcard.shortname() == card:
                        self.BadSet.append(Xcard.longname())
               
            self.NumErrs+=1
            score_infoc2=('Total Misses: {}'.format(self.NumErrs))
            score_lblc2=Label(display_frame,text=score_infoc2).grid(row=score_row,column=2, sticky="nsew")
            err_label1=Label(display_frame,text='Sorry, these cards:', bg='tomato').grid(row=score_row+1, column=0, columnspan=4,sticky='nsew')
            err_label2=Label(display_frame,text=self.BadSet[0]).grid(row=score_row+2, column=0, columnspan=4,sticky='nw')
            err_label3=Label(display_frame,text=self.BadSet[1]).grid(row=score_row+3, column=0, columnspan=4,sticky='nw')
            err_label4=Label(display_frame,text=self.BadSet[2]).grid(row=score_row+4, column=0, columnspan=4,sticky='nw')
            err_label5=Label(display_frame,text='do NOT form a SET', bg='tomato').grid(row=score_row+5, column=0, columnspan=4,sticky='nsew')
            
        # need to compare both dictionary values for equal
        if sorted(self.SETS.values()) == sorted(self.SETS_picked.values()):
            time_finished=time.time()
            minutes_to_solve=((time_finished-time_started)/60)
            my_string=("CONGRATULATIONS - YOU SOLVED IT IN {:.2f} MINUTES".format(minutes_to_solve))
            total_time+=minutes_to_solve
            time_started=time.time()
            win_label=Label(display_frame,text=my_string,background='aquamarine').grid(row=score_row+1,column=0,columnspan=4,sticky='nsew')
            self.NextHand=[]
            self.DiscardList=[]
            
            # this is messy.. we're still in the event driven callback but we've solved for the current hand.
            # breaking this out into a separate method seems like it would require a separate callback
            
            # clear score_frame
            for pick_row in range(10):
                for pick_col in (5,6,7):
                    pick_label=Label(score_frame,text='').grid(row=pick_row,column=pick_col,sticky=NW)
                    
            # now we can discard the cards used to form sets, and draw new ones to replace
            
            # Is the game more challenging if we begin every hand with a random 12 new cards instead of
            # just replacing the ones used to form SETS?
            
            # the lines commented and replaced below accomplish that
                        
            for card in self.hand:
                for myset in self.SETS.values():
                    for mycard in myset:
                        if card.shortname() == mycard:
                            if card not in self.DiscardList:
                                self.DiscardList.append(card)

            for card in self.hand:
                if card in self.DiscardList:
                    next
                else:
                    #self.NextHand.append(card)
                    mydeck.insert_in_deck(card)

            #cards_to_draw=12-len(self.NextHand)
            cards_to_draw=12
                
            if cards_to_draw > len(mydeck.cards):
                my_string=("Game Over - You cleared the deck in {:.2f} minutes".format(total_time))
                score_label=Label(display_frame,text=my_string, bg='aquamarine').grid(row=score_row+1, column=0,columnspan=4,sticky='nsew')
            else:
                self.hand=self.NextHand
                self.draw(mydeck,cards_to_draw)
                self.findsets(self.hand)
                if self.NumSets == 0:
                    self.swap_out_card()
                init_windows()
                self.paint_screen(self.hand)
                score_infoc3=('Cards Remaining: {}'.format(len(mydeck.cards)))
                score_lblc3=Label(display_frame,text=score_infoc3).grid(row=score_row,column=3, sticky="nsew")


# paint the screen and let user pick three cards
my_window = Tk()
my_window.title('SET Solitaire')

display_frame=Frame(my_window)
score_frame=Frame(my_window,borderwidth=5, relief='groove')
help_frame=Frame(my_window,borderwidth=5, relief='groove')
pickref=[]
score_row=5

def init_windows():
    global display_frame
    display_frame.grid(row=0,column=0,sticky="nsew")
    global score_frame
    score_frame.grid(row=0,column=1,sticky="nsew")
    global help_frame
    help_frame.grid(row=1,column=1,sticky="sew")
    global pickref
    global score_row
    pick_cols=(5,6,7)
    
    for pick_row in range(10):
        for pick_col in pick_cols:
            Label(score_frame,text='').grid(row=pick_row,column=pick_col,sticky='nsew')

init_windows()        

# Instantiate cards and shuffle deck
mydeck=SetDeck()
mydeck.shuffle()

# Initialize and pick 12 cards from the deck
mygame=SetGame()
mygame.draw(mydeck,12)

mygame.findsets(mygame.hand)
if mygame.NumSets==0:
    mygame.swap_out_card()

help_txt=Label(help_frame,text="A SET consists of 3 cards in which each of the \ncard's features, looked at one-by-one, are the \nsame on each card, or, are different on each card.").grid(sticky="nsew")
hint_button=Button(help_frame, text='Need a Hint?', command=lambda: mygame.show_hint(mygame.SETS)).grid(sticky="sew")

mygame.paint_screen(mygame.hand)
time_started=time.time()
total_time=0

my_window.mainloop()
        


                





                
    
    

        
