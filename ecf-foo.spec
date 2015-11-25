Name:           ecf-foo
Group:          System Environment/Libraries
Version:        1.0.0
Release:        1%{?dist}
Summary:        ECF "blank" rpm, for testing ecf-rpmtools
URL:            https://ecf-git.fnal.gov/ecf-foo

License:        Artistic 2.0
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       rsync
BuildRequires:  rsync

Source:         %{name}-%{version}-%{release}.tar.gz

%description
Just an empty rpm.  It's useful as a template, and as a test suite for the 
ecf-rpmtools Makefile.

%prep
%setup -q -c -n ecf-foo

%build
# Empty build section added per rpmlint

%install
if [[ $RPM_BUILD_ROOT != "/" ]]; then
    rm -rf $RPM_BUILD_ROOT
fi

for i in etc usr; do
    rsync -Crlpt --delete ./${i} ${RPM_BUILD_ROOT}
done

for i in bin sbin; do
    if [ -d ${RPM_BUILD_ROOT}/$i ]; then
        chmod 0755 ${RPM_BUILD_ROOT}
    fi
done

mkdir -p ${RPM_BUILD_ROOT}/usr/share/man/man8
for i in `ls usr/sbin`; do
    pod2man --section 8 --center="System Commands" usr/sbin/${i} \
        > ${RPM_BUILD_ROOT}/usr/share/man/man8/${i}.8 ;
done

%clean
# Adding empty clean section per rpmlint.  In this particular case, there is
# nothing to clean up as there is no build process

%files
%defattr(-,root,root)
%config(noreplace) /etc/ecf-foo/config
%{_sbindir}/ecf-foo
/usr/share/man/man8/*

%changelog
* Wed Nov 25 2015  Tim Skirvin <tskirvin@fnal.gov>      1.0.0-1
- added some docs, touched up the .spec file

* Wed Nov 25 2015  Tim Skirvin <tskirvin@fnal.gov>      1.0.0-0
- initial commit
