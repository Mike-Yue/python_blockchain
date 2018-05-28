# noinspection PyInterpreter
import random
import hashlib
import tkinter
import sqlite3
from tkinter import *
from datetime import datetime


#Prints text in the submit_text widget to console
#Mines new block with the text in the field as the data
def print_text_field():
    print(submit_text.get(1.0, END))
    global blocknum, BlockChain
    if blocknum == 0:
        new_block = Block(submit_text.get(1.0, END) + str(datetime.now()), "0000000000000000000000000000000000000000000000000000000000000000", blocknum)
    else:
        new_block = Block(submit_text.get(1.0, END) + str(datetime.now()), BlockChain[blocknum - 1].current_Hash, blocknum)
    new_block.mine_nonce()
    BlockChain.append(new_block)
    print (new_block.blocknum, new_block.nonce, new_block.data, new_block.previous_Hash, new_block.current_Hash)
    insert_block_command = """
    INSERT INTO BlockChain (Block_Number, Nonce, Data, Previous_Hash, Current_Hash) 
    VALUES ("{num}", "{non}", "{data_value}", "{prevhash}", "{currhash}");
    """
    insert_block_command = insert_block_command.format(num = BlockChain[blocknum].blocknum, non = BlockChain[blocknum].nonce,
                                                       data_value = BlockChain[blocknum].data, prevhash = BlockChain[blocknum].previous_Hash,
                                                       currhash = BlockChain[blocknum].current_Hash)
    cursor.execute(insert_block_command)
    connection.commit()
    blocknum += 1
    submit_text.delete(1.0, END)

#Quits GUI
def quit_gui():
    top.destroy()

def print_all_blocks():
    length = len(BlockChain)
    for i in range(0, length):
        print(BlockChain[i].blocknum, BlockChain[i].nonce, BlockChain[i].data, BlockChain[i].previous_Hash,
              BlockChain[i].current_Hash)

class Block:
    def __init__(self, data, previous_Hash, blocknum):
        self.blocknum = blocknum
        self.data = data
        self.previous_Hash = previous_Hash

    def mine_nonce(self):
        self.nonce = 0
        total_string = str(self.blocknum) + str(self.nonce) + self.data + self.previous_Hash
        hash_value = hashlib.sha256(total_string.encode('utf-8')).hexdigest()
        print ("Mining nonce...Please wait")
        while hash_value[0:6] != "000000":
            self.nonce += 1
            total_string = str(self.blocknum) + str(self.nonce) + self.data + self.previous_Hash
            hash_value = hashlib.sha256(total_string.encode('utf-8')).hexdigest()

        self.current_Hash = hash_value

    def check_self(self):
        total_string = str(self.blocknum) + str(self.nonce) + self.data + self.previous_Hash
        hash_value = hashlib.sha256(total_string.encode('utf-8')).hexdigest()
        if hash_value != self.current_Hash:
            return False
        return True



connection = sqlite3.connect("blockchain_storage.db")
cursor = connection.cursor()

create_table_command = """
CREATE TABLE BlockChain (
Block_Number INTEGER,
Nonce INTEGER,
Data VARCHAR(500),
Previous_Hash VARCHAR(64),
Current_Hash VARCHAR(64));
"""
cursor.execute(create_table_command)
cursor.execute("SELECT count(*) FROM BlockChain")
blocknum = cursor.fetchone()[0]
print (blocknum)
BlockChain = []

#Fills BlockChain list with data from SQLite database
for index in range (0, blocknum):
    print (index)
    fill_table_command = """
    SELECT * from BlockChain WHERE Block_Number = "{value}";
    """
    fill_table_command = fill_table_command.format(value = index)
    cursor.execute(fill_table_command)
    retrieved_data = cursor.fetchone()
    new_block = Block(retrieved_data[2], retrieved_data[3], index)
    new_block.nonce = retrieved_data[1]
    new_block.current_Hash = retrieved_data[4]
    BlockChain.append(new_block)


#cursor.execute(create_table_command)

top = tkinter.Tk()

#Captions
caption = Label(top, text = "Enter data for the block")
caption.grid(row = 0, columnspan = 2)

#Text entries
submit_text = Text(top, bd = 5)
submit_text.grid(row = 1, rowspan = 3)

#Buttons
print_blocks_button = tkinter.Button(top, text = "Print all blocks", command = print_all_blocks)
print_blocks_button.grid(row = 1, column = 1)
submit_button = tkinter.Button(top, text = "Mine New Block", command = print_text_field)
submit_button.grid(row = 2, column = 1)
quit_button = tkinter.Button(top, text = "Exit Application", command = quit_gui)
quit_button.grid(row = 3, column = 1)
top.mainloop()



