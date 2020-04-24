
%global last_py26_awslogs 1.1.0-1.3.amzn1

Summary:        Scripts for CloudWatch Logs Daemon
Name:           awslogs
Version:        1.1.4
Release:        3%{?dist}
License:        Amazon Software License
Group:          Amazon/Tools
URL:            http://aws.amazon.com/cloudwatch
Source1:        awslogs.conf
Source2:        awslogsd.sh
Source3:        awslogs.logrotate
Source4:        proxy.conf
Source5:        awslogsd.service
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   python
BuildArch:       noarch
Requires:        aws-cli-plugin-cloudwatch-logs
Requires:        systemd-units, initscripts
Requires:        rsyslog
Requires(post):  systemd-units, initscripts
Requires(preun): systemd-units, initscripts
BuildRequires:   systemd-units

%description
Scripts to run Amazon CloudWatch Logs as a daemon.

%prep

%build

%install
rm -rf %{buildroot}
install -D -m 644 %SOURCE1 %{buildroot}%{_sysconfdir}/awslogs/awslogs.conf
install -D -m 755 %SOURCE2 %{buildroot}%{_sbindir}/awslogsd
install -D -m 644 %SOURCE3 %{buildroot}%{_sysconfdir}/logrotate.d/awslogs
install -D -m 644 %SOURCE4 %{buildroot}%{_sysconfdir}/awslogs/proxy.conf
install -D -m 644 %SOURCE5 %{buildroot}%{_unitdir}/awslogsd.service
install -d -m 755 %{buildroot}%{_sharedstatedir}/awslogs
install -d -m 755 %{buildroot}%{_sysconfdir}/awslogs/config

%post
if [ $1 -eq 1 ] ; then
    # Enable the cwlogs plugin
    export AWS_CONFIG_FILE=%{_sysconfdir}/awslogs/awscli.conf
    aws configure set plugins.cwlogs cwlogs
    aws configure set default.region us-east-1
    # Initial installation
    systemctl preset awslogsd.service >/dev/null 2>&1 || :
fi

%preun
%systemd_preun awslogsd.service

%triggerin -- aws-cli-plugin-cloudwatch-logs, aws-cli
# Need to restart service if aws-cli python modules are updated
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    %systemd_postun awslogsd.service 
fi

%postun
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    %systemd_postun awslogsd.service
fi

%clean
rm -rf %{buildroot}

%files
%{_sbindir}/awslogsd
%{_unitdir}/awslogsd.service
%dir %{_sysconfdir}/awslogs
%dir %{_sysconfdir}/awslogs/config
%config(noreplace) %{_sysconfdir}/awslogs/awslogs.conf
%config(noreplace) %{_sysconfdir}/awslogs/proxy.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/awslogs
%config(noreplace) %ghost %{_sysconfdir}/awslogs/awscli.conf
%dir %{_sharedstatedir}/awslogs

%changelog
* Fri Mar 2 2018 Andrew Egelhofer <egelhofe@amazon.com> - 1.1.4.2
- Bump revision with new Requires: rsyslog
