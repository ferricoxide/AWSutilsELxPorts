%define _trivial .0
%define _buildid .1
%global packagename awscli-cwlogs

Summary:        CloudWatch Logs plugin for aws-cli
Name:           aws-cli-plugin-cloudwatch-logs
Version:        1.4.6
Release:        1%{?dist}%{?_trivial}%{?_buildid}
License:        ASL 2.0
Group:          Amazon/Tools
URL:            http://aws.amazon.com/cloudwatch
Source:         http://aws-cloudwatch.s3-website-us-east-1.amazonaws.com/%{packagename}/%{packagename}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildArch:      noarch
# The minimum version of aws-cli required is defined in setup.py of the source.
Requires:       awscli >= 1.11.41
Requires:       python-six >= 1.1.0
Requires:       python-dateutil >= 2.1
Provides:       %{packagename} = %{version}-%{release}
Provides:       %{name}(python) = %{version}-%{release}


%description
Amazon CloudWatch Logs is used to monitor, store, and access your system,
application, and custom log files from Amazon Elastic Compute Cloud
(Amazon EC2) instances or other sources. You can then retrieve the
associated log data from CloudWatch Logs using the Amazon CloudWatch
console, the CloudWatch Logs commands in the AWS CLI, or the CloudWatch
Logs SDK.

%prep
%setup -q -n %{packagename}-%{version}

%build
%__python setup.py build

%install
rm -rf %{buildroot}
%__python setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%doc CHANGELOG.rst LICENSE.txt MANIFEST.in
%doc README.rst
%{python_sitelib}/awscli_cwlogs-%{version}-py2.7.egg-info/PKG-INFO
%{python_sitelib}/awscli_cwlogs-%{version}-py2.7.egg-info/SOURCES.txt
%{python_sitelib}/awscli_cwlogs-%{version}-py2.7.egg-info/dependency_links.txt
%{python_sitelib}/awscli_cwlogs-%{version}-py2.7.egg-info/requires.txt
%{python_sitelib}/awscli_cwlogs-%{version}-py2.7.egg-info/top_level.txt
%{python_sitelib}/cwlogs/__init__.py*
%{python_sitelib}/cwlogs/filter.py*
%{python_sitelib}/cwlogs/kvstore.py*
%{python_sitelib}/cwlogs/parser.py*
%{python_sitelib}/cwlogs/pull.py*
%{python_sitelib}/cwlogs/push.py*
%{python_sitelib}/cwlogs/retry.py*
%{python_sitelib}/cwlogs/threads.py*
%{python_sitelib}/cwlogs/utils.py*
%dir %{python_sitelib}/cwlogs/examples
%dir %{python_sitelib}/cwlogs/examples/logs
%{python_sitelib}/cwlogs/examples/logs/pull.rst
%{python_sitelib}/cwlogs/examples/logs/push.rst
%{python_sitelib}/cwlogs/examples/logs/filter.rst

%changelog
* Tue Feb 25 2020 Chanchal Mathew <chancham@amazon.com> - 1.4.6-1
- Bump version to 1.4.6-1

* Wed Dec 06 2017 Heath Petty <hpetty@amazon.com> - 1.4.4-1
- Initial build for amzn2
