import os.path
from itertools import permutations

class Armstrong_Number_Colors:
    def __init__(self, user_remark):
        self.user_remark = user_remark

        self.key = self.__generate_key__(user_remark)
        self.color = self.__generate_color__()
        self.color_map = self.__generate_color_map__()

    def __generate_color__(self):
        #First 6 digits of the key are always unique
        red_code = (self.key[0] + self.key[1] + self.key[6] + self.key[7]) %256
        green_code = (self.key[2] + self.key[3] + self.key[8] + self.key[9]) % 256
        blue_code = (self.key[4] + self.key[5] + self.key[10] + self.key[11])  % 256
        return (red_code, green_code, blue_code)
        #return (27,151,110)


    def __generate_color_map__(self):
        color_map = []
        for color_band in self.color:
            map = []
            value = color_band
            for i in range(16):
                row_of_map = []
                for j in range(16):
                    row_of_map.append(value)
                    value = (value + 1) % 256
                map.append(row_of_map)
            color_map.append(map)
        return color_map

    def __generate_key__(self, user_remark):
        try:
            #Remove duplicate characters from user_remark
            temp = ''
            for ch in user_remark:
                if ch not in temp:
                    temp += ch
            user_remark = temp

            # Find the sum of ASCII values of the characters of user_remark
            addn = 0
            for x in user_remark:
                addn += ord(x)

            # Permutations_of_digits_of_Armstrong_Numbers
            armstrong_permutations = list(permutations([1, 5, 3, 7, 0, 4], 6))

            # Use the sum as an index to select a Permutation (duplicate selection possible)
            user_permutation = armstrong_permutations[addn % len(armstrong_permutations)]

            print('permutation: ', user_permutation)

            # Use the digits of the Permutation to pick the characters of the User_Remark
            picks = []
            for x in user_permutation:
                picks.append(ord(user_remark[x]))

            # Right pad the digits of the Permutation to the picked characters
            # print(picks)
            picks.extend(user_permutation)

            # Generate a 12 bit key
            key = picks[:12]
            print('key: ', key)
            return key

        except IndexError:
            raise Exception('Too Short Key, Try with lesser number of duplicate characters')

    def encrypt(self, source_file, target_file):
        if not os.path.exists(source_file):
            raise Exception(source_file + ' doesnt exist!')

        #open the source file for reading in binary mode
        src_file_handle = open(source_file, 'rb')

        #open the target file for writing in binary mode
        trgt_file_handle = open(target_file, 'wb')

        self.index = 0 #can be derived from the key
        self.map_index = 0 #can be derived from the key
        while True:
            #1 byte of  data from source file
            abyte = src_file_handle.read(1)
            if abyte:
                abyte = int.from_bytes(abyte, 'big')
                #level1 enc. data
                bbyte = self.__level1__(abyte)
                self.index = (self.index + 1) % len(self.key)
                #level2 enc. data
                cbyte = self.__elevel2__(bbyte)
                self.map_index = (self.map_index + 1) % len(self.color_map)
                #store in target file
                cbyte = int.to_bytes(cbyte,1,'big')
                trgt_file_handle.write(cbyte)

            else:
                break #@EOF
        src_file_handle.close()
        trgt_file_handle.close()

    def __level1__(self, data):
        return data ^ self.key[self.index]

    def __elevel2__(self, data):
        # break it into two nibbles
        lower_nibble = data & 15
        upper_nibble = data >> 4
        return self.color_map[self.map_index][upper_nibble][lower_nibble]

    def __dlevel2__(self, data):
        map = self.color_map[self.map_index]
        data = (data - map[0][0] + 256) % 256
        return data

    def decrypt(self, source_file, target_file):
        if not os.path.exists(source_file):
            raise Exception(source_file + ' doesnt exist!')

        # open the  source file for reading in binary mode
        src_file_handle = open(source_file, 'rb')

        # open the  target file for writing in binary mode
        trgt_file_handle = open(target_file, 'wb')

        self.index = 0 #can be derived from the key
        self.map_index = 0 #can be derived from the key
        while True:
            # original data from source file
            cbyte = src_file_handle.read(1)
            if cbyte:
                cbyte = int.from_bytes(cbyte, 'big')
                # level2 dec. data
                bbyte = self.__dlevel2__(cbyte)
                self.map_index = (self.map_index + 1) % len(self.color_map)
                # level1 dec. data
                abyte = self.__level1__(bbyte)
                self.index = (self.index + 1) % len(self.key)
                # store in target file
                abyte = int.to_bytes(abyte, 1, 'big')
                trgt_file_handle.write(abyte)

            else:
                break
        src_file_handle.close()
        trgt_file_handle.close()

def main():
    ch = 0
    while ch !=3:
        print('1. Encrypt')
        print('2. Decrypt')
        print('3. Exit')
        print('Enter Choice')

        ch = int(input())

        if ch == 1:
            try:
                print('Enter a new Cryptography remark')
                remark = input()
                input_file = 'd:/videos/output.avi'
                output_file = 'd:/temp/e_output.avi'
                anc = Armstrong_Number_Colors(remark)
                anc.encrypt(input_file, output_file)
                print('File encrypted successfully')
            except:
                print('File encryption failed')
        elif ch == 2:
            try:
                print('Enter a encryption remark')
                remark = input()
                input_file = 'd:/temp/e_output.avi'
                output_file = 'd:/temp/output.avi'
                anc = Armstrong_Number_Colors(remark)
                anc.decrypt(input_file, output_file)
                print('File decrypted successfully')
            except:
                print('File decryption failed')
        elif ch == 3:
            break
        else:
            print('Wrong Choice')
main()
