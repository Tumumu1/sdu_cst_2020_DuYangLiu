MPT(Merkle Patricia Tree)树：

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
