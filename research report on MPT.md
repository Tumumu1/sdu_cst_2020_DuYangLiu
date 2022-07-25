Merkle Patricia Tree简称MPT树，提供了一个基于加密学的，自校验防篡改的数据结构，采用[key,value]键值对来储存数据，在以太坊范围内，限定键值的类型只能是字符串。MPT树插入、删除、查找操作的时间复杂度均为O(log(n))，但相对于红黑树来说，MPT更好理解和编码。

MPT树结合了基数树(Radix Tree)、Merkle Tree、Patricia Tree的优点。Radix Tree的结构如下:
[i0, i1, ..., iN, value]，i0到iN要么指向一个节点，要么是NULL，value存储一个值，这是MPT树用来索引值的最基本结构。Patricia Tree解决了Radix Tree的低效和空间浪费问题。Merkle Tree解决了数据校验及防篡改问题。

在ethereum中，使用了一种特殊的十六进制前缀（hex-prefix，HP）编码，所以在字母表中就有16个字符。这其中的一个字符为一个nibble。
  
  
MPT树中的节点包括空节点、叶子节点、扩展节点和分支节点:

  1.空节点：简单的表示空，在代码中是一个空串；

  2.叶子节点（leaf），表示为[key,value]的一个键值对，其中key是key的一种特殊十六进制编码，value是value的RLP编码；

  3.扩展节点（extension），也是[key，value]的一个键值对，但是这里的value是其他节点的hash值，这个hash可以被用来查询数据库中的节点。也就是说通过hash链接到其他节点;

  4.分支节点（branch），因为MPT树中的key被编码成一种特殊的16进制的表示，再加上最后的value，所以分支节点是一个长度为17的list，前16个元素对应着key中的16个可能的十六进制字符，如果有一个[key,value]对在这个分支节点终止，最后一个元素代表一个值，即分支节点既可以搜索路径的终止也可以是路径的中间节点;
  
  MPT树中另外一个重要的概念是一个特殊的十六进制前缀(hex-prefix, HP)编码，用来对key进行编码。因为字母表是16进制的，所以每个节点可能有16个孩子。因为有两种[key,value]节点(叶节点和扩展节点)，引进一种特殊的终止符标识来标识key所对应的是值是真实的值，还是其他节点的hash。如果终止符标记被打开，那么key对应的是叶节点，对应的值是真实的value。如果终止符标记被关闭，那么值就是用于在数据块中查询对应的节点的hash。无论key奇数长度还是偶数长度，HP都可以对其进行编码。最后我们注意到一个单独的hex字符或者4bit二进制数字，即一个nibble。

  HP编码很简单。一个nibble被加到key前（下图中的prefix），对终止符的状态和奇偶性进行编码。最低位表示奇偶性，第二低位编码终止符状态。如果key是偶数长度，那么加上另外一个nibble，值为0来保持整体的偶特性。
![image](https://user-images.githubusercontent.com/105497838/180795257-f262e470-78a3-485d-94a6-e5f37e38a702.png)
如图所示:总共有2个扩展节点，2个分支节点，4个叶子节点。


其中叶子结点的键值情况为：

![image](https://user-images.githubusercontent.com/105497838/180795364-a47fe256-d40f-4fbf-ab3f-8dd2a9df5b6d.png)


节点的前缀：

![image](https://user-images.githubusercontent.com/105497838/180795410-e67977b0-5ef3-46e7-8901-87163323fdf4.png)


以太坊中树结构:
![image](https://user-images.githubusercontent.com/105497838/180797062-3e1c79d6-fc6e-400d-9848-c0196858c90d.png)
以太坊中所有的merkel树都是MPT 。在一个区块的头部（block head）中，有三颗MPT的树根。一个区块头里面，除了一些常规数据，还有三个很重要的数据就是三个梅克尔-帕特里夏树的树根，通过树根就可以访问以太坊底层数据库内的数据，stateRoot•状态树的树根，transactionRoot•交易树的树根，还有receiptsRoot•收据树的树根。

    1.State trie：世界状态树，随时更新；它存储的键值对(path, value)可以表示为(sha3(ethereumAddress), rlp(ethereumAccount) )。其中account是4个元素构成的数组：[nonce, balance, storageRoot,codeHash];


    2.·Storage trie：存储树是保存所有合约数据的地方；每个合约账户都有一个独立的存储空间;

    3.Transaction trie：每个区块都会有单独的交易树；它的路径（path）是rlp(transactionIndex)，只有在挖矿时才能确定；一旦出块，不再更改;

    4.Receipts trie：每个区块也有自己的收据树；路径也表示为rlp(transactionIndex);


以太坊数据的存储结构:
![image](https://user-images.githubusercontent.com/105497838/180797438-a3c300cd-9efd-407c-b39c-8f612d232c63.png)
上面是区块头，有个stateroot，是状态数的树根，状态树是一个世界状态，他包含了所有账户的状态的集合，所以他下面的树根据每个账户的地址hash作为key，然后存每个账户的数据。所以说如果访问一个账户，按照刚才的规则找路径，直到找到某一个叶子节点，他的叶子节点里面存的是什么呢，是账户account的内容，同时，codehash只是一个32字节的hash，他还对应到真正的code的存储空间 去，storageroot是梅克尔帕特里夏树的树根，它对应的是底层数据库中合约数据的存储位置。

MPT树的操作：

包括Get、Insert、Delete、Update，具体如下：

Get：

    1.若当前节点为叶子节点，存储的内容是数据项的内容，且搜索路径的内容与叶子节点的key一致，则表示找到该节点；反之则表示该节点在树中不存在；
    
    2.若当前节点为扩展节点，且存储的内容是哈希索引，则利用哈希索引从数据库中加载该节点，再将搜索路径作为参数，对新解析出来的节点递归地调用查找函数；
    
    3.若当前节点为扩展节点，存储的内容是另外一个节点的引用，且当前节点的key是搜索路径的前缀，则将搜索路径减去当前节点的key，将剩余的搜索路径作为参数，对其子节点递归地调用查找函数；若当前节点的key不是搜索路径的前缀，表示该节点在树中不存在；
    
    4.若当前节点为分支节点，若搜索路径为空，则返回分支节点的存储内容；反之利用搜索路径的第一个字节选择分支节点的孩子节点，将剩余的搜索路径作为参数递归地调用查找函数；
    
![image](https://user-images.githubusercontent.com/105497838/180798813-8ceab43a-a06e-453a-9088-b484c0ae169b.png)
查找过程可以由此图所示。
    
Insert：

    1.根据查找步骤，首先找到与新插入节点拥有最长相同路径前缀的节点，记为Node；

    2.若该Node为分支节点：  （1）剩余的搜索路径不为空，则将新节点作为一个叶子节点插入到对应的孩子列表中；     （2）剩余的搜索路径为空（完全匹配），则将新节点的内容存储在分支节点的第17个孩子节点项中（Value）；

    3.若该节点为叶子／扩展节点：    （1）剩余的搜索路径与当前节点的key一致，则把当前节点Val更新即可；      （2）剩余的搜索路径与当前节点的key不完全一致，则将叶子／扩展节点的孩子节点替换成分支节点，将新节点与当前节点key的共同前缀作为当前节点的key，将新节点与当前节点的孩子节点作为两个孩子插入到分支节点的孩子列表中，同时当前节点转换成了一个扩展节点（若新节点与当前节点没有共同前缀，则直接用生成的分支节点替换当前节点）；

    4.若插入成功，则将被修改节点的dirty标志置为true，hash标志置空（之前的结果已经不可能用），且将节点的诞生标记更新为现在；

![image](https://user-images.githubusercontent.com/105497838/180799707-8a8b7042-fff4-4d6e-b310-91f825d2f486.png)
上图是一次插入操作的示例。


Delete：

    1.根据3.1中描述的查找步骤，找到与需要插入的节点拥有最长相同路径前缀的节点，记为Node；

    2.若Node为叶子／扩展节点：（1）若剩余的搜索路径与node的Key完全一致，则将整个node删除；
（2）若剩余的搜索路径与node的key不匹配，则表示需要删除的节点不存于树中，删除失败；
（3）若node的key是剩余搜索路径的前缀，则对该节点的Val做递归的删除调用；

    3.若Node为分支节点：（1） 删除孩子列表中相应下标标志的节点；
（2） 删除结束，若Node的孩子个数只剩下一个，那么将分支节点替换成一个叶子／扩展节点；

    4.若删除成功，则将被修改节点的dirty标志置为true，hash标志置空（之前的结果已经不可能用），且将节点的诞生标记更新为现在；

![image](https://user-images.githubusercontent.com/105497838/180800432-8bb73201-22d0-4194-a73f-880a1a9781b2.png)
上图是一次删除操作的示例。

Update：

当用户调用Update函数时，若value不为空，则隐式地转为调用Insert；若value为空，则隐式地转为调用Delete。


reference：

1.https://blog.csdn.net/qq_40713201/article/details/124486307

2.https://blog.csdn.net/qq_35739903/article/details/116710047?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-1-116710047-blog-81476275.pc_relevant_multi_platform_whitelistv2_ad_hc&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-1-116710047-blog-81476275.pc_relevant_multi_platform_whitelistv2_ad_hc&utm_relevant_index=1

3.https://blog.csdn.net/gaowebber/article/details/79821034?spm=1001.2101.3001.6650.17&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-17-79821034-blog-90111899.pc_relevant_multi_platform_whitelistv1&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-17-79821034-blog-90111899.pc_relevant_multi_platform_whitelistv1&utm_relevant_index=24

4.https://blog.csdn.net/qq_33935254/article/details/55505472?spm=1001.2101.3001.6650.3&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-3-55505472-blog-80418923.pc_relevant_multi_platform_whitelistv3&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-3-55505472-blog-80418923.pc_relevant_multi_platform_whitelistv3&utm_relevant_index=6
