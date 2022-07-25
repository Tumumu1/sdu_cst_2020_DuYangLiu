"# sdu_cst_2020_DuYangLiu"  
SM3的实现参考自国家标准文档http://c.gb688.cn/bzgk/gb/showGb?type=online&hcno=45B1A67F20F3BF339211C391E9278F5E    
及https://blog.csdn.net/weixin_43936250?type=blog

实现思路是利用random模块随机生成两个原像，分别进行SM3，截取生成哈希值的前若干比特进行比较，若相等，则攻击成功，寻找到一个碰撞；但限于笔记本电脑的算力有限以及使用的编程语言是Python，且每次运行时会由于随机数的生成有较大的时间运行差异。

以前20bit的碰撞为例：![IIY49KMA{~B`WR@0F}YCLOS](https://user-images.githubusercontent.com/105497838/179647606-44853422-7794-4c0a-a1f7-c6cf9532ad60.png)
![{BV13$Q7FFQEPR(V$1W~_@U](https://user-images.githubusercontent.com/105497838/179647663-2c71669a-c56e-4d7e-ad31-de325e1bf7fc.png)
会出现随机数不同而产生的较大差异。

关于32bit的碰撞，本次实验做了尝试，但很遗憾没能运行出32bit的碰撞。

SM3的Rho攻击思路：
  类似于Pollard Rho算法的思想一样，对于选定的消息，分别进行一次和两次的SM3运算，然后进行不断地重复，直到“套圈现象”发生，则找到了一个碰撞。
  以20bit攻击为例：
![image](https://user-images.githubusercontent.com/105497838/180598081-4b4361df-9b8b-4a36-a573-9c9dfed0ab04.png)


SM4的优化是基于上个学期与同学一起实现过的任务（可能上学期的队友也上传了，但创新创业课我们并没有组队），使用C++实现，在基本实现的基础上进行了SIMD优化。


SM4运行结果：
![image](https://user-images.githubusercontent.com/105497838/180700101-53c2b634-4c58-493f-bb4b-4dcf110c2692.png)


SM4使用simd优化后的结果图：
![image](https://user-images.githubusercontent.com/105497838/180702842-4a370ea2-94d5-4142-937f-e4185ed7ffae.png)


Merkle Tree：生成了一个十万个节点的Merkle tree。
![image](https://user-images.githubusercontent.com/105497838/180698511-b7fb6cc5-926d-4f31-8d67-3b4b1c707250.png)
