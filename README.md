# iproute

```
Something I hope you know before go into the coding~
First, please watch or star this repo, I'll be more happy if you follow me.
Bug report, questions and discussion are welcome, you can post an issue or pull a request.
```

- iproute2 是一个 Linux 中的网络工具集，它提供了一组用于配置、监控和管理网络的命令行工具。
- iproute2 工具集基于新的网络栈实现，提供了对 TCP/IP 网络协议栈的全面支持，是继传统的 ifconfig 和 route 工具之后的下一代网络工具。
- 传统的 ifconfig 和 route 命令在与日俱增的网络需求和复杂性下逐渐显现出局限性。iproute2 工具集的引入填补了这些不足，并提供了更强大和灵活的网络管理功能。以下是一些 iproute2 的特点和背景：

1. 单一工具：传统的 ifconfig 和 route 命令拆分为多个不同的命令，例如 ip address、ip route、ip link 等，使得每个命令负责特定的功能。这种拆分提高了命令的可扩展性和灵活性。
2. 完整的网络栈支持：iproute2 提供了对 TCP/IP 网络栈的全面支持，包括 IPv4、IPv6、多路径路由、多台设备等。它能够处理复杂的网络配置和路由策略。
3. 使用新的内核机制：iproute2 工具集直接与内核网络栈中的底层机制进行交互，而不仅仅是读取和修改配置文件。这种新的交互方式提供了更高效、更准确和更可靠的网络管理。
4. 更强大的路由策略：iproute2 工具集支持高级的路由策略，例如源地址基于的路由 (Policy Routing)、网络地址转换 (Network Address Translation)、虚拟专网 (Virtual Private Networks) 等。这使得网络管理员能够根据实际需求灵活地配置和管理路由。
5. 支持网络设备的高级功能：iproute2 工具集提供了对网络设备高级功能的支持，例如虚拟局域网 (VLAN)、链路聚合 (Link Aggregation)、网络隧道 (Tunneling) 等。这些功能使得网络管理更加灵活和高效。

iproute2 工具集是一个强大的网络管理工具，为 Linux 系统提供了先进的网络配置、监控和管理功能。它广泛应用于服务器、路由器、防火墙和其他网络设备中，是网络管理员和系统工程师必备的工具之一。

```
Name         : iproute
Version      : 5.18.0
Release      : 1.1.el8_8
Architecture : src
Size         : 919 k
Source       : None
Repository   : baseos-source
Summary      : Advanced IP routing and network device configuration tools
URL          : https://kernel.org/pub/linux/utils/net/iproute2/
License      : GPLv2+ and Public Domain
Description  : The iproute package contains networking utilities (ip and rtmon, for example)
             : which are designed to use the advanced networking capabilities of the Linux
             : kernel.
```




## 相关站点

- Information: <https://wiki.linuxfoundation.org/networking/iproute2>
- Download: <http://www.kernel.org/pub/linux/utils/net/iproute2/>
- Stable version repository: <git://git.kernel.org/pub/scm/network/iproute2/iproute2.git>
- Development repository: <git://git.kernel.org/pub/scm/network/iproute2/iproute2-next.git>



## 目录

* [基本使用](docs/基本使用.md)
  * [address](docs/基本使用/address.md)
  * [route](docs/基本使用/route.md)
  * [neigh](docs/基本使用/neigh.md)
* [代码分析](docs/代码分析.md)










## 子命令


```
# ip help
Usage: ip [ OPTIONS ] OBJECT { COMMAND | help }
       ip [ -force ] -batch filename
where  OBJECT := { address | addrlabel | amt | fou | help | ila | ioam | l2tp |
                   link | macsec | maddress | monitor | mptcp | mroute | mrule |
                   neighbor | neighbour | netconf | netns | nexthop | ntable |
                   ntbl | route | rule | sr | tap | tcpmetrics |
                   token | tunnel | tuntap | vrf | xfrm }
       OPTIONS := { -V[ersion] | -s[tatistics] | -d[etails] | -r[esolve] |
                    -h[uman-readable] | -iec | -j[son] | -p[retty] |
                    -f[amily] { inet | inet6 | mpls | bridge | link } |
                    -4 | -6 | -M | -B | -0 |
                    -l[oops] { maximum-addr-flush-attempts } | -br[ief] |
                    -o[neline] | -t[imestamp] | -ts[hort] | -b[atch] [filename] |
                    -rc[vbuf] [size] | -n[etns] name | -N[umeric] | -a[ll] |
                    -c[olor]}

```

- address (ip address)：用于配置和管理网络接口的 IP 地址。可以使用该命令查看、添加、删除和修改网络接口上的 IP 地址。
- neighbor / neighbour (ip neighbor / ip neighbour)：用于管理邻居表（ARP 缓存）。可以使用该命令查看、添加、删除和修改邻居信息。
- route (ip route)：用于配置和管理路由表。可以使用该命令查看、添加、删除和修改路由信息。
- addrlabel (ip addrlabel)：用于配置和管理 IP 地址标签。IP 地址标签可用于路由策略和流量控制。
- amt (ip amt)：用于配置和管理 Automatic Multicast Tunneling (AMT) 设置。AMT 是一种用于跨越 IPv4 网络的组播隧道协议。
- fou (ip fou)：用于配置和管理 Generic Tunnel Encapsulation (GUE) 和 Generic Receive Offload (GRO) 封装设置。
- ila (ip ila)：用于配置和管理 Identifier Locator Addressing (ILA)，这是 IPv6 中的一种地址方案。
- ioam (ip ioam)：用于配置和管理 In-band OAM (Operations, Administration, and Maintenance) 设置。
- l2tp (ip l2tp)：用于配置和管理 Layer 2 Tunneling Protocol (L2TP) 设置，L2TP 是一种用于创建虚拟专用网络 (VPN) 的协议。
- link (ip link)：用于管理网络接口（网卡）。可以使用该命令显示接口信息，启用或禁用接口，设置最大传输单元（MTU）等。
- macsec (ip macsec)：用于配置和管理 MACsec (Media Access Control Security) 设置，这是一种加密以太网帧的安全协议。
- maddress (ip maddress)：用于配置和管理 Multicast 地址设置。可以使用该命令查看、添加、删除和修改组播地址。
- monitor (ip monitor)：用于监视网络接口和路由的变化。可以实时查看接口状态、路由更新等。
- mptcp (ip mptcp)：用于配置和管理 Multipath TCP (MPTCP) 设置。MPTCP 允许同时通过多个路径传输数据。
- mroute (ip mroute)：用于配置和管理 Multicast 路由设置。可以使用该命令查看、添加、删除和修改组播路由。
- mrule (ip mrule)：用于配置和管理 Multicast 路由规则。可以使用该命令查看、添加、删除和修改组播路由规则。
- netconf (ip netconf)：用于配置和管理网络参数和选项。
- netns (ip netns)：用于创建和管理网络命名空间。可以使用该命令创建和删除独立的网络环境。
- nexthop (ip nexthop)：用于配置和管理下一跳设置。可以在路由中指定下一跳地址和出口接口。
- ntable / ntbl (ip ntable / ip ntbl)：用于配置和管理 Neighbor 缓存表。可以使用该命令查看、添加、删除和修改邻居缓存表项。
- rule (ip rule)：用于配置和管理路由策略规则。可以使用该命令查看、添加、删除和修改路由策略。
- sr (ip sr)：用于配置和管理 Segment Routing (SR) 设置。SR 是一种网络编址和路由技术。
- tap (ip tap)：用于配置和管理 TAP (网络隧道接口) 设置。
- tcpmetrics (ip tcpmetrics)：用于显示 TCP 业务信息和统计数据。
- token (ip token)：用于配置和管理 IPsec Tokenized Authorization 数据包的设置。
- tunnel (ip tunnel)：用于配置和管理网络隧道设置。
- tuntap (ip tuntap)：用于配置和管理 TUN/TAP (网络隧道接口) 设置。
- vrf (ip vrf)：用于配置和管理 Virtual Routing and Forwarding (VRF) 设置。
- xfrm (ip xfrm)：用于配置和管理 IPsec 和 IPv6 的安全传输设置。











---
