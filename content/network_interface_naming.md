Title: Linux network interface naming
Date: 2015-12-18 03:25
Tags: linux, systemd, network interfaces
Slug: linux_network_interface_naming
Category: Networking
Author: James Nzomo
Summary: About how net-if's get their names - from the classic kernel to the biosdevname and systemd-udev way.


# Intro
If you are running a recent ubuntu release ( > 15.XX ), you've probably noticed
that your net interfaces have been "rebranded". Maybe this noticing came in the
form of your sripts being broken....your `/etc/network/if-up.d/XXX` script or
vagrant-libvirt deploy failed because you hard coded an interface name in your
scripts (bad practice which im guilty of). It worked previously on your
old-release, then you had to upgrade...but I digress.

In this post, I'll try talking about how net devices get their names, the schemes
employed and the tech behind the schemes.

---

# The classic naming scheme - `eth<0-n>`
Not so long ago, without any devops intervention, interface names were decided
solely by the Kernel based on the order in which they are enumerated which in
turn is based on the order in which their modules/drivers are loaded and then,
where multiple NICs catered for by the same driver are present, they'd be named
in the order in which they were discovered which in turn is again affected by
the order in which the PCI device list is enumerated.

When its all done, you'd have something like this :-

`eth<index>` = ethernet, `wlan<index>` = wireless, `usb<index>` = usbnet - prolly phone-tethered

While the scheme is good enough to tell about the type of connection, there's
not much in the way of name predictability and telling about the nature of
the hardware that provides a given interface i.e. are `eth0` and `eth1` provided
by different ports on the same NIC? Is `eth2` provided by a USB adapter?

Another problem is that if you leave it all up to the powers behind the scheme, the
device naming will probably not be the same after kernel, NIC or motherboard
upgrades or sometimes even reboots.

It's possible to get around the above mentioned limitations using [scripts
and udev rules](classic_naming_workarounds) but we live in modern times and
techies should not be bothered to jump through those hoops just to sort out
something that should be automagic.

---

# biosdevname - `em<port>`, `p<slot>p<port>`
One of the efforts at bringing order out of chaos is dell's [biosdevname][biosdevname]
project which according to the project description is <q>a udev helper for naming
devices per BIOS names.</q> This helper-utility determines device names based on
the <q>intended order of network devices</q> as suggested by the BIOS.

With the default policy, the naming scheme of it goes like so:-  

 - On-board net devices get named `em<port>[_<virtual instance>]`  
 - Add-on NICs devices get named `p<slot>p<port>[_<virtual instance>]`

where:- 

  - `em` = [ethernet-on-motherboard][dell_whitepaper],
  - `<slot>` = the respective PCI slot,
  - `<port>` the port number...for multi-port NICs.
  - `<virtual instance>` is the SRIOV and/or NPAR instance index
  - The "p"s in the Add-on card scheme stand for pci slot and port respectively

The above scheme is implemented here:- [naming_policy.c][biosdevname_naming_policy_src]

If you have the utility installed, you can try it out by booting your kernel
with `biosdevname=1` option or just run `biosdevname -i eth0 #(swap eth0
with any interface you have)` from the terminal. If conditions are right,
you should get something along the lines of `em1` or `p1p1`.

With this utility, names are stable, predictable and you can also tell what's embedded
and what's slotted in...but it has it's limitations, one of them being that it doesn't
cater for a wider range of interface types/devices. It refused to name my usb
ethernet dongle.

---

# systemd udev - `eno<index>`, `ens<slot>d<port>`
Starting version 197, shortly after udev was absorbed into systemd source
tree, native predictable naming was added to the mix.

According to [the systemd wiki on the topic][fd_pni_dox], and the
[systemd-udev sources][net_id_src], the names are generated based on:-


  - firmware/bios-provided for on-board devices - `<type>o<index>[d<dev_port>]`
  - firmware/bios-provided for pci-express hotplug slot - `<type>s<slot>[f<function>][d<dev_port>]`
  - physical/geographical location for PCI devices -  
    `<type>[P<domain>]p<bus>s<slot>[f<function>][[d<dev_port>]|[u<port>][..][c<config>][i<interface>]]`
  - the devices's MAC address - `<type>x<MAC>`

Where:-

- `<type>` is a two character prefix that tells the nature of the device/connection:-
`en` for ethernet, `sl` = [Serial Line Internet Protocol](https://tools.ietf.org/html/rfc1055),
`wl` = Wireless LAN/Wi-Fi and `ww` for Wireless WAN (LTE/3g device, probably even WiMAX)
- `<domain>` is pci device domain.
- `<function>` = SRIOV(or maybe also NPAR?) number for multi-function PCI devices.
- `u<port>` is a usb port

Thus for example `eno1` is an onboard ethernet device, `enp8s0` should be an
ethernet interface provided by a device on bus #8 slot #0 with only 1 port and
`wlp9s0` should be an wlan interface provided by device on bus #9 slot #0.

On trying out a usb ethernet dongle, I got `enp0s29f7u1` and going by the
location/path scheme we can tell that it's an ethernet interface provided by a
usb device connected to a usb controller on PCI bus #0, device #29, with function #7
plugged into usb port #1.


### systemd-udev Naming Policy
Net devices may have more than one name generated for them which you can
view by querying the udev database (filtering the results):-  

    :::shell
    udevadm info -q property -p /sys/class/net/ens33 | grep ID_NET_NAME
    ID_NET_NAME_MAC=enx112233445566
    ID_NET_NAME_PATH=enp2s0
    ID_NET_NAME_SLOT=ens33

In the above example, we have names by mac, location and bios provided index.
The choice of name is determined by a list if policies defined for `NamePolicy`
in the respective link config file (see `man systemd.link`). To find out what
link file is in use, query udevadm like so:-

    :::shell
    udevadm info -q property -p /sys/class/net/ens33 | grep LINK_FILE
    ID_NET_LINK_FILE=/lib/systemd/network/99-default.link

I get 99-default.link, contents of which are:-

    :::shell
    cat /lib/systemd/network/99-default.link
    [Link]
    NamePolicy=kernel database onboard slot path
    MACAddressPolicy=persistent

Looking at the `NamePolicy` entry, the precedence is defined by the order
in which they appear and the first successful one is used to set the device name.
In this case with ens33 being chosen, `kernel`, `database` and `onboard` failed,
`slot` passed and `path` wasn't considered.


# Outro
systemd-udev is now standard on most big name distros (ubuntu included) and has
naturally superseded biosdevname where it reigned. There is no need to sweat it out
with unpredictable interface names like the techies of yesterday but just in case
you want to, you can disable all manner of predictability by passing `net.ifnames=0`
and `biosdevname=0` to the kernel at boot time.

### Resources, Refs & google juice:-
  - [wiki.freedesktop.org article on the subject][fd_pni_dox]{: target="_blank" }
  - [Well commented source on systemd net-dev naming][net_id_src]{: target="_blank" }
  - [biosdevname homepage][biosdevname]{: target="_blank" }
  - [biosdevname naming policy source][biosdevname_naming_policy_src]{: target="_blank" }
  - [An ice article on classic naming scheme and problem workarounds][classic_naming_workarounds]{: target="_blank" }
  - [How Linux Works: What Every Superuser Should Know][how_linux_works]{: target="_blank" } by Brian Ward

[fd_pni_dox]: http://wiki.freedesktop.org/www/Software/systemd/PredictableNetworkInterfaceNames/
[net_id_src]: https://github.com/systemd/systemd/blob/3f65d73149cd0f64eb3fdb0c71f55f6c1133fefe/src/udev/udev-builtin-net_id.c
[net_id_src_L479]: https://github.com/systemd/systemd/blob/3f65d73149cd0f64eb3fdb0c71f55f6c1133fefe/src/udev/udev-builtin-net_id.c#L479
[link_config_src_L414]: https://github.com/systemd/systemd/blob/3f65d73149cd0f64eb3fdb0c71f55f6c1133fefe/src/udev/net/link-config.c#L414
[redhat_take]: https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Deployment_Guide/appe-Consistent_Network_Device_Naming.html
[fedora_take]: https://fedoraproject.org/wiki/Features/SystemdPredictableNetworkInterfaceNames
[ubuntu_take]: https://wiki.ubuntu.com/SystemdForUpstartUsers
[biosdevname]: http://linux.dell.com/biosdevname/
[biosdevname_naming_policy_src]: http://linux.dell.com/cgi-bin/cgit.cgi/biosdevname.git/tree/src/naming_policy.c?id=e51172768cec37ab0a350e439d2827b0c4e604a4#n31
[biosdevname_fedora]: https://fedoraproject.org/wiki/Features/ConsistentNetworkDeviceNaming
[biosdevname_linux_die]: http://linux.die.net/man/1/biosdevname
[dell_whitepaper]: http://linux.dell.com/files/whitepapers/consistent_network_device_naming_in_linux.pdf
[classic_naming_workarounds]: https://ivi.fnwi.uva.nl/sne/air//wiki/LogicalInterfaceNames/
[how_linux_works]: http://www.amazon.com/gp/product/B00PKTGLWM?psc=1&redirect=true&ref_=oh_aui_d_detailpage_o00
