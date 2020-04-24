# amazon linux merge strategy: never-merge

%global module_name amazon_linux_extras

Name:           amazon-linux-extras
Version:        1.6.10
Release:        1%{?dist}
Summary:        Command line tool for managing Amazon Linux Extras

License:        GPLv2
URL:            https://aws.amazon.com/amazon-linux-2/
Source0:        SOURCES/%{name}-%{version}.tar.xz

Requires:       python >= 2.6
Requires:       coreutils
Requires:       system-release
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  gettext
BuildRequires:  pytest

%description
A tool for selective enabling of fresh not-as-stable software from specific,
topical RPM repositories for Amazon Linux.

%package yum-plugin
Summary:        Yum plugin assists Extras discovery
Requires:       amazon-linux-extras

%description yum-plugin
Makes any failed installation of a named package also help the user know
an Extra could provide what they wished for.

%prep
%setup -q


%build
%{__python} setup.py build

echo "#!/bin/bash"                                             >%{_tmppath}/update-motd
echo "timeout 5s amazon-linux-extras system_motd 2>/dev/null" >>%{_tmppath}/update-motd


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
install -Dpm 0644 man/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
%find_lang %{module_name}

install -Dm 0755 %{_tmppath}/update-motd %{buildroot}%{_sysconfdir}/update-motd.d/50-amazon-linux-extras-news
rm               %{_tmppath}/update-motd

install -Dpm 0644 supporting-files/yum-plugin-suggestions %{buildroot}%{_libdir}/yum-plugins/extras_suggestions.py
install -Dpm 0644 supporting-files/yum-pluginconf-suggestions %{buildroot}%{_sysconfdir}/yum/pluginconf.d/extras_suggestions.conf
install -dpm 0700 %{buildroot}/var/cache/amzn2extras
touch             %{buildroot}/var/cache/amzn2extras/catalog-cache-0   # rpm-build requires existence for ghost-ing

%check
%{__python} setup.py test



%files -f %{module_name}.lang
%defattr(0644,root,root,755)
%doc README
%{python_sitelib}/%{module_name}
%{python_sitelib}/%{module_name}*.egg-info
%attr(755,-,-) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%attr(755, root, root) %{_sysconfdir}/update-motd.d/50-amazon-linux-extras-news
%ghost /var/cache/amzn2extras/catalog-cache-0

%files yum-plugin
%defattr(0644,root,root,755)
%{_sysconfdir}/yum/pluginconf.d/extras_suggestions.conf
%{_libdir}/yum-plugins/extras_suggestions.py*


%changelog
* Thu Feb 20 2020 Jason Green <jasg@amazon.com> - 1.6.10-1
- Add skip_if_unavailable on extras repositories

* Mon Sep 9 2019 Chuanhao Jin <haroldji@amazon.com> - 1.6.9-2
- Fix unwanted console message, "Couldn't write catalog to cache"
  when running list command with /tmp dir mounted as tmpfs

* Tue May 21 2019 Chad Miller <millchad@amazon.com> - 1.6.9-1
- Store catalog cache in private location.
- Add Ghost manifest for /var/cache cache location.
- Make plugin package depend on main package.

* Tue Apr 02 2019 Andrew Egelhofer <egelhofe@amazon.com> - 1.6.8-1
- Extend URL_FMT formatter to support uppercasing variables within python's 
  formatting strings

* Mon Feb 04 2019 Chad Miller <millchad@amazon.com> - 1.6.7-1
- Add timeout to extras-visibility yum plugin

* Tue Jan 29 2019 Frederick Lefebvre <fredlef@amazon.com> - 1.6.6-1
- Parameterized extras repo urls.

* Fri Nov 30 2018 Chad Miller <millchad@amazon.com> - 1.6.5-1
- Fix 'yum' command suggestion at enable-time.

* Wed Oct 31 2018 Chad Miller <millchad@amazon.com> - 1.6.4-1
- Require system-release pkg providing gpg key
- Read from configuration files
    /etc/amazon-linux-extras.conf
    /usr/local/etc/amazon-linux-extras.conf
    $HOME/.config/amazon-linux/amazon-linux-extras.conf

* Tue Sep 04 2018 Chad Miller <millchad@amazon.com> - 1.6.3-1
- Provide expiration of Topics.

* Wed Aug 01 2018 Chad Miller <millchad@amazon.com> - 1.6.2-1
- Include more help introducing Extras in yum plugin.

* Tue Jun 26 2018 Chad Miller <millchad@amazon.com> - 1.6.1-1
- Use correct URL in yum-plugin. It changed.

* Wed Jun 20 2018 Chad Miller <millchad@amazon.com> - 1.6-2
- Never delay motd more than 5 seconds.
- Explicit Require of python and coreutils.

* Thu May 24 2018 Chad Miller <millchad@amazon.com> - 1.6-1
- Hide expired extras.
- Roll back config on yum failure.
- Write motd hook as executable.

* Tue Apr 03 2018 Chad Miller <millchad@amazon.com> - 1.5-1
- Include a yum 'install' plugin and subpackage to aid discovery.

* Mon Mar 19 2018 Chad Miller <millchad@amazon.com> - 1.4-1
- Write a system message-of-the-day if applicable.

* Fri Jan 12 2018 Frederick Lefebvre <fredlef@amazon.com> - 1.3.1-2
- Set priority for each repo definition

* Tue Dec 12 2017 Chad Miller <millchad@amazon.com> - 1.3.1-1
- Verbose yum at install with "-v" parameter.
- Add debuginfo and sources repos.

* Mon Nov 27 2017 Chad Miller <millchad@amazon.com> - 1.2-1
- Use mirrorlist instead of baseurl for extra locations.

* Wed Nov 22 2017 Chad Miller <millchad@amazon.com> - 1.1-1
- Change license to GPLv2

* Tue Aug  8 2017 Iliana Weller <iweller@amazon.com> - 1.0-1
- Initial package build
