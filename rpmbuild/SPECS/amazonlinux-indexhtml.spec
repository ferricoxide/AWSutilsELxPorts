Summary: Browser default start page
Name: amazonlinux-indexhtml
Version: 1
Release: 1%{?dist}
License: Distributable
Group: Documentation
BuildArch: noarch
Source0: index.html
Provides: redhat-indexhtml
Provides: centos-indexhtml

%description
The welcome page shown by your Web browser after you install Amazon Linux

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_defaultdocdir}/HTML/en-US
cp -a %{SOURCE0} $RPM_BUILD_ROOT/%{_defaultdocdir}/HTML/
pushd $RPM_BUILD_ROOT/%{_defaultdocdir}/HTML/en-US
ln -s ../index.html .
test -d ../img && ln -s ../img/ .
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_defaultdocdir}/HTML/*

%changelog
* Wed Dec 06 2017 Chad Miller <millchad@amazon.com> 1
- Initial release
