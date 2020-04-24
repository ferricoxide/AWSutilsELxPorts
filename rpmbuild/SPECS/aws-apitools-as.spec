%define aws_product_name_env  AWS_AUTO_SCALING_HOME
%define aws_product_name      as

Summary:   The Command Line Tool serves as the client interface to the Auto Scaling web service. Use this tool to create auto scaling groups and define triggers to launch and terminate Amazon EC2 instances automatically.
Name:      aws-apitools-%{aws_product_name}
Version:   1.0.61.6
Release:   2%{?dist}
License:   Amazon Software License
Group:     Amazon/Tools
# http://aws.amazon.com/developertools/2535
URL:       http://aws.amazon.com/autoscaling/
Source0:   %{name}-%{version}.zip
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Prefix:    /opt
Vendor:    Amazon AWS
Requires:  coreutils
Requires:  jre-headless >= 1.6.0
Requires:  aws-apitools-common
BuildRequires: dos2unix

%define aws_path              %{prefix}/aws
%define aws_bin_path          %{aws_path}/bin
%define aws_product_name_v    %{aws_product_name}-%{version}
%define aws_product_path      %{aws_path}/apitools/%{aws_product_name_v}
%define aws_product_path_link %{aws_path}/apitools/%{aws_product_name}

%description
Auto Scaling allows you to scale your Amazon EC2 capacity up or down automatically according to conditions you define. With Auto Scaling, you can ensure that the number of Amazon EC2 instances you're using increases seamlessly during demand spikes to maintain performance, and decreases automatically during demand lulls to minimize costs. Auto Scaling is particularly well suited for applications that experience hourly, daily, or weekly variability in usage. Auto Scaling is enabled by Amazon CloudWatch and available at no additional charge beyond Amazon CloudWatch fees.

%prep
%setup -q -n AutoScaling-%{version}
for i in $(find %{_builddir} -type f); do
    if [ ! "$(file $i | grep CRLF)" = "" ]; then
        dos2unix $i
    fi
done

%build
#Released as jar files at this point, no need to build

# Make sure we don't install .cmd files
%__rm bin/*.cmd
%___build_post

%install
[ ${RPM_BUILD_ROOT} != "/" ] && %__rm -rf ${RPM_BUILD_ROOT}

# Build installation directory structure
%__mkdir_p %{buildroot}/%{aws_product_path}
%__mkdir   %{buildroot}/%{aws_product_path}/bin
%__mkdir   %{buildroot}/%{aws_product_path}/lib
%__ln_s    %{aws_product_name_v} %{buildroot}/%{aws_product_path_link}

%__mkdir_p %{buildroot}/%{aws_bin_path}

# Install all scripts in bin directory
%__install -m 755 bin/* %{buildroot}/%{aws_product_path}/bin

# Install all text files:
%__install -m 644 *.txt  %{buildroot}/%{aws_product_path}/
%__install -m 644 *.TXT  %{buildroot}/%{aws_product_path}/

# Install Java libs
%__install -m 755 lib/* %{buildroot}/%{aws_product_path}/lib

# Create sym links
for i in %{buildroot}/%{aws_product_path}/bin/*; do
    %define command_name $(basename $i)
    if [ "%{command_name}" = "service" ]; then
        continue
    fi
    %__ln_s %{aws_product_path}/bin/%{command_name} \
        %{buildroot}/%{aws_bin_path}/%{command_name}
done

# Build the environment script
echo "# Set %{aws_product_name_env}.  Called from /etc/profile.d/aws-product-common" > %{buildroot}/%{aws_product_path}/environment.sh
echo "[ -z \"\$%{aws_product_name_env}\" ] && %{aws_product_name_env}=\"%{aws_product_path_link}\"" >> %{buildroot}/%{aws_product_path}/environment.sh
echo "export %{aws_product_name_env}" >> %{buildroot}/%{aws_product_path}/environment.sh

%clean
[ ${RPM_BUILD_ROOT} != "/" ] && %__rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(0644,root,root,-)
%doc %{aws_product_path}/*.txt
%doc %{aws_product_path}/*.TXT

%attr(0755,root,root) %dir %{aws_product_path}
%attr(0755,root,root) %dir %{aws_product_path}/lib

# Scripts installed with execute permission
%attr(0755,root,root) %dir %{aws_product_path}/bin
%attr(0755,root,root) %dir %{aws_bin_path}

# The sym links for easy access
%{aws_bin_path}/*
%{aws_product_path_link}

# Everything else
%{aws_product_path}/lib/*
%attr(0755,root,root) %{aws_product_path}/bin/*
%{aws_product_path}/environment.sh

%changelog
* Tue Aug 09 2011 Nathan Blackham <blackham@amazon.com>
- add compat libs 

* Tue Apr 13 2010 KaOS <kaos@amazon.com>
- Requires: jre

* Thu Feb 25 2010 KaOS <kaos@amazon.com>
- 1.0.9.0
- Initial packaging

