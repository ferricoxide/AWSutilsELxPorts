%define aws_product_name_env  EC2_HOME
%define aws_product_name      ec2

Summary:   The API tools serve as the client interface to the Amazon EC2 web service. Use these tools to register and launch instances, manipulate security groups, and more. 
Name:      aws-apitools-%{aws_product_name}
Version:   1.7.3.0
Release:   2%{?dist}
License:   Amazon Software License
Group:     Amazon/Tools
# http://aws.amazon.com/developertools/351
URL:       http://aws.amazon.com/%{aws_product_name}
Source0:   https://ec2-downloads.s3.amazonaws.com/ec2-api-tools-%{version}.zip
BuildArch: noarch
Prefix:    /opt
Vendor:    Amazon AWS
Requires:  jre-headless >= 1.6.0
Requires:  aws-apitools-common

%define aws_path              %{prefix}/aws
%define aws_bin_path          %{aws_path}/bin
%define aws_product_name_v    %{aws_product_name}-%{version}
%define aws_product_path      %{aws_path}/apitools/%{aws_product_name_v}
%define aws_product_path_link %{aws_path}/apitools/%{aws_product_name}

%description
Amazon Elastic Compute Cloud (Amazon EC2) is a web service that
provides resizable compute capacity in the cloud. It is designed to
make web-scale computing easier for developers.

Amazon EC2's simple web service interface allows you to obtain and
configure capacity with minimal friction. It provides you with
complete control of your computing resources and lets you run on
Amazon's proven computing environment. Amazon EC2 reduces the time
required to obtain and boot new server instances to minutes,
allowing you to quickly scale capacity, both up and down, as your
computing requirements change. Amazon EC2 changes the economics of
computing by allowing you to pay only for capacity that you
actually use. Amazon EC2 provides developers the tools to build
failure resilient applications and isolate themselves from common
failure scenarios.

%prep
%setup -q -n ec2-api-tools-%{version}

%build
#Released as jar files at this point, no need to build

# Make sure we don't install .cmd files
%__rm bin/*.cmd
%___build_post

%install
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
    %__ln_s %{aws_product_path}/bin/%{command_name} \
        %{buildroot}/%{aws_bin_path}/%{command_name}
done

# Build the environment script
echo "# Set %{aws_product_name_env}.  Called from /etc/profile.d/aws-product-common" > %{buildroot}/%{aws_product_path}/environment.sh
echo "[ -z \"\$%{aws_product_name_env}\" ] && %{aws_product_name_env}=\"%{aws_product_path_link}\"" >> %{buildroot}/%{aws_product_path}/environment.sh
echo "export %{aws_product_name_env}" >> %{buildroot}/%{aws_product_path}/environment.sh


%files
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
* Tue Apr 13 2010 KaOS <kaos@amazon.com>
- Requires: jre

* Thu Feb 25 2010 KaOS <kaos@amazon.com>
- 1.3.46266
- Initial packaging
