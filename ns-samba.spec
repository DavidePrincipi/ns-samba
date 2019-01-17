Name: ns-samba
Version: 4.8.6
Release: 1%{?dist}
Summary: Namespaced Samba AD domain controller
Autoprov: 0

License: GPLv3+
URL: %{url_prefix}/%{name}
Source0: %{name}-%{version}.tar.gz
Source1: https://download.samba.org/pub/samba/stable/samba-%{version}.tar.gz

BuildRequires: docbook-xsl
BuildRequires: gnutls-devel
BuildRequires: gpgme-devel
BuildRequires: jansson-devel
BuildRequires: libacl-devel
BuildRequires: libarchive-devel
BuildRequires: lmdb-devel
BuildRequires: nethserver-devtools
BuildRequires: openldap-devel
BuildRequires: pam-devel
BuildRequires: pygpgme
BuildRequires: python-devel
BuildRequires: systemd-devel
BuildRequires: bind-utils, bind-devel
BuildRequires: libtalloc-devel
BuildRequires: libtevent-devel
BuildRequires: libtdb-devel


BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: bind-utils

%description
This is a Samba %{version} domain controller build for CentOS that runs in
separate Linux namespaces. It requires a network bridge to attach its private
interface and it can coexists with the existing samba daemons.

%prep
%setup 
%setup -D -T -b 1

%build
cd %{_builddir}/samba-%{version}

# /var/lib/ns-samba/locks/sysvol
# /opt/ns-samba/private/

./configure --prefix=/opt/%{name} --localstatedir=/var/lib/%{name} --sysconfdir=/etc/%{name} --with-systemd
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

(cd root ; find . -depth -print | cpio -dump %{buildroot})

pushd %{_builddir}/samba-%{version}
%make_install
popd

%{genfilelist} %{buildroot} > %{name}.filelist

%files -f %{name}.filelist
%defattr(-,root,root)
%doc COPYING
%dir /var/lib/%{name}
%config(noreplace) %ghost %{_sysconfdir}/%{name}/smb.conf

%post
%systemd_post samba.service

%preun
%systemd_preun samba.service

%postun
%systemd_postun

%changelog
* Mon Nov 12 2018 Davide Principi <davide.principi@nethesis.it> - 4.8.6-1
- Bump version 4.8.6

* Mon Sep  3 2018 Davide Principi <davide.principi@nethesis.it> - 4.7.10-1
- Bump version 4.7.10

* Mon Sep  3 2018 Davide Principi <davide.principi@nethesis.it> - 4.7.9-1
- Bump version 4.7.9

* Tue Jun 26 2018 Davide Principi <davide.principi@nethesis.it> - 4.7.8-1
- Bump version 4.7.8

* Thu Apr 26 2018 Davide Principi <davide.principi@nethesis.it> - 4.7.7-1
- Bump version 4.7.7

* Mon Apr 16 2018 Davide Principi <davide.principi@nethesis.it> - 4.7.6-1
- Bump version 4.7.6

* Thu Mar 15 2018 Davide Principi <davide.principi@nethesis.it> - 4.6.14-1
- Bump version 4.6.14

* Mon Jan 15 2018  Davide Principi <davide.principi@nethesis.it> - 4.6.12-1
- Bump version 4.6.12

* Fri Dec 01 2017 Davide Principi <davide.principi@nethesis.it> - 4.6.11-1
- Bump version 4.6.11

* Fri Oct 13 2017 Davide Principi <davide.principi@nethesis.it> - 4.6.8-1
- Bump version 4.6.8

* Fri Oct 06 2017 Davide Principi <davide.principi@nethesis.it> - 4.7.0-1
- Bump version 4.7.0
 
* Mon Jun 26 2017 Davide Principi <davide.principi@nethesis.it> - 4.6.5-1
- Bump version 4.6.5

* Wed May 24 2017 Davide Principi <davide.principi@nethesis.it> - 4.6.4-1
- Bump version 4.6.4

* Wed May 03 2017 Davide Principi <davide.principi@nethesis.it> - 4.6.3-1
- Bump version 4.6.3

* Mon Apr 10 2017 Davide Principi <davide.principi@nethesis.it> - 4.6.2-1
- Bump version 4.6.2

* Fri Mar 24 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 4.6.0-1
- Bump version 4.6.0

* Mon Dec 12 2016 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.1-1
- Bump version 4.5.2

* Thu Jul 07 2016 Davide Principi <davide.principi@nethesis.it> - 1.0.0-1
- Bump version 4.4.5

* Tue May 17 2016 Davide Principi <davide.principi@nethesis.it>
- Bump Samba 4.4.3

* Mon Apr 11 2016 Davide Principi <davide.principi@nethesis.it>
- Bump Samba 4.3.6

* Wed Jan 27 2016 Davide Principi <davide.principi@nethesis.it>
- Initial build
