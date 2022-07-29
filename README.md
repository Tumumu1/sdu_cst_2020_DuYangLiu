"# sdu_cst_2020_DuYangLiu"  

小组成员：杜杨柳，2020级网安3班，GitHub名称Tumumu1

所完成的项目（未组队，完成人仅杜杨柳）：

    1.SM3的实现；
    2.SM3的生日攻击（可以实现到24bit与28bit，32bit未碰撞成功）；
    3.SM3的rho攻击（可以碰撞到28bit，但32bit未碰撞成功）；
    4.SM4的实现及SM4的simd优化（这个是基于上学期的一门课小组所做过的实验，或许当时的队友也在创新创业课上传了，在此备注）；
    5.生成一个包含十万个节点的Merkle Tree（但是未结合RFC6962,只是正常构造的Merkle Tree）；
    6.SHA256的长度扩展攻击；
    7.完成了 research report on MPT的project；
    8.完成结合RFC6979实现sm2；
未完成的项目：

    1.*Project:send a tx on Bitcoin testnet,andparse the tx data down to everybit,betterwrite script yourself
    2.*Project:forge a signature to pretend that youare Satoshi
    3.*Project:verify the above pit falls withproof-of-concept code
    4.*Project:lmplement the above ECMH schemeDecrypt
    5.*Project:Implement a PGP scheme with SM2
    6.*Project:implement sm2 2P sign with realnetwork communication
    7.*Project:implement sm2 2P decrypt with realnetwork communication
    8.*Project:do your best to optimize SM3implementation(software)
    9.*Project:Try to lmplement this-GeneralizingHash Chains
1.SM3的实现；

说明：SM3的实现是参考国家标准文档，编程语言为python，在实现各个小步骤后进行测试，成功输出结果。

其中各个逻辑运算均用逻辑运算符进行的简单实现，比如：

    #布尔函数FF
        def ff(self, x, y, z, j):

            result = 0
            if j < 16:
                result = x ^ y ^ z
            elif j >= 16:
                result = (x & y) | (x & z) | (y & z)
            return result

填充函数，根据填充规则进行填充，实现时为了方便及代码简单易读所以采用字节数组进行处理：

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

SM3运行结果：
![image](https://user-images.githubusercontent.com/105497838/180703965-d23dfdfd-a32e-4158-978a-8189874a90be.png)

2.SM3的生日攻击；

说明：SM3的生日攻击是在实现sm3后，随机选取原像进行SM3算法，比较输出结果的前n比特，如果一致则攻击成功，但是由于random模块的不随机性以及python语言本身并不高效，可以实现到24bit与28bit，遗憾32bit未碰撞成功。

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

以前20bit的碰撞为例：![IIY49KMA{~B`WR@0F}YCLOS](https://user-images.githubusercontent.com/105497838/179647606-44853422-7794-4c0a-a1f7-c6cf9532ad60.png)
![{BV13$Q7FFQEPR(V$1W~_@U](https://user-images.githubusercontent.com/105497838/179647663-2c71669a-c56e-4d7e-ad31-de325e1bf7fc.png)
会出现随机数不同而产生的较大差异。

3.SM3的rho攻击；

说明：SM3的rho攻击原理参考自Pollard Rho算法，对于一个随机选取的初值，分别每次进行一次SM3操作以及两次SM3操作，直到“套圈”现象的发生，但还是局限于随机初值的选取以及python的低效，
可以碰撞到28bit，但32bit未碰撞成功。

对初始值进行初始的一次和两次SM3操作并分别存储：

    def rho_attack_init():
        #对"abc"进行一次SM3
        plaintext1 = bytearray("abc", encoding="utf-8")
        test1 = SM3()
        test1.sm3_update(plaintext1)
        cipher1 = test1.sm3_final().lower()

        #对"abc"进行两次SM3
        plaintext2_1 = bytearray("abc", encoding="utf-8")
        test2_1 = SM3()
        test2_1.sm3_update(plaintext2_1)
        cipher2_1 = test2_1.sm3_final().lower()
        plaintext2_2 = bytearray(cipher2_1, encoding="utf-8")
        test2_2 = SM3()
        test2_2.sm3_update(plaintext2_2)
        cipher2_2 = test2_2.sm3_final().lower()
        return (cipher1,cipher2_2)
        
然后进行循环测试，直到成功：

    c1,c2_2 = rho_attack_init()
        while True:
            # 对c1进行两次SM3
            plain1 = bytearray(c1, encoding="utf-8")
            t1 = SM3()
            t1.sm3_update(plain1)
            c1 = t1.sm3_final().lower()

            # 对c2进行两次SM3
            plain2_1 = bytearray(c2_2, encoding="utf-8")
            t2_1 = SM3()
            t2_1.sm3_update(plain2_1)
            c2_1 = t2_1.sm3_final().lower()
            plain2_2 = bytearray(c2_1, encoding="utf-8")
            t2_2 = SM3()
            t2_2.sm3_update(plain2_2)
            c2_2 = t2_2.sm3_final().lower()
            if(c1[0:5] == c2_2[0:5]):
                print("Attack successful!")
                break
                
 以20bit攻击为例：
![image](https://user-images.githubusercontent.com/105497838/180598081-4b4361df-9b8b-4a36-a573-9c9dfed0ab04.png)
4.SM4的实现；

说明：SM4的实现是参考自国家标准文档，编程语言为C++，同样也是实现算法的各个小步骤后进行输出测试。

SM4运行结果：
![image](https://user-images.githubusercontent.com/105497838/180700101-53c2b634-4c58-493f-bb4b-4dcf110c2692.png)

5.SM4的simd优化；

说明：SM4的simd优化在学习了simd的原理后进行优化，这个是基于上学期的一门课小组所做过的实验，或许当时的队友也在创新创业课上传了，在此备注。

SM4使用simd优化后的结果图：
![image](https://user-images.githubusercontent.com/105497838/180702842-4a370ea2-94d5-4142-937f-e4185ed7ffae.png)

6.生成一个包含十万个节点的Merkle Tree；

说明：简单实现了所需要使用的数据结构，并根据Merkle Tree的原理，结合python中哈希库使用SHA256最后生成了包含十万个节点的Merkle Tree。

选用SHA256为merkle tree的哈希算法：

     def hash(input):
            return sha256(str(input).encode('utf-8')).hexdigest()

选用列表当容器，根据所学的数据结构知识进行构造：

    def generate_tree(datablocks):
        child_nodes = []
        for datablock in datablocks:
            child_nodes.append(Node(None, MerkleTree.hash(datablock), None))
        return MerkleTree.build_tree(child_nodes)

    def build_tree(child_nodes):
        parents = []
        while len(child_nodes) != 1:
            index = 0
            length = len(child_nodes)
            while index < length:
                left_child = child_nodes[index]
                if (index + 1) < length:
                    right_child = child_nodes[index + 1]
                else:
                    right_child = Node(None, left_child.hash, None)
                parent_hash = MerkleTree.hash(left_child.hash + right_child.hash)
                parents.append(Node(left_child, parent_hash, right_child))
                index += 2
            child_nodes = parents
            parents = []
        return child_nodes[0]


Merkle Tree：生成了一个十万个节点的Merkle tree。
![image](https://user-images.githubusercontent.com/105497838/180698511-b7fb6cc5-926d-4f31-8d67-3b4b1c707250.png)


7.SHA256的长度扩展攻击：

说明：SHA256算法的代码来自于https://github.com/keanemind/Python-SHA-256   这里是在SHA256的基础上根据上学期密码学引论所学的长度扩展攻击的相关知识，对长度扩展攻击进行了测试。

SHA256的长度扩展攻击结果运行图：
![image](https://user-images.githubusercontent.com/105497838/180724999-9b0b50a5-bc5f-492a-9b52-d1617006dcdb.png)

8.通过查阅资料，学习了以下MPT，完成了 research report on MPT的project。

说明：在仓里的同名md文件。


9.完成结合RFC6979实现sm2：

说明：sm2调用的是python中的gmssl模块，根据RFC6979官方文档，将生成k的方法实现并结合到了sm2中。

首先利用Miller Rabin算法对随机选取的160bit大数进行素性检测，通过检测的“素数”才进行下一步的使用：

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

根据RFC6979官方手册实现数据类型的转换，以其中一个为例：

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
        
结果运行图：
![image](https://user-images.githubusercontent.com/105497838/181406316-e73be5e9-8c48-45af-8e30-bf7ef115fe63.png)
