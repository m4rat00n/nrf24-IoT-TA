from random import randint
from time import sleep
import timeit
from datetime import datetime
import json
import binascii

#mycode='''

class SpeckCipher(object):
    """Speck Block Cipher Object"""
    # valid cipher configurations stored:
    # block_size:{key_size:number_rounds}
    __valid_setups = {32: {64: 22},
                      48: {72: 22, 96: 23},
                      64: {96: 26, 128: 27},
                      96: {96: 28, 144: 29},
                      128: {128: 32, 192: 33, 256: 34}}

    __valid_modes = ['ECB', 'CTR', 'CBC', 'PCBC', 'CFB', 'OFB']

    def encrypt_round(self, x, y, k):
        """Complete One Round of Feistel Operation"""
        rs_x = ((x << (self.word_size - self.alpha_shift)) + (x >> self.alpha_shift)) & self.mod_mask

        add_sxy = (rs_x + y) & self.mod_mask

        new_x = k ^ add_sxy

        ls_y = ((y >> (self.word_size - self.beta_shift)) + (y << self.beta_shift)) & self.mod_mask

        new_y = new_x ^ ls_y

        return new_x, new_y

    def decrypt_round(self, x, y, k):
        """Complete One Round of Inverse Feistel Operation"""

        xor_xy = x ^ y

        new_y = ((xor_xy << (self.word_size - self.beta_shift)) + (xor_xy >> self.beta_shift)) & self.mod_mask

        xor_xk = x ^ k

        msub = ((xor_xk - new_y) + self.mod_mask_sub) % self.mod_mask_sub

        new_x = ((msub >> (self.word_size - self.alpha_shift)) + (msub << self.alpha_shift)) & self.mod_mask

        return new_x, new_y

    def __init__(self, key, key_size=128, block_size=128, mode='ECB', init=0, counter=0):

        # Setup block/word size
        try:
            self.possible_setups = self.__valid_setups[block_size]
            self.block_size = block_size
            self.word_size = self.block_size >> 1
        except KeyError:
            print('Invalid block size!')
            print('Please use one of the following block sizes:', [x for x in self.__valid_setups.keys()])
            raise

        # Setup Number of Rounds and Key Size
        try:
            self.rounds = self.possible_setups[key_size]
            self.key_size = key_size
        except KeyError:
            print('Invalid key size for selected block size!!')
            print('Please use one of the following key sizes:', [x for x in self.possible_setups.keys()])
            raise

        # Create Properly Sized bit mask for truncating addition and left shift outputs
        self.mod_mask = (2 ** self.word_size) - 1

        # Mod mask for modular subtraction
        self.mod_mask_sub = (2 ** self.word_size)

        # Setup Circular Shift Parameters
        if self.block_size == 32:
            self.beta_shift = 2
            self.alpha_shift = 7
        else:
            self.beta_shift = 3
            self.alpha_shift = 8

        # Parse the given iv and truncate it to the block length
        try:
            self.iv = init & ((2 ** self.block_size) - 1)
            self.iv_upper = self.iv >> self.word_size
            self.iv_lower = self.iv & self.mod_mask
        except (ValueError, TypeError):
            print('Invalid IV Value!')
            print('Please Provide IV as int')
            raise

        # Parse the given Counter and truncate it to the block length
        try:
            self.counter = counter & ((2 ** self.block_size) - 1)
        except (ValueError, TypeError):
            print('Invalid Counter Value!')
            print('Please Provide Counter as int')
            raise

        # Check Cipher Mode
        try:
            position = self.__valid_modes.index(mode)
            self.mode = self.__valid_modes[position]
        except ValueError:
            print('Invalid cipher mode!')
            print('Please use one of the following block cipher modes:', self.__valid_modes)
            raise

        # Parse the given key and truncate it to the key length
        try:
            self.key = key & ((2 ** self.key_size) - 1)
        except (ValueError, TypeError):
            print('Invalid Key Value!')
            print('Please Provide Key as int')
            raise

        # Pre-compile key schedule
        self.key_schedule = [self.key & self.mod_mask]
        l_schedule = [(self.key >> (x * self.word_size)) & self.mod_mask for x in
                      range(1, self.key_size // self.word_size)]

        for x in range(self.rounds - 1):
            new_l_k = self.encrypt_round(l_schedule[x], self.key_schedule[x], x)
            l_schedule.append(new_l_k[0])
            self.key_schedule.append(new_l_k[1])

    def encrypt(self, plaintext):
        try:
            b = (plaintext >> self.word_size) & self.mod_mask
            a = plaintext & self.mod_mask
        except TypeError:
            print('Invalid plaintext!')
            print('Please provide plaintext as int')
            raise

        if self.mode == 'ECB':
            b, a = self.encrypt_function(b, a)

        elif self.mode == 'CTR':
            true_counter = self.iv + self.counter
            d = (true_counter >> self.word_size) & self.mod_mask
            c = true_counter & self.mod_mask
            d, c = self.encrypt_function(d, c)
            b ^= d
            a ^= c
            self.counter += 1

        elif self.mode == 'CBC':
            b ^= self.iv_upper
            a ^= self.iv_lower
            b, a = self.encrypt_function(b, a)

            self.iv_upper = b
            self.iv_lower = a
            self.iv = (b << self.word_size) + a

        elif self.mode == 'PCBC':
            f, e = b, a
            b ^= self.iv_upper
            a ^= self.iv_lower
            b, a = self.encrypt_function(b, a)
            self.iv_upper = (b ^ f)
            self.iv_lower = (a ^ e)
            self.iv = (self.iv_upper << self.word_size) + self.iv_lower

        elif self.mode == 'CFB':
            d = self.iv_upper
            c = self.iv_lower
            d, c = self.encrypt_function(d, c)
            b ^= d
            a ^= c
            self.iv_upper = b
            self.iv_lower = a
            self.iv = (b << self.word_size) + a

        elif self.mode == 'OFB':
            d = self.iv_upper
            c = self.iv_lower
            d, c = self.encrypt_function(d, c)
            self.iv_upper = d
            self.iv_lower = c
            self.iv = (d << self.word_size) + c

            b ^= d
            a ^= c

        ciphertext = (b << self.word_size) + a

        return ciphertext

    def decrypt(self, ciphertext):
        try:
            b = (ciphertext >> self.word_size) & self.mod_mask
            a = ciphertext & self.mod_mask
        except TypeError:
            print('Invalid ciphertext!')
            print('Please provide plaintext as int')
            raise

        if self.mode == 'ECB':
            b, a = self.decrypt_function(b, a)

        elif self.mode == 'CTR':
            true_counter = self.iv + self.counter
            d = (true_counter >> self.word_size) & self.mod_mask
            c = true_counter & self.mod_mask
            d, c = self.encrypt_function(d, c)
            b ^= d
            a ^= c
            self.counter += 1

        elif self.mode == 'CBC':
            f, e = b, a
            b, a = self.decrypt_function(b, a)
            b ^= self.iv_upper
            a ^= self.iv_lower

            self.iv_upper = f
            self.iv_lower = e
            self.iv = (f << self.word_size) + e

        elif self.mode == 'PCBC':
            f, e = b, a

            b, a = self.decrypt_function(b, a)

            b ^= self.iv_upper
            a ^= self.iv_lower
            self.iv_upper = (b ^ f)
            self.iv_lower = (a ^ e)
            self.iv = (self.iv_upper << self.word_size) + self.iv_lower

        elif self.mode == 'CFB':
            d = self.iv_upper
            c = self.iv_lower
            self.iv_upper = b
            self.iv_lower = a
            self.iv = (b << self.word_size) + a
            d, c = self.encrypt_function(d, c)

            b ^= d
            a ^= c

        elif self.mode == 'OFB':
            d = self.iv_upper
            c = self.iv_lower
            d, c = self.encrypt_function(d, c)

            self.iv_upper = d
            self.iv_lower = c
            self.iv = (d << self.word_size) + c

            b ^= d
            a ^= c

        plaintext = (b << self.word_size) + a

        return plaintext

    def encrypt_function(self, upper_word, lower_word):

        x = upper_word
        y = lower_word

        # Run Encryption Steps For Appropriate Number of Rounds
        for k in self.key_schedule:
            rs_x = ((x << (self.word_size - self.alpha_shift)) + (x >> self.alpha_shift)) & self.mod_mask

            add_sxy = (rs_x + y) & self.mod_mask

            x = k ^ add_sxy

            ls_y = ((y >> (self.word_size - self.beta_shift)) + (y << self.beta_shift)) & self.mod_mask

            y = x ^ ls_y

        return x, y

    def decrypt_function(self, upper_word, lower_word):

        x = upper_word
        y = lower_word

        # Run Encryption Steps For Appropriate Number of Rounds
        for k in reversed(self.key_schedule):
            xor_xy = x ^ y

            y = ((xor_xy << (self.word_size - self.beta_shift)) + (xor_xy >> self.beta_shift)) & self.mod_mask

            xor_xk = x ^ k

            msub = ((xor_xk - y) + self.mod_mask_sub) % self.mod_mask_sub

            x = ((msub >> (self.word_size - self.alpha_shift)) + (msub << self.alpha_shift)) & self.mod_mask

        return x, y

    def update_iv(self, new_iv=None):
        if new_iv:
            try:
                self.iv = new_iv & ((2 ** self.block_size) - 1)
                self.iv_upper = self.iv >> self.word_size
                self.iv_lower = self.iv & self.mod_mask
            except TypeError:
                print('Invalid Initialization Vector!')
                print('Please provide IV as int')
                raise
        return self.iv

    def getBinary(word):
        return int(binascii.hexlify(word), 16)

def print_en(mess, ciphertext,block_size, key_size,date_now):
    print("Message\t\t: ",mess)
    print("Block Size\t: ", block_size)
    print("Key Size\t: ",key_size)
    print("Ciphertext\t: ", ciphertext, "\n")
    print("Length\t\t: ", len(ciphertext), "Bytes")
    print("Just published a message to topic Speck at "+ date_now, "\n")
    
def print_de(plaintext):
    print("Decrypt Message\t: ",plaintext)

    
def pencatatan(r, mess,date_now, ciphertxt, encryption_periode,block_size,key_size):
    f = open('Speck_enc.csv', 'a')
    f.write(";"+"Message ke-" + str(r+1) + ";" + str(len(mess))+";" + str(mess) + ";" +str(block_size)+ ";" + str(key_size)+ ";" + str(ciphertxt) + ";"  + str(encryption_periode)+";"  +str(date_now)+";"+  "\n")   
    
def getBinary(word):
    return int(binascii.hexlify(word), 16)

def encrypt_dt(msg,block_sizes,key_sizes,msg_sizes):    

    
    # Record the start time
    start = timeit.default_timer()

    key = 0x1FE2548B4A0D14DC7677770989767657

    #key = 0x1f1e1d1c1b1a19181716151413121110
    #key = 0x1f1e1d1c1b1a191817161514131211100f0e0d0c0b0a0908
    # key = 0x1f1e1d1c1b1a191817161514131211100f0e0d0c0b0a09080706050403020100
    key_size=key_sizes
    block_size=block_sizes
    i=0
    cipher = SpeckCipher(key, key_size, block_size, mode='ECB')
    enc2=[]


    for r in range(1):
        # Creating random integer as paintext
        start1 = timeit.default_timer()    
        
        mess =msg 
        s=msg_sizes;l=0
        split_mess = [mess[l:l+s] for l in range(0, len(mess), s)]
        mess= str(split_mess[l])

        for m in split_mess:
            # print(m)
            enc = []
            i=0
            enc = []
    
        #fragmenting the message
            if block_size==32 :
                n = 4	# every 6 characters
                split_mess = [m[i:i+n] for i in range(0, len(m), n)]
                while("" in split_mess) :
                    split_mess.remove("")
                for x in split_mess:
                    plaintext= int.from_bytes(split_mess[i].encode('utf-8'), byteorder='big', signed=False) #ubah ke decimal
                    i=i+1
                    scale = 16
                    # binary = (bin((plaintext)).replace("0b","")).zfill(64) #ubah ke binary
                    
                    # Encrypting the plaintext
                    encrypted_message = hex(cipher.encrypt(plaintext))
                    ct=(encrypted_message[2:].zfill(8))
                    enc.append(ct)
                    
                    date_now = str(datetime.now().timestamp())
                a=""
                ciphertext = a.join(enc) #ciphertext
                enc2.append(ciphertext)

            if block_size==48 :
                n = 6	# every 6 characters
                split_mess = [m[i:i+n] for i in range(0, len(m), n)]
                while("" in split_mess) :
                    split_mess.remove("")
                for x in split_mess:
                    plaintext= int.from_bytes(split_mess[i].encode('utf-8'), byteorder='big', signed=False) #ubah ke decimal
                    i=i+1
                    scale = 16
                    # binary = (bin((plaintext)).replace("0b","")).zfill(64) #ubah ke binary
                    
                    # Encrypting the plaintext
                    encrypted_message = hex(cipher.encrypt(plaintext))
                    ct=(encrypted_message[2:].zfill(12))
                    enc.append(ct)
                    
                    date_now = str(datetime.now().timestamp())
                a=""
                ciphertext = a.join(enc) #ciphertext
                enc2.append(ciphertext)

            elif block_size==64 :
                n = 8	# every 6 characters
                split_mess = [m[i:i+n] for i in range(0, len(m), n)]
                while("" in split_mess) :
                    split_mess.remove("")
                for x in split_mess:
                    plaintext= int.from_bytes(split_mess[i].encode('utf-8'), byteorder='big', signed=False) #ubah ke decimal
                    i=i+1
                    scale = 16
                    # binary = (bin((plaintext)).replace("0b","")).zfill(64) #ubah ke binary
                    
                    # Encrypting the plaintext
                    encrypted_message = hex(cipher.encrypt(plaintext))
                    ct=(encrypted_message[2:].zfill(16))
                    enc.append(ct)
                    
                    date_now = str(datetime.now().timestamp())
                a=""
                ciphertext = a.join(enc) #ciphertext
                enc2.append(ciphertext)

        b=""
        ciphertxt=b.join(enc2)
        print("cipher:"+ciphertxt)
                
    stop1 = timeit.default_timer()
    encryption_periode = stop1 - start1
    print("Waktu akumulasi : "+str(encryption_periode))
    
    # Make the data record
    pencatatan(r, mess,date_now, ciphertxt, encryption_periode,block_size,key_size) 
    print()
    print("Encrypted msg : "+ciphertxt)
    return ciphertxt

# # Record the finished time
# stop = timeit.default_timer()
# encryption_duration = stop - start
# print("Waktu Total : "+str(encryption_duration))
