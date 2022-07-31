ECDSA:

假设Alice要给Bob发一个经过数字签名的消息，他们首先需要定义一组共同接受的椭圆曲线加密用参数，简单的，这组参数可表示为(CURVE, G, n)。

其中，CURVE表示椭圆曲线点域和几何方程；G是所有点倍积运算的基点；n是该椭圆曲线的可倍积阶数(multiplicative order)，作为一个很大的质数，n的几何意义在于，nG = 0，即点倍积nG的结果不存在，而对于小于n的任何一个正整数 m = [1，n-1]，点倍积mG都可以得到一个合理的处于该椭圆曲线上的点。

其次，Alice要创建一对钥，即一个私钥和一个公钥。

私钥来自于[1, n-1]范围内一个随机数：dA=rand(1,n-1)。

公钥来自私钥和基点的椭圆曲线点倍积：QA=dA * G。

假设Alice想要对消息m作数字签名，需要进行这些步骤：

    1.计算 e = HASH(m);
    2.计算 z，来自e的二进制形式下最左边（即最高位）L_n个bits，而L_n是上述椭圆曲线参数中的可倍积阶数n的二进制长度,注意z 可能大于n，但长度绝对不会比 n 更长;
    3.从 [1, n-1] 内，随机选择一个符合加密学随机安全性的整数k;
    4.计算一个椭圆曲线上点：(x_1,y_1)=k * G;
    5.根据r=x_1 mod n计算 r 值， 如果r == 0, 则返回步骤3重新计算;
    6.根据s=k^(-1) * (z + r * dA) mod n计算 s 值，如果 s == 0，则返回步骤3重新计算;
    7.生成的数字签名就是 (r, s)

 ps:在每次生成一个新的数字签名时，这个 k 必须每次都要更新。否则，通过上述数字签名过程中的算式相互换算，会出现安全问题。
 
 对于消息的接收方Bob来说，他除了收到数字签名文件外，还会有一份公钥。所以Bob的验证分两部分，首先验证公钥，然后验证签名文件(r, s)。
 
 验证公钥：
 
   1.公钥的坐标是有效的，不会是一个极限值空点；
   2.通过公钥的坐标验证它必须是处于该椭圆曲线上的点；
   3.要满足n * QA = O，（QA为公钥）；

验证签名：

  1.验证 r 和 s 均是处于[1, n-1]范围内的整型数,否则验证失败;
  2.计算 e = HASH(n)，HAHS()即签名生成过程步骤1中使用的哈希函数;
  3.计算 z，来自 e的最左边L_n个bits;
  4.根据w = s^(-1) mod n计算参数 w;
  5.根据u_1 = zw mod n,u_2 =rw mod n计算两个参数 u1 和 u2;
  6.计算(x1, y1)，如果(x1, y1)不是一个椭圆曲线上的点，则验证失败;
  7.如果r = x_1 mod n恒等式不成立，则验证失败;

ethereum中的ECDSA：

  1.ecdsa.PublicKey结构体通过持有一个elliptic,Curve接口的实现体，可以提供椭圆曲线的所有属性，和相关操作；PublicKey的成员（X，Y），对应于公钥QA的坐标。
  2.elliptic.Curve接口声明了椭圆曲线的相关操作方法，其中Add()方法就是椭圆曲线点倍积中的“点相加”操作，Double()就是点倍积中的“点翻倍”操作，ScalarMult()根本就是一个点倍积运算（参数k是标量），IsOnCurve()检查参数所代表的点是否在该椭圆曲线上；
  3.elliptic.CurveParams结构体实现了<Curve>接口的所有方法，另外用成员属性定义了一个具体的椭圆曲线，比如(Gx, Gy) 表示该椭圆曲线的基点，即算法理论中的G点； N 是与基点对应的可倍积阶数n；B是椭圆曲线几何方程中的参数b，注意此处ecdsa代码包中隐含的椭圆曲线方程为y^2 = x^3 - 3x + b，故只需一项参数b即可。
  4.ecdsa.PrivateKey是暴露给外部使用的主要结构体类型，它其实是算法理论中的私钥和公钥的集合。它的成员D，才真正对应于算法理论中的(标量)私钥dA。
  5.ecdsa.ecdsaSignature对应于生成的数字签名(r, s)。

以太坊中的数字签名全部采用椭圆曲线数字加密算法(ECDSA)， 它的理论基础是椭圆曲线密码学(ECC)，而ECC存在的理论基础是点倍积(point multiplication)算式 Q = dP 中的私钥 d (几乎)不可能被破译。ECC相对于基于大质数分解的RSA，在提供相同安全级别的情况下，仅需长度更短的公钥。

参考链接：

  1.https://blog.csdn.net/z1015840017/article/details/125333882?ops_request_misc=&request_id=&biz_id=102&utm_term=ecdsa%E5%9C%A8%E4%BB%A5%E5%A4%AA%E5%9D%8A%E4%B8%AD%E7%9A%84%E4%BD%BF%E7%94%A8&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~sobaiduweb~default-7-125333882.nonecase&spm=1018.2226.3001.4450
  2.https://blog.csdn.net/teaspring/article/details/77834360?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-2-77834360-blog-109252225.pc_relevant_multi_platform_whitelistv2_exp3w&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-2-77834360-blog-109252225.pc_relevant_multi_platform_whitelistv2_exp3w&utm_relevant_index=5

