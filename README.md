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

SM3运行结果：
![image](https://user-images.githubusercontent.com/105497838/180703965-d23dfdfd-a32e-4158-978a-8189874a90be.png)

2.SM3的生日攻击；

说明：SM3的生日攻击是在实现sm3后，随机选取原像进行SM3算法，比较输出结果的前n比特，如果一致则攻击成功，但是由于random模块的不随机性以及python语言本身并不高效，可以实现到24bit与28bit，遗憾32bit未碰撞成功。

以前20bit的碰撞为例：![IIY49KMA{~B`WR@0F}YCLOS](https://user-images.githubusercontent.com/105497838/179647606-44853422-7794-4c0a-a1f7-c6cf9532ad60.png)
![{BV13$Q7FFQEPR(V$1W~_@U](https://user-images.githubusercontent.com/105497838/179647663-2c71669a-c56e-4d7e-ad31-de325e1bf7fc.png)
会出现随机数不同而产生的较大差异。

3.SM3的rho攻击；

说明：SM3的rho攻击原理参考自Pollard Rho算法，对于一个随机选取的初值，分别每次进行一次SM3操作以及两次SM3操作，直到“套圈”现象的发生，但还是局限于随机初值的选取以及python的低效，
可以碰撞到28bit，但32bit未碰撞成功。

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

结果运行图：
![image](https://user-images.githubusercontent.com/105497838/181406316-e73be5e9-8c48-45af-8e30-bf7ef115fe63.png)
