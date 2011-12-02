%define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

%define sourcedir syncer

Summary: Atomia DNS PowerDNS Sync application
Name: atomiadns-powerdnssync
Version: 1.0.31
Release: 1%{?dist}
License: Commercial
Group: System Environment/Daemons
URL: http://www.atomia.com/atomiadns/
Source: atomiadns-powerdns_sync.tar.gz

Packager: Jimmy Bergman <jimmy@atomia.com>
Vendor: Atomia AB RPM Repository http://rpm.atomia.com/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Requires(pre): shadow-utils
Requires: perl-Class-MOP >= 0.92

BuildArch: noarch
BuildRequires: perl
BuildRequires: perl(ExtUtils::MakeMaker)

%description
Atomia DNS PowerDNS Sync application.

%prep
%setup -n %{sourcedir}

%build
%{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install
%{__rm} -f %{buildroot}%{perl_vendorarch}/auto/*/*/*/.packlist
%{__mkdir} -p %{buildroot}/etc/init.d
%{__cp} SPECS/atomiadns-atomiapowerdnssync.init %{buildroot}/etc/init.d/atomiapowerdnssync
%{__mkdir} -p %{buildroot}/usr/share/atomia/conf
%{__cp} conf/atomiadns.conf.atomiapowerdnssync %{buildroot}/usr/share/atomia/conf/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
/usr/bin/atomiapowerdnssync
/usr/share/atomia/conf/atomiadns.conf.atomiapowerdnssync
/etc/init.d/atomiapowerdnssync
%{perl_vendorlib}/Atomia/DNS/PowerDNSSyncer.pm
%doc %{_mandir}/man1/atomiapowerdnssync.1.gz

%post
/sbin/chkconfig --add atomiapowerdnssync

if [ -f /etc/atomiadns.conf ]; then
	if [ -z "$(grep "^powerdns" /etc/atomiadns.conf)" ]; then
		cat /usr/share/atomia/conf/atomiadns.conf.atomiapowerdnssync >> /etc/atomiadns.conf
	fi
else
	cp /usr/share/atomia/conf/atomiadns.conf.atomiapowerdnssync /etc/atomiadns.conf
fi

if [ "$1" -gt 1 ]; then
	/sbin/service atomiapowerdnssync restart
fi

exit 0

%preun
if [ "$1" = 0 ]; then
	/sbin/service atomiapowerdnssync stop
	/sbin/chkconfig --del atomiapowerdnssync 
fi
exit 0

%changelog
* Fri Dec 02 2011 Jimmy Bergman <jimmy@atomia.com> - 1.0.31-1
- Add missing libmime-base32-perl dependency
* Thu Dec 01 2011 Jimmy Bergman <jimmy@atomia.com> - 1.0.30-1
- Improve domainmetadata view and support NSEC + NSEC3 instead of only NSEC3NARROW
* Wed Sep 28 2011 Jimmy Bergman <jimmy@atomia.com> - 1.0.29-1
- Make DNSSEC key generation more robust and improve slave support (multi-master + TSIG) and database schema in PowerDNS agent
* Fri Sep 16 2011 Jimmy Bergman <jimmy@atomia.com> - 1.0.28-1
- Improve performance of validation trigger + indexing for large zones
* Mon Jul 18 2011 Jimmy Bergman <jimmy@atomia.com> - 1.0.27-1
- Fix powerdns database setup
* Mon Jul 18 2011 Jimmy Bergman <jimmy@atomia.com> - 1.0.26-1
- Fix powerdns database setup
* Mon Jul 18 2011 Jimmy Bergman <jimmy@atomia.com> - 1.0.25-1
- Fix powerdns database schema to include version-table forgotten in first release, and change so that powerdns syncer can run on the same server as Atomia DNS
* Wed Jun 08 2011 Jimmy Bergman <jimmy@atomia.com> - 1.0.24-1
- Fix PowerDNS sync agent to not have trailing dot in MNAME
* Thu May 05 2011 Jimmy Bergman <jimmy@atomia.com> - 1.0.23-1
- Forgot to include powerdns_sync in 1.0.22 build
* Thu Jan 27 2011 Jimmy Bergman <jimmy@atomia.com> - 1.0.16-1
- DNSSEC support and changing the bind-dlz syncer to only load 10000 zones per sync_updated_zones batch
