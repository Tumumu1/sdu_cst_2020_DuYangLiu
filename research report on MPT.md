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

包括Get、Insert、Delete、Update、Commit，具体如下：

Get：
    1.若当前节点为叶子节点，存储的内容是数据项的内容，且搜索路径的内容与叶子节点的key一致，则表示找到该节点；反之则表示该节点在树中不存在；
    2.若当前节点为扩展节点，且存储的内容是哈希索引，则利用哈希索引从数据库中加载该节点，再将搜索路径作为参数，对新解析出来的节点递归地调用查找函数；
    3.若当前节点为扩展节点，存储的内容是另外一个节点的引用，且当前节点的key是搜索路径的前缀，则将搜索路径减去当前节点的key，将剩余的搜索路径作为参数，对其子节点递归地调用查找函数；若当前节点的key不是搜索路径的前缀，表示该节点在树中不存在；
    4.若当前节点为分支节点，若搜索路径为空，则返回分支节点的存储内容；反之利用搜索路径的第一个字节选择分支节点的孩子节点，将剩余的搜索路径作为参数递归地调用查找函数；
    ![image](https://user-images.githubusercontent.com/105497838/180798813-8ceab43a-a06e-453a-9088-b484c0ae169b.png)
    查找过程可以由此图所示。

