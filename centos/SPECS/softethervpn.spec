%define majorversion 4
%define minorversion 29
%define buildversion 9680
%define dateversion 2019.02.28
%define buildrelease rtm

Name:           softethervpn
Version:        %{majorversion}.%{minorversion}.%{buildversion}
Release:        1%{?dist}
Summary:        An Open-Source Free Cross-platform Multi-protocol VPN Program

Group:          Applications/Internet
License:        GPLv2
URL:            http://www.softether.org/
Source0:        https://www.softether-download.com/files/softether/v%{majorversion}.%{minorversion}-%{buildversion}-%{buildrelease}-%{dateversion}-tree/Source_Code/softether-src-v%{majorversion}.%{minorversion}-%{buildversion}-%{buildrelease}.tar.gz

BuildRequires:  ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	readline-devel

Requires(post):		chkconfig
Requires(postun):	initscripts
Requires(preun):	chkconfig
Requires(preun):	initscripts

%description
SoftEther VPN is one of the world's most powerful and easy-to-use multi-protocol VPN software. It runs on Windows, Linux, Mac, FreeBSD, and Solaris.

%prep
%setup -q -n v%{majorversion}.%{minorversion}-%{buildversion}

%build
%ifarch i386 i686
cp $RPM_SOURCE_DIR/linux_32bit.mak Makefile
%else
cp $RPM_SOURCE_DIR/linux_64bit.mak Makefile
%endif
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -m 755 -d $RPM_BUILD_ROOT/usr/bin/
install -m 755 -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m 755 $RPM_SOURCE_DIR/scripts/vpnserver $RPM_BUILD_ROOT/usr/bin/vpnserver
install -m 755 $RPM_SOURCE_DIR/scripts/vpnbridge $RPM_BUILD_ROOT/usr/bin/vpnbridge
install -m 755 $RPM_SOURCE_DIR/scripts/vpnclient $RPM_BUILD_ROOT/usr/bin/vpnclient
install -m 755 $RPM_SOURCE_DIR/scripts/vpncmd $RPM_BUILD_ROOT/usr/bin/vpncmd
install -m 755 $RPM_SOURCE_DIR/init.d/vpnserver $RPM_BUILD_ROOT/etc/rc.d/init.d/vpnserver

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_usr}/bin/vpnserver
%{_usr}/bin/vpnbridge
%{_usr}/bin/vpnclient
%{_usr}/bin/vpncmd
%{_usr}/vpnserver/hamcore.se2
%{_usr}/vpnserver/vpnserver
%{_usr}/vpnbridge/hamcore.se2
%{_usr}/vpnbridge/vpnbridge
%{_usr}/vpnclient/hamcore.se2
%{_usr}/vpnclient/vpnclient
%{_usr}/vpncmd/hamcore.se2
%{_usr}/vpncmd/vpncmd
%{_usr}/vpnserver/
%{_usr}/vpnbridge/
%{_usr}/vpnclient/
%{_usr}/vpncmd/
%{_initddir}/vpnserver
%doc AUTHORS.TXT BUILD_UNIX.TXT BUILD_WINDOWS.TXT ChangeLog ChangeLog.txt LICENSE LICENSE.TXT README README.TXT THIRD_PARTY.TXT WARNING.TXT

%post
/sbin/chkconfig --add vpnserver

#%postun
#if [ "$1" -ge "1" ]; then
#	/sbin/service vpnserver condrestart >/dev/null 2>&1 || :
#fi

%preun
if [ $1 -eq 0 ]; then
	/sbin/service vpnserver stop >/dev/null 2>&1
	/sbin/chkconfig --del vpnserver
fi

%changelog
* Thu Feb 28 2019 - 4.29.9680-rtm
- Switched the license of SoftEther VPN from GPLv2 to Apache License 2.0. Text messages on source codes and UIs have been modified.
- Supports 4-digit expiration date on X.509 certificates.
- Replaced SHA-0 implementation.
- Improved integrity and security of C source codes. Fixed several buffer overflows and integer overflows. Enforced NULL pointer checks. Fixed problems on the size of malloc() and Zero Memory functions. These problems include a vulnerability that a malformed packet will cause the buffer overflow at the receive path. This vulnerability may occur abnormal process exit with the buffer security check mechanism built-in with SoftEther VPN binary. Although this buffer overflow can theoretically bypass the security check in theory, in the actual binary it is detected by the buffer security check inserted by the C compiler and the process is forcibly terminated. Therefore, as a result, it can be abused by a DoS attacker. Acknowledgments: The last problems is discovered and reported by Fabrizio Steiner.
- Modified the behavior at the executing of the ethtool command to call just the command name instead of the full path.
- Fixed a single code on the SecureNAT function that SYN and ACK were reverse.
- Fixed the bug on the creating of SingleInstance objects that the temporary file will remain as a garbage after the file lock will fail on UNIX operating systems.
- Fixed the problem that the full path of the home directory will be sometimes obtained as wrong value on UNIX operating systems.
- Fixed the problem that processing the system datetime values which are before 1970-01-01.
