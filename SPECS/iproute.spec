Summary:            Advanced IP routing and network device configuration tools
Name:               iproute
Version:            5.18.0
Release:            1.1%{?dist}%{?buildid}
%if 0%{?rhel}
Group:              Applications/System
%endif
URL:                https://kernel.org/pub/linux/utils/net/%{name}2/
Source0:            https://kernel.org/pub/linux/utils/net/%{name}2/%{name}2-%{version}.tar.xz
Source1:            rt_dsfield.deprecated
Patch0:             0001-Update-kernel-headers.patch
Patch1:             0002-macvlan-Add-bclim-parameter.patch

License:            GPLv2+ and Public Domain
BuildRequires:      bison
BuildRequires:      elfutils-libelf-devel
BuildRequires:      flex
BuildRequires:      gcc
BuildRequires:      iptables-devel >= 1.4.5
BuildRequires:      libbpf-devel
BuildRequires:      libcap-devel
BuildRequires:      libdb-devel
BuildRequires:      libmnl-devel
BuildRequires:      libselinux-devel
BuildRequires:      make
BuildRequires:      pkgconfig
%if ! 0%{?_module_build}
%if 0%{?fedora}
BuildRequires:      linux-atm-libs-devel
%endif
%endif
Requires:           libbpf
Requires:           psmisc
Provides:           /sbin/ip

%description
The iproute package contains networking utilities (ip and rtmon, for example)
which are designed to use the advanced networking capabilities of the Linux
kernel.

%package tc
Summary:            Linux Traffic Control utility
%if 0%{?rhel}
Group:              Applications/System
%endif
License:            GPLv2+
Requires:           %{name}%{?_isa} = %{version}-%{release}
Provides:           /sbin/tc

%description tc
The Traffic Control utility manages queueing disciplines, their classes and
attached filters and actions. It is the standard tool to configure QoS in
Linux.

%if ! 0%{?_module_build}
%package doc
Summary:            Documentation for iproute2 utilities with examples
%if 0%{?rhel}
Group:              Applications/System
%endif
License:            GPLv2+
Requires:           %{name} = %{version}-%{release}

%description doc
The iproute documentation contains howtos and examples of settings.
%endif

%package devel
Summary:            iproute development files
%if 0%{?rhel}
Group:              Development/Libraries
%endif
License:            GPLv2+
Requires:           %{name} = %{version}-%{release}
Provides:           iproute-static = %{version}-%{release}

%description devel
The libnetlink static library.

%prep
%autosetup -p1 -n %{name}2-%{version}

%build
%configure
%make_build

%install
export SBINDIR='%{_sbindir}'
export LIBDIR='%{_libdir}'
%make_install

echo '.so man8/tc-cbq.8' > %{buildroot}%{_mandir}/man8/cbq.8

# libnetlink
install -D -m644 include/libnetlink.h %{buildroot}%{_includedir}/libnetlink.h
install -D -m644 lib/libnetlink.a %{buildroot}%{_libdir}/libnetlink.a

# drop these files, iproute-doc package extracts files directly from _builddir
rm -rf '%{buildroot}%{_docdir}'

# append deprecated values to rt_dsfield for compatibility reasons
%if ! 0%{?fedora}
cat %{SOURCE1} >>%{buildroot}%{_sysconfdir}/iproute2/rt_dsfield
%endif

%files
%dir %{_sysconfdir}/iproute2
%license COPYING
%doc README README.devel
%{_mandir}/man7/*
%exclude %{_mandir}/man7/tc-*
%{_mandir}/man8/*
%exclude %{_mandir}/man8/tc*
%exclude %{_mandir}/man8/cbq*
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/iproute2/*
%{_sbindir}/*
%exclude %{_sbindir}/tc
%exclude %{_sbindir}/routel
%{_datadir}/bash-completion/completions/devlink

%files tc
%license COPYING
%{_mandir}/man7/tc-*
%{_mandir}/man8/tc*
%{_mandir}/man8/cbq*
%dir %{_libdir}/tc/
%{_libdir}/tc/*
%{_sbindir}/tc
%{_datadir}/bash-completion/completions/tc

%if ! 0%{?_module_build}
%files doc
%license COPYING
%doc examples
%endif

%files devel
%license COPYING
%{_mandir}/man3/*
%{_libdir}/libnetlink.a
%{_includedir}/libnetlink.h
%{_includedir}/iproute2/bpf_elf.h

%changelog
* Tue Jun 06 2023 Andrea Claudi <aclaudi@redhat.com> - 5.18.0-1.1.el8
- macvlan: Add bclim parameter (Andrea Claudi) [2209687]
- Update kernel headers (Andrea Claudi) [2209687]

* Wed Jun 08 2022 Wen Liang <wenliang@redhat.com> - 5.18.0-1.el8
- New version 5.18.0 [2074607]

* Mon Mar 21 2022 Andrea Claudi <aclaudi@redhat.com> - 5.15.0-4.el8
- vdpa: Update man page with added support to configure max vq pair (Andrea Claudi) [2056827]
- vdpa: Support reading device features (Andrea Claudi) [2056827]
- vdpa: Support for configuring max VQ pairs for a device (Andrea Claudi) [2056827]
- vdpa: Allow for printing negotiated features of a device (Andrea Claudi) [2056827]
- vdpa: Remove unsupported command line option (Andrea Claudi) [2056827]
- uapi: update vdpa.h (Andrea Claudi) [2056827]
- Update kernel headers and import virtio_net (Andrea Claudi) [2056827]

* Mon Feb 07 2022 Andrea Claudi <aclaudi@redhat.com> - 5.15.0-3.el8
- tc: u32: add json support in `print_raw`, `print_ipv4`, `print_ipv6` (Andrea Claudi) [1989591]
- tc: u32: add support for json output (Andrea Claudi) [1989591]

* Wed Jan 26 2022 Andrea Claudi <aclaudi@redhat.com> - 5.15.0-2.el8
- vdpa: Enable user to set mtu of the vdpa device (Andrea Claudi) [2036880]
- vdpa: Enable user to set mac address of vdpa device (Andrea Claudi) [2036880]
- vdpa: Enable user to query vdpa device config layout (Andrea Claudi) [2036880]
- vdpa: align uapi headers (Andrea Claudi) [2036880]

* Tue Nov 23 2021 Andrea Claudi <aclaudi@redhat.com> - 5.15.0-1.el8
- New version 5.15.0 (Andrea Claudi) [2016061]

* Thu Oct 07 2021 Andrea Claudi <aclaudi@redhat.com> [5.12.0-4.el8]
- lib: bpf_legacy: fix bpffs mount when /sys/fs/bpf exists (Andrea Claudi) [1995082]

* Thu Aug 12 2021 Andrea Claudi <aclaudi@redhat.com> [5.12.0-3.el8]
- tc: htb: improve burst error messages (Andrea Claudi) [1910745]
- tc: u32: Fix key folding in sample option (Andrea Claudi) [1979425]
- police: Fix normal output back to what it was (Andrea Claudi) [1981393]
- police: Add support for json output (Andrea Claudi) [1981393]
- police: add support for packet-per-second rate limiting (Andrea Claudi) [1981393]
- Update kernel headers (Andrea Claudi) [1981393]
- mptcp: add support for port based endpoint (Andrea Claudi) [1984733]

* Fri Aug 06 2021 Andrea Claudi <aclaudi@redhat.com> [5.12.0-2.el8]
- add build and run-time dependencies on libbpf (Andrea Claudi) [1990402]

* Mon Jun 28 2021 Andrea Claudi <aclaudi@redhat.com> [5.12.0-1.el8]
- tc: f_flower: Add missing ct_state flags to usage description (Andrea Claudi) [1957243]
- tc: f_flower: Add option to match on related ct state (Andrea Claudi) [1957243]

* Thu Apr 29 2021 Andrea Claudi <aclaudi@redhat.com> [5.12.0-0.el8]
- New version 5.12.0 [1939382]

* Fri Mar 12 2021 Andrea Claudi <aclaudi@redhat.com> [5.9.0-4.el8]
- iplink_bareudp: cleanup help message and man page (Andrea Claudi) [1912412]

* Tue Feb 09 2021 Andrea Claudi <aclaudi@redhat.com> [5.9.0-3.el8]
- iproute: force rtm_dst_len to 32/128 (Andrea Claudi) [1852038]

* Thu Jan 28 2021 Andrea Claudi <aclaudi@redhat.com> [5.9.0-2.el8]
- tc: flower: fix json output with mpls lse (Andrea Claudi) [1885770]
- tc-mpls: fix manpage example and help message string (Andrea Claudi) [1885770]
- tc-vlan: fix help and error message strings (Andrea Claudi) [1885770]
- m_mpls: test the 'mac_push' action after 'modify' (Andrea Claudi) [1885770]
- m_mpls: add mac_push action (Andrea Claudi) [1885770]
- m_vlan: add pop_eth and push_eth actions (Andrea Claudi) [1885770]
- Update kernel headers (Andrea Claudi) [1885770]

* Tue Nov 17 2020 Andrea Claudi <aclaudi@redhat.com> [5.9.0-1.el8]
- Rebase iproute to v5.9.0 [1896011]

* Mon Jun 29 2020 Andrea Claudi <aclaudi@redhat.com> [5.3.0-5.el8]
- man: tc-ct.8: Add manual page for ct tc action (Andrea Claudi) [1844637]
- tc: flower: Add matching on conntrack info (Andrea Claudi) [1844637]
- tc: Introduce tc ct action (Andrea Claudi) [1844637]
- tc: add NLA_F_NESTED flag to all actions options nested block (Andrea Claudi) [1844637]
- Import tc_act/tc_ct.h uapi file (Andrea Claudi) [1844637]
- ss: allow dumping kTLS info (Andrea Claudi) [1812207]
- devlink: Add health error recovery status monitoring (Andrea Claudi) [1821039]

* Fri Jun 05 2020 Andrea Claudi <aclaudi@redhat.com> [5.3.0-4.el8]
- tc: f_flower: add options support for erspan (Andrea Claudi) [1830485]
- tc: f_flower: add options support for vxlan (Andrea Claudi) [1830485]
- tc: m_tunnel_key: add options support for erpsan (Andrea Claudi) [1830485]
- tc: m_tunnel_key: add options support for vxlan (Andrea Claudi) [1830485]
- iproute_lwtunnel: add options support for erspan metadata (Andrea Claudi) [1830485]
- iproute_lwtunnel: add options support for vxlan metadata (Andrea Claudi) [1830485]
- iproute_lwtunnel: add options support for geneve metadata (Andrea Claudi) [1830485]
- Update kernel headers (Andrea Claudi) [1830485]
- man: ip.8: add reference to mptcp man-page (Andrea Claudi) [1812207]
- man: mptcp man page (Andrea Claudi) [1812207]
- ss: allow dumping MPTCP subflow information (Andrea Claudi) [1812207]
- Update kernel headers (Andrea Claudi) [1812207]
- Update kernel headers (Andrea Claudi) [1812207]
- add support for mptcp netlink interface (Andrea Claudi) [1812207]
- Update kernel headers and import mptcp.h (Andrea Claudi) [1812207]
- ip: xfrm: add espintcp encapsulation (Andrea Claudi) [1844045]
- Update kernel headers and import udp.h (Andrea Claudi) [1844045]

* Thu Apr 30 2020 Andrea Claudi <aclaudi@redhat.com> [5.3.0-3.el8]
- xfrm: also check for ipv6 state in xfrm_state_keep (Andrea Claudi) [1828033]
- man: bridge.8: fix bridge link show description (Andrea Claudi) [1817571]
- ip: fix ip route show json output for multipath nexthops (Andrea Claudi) [1738633]
- ip link: xstats: fix TX IGMP reports string (Andrea Claudi) [1796041]
- nstat: print useful error messages in abort() cases (Andrea Claudi) [1824896]

* Thu Apr 23 2020 Andrea Claudi <aclaudi@redhat.com> [5.3.0-2.el8]
- man: ip.8: Add missing vrf subcommand description (Andrea Claudi) [1780010]
- xfrm: not try to delete ipcomp states when using deleteall (Andrea Claudi) [1808634]
- ip-xfrm: Fix help messages (Andrea Claudi) [1796045]
- man: rdma.8: Add missing resource subcommand description (Andrea Claudi) [1786576]
- man: rdma-statistic: Add filter description (Andrea Claudi) [1786565]
- tc: implement support for action flags (Andrea Claudi) [1770671]
- Update kernel headers (Andrea Claudi) [1770671]
- Update kernel headers (Andrea Claudi) [1770671]

* Tue Oct 15 2019 Andrea Claudi <aclaudi@redhat.com> [5.3.0-1.el8]
- New version 5.3.0 [1752857]

* Thu Jul 04 2019 Andrea Claudi <aclaudi@redhat.com> [4.18.0-15.el8]
- netns: make netns_{save,restore} static (Andrea Claudi) [1719759]
- ip vrf: use hook to change VRF in the child (Andrea Claudi) [1719759]
- netns: switch netns in the child when executing commands (Andrea Claudi) [1719759]
- m_mirred: don't bail if the control action is missing (Andrea Claudi) [1711760]
- tc: introduce support for chain templates (Andrea Claudi) [1710291]
- ip: reset netns after each command in batch mode (Andrea Claudi) [1671016]

* Thu Jun 20 2019 Andrea Claudi <aclaudi@redhat.com> [4.18.0-14.el8]
- ss: Review ssfilter (Andrea Claudi) [1698401]

* Fri Jun 14 2019 Andrea Claudi <aclaudi@redhat.com> [4.18.0-13.el8]
- ip-xfrm: Respect family in deleteall and list commands (Andrea Claudi) [1656717]
- Update kernel headers (Andrea Claudi) [1716361]
- uapi: update bpf header (Andrea Claudi) [1716361]
- uapi: update headers to 4.20-rc1 (Andrea Claudi) [1716361]
- bpf: add btf func and func_proto kind support (Andrea Claudi) [1716361]
- lib/bpf: fix build warning if no elf (Andrea Claudi) [1716361]
- bpf: initialise map symbol before retrieving and comparing its type (Andrea Claudi) [1716361]
- Include bsd/string.h only in include/utils.h (Andrea Claudi) [1716361]
- Use libbsd for strlcpy if available (Andrea Claudi) [1716361]
- bpf: check map symbol type properly with newer llvm compiler (Andrea Claudi) [1716361]
- bpf: implement btf handling and map annotation (Andrea Claudi) [1716361]
- bpf: implement bpf to bpf calls support (Andrea Claudi) [1716361]
- bpf: remove strict dependency on af_alg (Andrea Claudi) [1716361]
- bpf: move bpf_elf_map fixup notification under verbose (Andrea Claudi) [1716361]
- iplink: add support for reporting multiple XDP programs (Andrea Claudi) [1716361]
- rdma: Document IB device renaming option (Andrea Claudi) [1663228]
- rdma: Add an option to rename IB device interface (Andrea Claudi) [1663228]
- rdma: Introduce command execution helper with required device name (Andrea Claudi) [1663228]
- rdma: Update kernel include file to support IB device renaming (Andrea Claudi) [1663228]
- libnetlink: Convert GETADDR dumps to use rtnl_addrdump_req (Andrea Claudi) [1716772]

* Wed May 29 2019 Andrea Claudi <aclaudi@redhat.com> [4.18.0-12.el8]
- devlink: Add param command support (Andrea Claudi) [1663199]
- rdma: Fix representation of PortInfo CapabilityMask (Andrea Claudi) [1664694]
- uapi: update ib_verbs (Andrea Claudi) [1664694]
- tc: flower: Add support for QinQ (Andrea Claudi) [1615928]
- ip rule: Add ipproto and port range to filter list (Andrea Claudi) [1678111]

* Thu Jan 31 2019 Phil Sutter <psutter@redhat.com> [4.18.0-11.el8]
- tc: m_tunnel_key: Add tunnel option support to act_tunnel_key (Phil Sutter) [1654761]
- tc: f_flower: add geneve option match support to flower (Phil Sutter) [1654761]
- l2tp: Fix printing of cookie and peer_cookie values (Phil Sutter) [1643805]

* Tue Dec 18 2018 Phil Sutter <psutter@redhat.com> [4.18.0-10.el8]
- iplink: fix incorrect any address handling for ip tunnels (Phil Sutter) [1626304]

* Tue Dec 11 2018 Phil Sutter <psutter@redhat.com> [4.18.0-9.el8]
- man: rdma: Add reference to rdma-resource.8 (Phil Sutter) [1610334]

* Thu Nov 29 2018 Phil Sutter <psutter@redhat.com> [4.18.0-8.el8]
- Bump release to run fresh CI tests.

* Mon Nov 26 2018 Phil Sutter <psutter@redhat.com> [4.18.0-7.el8]
- ip-route: Fix nexthop encap parsing (Phil Sutter) [1625358]
- man: ip-route.8: Document nexthop limit (Phil Sutter) [1625358]

* Thu Oct 25 2018 Phil Sutter <psutter@redhat.com> [4.18.0-6.el8]
- Update kernel headers (Phil Sutter) [1637440]
- tc_util: Add support for showing TCA_STATS_BASIC_HW statistics (Phil Sutter) [1637440]
- tc: Remove pointless assignments in batch() (Phil Sutter) [1602555]
- tipc: Drop unused variable 'genl' (Phil Sutter) [1602555]
- ip-route: Fix parse_encap_seg6() srh parsing (Phil Sutter) [1602555]
- rdma: Don't pass garbage to rd_check_is_filtered() (Phil Sutter) [1602555]
- ip-route: Fix for memleak in error path (Phil Sutter) [1602555]
- rdma: Fix for ineffective check in add_filter() (Phil Sutter) [1602555]
- devlink: Fix error reporting in cmd_resource_set() (Phil Sutter) [1602555]
- libnetlink: fix use-after-free of message buf (Phil Sutter) [1602555]
- libnetlink: don't return error on success (Phil Sutter) [1602555]
- libnetlink: fix leak and using unused memory on error (Phil Sutter) [1602555]
- tc: htb: Print default value in hex (Phil Sutter) [1641053]

* Thu Oct 18 2018 Phil Sutter <psutter@redhat.com> [4.18.0-5.el8]
- utils: fix get_rtnl_link_stats_rta stats parsing (Phil Sutter) [1626306]
- uapi: add snmp header file (Phil Sutter) [1626306]
- macsec: fix off-by-one when parsing attributes (Phil Sutter) [1628428]
- json: make 0xhex handle u64 (Phil Sutter) [1628428]

* Thu Oct 18 2018 Phil Sutter <psutter@redhat.com> [4.18.0-4.el8]
- iplink_vxlan: take into account preferred_family creating vxlan device (Phil Sutter) [1626321]
- ip-addrlabel: Fix printing of label value (Phil Sutter) [1639412]
- bridge: fdb: Fix for missing keywords in non-JSON output (Phil Sutter) [1636532]

* Wed Sep 19 2018 Phil Sutter <psutter@redhat.com> [4.18.0-3.el8]
- lib: introduce print_nl (Phil Sutter) [1625500]

* Wed Sep 19 2018 Phil Sutter <psutter@redhat.com> [4.18.0-2.el8]
- bridge/mdb: fix missing new line when show bridge mdb (Phil Sutter) [1625500]
- ip-route: Fix segfault with many nexthops (Phil Sutter) [1625358]
- Update kernel headers (Phil Sutter) [1615915]
- tc/flower: Add match on encapsulating tos/ttl (Phil Sutter) [1615915]
- tc/act_tunnel_key: Enable setup of tos and ttl (Phil Sutter) [1615915]
- iprule: Fix destination prefix output (Phil Sutter) [1623503]
- ip: Add missing -M flag to help text (Phil Sutter) [1612704]
- man: ss.8: Describe --events option (Phil Sutter) [1612704]
- rtmon: List options in help text (Phil Sutter) [1612704]
- man: rtacct.8: Fix nstat options (Phil Sutter) [1612704]
- man: ifstat.8: Document --json and --pretty options (Phil Sutter) [1612704]
- genl: Fix help text (Phil Sutter) [1612704]
- man: devlink.8: Document -verbose option (Phil Sutter) [1612704]
- devlink: trivial: Make help text consistent (Phil Sutter) [1612704]
- bridge: trivial: Make help text consistent (Phil Sutter) [1612704]
- man: bridge.8: Document -oneline option (Phil Sutter) [1612704]

* Tue Aug 14 2018 Phil Sutter - 4.18.0-1
- New version 4.18.0

* Thu Aug 09 2018 Phil Sutter <psutter@redhat.com> [4.17.0-1.el8]
- rdma: print driver resource attributes (Phil Sutter) [1610334]
- rdma: update rdma_netlink.h to get new driver attributes (Phil Sutter) [1610334]
- rdma: Print net device name and index for RDMA device (Phil Sutter) [1610334]
- devlink: CTRL_ATTR_FAMILY_ID is a u16 (Phil Sutter) [1589317]
- tc: Do not use addattr_nest_compat on mqprio and netem (Phil Sutter) [1589317]
- ipaddress: Fix and make consistent label match handling (Phil Sutter) [1589317]
- rt_dsfield: Ship deprecated values for compatibility (Phil Sutter) [1595683]
- New version 4.17.0 including upstream-suggested fixes (Phil Sutter) [1589317]

* Fri Feb 09 2018 Phil Sutter <psutter@redhat.com> - 4.15.0-1
- New version 4.15.0

* Fri Feb  9 2018 Florian Weimer <fweimer@redhat.com> - 4.14.1-6
- Use LDFLAGS defaults from redhat-rpm-config

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.14.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 11 2017 Phil Sutter <psutter@redhat.com> - 4.14.1-4
- Add missing patch files.

* Mon Dec 11 2017 Phil Sutter <psutter@redhat.com> - 4.14.1-3
- Add upstream suggested backports.
- Make use of %%autosetup macro.

* Wed Nov 15 2017 Phil Sutter <psutter@redhat.com> - 4.14.1-2
- Drop unused build dependencies

* Wed Nov 15 2017 Phil Sutter <psutter@redhat.com> - 4.14.1-1
- New version 4.14.1

* Tue Sep 19 2017 Phil Sutter <psutter@redhat.com> - 4.13.0-1
- New version 4.13.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Phil Sutter <psutter@redhat.com> - 4.12.0-1
- New version 4.12.0

* Tue May 23 2017 Phil Sutter <psutter@redhat.com> - 4.11.0-1
- Add virtual capability to tc subpackage so it's easier found
- New version 4.11.0

* Thu May 11 2017 Karsten Hopp <karsten@redhat.com> - 4.10.0-3
- don't build docs for module builds to limit dependencies

* Fri Mar 17 2017 Phil Sutter <psutter@redhat.com> - 4.10.0-2
- Add two fixes to 4.10.0 release from upstream.

* Tue Mar 14 2017 Phil Sutter <psutter@redhat.com> - 4.10.0-1
- Ship new header iproute2/bpf_elf.h
- Document content of remaining docs fixup patch in spec file
- Drop patches already applied upstream
- New version 4.10.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb  2 2017 Thomas Woerner <twoerner@redhat.com> - 4.9.0-3
- Release bump for iptables-1.6.1 (libxtables.so.12)

* Sat Jan 28 2017 Phil Sutter <psutter@redhat.com> - 4.9.0-2
- Fix for failing 'make install'

* Sat Jan 28 2017 Phil Sutter <psutter@redhat.com> - 4.9.0-1
- New version 4.9.0

* Fri Jan 13 2017 Phil Sutter <psutter@redhat.com> - 4.8.0-2
- Fix segfault in xt action

* Wed Nov 30 2016 Phil Sutter <psutter@redhat.com> - 4.8.0-1
- New version 4.8.0

* Wed Aug 10 2016 Phil Sutter <psutter@redhat.com> - 4.7.0-1
- New version 4.7.0

* Wed May 04 2016 Phil Sutter <psutter@redhat.com> - 4.6.0-1
- New version 4.6.0

* Wed Apr 13  2016 Thomas Woerner <twoerner@redhat.com> - 4.5.0-4
- Rebuild for new iptables-1.6.0 with libxtables so bump

* Fri Apr 08 2016 Phil Sutter <psutter@redhat.com> - 4.5.0-3
- Fix upgrade path by adding correct Requires/Obsoletes statements to spec file
- Move README.iproute2+tc into tc subpackage

* Fri Mar 18 2016 Phil Sutter <psutter@redhat.com> - 4.5.0-2
- Split tc into it's own subpackage

* Fri Mar 18 2016 Phil Sutter <psutter@redhat.com> - 4.5.0-1
- New version 4.5.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Phil Sutter <psutter@redhat.com> - 4.4.0-1
- New version 4.4.0

* Sun Oct 04 2015 Phil Sutter <psutter@redhat.com> - 4.2.0-4
- Simplify RPM install stage by using package's install target

* Sun Oct 04 2015 Phil Sutter <psutter@redhat.com> - 4.2.0-3
- Add missing build dependency to libmnl-devel
- Ship tipc utility

* Thu Sep 24 2015 Phil Sutter <psutter@redhat.com> - 4.2.0-2
- Add missing build dependency to libselinux-devel

* Wed Sep 02 2015 Pavel Šimerda <psimerda@redhat.com> - 4.2.0-1
- new version 4.2.0

* Tue Jul 07 2015 Pavel Šimerda <psimerda@redhat.com> - 4.1.1-1
- new version 4.1.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Pavel Šimerda <psimerda@redhat.com> - 4.0.0-3
- remove patch rejected by upstream

* Mon May 11 2015 Pavel Šimerda <psimerda@redhat.com> - 4.0.0-2
- Remove patch rejected by upstream

* Tue Apr 14 2015 Pavel Šimerda <psimerda@redhat.com> - 4.0.0-1
- new version 4.0.0

* Fri Mar 13 2015 Pavel Šimerda <psimerda@redhat.com> - 3.19.0-1
- new version 3.19.0

* Sat Oct 04 2014 Lubomir Rintel <lkundrak@v3.sk> - 3.16.0-3
- Backport fix for ip link add name regression that broke libvirt

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 05 2014 Petr Šabata <contyk@redhat.com> - 3.16.0-1
- 3.16 bump

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 3.15.0-2
- fix license handling

* Thu Jun 12 2014 Petr Šabata <contyk@redhat.com> - 3.15.0-1
- 3.15.0 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 06 2014 Petr Šabata <contyk@redhat.com> - 3.14.0-2
- Fix incorrect references in ss(8), #1092653

* Tue Apr 15 2014 Petr Šabata <contyk@redhat.com> - 3.14.0-1
- 3.14 bump
- Drop out iplink_have_newlink() fix in favor of upstream's approach

* Tue Nov 26 2013 Petr Šabata <contyk@redhat.com> - 3.12.0-2
- Drop libnl from dependencies (#1034454)

* Mon Nov 25 2013 Petr Šabata <contyk@redhat.com> - 3.12.0-1
- 3.12.0 bump

* Thu Nov 21 2013 Petr Šabata <contyk@redhat.com> - 3.11.0-2
- Fix the rtt time parsing again

* Tue Oct 22 2013 Petr Šabata <contyk@redhat.com> - 3.11.0-1
- 3.11 bump

* Tue Oct 01 2013 Petr Pisar <ppisar@redhat.com> - 3.10.0-8
- Close file with bridge monitor file (bug #1011822)

* Tue Sep 24 2013 Petr Pisar <ppisar@redhat.com> - 3.10.0-7
- Add tc -OK option
- Document "bridge mdb" and "bridge monitor mdb"

* Fri Aug 30 2013 Petr Šabata <contyk@redhat.com> - 3.10.0-6
- Fix lnstat -i properly this time

* Thu Aug 29 2013 Petr Šabata <contyk@redhat.com> - 3.10.0-5
- Fix an 'ip link' hang (#996537)

* Tue Aug 13 2013 Petr Šabata <contyk@redhat.com> - 3.10.0-4
- lnstat -i: Run indefinitely if the --count isn't specified (#977845)
- Switch to unversioned %%docdir

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Šabata <contyk@redhat.com> - 3.10.0-2
- Fix the XFRM patch

* Wed Jul 17 2013 Petr Šabata <contyk@redhat.com> - 3.10.0-1
- 3.10.0 bump
- Drop the SHAREDIR patch and revert to upstream ways (#966445)
- Fix an XFRM regression with FORTIFY_SOURCE

* Tue Apr 30 2013 Petr Šabata <contyk@redhat.com> - 3.9.0-1
- 3.9.0 bump

* Thu Apr 25 2013 Petr Šabata <contyk@redhat.com> - 3.8.0-4
- ATM is available in Fedora only

* Tue Mar 12 2013 Petr Šabata <contyk@redhat.com> - 3.8.0-3
- Mention the "up" argument in documentation and help outputs (#907468)

* Mon Mar 04 2013 Petr Šabata <contyk@redhat.com> - 3.8.0-2
- Bump for 1.4.18 rebuild

* Tue Feb 26 2013 Petr Šabata <contyk@redhat.com> - 3.8.0-1
- 3.8.0 bump

* Fri Feb 08 2013 Petr Šabata <contyk@redhat.com> - 3.7.0-2
- Don't propogate mounts out of ip (#882047)

* Wed Dec 12 2012 Petr Šabata <contyk@redhat.com> - 3.7.0-1
- 3.7.0 bump

* Mon Nov 19 2012 Petr Šabata <contyk@redhat.com> - 3.6.0-3
- Include section 7 manpages (#876857)
- Fix ancient bogus dates in the changelog (correction based upon commits)
- Explicitly require some TeX fonts no longer present in the base distribution

* Thu Oct 04 2012 Petr Šabata <contyk@redhat.com> - 3.6.0-2
- List all interfaces by default

* Wed Oct 03 2012 Petr Šabata <contyk@redhat.com> - 3.6.0-1
- 3.6.0 bump

* Thu Aug 30 2012 Petr Šabata <contyk@redhat.com> - 3.5.1-2
- Remove the explicit iptables dependency (#852840)

* Tue Aug 14 2012 Petr Šabata <contyk@redhat.com> - 3.5.1-1
- 3.5.1 bugfix release bump
- Rename 'br' to 'bridge'

* Mon Aug 06 2012 Petr Šabata <contyk@redhat.com> - 3.5.0-2
- Install the new bridge utility

* Thu Aug 02 2012 Petr Šabata <contyk@redhat.com> - 3.5.0-1
- 3.5.0 bump
- Move to db5.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012 Petr Šabata <contyk@redhat.com> - 3.4.0-1
- 3.4.0 bump
- Drop the print route patch (included upstream)

* Mon Apr 30 2012 Petr Šabata <contyk@redhat.com> - 3.3.0-2
- Let's install rtmon too... (#814819)

* Thu Mar 22 2012 Petr Šabata <contyk@redhat.com> - 3.3.0-1
- 3.3.0 bump
- Update source URL

* Mon Feb 27 2012 Petr Šabata <contyk@redhat.com> - 3.2.0-3
- Address dangerous /tmp files security issue (CVE-2012-1088, #797881, #797878)

* Fri Jan 27 2012 Petr Šabata <contyk@redhat.com> - 3.2.0-2
- Simplify the spec a bit thanks to the UsrMove feature

* Fri Jan 06 2012 Petr Šabata <contyk@redhat.com> - 3.2.0-1
- 3.2.0 bump
- Removing a useless, now conflicting patch (initcwnd already decumented)

* Thu Nov 24 2011 Petr Šabata <contyk@redhat.com> - 3.1.0-1
- 3.1.0 bump
- Point URL and Source to the new location on kernel.org
- Remove now obsolete defattr
- Dropping various patches now included upstream
- Dropping iproute2-2.6.25-segfault.patch; I fail to understand the reason for
  this hack

* Tue Nov 15 2011 Petr Šabata <contyk@redhat.com> - 2.6.39-6
- ss -ul should display UDP CLOSED sockets (#691100)

* Thu Oct 06 2011 Petr Sabata <contyk@redhat.com> - 2.6.39-5
- Fix ss, lnstat and arpd usage and manpages

* Wed Sep 07 2011 Petr Sabata <contyk@redhat.com> - 2.6.39-4
- lnstat should dump (-d) to stdout instead of stderr (#736332)

* Tue Jul 26 2011 Petr Sabata <contyk@redhat.com> - 2.6.39-3
- Rebuild for xtables7

* Tue Jul 12 2011 Petr Sabata <contyk@redhat.com> - 2.6.39-2
- Rebuild for xtables6

* Thu Jun 30 2011 Petr Sabata <contyk@redhat.com> - 2.6.39-1
- 2.6.39 bump

* Wed Apr 27 2011 Petr Sabata <psabata@redhat.com> - 2.6.38.1-4
- Link [cr]tstat to lnstat

* Wed Apr 27 2011 Petr Sabata <psabata@redhat.com> - 2.6.38.1-3
- Install ctstat, rtstat and routef manpage symlinks
- Install m_xt & m_ipt tc modules
- Creating devel and virtual static subpackages with libnetlink

* Thu Apr 21 2011 Petr Sabata <psabata@redhat.com> - 2.6.38.1-2
- General cleanup
- Use global instead of define
- Buildroot removal
- Correcting URL and Source links
- Install genl, ifstat, routef, routel and rtpr (rhbz#697319)

* Fri Mar 18 2011 Petr Sabata <psabata@redhat.com> - 2.6.38.1-1
- 2.6.38.1 bump

* Wed Mar 16 2011 Petr Sabata <psabata@redhat.com> - 2.6.38-1
- 2.6.38 bump

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Petr Sabata <psabata@redhat.com> - 2.6.37-2
- man-pages.patch update, ip(8) TYPE whitespace

* Mon Jan 10 2011 Petr Sabata <psabata@redhat.com> - 2.6.37-1
- 2.6.37 upstream release
- ss(8) improvements patch removed (included upstream)

* Wed Dec 08 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-10
- fix a typo in ss(8) improvements patch, rhbz#661267

* Tue Nov 30 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-9
- ss(8) improvements patch by jpopelka; should be included in 2.6.36

* Tue Nov 09 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-8
- rhbz#641599, use the versioned path, man-pages.patch update, prep update

* Tue Oct 12 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-7
- Do not segfault if peer name is omitted when creating a peer veth link, rhbz#642322

* Mon Oct 11 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-6
- Man-pages update, rhbz#641599

* Wed Sep 29 2010 jkeating - 2.6.35-5
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-4
- Modified man-pages.patch to fix cbq manpage, rhbz#635877

* Tue Sep 21 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-3
- Don't print routes with negative metric fix, rhbz#628739

* Wed Aug 18 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-2
- 'ip route get' fix, iproute2-2.6.35-print-route.patch
- rhbz#622782

* Thu Aug 05 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-1
- 2.6.35 version bump
- iproute2-tc-priority.patch removed (included in upstream now)

* Thu Jul 08 2010 Petr Sabata <psabata@redhat.com> - 2.6.34-5
- Licensing guidelines compliance fix

* Wed Jul 07 2010 Petr Sabata <psabata@redhat.com> - 2.6.34-4
- Requires: iptables >= 1.4.5, BuildRequires: iptables-devel >= 1.4.5

* Thu Jul 01 2010 Petr Sabata <psabata@redhat.com> - 2.6.34-3
- Build now runs ./configure to regenerate Makefile for ipt/xt detection

* Mon Jun 21 2010 Petr Sabata <psabata@redhat.com> - 2.6.34-2
- iproute-tc-priority.patch, rhbz#586112

* Mon Jun 21 2010 Petr Sabata <psabata@redhat.com> - 2.6.34-1
- 2.6.34 version bump

* Tue Apr 20 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.33-2
- 578729 6rd tunnel correctly 3979ef91de9ed17d21672aaaefd6c228485135a2
- change BR texlive to tex according to guidelines

* Thu Feb 25 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.33-1
- update

* Tue Jan 26 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.32-2
- add macvlan aka VESA support d63a9b2b1e4e3eab0d0577d0a0f412d50be1e0a7
- kernel headers 2.6.33 ab322673298bd0b8927cdd9d11f3d36af5941b93
  are needed for macvlan features and probably for other added later.
- fix number of release which contains 2.6.32 kernel headers and features
  but it was released as 2.6.31

* Mon Jan  4 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.31-1
- update to 2.6.31

* Fri Nov 27 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-5.1.20091106gita7a9ddbb
- 539232 patch cbq initscript

* Fri Nov 27 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-5.0.20091106gita7a9ddbb
- snapshot with kernel headers for 2.6.32

* Fri Oct  9 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-5.0.20091009gitdaf49fd6
- new official version isn't available but it's needed -> switch to git snapshots

* Thu Sep 24 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-5
- create missing man pages

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 23 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-3
- new iptables (xtables) bring problems to tc, when ipt is used. 
  rhbz#497344 still broken. tc_modules.patch brings correct paths to
  xtables, but that doesn't fix whole issue.
- 497355 ip should allow creation of an IPsec SA with 'proto any' 
  and specified sport and dport as selectors

* Tue Apr 14 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-2
- c3651bf4763d7247e3edd4e20526a85de459041b ip6tunnel: Fix no default 
 display of ip4ip6 tunnels
- e48f73d6a5e90d2f883e15ccedf4f53d26bb6e74 missing arpd directory

* Wed Mar 25 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-1
- update to 2.6.29
- remove DDR patch which became part of sourc
- add patch with correct headers 1957a322c9932e1a1d2ca1fd37ce4b335ceb7113

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb  4 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.28-2
- 483484 install distribution files into /usr/share and also fixed
 install paths in spec
- add the latest change from git which add DRR support
 c86f34942a0ce9f8203c0c38f9fe9604f96be706

* Mon Jan 19 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.28-1
- previous two patches were included into 2.6.28 release.
- update

* Mon Jan 12 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.27-2
- 475130 - Negative preferred lifetimes of IPv6 prefixes/addresses
  displayed incorrectly
- 472878 - “ip maddr show” in IB interface causes a stack corruption
- both patches will be probably in iproute v2.6.28

* Thu Dec 4 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.27-1
- aead support was included into upstream version
- patch for moving libs is now deprecated
- update to 2.6.27

* Tue Aug 12 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.26-1
- update to 2.6.26
- clean patches

* Tue Jul 22 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.25-5
- fix iproute2-2.6.25-segfault.patch

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.6.25-4
- rebuild for new db4-4.7

* Thu Jul  3 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.25-3
- 449933 instead of failing strncpy use copying byte after byte

* Wed May 14 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.25-2
- allow replay setting, solve also 444724

* Mon Apr 21 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.25-1
- update
- remove patch for backward compatibility
- add patch for AEAD compatibility

* Thu Feb 21 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.23-4
- add creating ps file again. Fix was done in texlive

* Wed Feb  6 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.23-3
- rebuild without tetex files. It isn't working in rawhide yet. Added
  new source for ps files. 
- #431179 backward compatibility for previous iproute versions

* Mon Jan 21 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.23-2
- rebuild with fix tetex and linuxdoc-tools -> manual pdf
- clean unnecessary patches
- add into spec *.so objects, new BR linux-atm-libs-devel

* Wed Oct 31 2007 Marcela Maslanova <mmaslano@redhat.com> - 2.6.23-1
- new version from upstrem 2.3.23

* Tue Oct 23 2007 Marcela Maslanova <mmaslano@redhat.com> - 2.6.22-5
- move files from /usr/lib/tc to /usr/share/tc
- remove listing files twice

* Fri Aug 31 2007 Marcela Maslanova <mmaslano@redhat.com> - 2.6.22-3
- package review #225903

* Mon Aug 27 2007 Jeremy Katz <katzj@redhat.com> - 2.6.22-2
- rebuild for new db4

* Wed Jul 11 2007 Radek Vokál <rvokal@redhat.com> - 2.6.22-1
- upgrade to 2.6.22

* Mon Mar 19 2007 Radek Vokál <rvokal@redhat.com> - 2.6.20-2
- fix broken tc-pfifo man page (#232891)

* Thu Mar 15 2007 Radek Vokál <rvokal@redhat.com> - 2.6.20-1
- upgrade to 2.6.20

* Fri Dec 15 2006 Radek Vokál <rvokal@redhat.com> - 2.6.19-1
- upgrade to 2.6.19

* Mon Dec 11 2006 Radek Vokál <rvokal@redhat.com> - 2.6.18-5
- fix snapshot version

* Fri Dec  1 2006 Radek Vokál <rvokal@redhat.com> - 2.6.18-4
- spec file cleanup
- one more rebuilt against db4

* Thu Nov 16 2006 Radek Vokál <rvokal@redhat.com> - 2.6.18-3
- fix defective manpage for tc-pfifo (#215399)

* Mon Nov 13 2006 Radek Vokál <rvokal@redhat.com> - 2.6.18-2
- rebuilt against new db4

* Tue Oct  3 2006 Radek Vokal <rvokal@redhat.com> - 2.6.18-1
- upgrade to upstream 2.6.18
- initcwnd patch merged
- bug fix for xfrm monitor
- alignment fixes for cris
- documentation corrections
        
* Mon Oct  2 2006 Radek Vokal <rvokal@redhat.com> - 2.6.16-7
- fix ip.8 man page, add initcwnd option

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.6.16-6
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Radek Vokal <rvokal@redhat.com> - 2.6.16-5
- fix crash when resolving ip address

* Mon Aug 21 2006 Radek Vokál <rvokal@redhat.com> - 2.6.16-4
- add LOWER_UP and DORMANT flags (#202199)
- use dist tag

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.6.16-3.1
- rebuild

* Mon Jun 26 2006 Radek Vokál <rvokal@redhat.com> - 2.6.16-3
- improve handling of initcwnd value (#179719)

* Sun May 28 2006 Radek Vokál <rvokal@redhat.com> - 2.6.16-2
- fix BuildRequires: flex (#193403)

* Sun Mar 26 2006 Radek Vokál <rvokal@redhat.com> - 2.6.16-1
- upgrade to 2.6.16-060323
- don't hardcode /usr/lib in tc (#186607)

* Wed Feb 22 2006 Radek Vokál <rvokal@redhat.com> - 2.6.15-2
- own /usr/lib/tc (#181953)
- obsoletes shapecfg (#182284)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.6.15-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.6.15-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 17 2006 Radek Vokal <rvokal@redhat.com> 2.6.15-1
- upgrade to 2.6.15-060110

* Mon Dec 12 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-11
- rebuilt

* Fri Dec 09 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-10
- remove backup of config files (#175302)

* Fri Nov 11 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-9
- use tc manpages and cbq.init from source tarball (#172851)

* Thu Nov 10 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-8
- new upstream source 

* Mon Oct 31 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-7
- add warning to ip tunnel add command (#128107)

* Fri Oct 07 2005 Bill Nottingham <notting@redhat.com> 2.6.14-6
- update from upstream (appears to fix #170111)

* Fri Oct 07 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-5
- update from upstream
- fixed host_len size for memcpy (#168903) <Matt_Domsch@dell.com>

* Fri Sep 23 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-4
- add RPM_OPT_FLAGS

* Mon Sep 19 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-3
- forget to apply the patch :( 

* Mon Sep 19 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-2
- make ip help work again (#168449)

* Wed Sep 14 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-1
- upgrade to ss050901 for 2.6.14 kernel headers

* Fri Aug 26 2005 Radek Vokal <rvokal@redhat.com> 2.6.13-3
- added /sbin/cbq script and sample configuration files (#166301)

* Fri Aug 19 2005 Radek Vokal <rvokal@redhat.com> 2.6.13-2
- upgrade to iproute2-050816

* Thu Aug 11 2005 Radek Vokal <rvokal@redhat.com> 2.6.13-1
- update to snapshot for 2.6.13+ kernel

* Tue May 24 2005 Radek Vokal <rvokal@redhat.com> 2.6.11-2
- removed useless initvar patch (#150798)
- new upstream source 

* Tue Mar 15 2005 Radek Vokal <rvokal@redhat.com> 2.6.11-1
- update to iproute-2.6.11

* Fri Mar 04 2005 Radek Vokal <rvokal@redhat.com> 2.6.10-2
- gcc4 rebuilt

* Wed Feb 16 2005 Radek Vokal <rvokal@redhat.com> 2.6.10-1
- update to iproute-2.6.10

* Thu Dec 23 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-6
- added arpd into sbin

* Mon Nov 29 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-5
- debug info removed from makefile and from spec (#140891)

* Tue Nov 16 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-4
- source file updated from snapshot version
- endian patch adding <endian.h> 

* Sat Sep 18 2004 Joshua Blanton <jblanton@cs.ohiou.edu> 2.6.9-3
- added installation of netem module for tc

* Mon Sep 06 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-2
- fixed possible buffer owerflow, path by Steve Grubb <linux_4ever@yahoo.com>

* Wed Sep 01 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-1
- updated to iproute-2.6.9, spec file change, patches cleared

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 26 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.7-16
- Took tons of manpages from debian, much more complete (#123952).

* Thu May 06 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.7-15
- rebuilt

* Thu May 06 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.7-13.2
- Built security errata version for FC1.

* Wed Apr 21 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.7-14
- Fixed -f option for ss (#118355).
- Small description fix (#110997).
- Added initialization of some vars (#74961). 
- Added patch to initialize "default" rule as well (#60693).

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Nov 05 2003 Phil Knirsch <pknirsch@redhat.com> 2.4.7-12
- Security errata for netlink (CAN-2003-0856).

* Thu Oct 23 2003 Phil Knirsch <pknirsch@redhat.com>
- Updated to latest version. Used by other distros, so seems stable. ;-)
- Quite a few patches needed updating in that turn.
- Added ss (#107363) and several other new nifty tools.

* Tue Jun 17 2003 Phil Knirsch <pknirsch@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan 16 2003 Phil Knirsch <pknirsch@redhat.com> 2.4.7-7
- Added htb3-tc patch from http://luxik.cdi.cz/~devik/qos/htb/ (#75486).

* Fri Oct 11 2002 Bill Nottingham <notting@redhat.com> 2.4.7-6
- remove flags patch at author's request

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Phil Knirsch <pknirsch@redhat.com> 2.4.7-4
- Don't forcibly strip binaries

* Mon May 27 2002 Phil Knirsch <pknirsch@redhat.com> 2.4.7-3
- Fixed missing diffserv and atm support in config (#57278).
- Fixed inconsistent numeric base problem for command line (#65473).

* Tue May 14 2002 Phil Knirsch <pknirsch@redhat.com> 2.4.7-2
- Added patch to fix crosscompiling by Adrian Linkins.

* Fri Mar 15 2002 Phil Knirsch <pknirsch@redhat.com> 2.4.7-1
- Update to latest stable release 2.4.7-now-ss010824.
- Added simple man page for ip.

* Wed Aug  8 2001 Bill Nottingham <notting@redhat.com>
- allow setting of allmulti & promisc flags (#48669)

* Mon Jul 02 2001 Than Ngo <than@redhat.com>
- fix build problem in beehive if kernel-sources is not installed

* Fri May 25 2001 Helge Deller <hdeller@redhat.de>
- updated to iproute2-2.2.4-now-ss001007.tar.gz 
- bzip2 source tar file
- "License" replaces "Copyright"
- added "BuildPrereq: tetex-latex tetex-dvips psutils"
- rebuilt for 7.2

* Tue May  1 2001 Bill Nottingham <notting@redhat.com>
- use the system headers - the included ones are broken
- ETH_P_ECHO went away

* Sat Jan  6 2001 Jeff Johnson <jbj@redhat.com>
- test for specific KERNEL_INCLUDE directories.

* Thu Oct 12 2000 Than Ngo <than@redhat.com>
- rebuild for 7.1

* Thu Oct 12 2000 Than Ngo <than@redhat.com>
- add default configuration files for iproute (Bug #10549, #18887)

* Tue Jul 25 2000 Jakub Jelinek <jakub@redhat.com>
- fix include-glibc/ to cope with glibc 2.2 new resolver headers

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Than Ngo <than@redhat.de>
- rebuilt in the new build environment
- use RPM macros
- handle RPM_OPT_FLAGS

* Sat Jun 03 2000 Than Ngo <than@redhat.de>
- fix iproute to build with new glibc

* Fri May 26 2000 Ngo Than <than@redhat.de>
- update to 2.2.4-now-ss000305
- add configuration files

* Mon Sep 13 1999 Bill Nottingham <notting@redhat.com>
- strip binaries

* Mon Aug 16 1999 Cristian Gafton <gafton@redhat.com>
- first build
