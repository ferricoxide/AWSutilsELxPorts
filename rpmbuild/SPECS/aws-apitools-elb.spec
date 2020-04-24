%define aws_product_name_env  AWS_ELB_HOME
%define aws_product_name      elb

Summary:   The API tools serve as the client interface to the Elastic Load Balancing web service. Use these tools to create elastic load balancers and register instances to load balance your application running in Amazon EC2. 
Name:      aws-apitools-%{aws_product_name}
Version:   1.0.35.0
Release:   2%{?dist}
License:   Amazon Software License
Group:     Amazon/Tools
# http://aws.amazon.com/developertools/Amazon-EC2/2536
URL:       http://aws.amazon.com/elasticloadbalancing/
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
Elastic Load Balancing automatically distributes incoming application traffic across multiple Amazon EC2 instances. It enables you to achieve even greater fault tolerance in your applications, seamlessly providing the amount of load balancing capacity needed in response to incoming application traffic. Elastic Load Balancing detects unhealthy instances within a pool and automatically reroutes traffic to healthy instances until the unhealthy instances have been restored. Customers can enable Elastic Load Balancing within a single Availability Zone or across multiple zones for even more consistent application performance. Elastic Load Balancing can also be used in an Amazon Virtual Private Cloud ("VPC") to distribute traffic between application tiers.

%prep
%setup -q -n ElasticLoadBalancing-%{version}
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

