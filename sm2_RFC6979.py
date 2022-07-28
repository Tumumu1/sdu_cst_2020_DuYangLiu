import hashlib, hmac, random
from gmssl import sm2, sm3, func

q_length = 256
r_length = 256

#使用Miller rabin进行素性检测，用来生成大素数
def Miller_rabin(n):
    if n % 2 == 0:
        return 0
    t = 0
    d = n-1
    while d % 2 == 0:
        t += 1
        d //= 2
    for i in range(1, 20):
        y = 0
        a = random.randint(2, n-1)
        x = pow(int(a), int(d), int(n))
        for j in range(1, t+1):
            y = pow(int(x), 2, int(n))
            if y == 1 and x != 1 and x != n-1:
                return 0
            x = y
        if y != 1:
            return 0

    return 1

def generate_q():
    #生成大素数q
    n = random.randint(2 ** 160, 2 ** 161-1)
    while Miller_rabin(n) != 1:
        if Miller_rabin(n) == 1:
            break
        else:
            n = random.randint(2 ** 160, 2 ** 161-1)
    return n


def Integer_to_OctetString(x):
    base = 256
    minlen = 32
    code_string = ''.join([chr(x) for x in range(256)])
    result = ""
    while x > 0:
        temp = x % base
        result = code_string[temp] + result
        x //= base
    if len(result) >= minlen:
        return result
    return 'a' * (minlen - len(result)) + result

def BitString_to_Integer(string):
    #将一个blen位序列作为输入，并输出一个小于2^qlen的非负整数。
    code_string =''.join([chr(x) for x in range(256)])
    if len(string) >= q_length:
        string = string[:q_length]
    else:
        string = (q_length - len(string)) * code_string[0] + string
    result = 0
    while len(string) > 0:
        result *= 2
        result += code_string.find(string[0])
        string = string[1:]
    return result


def BitString_to_OctetString(string,q):
    #变换将一个blen位序列作为输入，并输出一个rlen位序列。
    z1 = BitString_to_Integer(string)
    z2 = z1 % q
    return Integer_to_OctetString(z2)

def generate_k(data,x,q):
    v = '\x01' * 32
    k = '\x00' * 32
    h1 = sm3.sm3_hash(func.bytes_to_list(data))
    tx = Integer_to_OctetString(x)
    th1 = BitString_to_OctetString(h1, q)
    k = hmac.new(k.encode(), (v + '\x00'+tx+th1).encode(), hashlib.sha256).digest()
    v = hmac.new(k, v.encode(), hashlib.sha256).digest()
    k = hmac.new(k, v + ('\x01' + tx + th1).encode(), hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    t_length = 0
    T = b''
    while t_length < q_length:
        v = hmac.new(k, v, hashlib.sha256).digest()
        T = T + v
        t_length = len(T)
    TT = T.decode(errors='ignore')
    K = BitString_to_Integer(TT)
    if K >= 1 & K < q:
        return K
    else:
        while K >= q:
            k = hmac.new(k, v + ('\x00' ).encode(), hashlib.sha256).digest()
            v = hmac.new(k, v, hashlib.sha256).digest()
            K = BitString_to_Integer(T.decode(errors='ignore'))
    return K

if __name__ == "__main__":
    q = generate_q()
    print("q:",q)
    private_key = 'EE6ABE628606DB2494DAE70036A2A575049E2D63037F94E0EF70432B3F9B4168'
    public_key = '7FEC58C733965777908DF7AADFCD8ADB03F3D1D2B3B228BFC51D6F2B298F83F56ED7C5D273807AF649F961488B37BC1C4BD9781170CC7C30E4C717B519250ECB'
    sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
    data = b"1111"
    k = generate_k(data, int(private_key, 16), q)
    print("k:",k)
    sign = sm2_crypt.sign(data, hex(k)[2:])
    assert sm2_crypt.verify(sign, data)



