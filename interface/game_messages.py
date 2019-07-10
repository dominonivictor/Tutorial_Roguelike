import tcod

import textwrap


class Message:
    def __init__(self, text, color=tcod.white):
        self.text = text
        self.color = color

class MessageLog:
    def __init__(self, x, width, height):
        self.msgs = []
        self.x = x
        self.width = width
        self.height = height

    def add_msg(self, msg):
        #Split msg over multi lines if necessary
        new_msg_lines = textwrap.wrap(msg.text, self. width)

        for line in new_msg_lines:
            #If buffer full, rm 1st line for a new one
            if len(self.msgs) == self.height:
                del self.msgs[0]
            #Add \n as a msg obj, w/ txt and color
            self.msgs.append(Message(line, msg.color))
