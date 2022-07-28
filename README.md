"# sdu_cst_2020_DuYangLiu"  

小组成员：杜杨柳，2020级网安3班，GitHub名称Tumumu1

所完成的项目（未组队，完成人仅杜杨柳）：

    1.SM3的实现；
    2.SM3的生日攻击（可以实现到24bit与28bit，32bit未碰撞成功）；
    3.SM3的rho攻击（可以碰撞到28bit，但32bit未碰撞成功）；
    4.SM4的实现；
    5.SM4的simd优化（这个是基于上学期的一门课小组所做过的实验，或许当时的队友也在创新创业课上传了，在此备注）；
    6.生成一个包含十万个节点的Merkle Tree（但是未结合RFC6962,只是正常构造的Merkle Tree）；
    7.SHA256的长度扩展攻击；
    8.完成了 research report on MPT的project；
    9.完成结合RFC6979实现sm2；
未完成的项目：

    1.Project : Find a key with hash value "sdu _ cst_20220610”under a message composed ofyour name folowed by your student ID . Forexample ," San Zhan 202000460001”.
    2.Project : Find a 64-byte message under somek fulfilling that their hash value is symmetrical .
    3.*Project:send a tx on Bitcoin testnet,andparse the tx data down to everybit,betterwrite script yourself
    4.*Project:forge a signature to pretend that youare Satoshi
    5.*Project:report on the application of thisdeduce technique in Ethereum with ECDSA
    6.*Project:verify the above pit falls withproof-of-concept code
    7.*Project:lmplement the above ECMH schemeDecrypt
    8.*Project:Implement a PGP scheme with SM2
    9.*Project:implement sm2 2P sign with realnetwork communication
    10.*Project:implement sm2 2P decrypt with realnetwork communication
    11.*Project:do your best to optimize SM3implementation(software)
    12.*Project:Try to lmplement this-GeneralizingHash Chains
1.SM3的实现；

SM3运行结果：
![image](https://user-images.githubusercontent.com/105497838/180703965-d23dfdfd-a32e-4158-978a-8189874a90be.png)

2.SM3的生日攻击（可以实现到24bit与28bit，32bit未碰撞成功）；

以前20bit的碰撞为例：![IIY49KMA{~B`WR@0F}YCLOS](https://user-images.githubusercontent.com/105497838/179647606-44853422-7794-4c0a-a1f7-c6cf9532ad60.png)
![{BV13$Q7FFQEPR(V$1W~_@U](https://user-images.githubusercontent.com/105497838/179647663-2c71669a-c56e-4d7e-ad31-de325e1bf7fc.png)
会出现随机数不同而产生的较大差异。

3.SM3的rho攻击（可以碰撞到28bit，但32bit未碰撞成功）；

 以20bit攻击为例：
![image](https://user-images.githubusercontent.com/105497838/180598081-4b4361df-9b8b-4a36-a573-9c9dfed0ab04.png)
4.SM4的实现；

SM4运行结果：
![image](https://user-images.githubusercontent.com/105497838/180700101-53c2b634-4c58-493f-bb4b-4dcf110c2692.png)

5.SM4的simd优化（这个是基于上学期的一门课小组所做过的实验，或许当时的队友也在创新创业课上传了，在此备注）；


SM4使用simd优化后的结果图：
![image](https://user-images.githubusercontent.com/105497838/180702842-4a370ea2-94d5-4142-937f-e4185ed7ffae.png)

6.生成一个包含十万个节点的Merkle Tree；


Merkle Tree：生成了一个十万个节点的Merkle tree。
![image](https://user-images.githubusercontent.com/105497838/180698511-b7fb6cc5-926d-4f31-8d67-3b4b1c707250.png)


7.SHA256的长度扩展攻击：

（ps：SHA256的代码来自于https://github.com/keanemind/Python-SHA-256   这里只是对长度扩展攻击进行了测试）
![image](https://user-images.githubusercontent.com/105497838/180724999-9b0b50a5-bc5f-492a-9b52-d1617006dcdb.png)

8.通过查阅资料，学习了以下MPT，完成了 research report on MPT的project。

（在仓里的md文件）


9.完成结合RFC6979实现sm2：

![image](https://user-images.githubusercontent.com/105497838/181406316-e73be5e9-8c48-45af-8e30-bf7ef115fe63.png)
