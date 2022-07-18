import time
import random


#循环左移
def rotation_left(x, num):

    num %= 32
    left = (x << num) % (2 ** 32)
    right = (x >> (32 - num)) % (2 ** 32)
    result = left ^ right
    return result

#转为二进制
def Int2Bin(x, k):

    x = str(bin(x)[2:])
    result = "0" * (k - len(x)) + x
    return result

class SM3:
    #初始化
    def __init__(self):

        self.IV = [0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600, 0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E]
        self.T = [0x79cc4519, 0x7a879d8a]
        self.maxu32 = 2 ** 32
        self.w1 = [0] * 68
        self.w2 = [0] * 64

    #布尔函数FF
    def ff(self, x, y, z, j):

        result = 0
        if j < 16:
            result = x ^ y ^ z
        elif j >= 16:
            result = (x & y) | (x & z) | (y & z)
        return result

    #布尔函数GG
    def gg(self, x, y, z, j):

        result = 0
        if j < 16:
            result = x ^ y ^ z
        elif j >= 16:
            result = (x & y) | (~x & z)
        return result

    #置换函数P
    def p(self, x, mode):
        result = 0
        # 输入参数X的长度为32bit(=1个字)
        # 输入参数mode共两种取值：0和1
        if mode == 0:
            result = x ^ rotation_left(x, 9) ^ rotation_left(x, 17)
        elif mode == 1:
            result = x ^ rotation_left(x, 15) ^ rotation_left(x, 23)
        return result

    #填充函数
    def sm3_fill(self, plain):

        length = len(plain)   # plain的长度（单位：byte）
        l = length * 8      # plain的长度（单位：bit）

        num = length // 64
        remain_byte = length % 64
        plain_remain_bin = ""
        plain_new_bytes = bytearray((num + 1) * 64)  #填充后的消息长度，单位：byte

        # 将原数据存储至plain_new_bytes中
        for i in range(length):
            plain_new_bytes[i] = plain[i]

        # remain部分以二进制字符串形式存储
        remain_bit = remain_byte * 8     #单位：bit
        for i in range(remain_byte):
            plain_remain_bin += "{:08b}".format(plain[num * 64 + i])

        k = (448 - l - 1) % 512
        while k < 0:
            # k为满足 l + k + 1 = 448 % 512 的最小非负整数
            k += 512

        plain_remain_bin += "1" + "0" * k + Int2Bin(l, 64)

        for i in range(0, 64 - remain_byte):
            str = plain_remain_bin[i * 8 + remain_bit: (i + 1) * 8 + remain_bit]
            temp = length + i
            plain_new_bytes[temp] = int(str, 2) #将2进制字符串按byte为组转换为整数
        return plain_new_bytes

    #扩展函数: 将512bit的数据plain扩展为132个字（w1共68个字，w2共64个字）
    def sm3_plain_extend(self, plain):

        for i in range(0, 16):
            self.w1[i] = int.from_bytes(plain[i * 4:(i + 1) * 4], byteorder="big")

        for i in range(16, 68):
            self.w1[i] = self.p(self.w1[i-16] ^ self.w1[i-9] ^ rotation_left(self.w1[i-3], 15), 1) ^ rotation_left(self.w1[i-13], 7) ^ self.w1[i-6]

        for i in range(64):
            self.w2[i] = self.w1[i] ^ self.w1[i+4]

    #压缩函数
    def sm3_compress(self,plain):

        self.sm3_plain_extend(plain)
        ss1 = 0

        A = self.IV[0]
        B = self.IV[1]
        C = self.IV[2]
        D = self.IV[3]
        E = self.IV[4]
        F = self.IV[5]
        G = self.IV[6]
        H = self.IV[7]

        for j in range(64):
            if j < 16:
                ss1 = rotation_left((rotation_left(A, 12) + E + rotation_left(self.T[0], j)) % self.maxu32, 7)
            elif j >= 16:
                ss1 = rotation_left((rotation_left(A, 12) + E + rotation_left(self.T[1], j)) % self.maxu32, 7)
            ss2 = ss1 ^ rotation_left(A, 12)
            tt1 = (self.ff(A, B, C, j) + D + ss2 + self.w2[j]) % self.maxu32
            tt2 = (self.gg(E, F, G, j) + H + ss1 + self.w1[j]) % self.maxu32
            D = C
            C = rotation_left(B, 9)
            B = A
            A = tt1
            H = G
            G = rotation_left(F, 19)
            F = E
            E = self.p(tt2, 0)

        self.IV[0] ^= A
        self.IV[1] ^= B
        self.IV[2] ^= C
        self.IV[3] ^= D
        self.IV[4] ^= E
        self.IV[5] ^= F
        self.IV[6] ^= G
        self.IV[7] ^= H

    #迭代函数
    def sm3_update(self, plain):

        plain_new = self.sm3_fill(plain)   # plain_new经过填充后一定是512的整数倍
        n = len(plain_new) // 64         # n是整数，n>=1

        for i in range(0, n):
            self.sm3_compress(plain_new[i * 64:(i + 1) * 64])

    def sm3_final(self):
        digest_str = ""
        for i in range(len(self.IV)):
            digest_str += hex(self.IV[i])[2:]

        return digest_str.upper()

    def hashFile(self, filename):
        with open(filename,'rb') as fp:
            contents = fp.read()
            self.sm3_update(bytearray(contents))
        return self.sm3_final()

if __name__ == "__main__":

    start = time.perf_counter()
    while True:
        h1 = str(hex(random.randint(0, 2 ** 256))[2:])
        h2 = str(hex(random.randint(0, 2 ** 256))[2:])
        plaintext1 = bytearray(h1,encoding="utf-8")
        test1=SM3()
        test1.sm3_update(plaintext1)
        cipher1 = test1.sm3_final().lower()
        plaintext2 = bytearray(h2,encoding="utf-8")
        test2 = SM3()
        test2.sm3_update(plaintext2)
        cipher2 = test2.sm3_final().lower()
        if(cipher1[0:8] == cipher2[0:8]):
            print("Attack successful!")
            break

    end = time.perf_counter()
    print("运行时间为", round(end - start), 'seconds')