%global aws_product_name      cfn-init
%global aws_path              /opt/aws
%global aws_bin_path          %{aws_path}/bin
%global aws_product_name_v    %{aws_product_name}-%{version}-%{release}
%global aws_product_path      %{aws_path}/apitools/%{aws_product_name_v}
%global aws_product_path_link %{aws_path}/apitools/%{aws_product_name}

%global upstream_rev 31

Summary: An EC2 bootstrapper for CloudFormation
Name: aws-cfn-bootstrap
Version: 1.4
Release: %{upstream_rev}%{?dist}
Source0: https://s3.amazonaws.com/cfn-init-staging/%{name}-%{version}-%{upstream_rev}.tar.gz
License: Apache 2.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
BuildRequires: python
Requires: python-daemon
Requires: pystache
Requires: python-setuptools
Provides: bundled(python-requests) = 2.6.0
Url: http://aws.amazon.com/cloudformation/

%description
Bootstraps EC2 instances by retrieving and processing the Metadata block of a CloudFormation resource.

%prep
%setup -n %{name}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES --install-scripts=%{aws_product_path}/bin --install-data=%{aws_product_path}

# Install/Upgrade - Create symlink from versioned
# directory to product name directory if it doesn't exist
pushd  %{buildroot}/%{aws_path}/apitools
 ln -s  ./%{aws_product_name_v} %{aws_product_name}
popd

# Create aws bin directory if it doesn't exist:
if [ ! -d %{buildroot}/%{aws_bin_path} ]; then
    mkdir %{buildroot}/%{aws_bin_path}
fi

pushd %{buildroot}/%{aws_path}
for command in apitools/%{aws_product_name}/bin/*; do
    %define command_name $(basename $command)
    # Install relative symlink from generic directory to aws shared directory
    ln -s ../apitools/%{aws_product_name}/bin/%{command_name}  bin/%{command_name}
done
popd
# Create link to init script
mkdir -p %{buildroot}/%{_initrddir}
pushd %{buildroot}/
ln -s ../../..%{aws_product_path_link}/init/redhat/cfn-hup  .%{_initrddir}/cfn-hup
popd
chmod 755 %{buildroot}/%{_initrddir}/cfn-hup
chmod 755 %{buildroot}/%{aws_product_path_link}/init/redhat/cfn-hup

%clean
rm -rf $RPM_BUILD_ROOT

%postun
if [ "$1" = "0" ]; then
    if [ ! "$(ls -A %{aws_bin_path})" ]; then
        rmdir %{aws_bin_path}
    fi
    if [ ! "$(ls -A %{aws_path}/apitools)" ]; then
        rmdir %{aws_path}/apitools
    fi

    if [ ! "$(ls -A %{aws_path})" ]; then
        rmdir %{aws_path}
    fi
fi

%files -f INSTALLED_FILES
%{_initrddir}/cfn-hup
%{aws_path}/apitools/cfn-init
%{aws_path}/apitools/%{aws_product_name_v}
%{aws_path}/bin/cfn-elect-cmd-leader
%{aws_path}/bin/cfn-get-metadata
%{aws_path}/bin/cfn-hup
%{aws_path}/bin/cfn-init
%{aws_path}/bin/cfn-send-cmd-event
%{aws_path}/bin/cfn-send-cmd-result
%{aws_path}/bin/cfn-signal


%changelog
* Fri Jan 04 2019 Heath Petty <hpetty@amazon.com> - 1.4-31
- Update to 1.4-31

* Fri Aug 20 2017 Praveen K paladugu <praween@amazon.com> - 1.4-21
- Package aws-cfn-bootstrap for amzn2
