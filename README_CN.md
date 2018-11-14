# 本体去中心化数据交换机器人

[English](README.md) | 中文

<!-- TOC -->

- [1. 基于椭圆曲线的整合加密方案（ECIES）](#1-基于椭圆曲线的整合加密方案ecies)
- [2. 本体分布式身份框架 （ONT ID）](#2-本体分布式身份框架-ont-id)
- [3. 星际文件系统 （IPFS）](#3-星际文件系统-ipfs)
    - [3.1. 星际文件系统是如何工作的？](#31-星际文件系统是如何工作的)
    - [3.2. 星际文件系统 HTTP API](#32-星际文件系统-http-api)
    - [3.3. 初始化你的星际文件系统存储库](#33-初始化你的星际文件系统存储库)
    - [3.4. 创建你的私有星际文件系统网络（可选）](#34-创建你的私有星际文件系统网络可选)
    - [3.5. 运行你的星际文件系统节点](#35-运行你的星际文件系统节点)
    - [3.6. 星际文件系统客户端 API 库](#36-星际文件系统客户端-api-库)
- [4. 数据通证](#4-数据通证)
- [5. Bancor 协议](#5-bancor-协议)
    - [5.1. 简介](#51-简介)
    - [5.2. 一种价格发现的新方法](#52-一种价格发现的新方法)
- [6. 原子交换](#6-原子交换)
    - [6.1. 简介](#61-简介)
    - [原子交换流程](#原子交换流程)

<!-- /TOC -->

## 1. 基于椭圆曲线的整合加密方案（ECIES）

基于椭圆曲线的整合加密方案是一种由 Victor Shoup 在2001年提出的混合加密体系。Shoup 的提案可以在[这里](https://www.shoup.net/papers/iso-2_1.pdf)找到。

## 2. 本体分布式身份框架 （ONT ID）

本体身份数字身份标识（简称为 ONT ID）是一个建立在 W3C 数字身份标识规范基础之上的分布式身份标识协议。ONT ID 为每个实体建立了一个以密码学为基础的数字身份，实现了数据授权的自主性以及所有权的确认，这使得身份和数据成为了用户真正可以控制的资产。

如果你对 ONT ID 感兴趣，你可以在[这里](https://ontio.github.io/documentation/ontology_DID_zh.html)找到更多的信息。

<div align=center><img height="400" src="img/ontid.jpg"/></div>

## 3. 星际文件系统 （IPFS）

行星际文件系统（IPFS）是一种基于内容寻址的协议和一个点对点网络，旨在提供一种在分布式文件系统中存储和共享超媒体的方法。

<div align=center><img height="400" src="img/ipfs.jpeg"/></div>

### 3.1. 星际文件系统是如何工作的？

你也许会对星际文件系统的工作方式感兴趣。实际上，当我们向IPFS添加文件时：

- 每个文件及其中的所有块都被赋予了一个称为加密哈希的唯一指纹。
- IPFS消除了网络上的重复。
- 每个网络节点仅存储它感兴趣的内容，以及一些索引信息，帮助确定谁在存储什么。
- 查找文件时，你通过一个唯一的哈希值去请求网络查找内容存储节点。
- 使用名为IPNS的去中心化命名系统，可通过人类可读的名称找到每个文件。

### 3.2. 星际文件系统 HTTP API

当星际文件系统节点作为守护程序运行时，它会公开一个HTTP API，允许你控制节点并在命令行运行相同的命令。

在许多情况下，使用此API比在程序中直接嵌入星际文件系统更好——它允许你维护比你的应用程序更长的对等连接，并且如果你的应用程序会启动多次，你可以保持单个IPFS节点运行而不是多次。 实际上，IPFS CLI命令在联机模式下运行时会使用此API。

星际文件系统 HTTP API旨在使不同的星际文件系统实现保持相同的 HTTP API。但是，并非所有实现都同样是最新的，功能最完整（以及此规范的当前参考）是 go-ipfs。

<div align=center><img height="400" src="img/ipfsHttp.png"/></div>

### 3.3. 初始化你的星际文件系统存储库

星际文件系统将其所有设置和内部数据存储在称为存储库（repository）的目录中。 在第一次使用星际文件系统之前，您需要使用 `ipfs init` 命令初始化存储库：

```shell
PS C:\Users> ipfs init
initializing IPFS node at C:\Users\.ipfs
generating 2048-bit RSA keypair...done
peer identity: QmbhtBLaPLLUXgon7Quue1JkLjRmoQmm97cqto9JdJ4KuR
to get started, enter:

        ipfs cat /ipfs/QmS4ustL54uo8FzR9455qaxZwuMiUhyvMcX9Ba8nUH4uVv/readme
```

在 `peer identity` 之后的哈希值是你节点的ID，并且会与上面输出的值不同。网络上的其他节点使用它来查找并连接到你的节点。如果需要，您可以随时运行 `ipfs id` 以再次获取它。

### 3.4. 创建你的私有星际文件系统网络（可选）

星际文件系统的引导列表是星际文件系统守护进程与网络上的其他对等节点进行通信的节点列表。星际文件系统附带一个可信节点的默认列表，但是你可以自由修改列表以满足特定的需要。自定义引导列表的一个常用用途是创建私有星际文件系统网络。你可以通过 `bootstrap` 命令获取星际文件系统引导列表。

```shell
PS C:\Users> ipfs bootstrap
/dnsaddr/bootstrap.libp2p.io/ipfs/QmNnooDu7bfjPFoTZYxMNLWUQJyrVwtbZg5gBMjTezGAJN
/dnsaddr/bootstrap.libp2p.io/ipfs/QmQCU2EcMqAqQPR2i9bChDtGNJchTbq5TbXJJ16u19uLTa
/dnsaddr/bootstrap.libp2p.io/ipfs/QmbLHAnMoJPWSCR5Zhtx6BHJX9KiKNN6tpvbUcqanj75Nb
/dnsaddr/bootstrap.libp2p.io/ipfs/QmcZf59bWwK5XFi76CZX8cbJ4BhTzzA3gU1ZjYZcYW3dwt
/ip4/104.131.131.82/tcp/4001/ipfs/QmaCpDMGvV2BGHeYERUEnRQAwe3N8SzbUtfsmvsqQLuvuJ
/ip4/104.236.179.241/tcp/4001/ipfs/QmSoLPppuBtQSGwKDZT2M73ULpjvfd3aZ6ha4oFGL1KrGM
/ip4/104.236.76.40/tcp/4001/ipfs/QmSoLV4Bbm51jM9C4gDYZQ9Cy3U6aXMJDAbzgu2fzaDs64
/ip4/128.199.219.111/tcp/4001/ipfs/QmSoLSafTMBsPKadTEgaXctDQVcqN88CNLHXMkTNwMKPnu
/ip4/178.62.158.247/tcp/4001/ipfs/QmSoLer265NRgSp2LA3dPaeykiS1J6DifTC88f5uVQKNAd
/ip6/2400:6180:0:d0::151:6001/tcp/4001/ipfs/QmSoLSafTMBsPKadTEgaXctDQVcqN88CNLHXMkTNwMKPnu
/ip6/2604:a880:1:20::203:d001/tcp/4001/ipfs/QmSoLPppuBtQSGwKDZT2M73ULpjvfd3aZ6ha4oFGL1KrGM
/ip6/2604:a880:800:10::4a:5001/tcp/4001/ipfs/QmSoLV4Bbm51jM9C4gDYZQ9Cy3U6aXMJDAbzgu2fzaDs64
/ip6/2a03:b0c0:0:1010::23:1001/tcp/4001/ipfs/QmSoLer265NRgSp2LA3dPaeykiS1J6DifTC88f5uVQKNAd
```

**注意**：在执行此操作之前，您**必须**充分了解在文件系统节点的引导列表中添加或删除节点所可能带来的风险。

因此，如果要创建私有的星际文件系统网络，需要删除默认的可信节点，并添加你信任的节点。

```shell
PS C:\Users> ipfs bootstrap rm --all
removed /dnsaddr/bootstrap.libp2p.io/ipfs/QmNnooDu7bfjPFoTZYxMNLWUQJyrVwtbZg5gBMjTezGAJN
removed /dnsaddr/bootstrap.libp2p.io/ipfs/QmQCU2EcMqAqQPR2i9bChDtGNJchTbq5TbXJJ16u19uLTa
removed /dnsaddr/bootstrap.libp2p.io/ipfs/QmbLHAnMoJPWSCR5Zhtx6BHJX9KiKNN6tpvbUcqanj75Nb
removed /dnsaddr/bootstrap.libp2p.io/ipfs/QmcZf59bWwK5XFi76CZX8cbJ4BhTzzA3gU1ZjYZcYW3dwt
removed /ip4/104.131.131.82/tcp/4001/ipfs/QmaCpDMGvV2BGHeYERUEnRQAwe3N8SzbUtfsmvsqQLuvuJ
removed /ip4/104.236.179.241/tcp/4001/ipfs/QmSoLPppuBtQSGwKDZT2M73ULpjvfd3aZ6ha4oFGL1KrGM
removed /ip4/104.236.76.40/tcp/4001/ipfs/QmSoLV4Bbm51jM9C4gDYZQ9Cy3U6aXMJDAbzgu2fzaDs64
removed /ip4/128.199.219.111/tcp/4001/ipfs/QmSoLSafTMBsPKadTEgaXctDQVcqN88CNLHXMkTNwMKPnu
removed /ip4/178.62.158.247/tcp/4001/ipfs/QmSoLer265NRgSp2LA3dPaeykiS1J6DifTC88f5uVQKNAd
removed /ip6/2400:6180:0:d0::151:6001/tcp/4001/ipfs/QmSoLSafTMBsPKadTEgaXctDQVcqN88CNLHXMkTNwMKPnu
removed /ip6/2604:a880:1:20::203:d001/tcp/4001/ipfs/QmSoLPppuBtQSGwKDZT2M73ULpjvfd3aZ6ha4oFGL1KrGM
removed /ip6/2604:a880:800:10::4a:5001/tcp/4001/ipfs/QmSoLV4Bbm51jM9C4gDYZQ9Cy3U6aXMJDAbzgu2fzaDs64
removed /ip6/2a03:b0c0:0:1010::23:1001/tcp/4001/ipfs/QmSoLer265NRgSp2LA3dPaeykiS1J6DifTC88f5uVQKNAd
```

**提示**：当引导列表为空时，我们可以通过 `--default` 选项恢复默认的引导列表。

```shell
ipfs bootstrap add --default
```

谨慎起见，你还可以将环境变量 `LIBP2P_FORCE_PNET` 设置为 `1` 以强制使用私有网络。如果未配置私有网络，则守护进程将无法启动。

```shell
user@ubuntu:~$ export LIBP2P_FORCE_PNET=1
user@ubuntu:~$ echo $LIBP2P_FORCE_PNET
1
```

要创建私有网络，我们还需要创建一个 `swarm.key` 文件来启用星际文件系统的私有网络功能。我们需要首先创建一个名为 `swarm.key` 的密钥，星际文件系统中共享`swarm.key` 文件的节点将成为私有网络的一部分。

如果你有Go环境，可以运行以下命令来安装一个用于生成 `swarm.key` 的实用程序：

```shell
go get -u github.com/Kubuxu/go-ipfs-swarm-key-gen/ipfs-swarm-key-gen
```

安装完成后，你可以在其中的一个节点中运行它，如下所示：

```shell
ipfs-swarm-key-gen > ~/.ipfs/swarm.key
```

然后，你需要将生成的 `swarm.key` 文件复制到每个星际文件系统节点的目录下。

现在，你可以添加新的引导列表以构建你的专用网络。例如：

```shell
PS C:\Users> ipfs bootstrap add /ip4/192.168.181.141/tcp/4001/ipfs/QmYzdL2Pe3JvoqMZ1qvcVMnAWo4fVqyvw2S8XDnxHLK8MV
added /ip4/192.168.181.141/tcp/4001/ipfs/QmYzdL2Pe3JvoqMZ1qvcVMnAWo4fVqyvw2S8XDnxHLK8MV
```

### 3.5. 运行你的星际文件系统节点

在我们使用星际文件系统 HTTP API 之前，我们需要将我们的星际文件系统节点作为守护进程运行。

```shell
Initializing daemon...
Swarm is limited to private network of peers with the swarm key
Swarm key fingerprint: e06fa4c6c256f4524bc3abb4a1515556
Swarm listening on /ip4/127.0.0.1/tcp/4001
Swarm listening on /ip4/169.254.120.205/tcp/4001
Swarm listening on /ip4/169.254.28.251/tcp/4001
Swarm listening on /ip4/169.254.77.95/tcp/4001
Swarm listening on /ip4/192.168.182.1/tcp/4001
Swarm listening on /ip4/192.168.50.211/tcp/4001
Swarm listening on /ip4/192.168.56.1/tcp/4001
Swarm listening on /ip4/192.168.99.1/tcp/4001
Swarm listening on /ip6/::1/tcp/4001
Swarm listening on /p2p-circuit/ipfs/QmauvPUxzGN32aBtHXGRGCbNPxkpCA5ZFc637ABFjGe2mF
Swarm announcing /ip4/127.0.0.1/tcp/4001
Swarm announcing /ip4/169.254.120.205/tcp/4001
Swarm announcing /ip4/169.254.28.251/tcp/4001
Swarm announcing /ip4/169.254.77.95/tcp/4001
Swarm announcing /ip4/192.168.182.1/tcp/4001
Swarm announcing /ip4/192.168.3.90/tcp/49660
Swarm announcing /ip4/192.168.50.211/tcp/4001
Swarm announcing /ip4/192.168.56.1/tcp/4001
Swarm announcing /ip4/192.168.99.1/tcp/4001
Swarm announcing /ip6/::1/tcp/4001
API server listening on /ip4/127.0.0.1/tcp/5001
Gateway (readonly) server listening on /ip4/127.0.0.1/tcp/8080
Daemon is ready
```

### 3.6. 星际文件系统客户端 API 库

- [Go](https://github.com/ipfs/go-ipfs-api)
- [Python](https://github.com/ipfs/py-ipfs-api)
- [JavaScript](https://github.com/ipfs/js-ipfs)

## 4. 数据通证

数据通证（DataToken，DToken），是将现实中的任何资产或者数据映射到本体区块链的合约内数字资产。对于所要交易的数据或链外资产，需要按照本体合约资产接口规范，定义好智能合约，在链上注册，以便于链上交易。

DataToken中包括元数据MetaData，MetaData是对于资产化数据的数据结构和约束的描述。

## 5. Bancor 协议

### 5.1. 简介

通证在价值互联网中至关重要，但却还没有像信息互联网那样建立顺畅的联系。当互联网的交换节点将信息互联网连接起来的时候，价值互联网中“交换机”的角色实际上由各大交易所中活跃的交易者们所扮演着。

当前的通证交换模式有一个扬中的障碍，即需要一定的交易量来实现市场的流动性。这使得小规模通证，如社区通证、商家积分以及各种自定义通证，难以通过市场发现合理的兑换率并与主流的通证进行交换。

在去中心化数据交易应用框架（简记为DDXF）中，Bancor 协议使得基于智能合约发行的通证的价格发现和流通机制成为了可能。这些合约通证（DToken）持有 ONT 或 ONG 作为准备金。那些被持有的 ONT 和 ONG，我们统称为保证金通证。持有 DToken 的人可以通过智能合约以一个数学公式计算出的实时价格用保证金通证即时买入或卖出 DToken。

Bancor 协议的命名是为了超主权货币的凯恩斯计划致敬，该计划引入了一种名为 Bancor 的超主权准备金货币以推动形成二战后的国际货币兑付体系。

### 5.2. 一种价格发现的新方法

DToken 利用了一种基础恒定准备金率（简记为CRR）的价格发现机制。CRR由 DToken 的发行方基于 ONT 或 ONG 设定。DToken 价格通过CRR、DToken的当前供应量以及 ONT 或 ONG 的当前余额计算得出。公式如下：

<div align=center><a href="https://www.codecogs.com/eqnedit.php?latex=Price&space;=&space;\frac{Balance}{Supply&space;\times&space;CRR}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Price&space;=&space;\frac{Balance}{Supply&space;\times&space;CRR}" title="Price = \frac{Balance}{Supply \times CRR}" /></a></div>

这一价格计算方式确保了在 ONT 或 ONG 的当前余额和 DToken 的市值之间能够保持恒定的比率，即 当前供应量乘以价格。当购买DToken（以任何其储备货币）时，购买的付款将被添加到储备金余额中，并根据计算新的价格，新的 DToken 将发放买方。基于该价格公式，购买 CRR 低于100％的 DToken 都将导致其价格上涨，虽然储备余额和供应量都在增加，但供应量被乘上了一个因子。

## 6. 原子交换

### 6.1. 简介

原子交换是一种智能合约技术，可以在不使用中心化中介（如交易所）的情况下为另一种加密货币进行交换。

原子交换可以直接在不同加密货币（归属于不同的区块链）之间进行，也可以在远离主链的情况下进行链下交换。该技术在2017年9月首次被提出，当时在 Decred 和 Litecoin 之间进行了[原子交换](https://twitter.com/decredproject/status/910224860625780736)。

从那时起，其他创业公司和去中心化交易所开始允许用户使用相同的设施。例如，Lightning Labs是一家使用比特币闪电网络进行交易的初创公司，它使用该技术进行了链下交换。

在去中心化数据交易框架（DDXF）中，原子交换用来确保当且仅当数据请求者获得加密后的星际文件系统寻址地址时，数据提供方才可以从交换合约中提取 DToken。

在冻结期，数据请求方可以申请仲裁解决数据交易中发生的冲突，而仲裁者由双方在数据交易前选取。

### 原子交换流程

DDXF 原子交换是一个数据驱动模型，它确保了加密星际文件系统寻址地址与 DToken 之间交换的原子性。