%define aws_product_name_env  AWS_CLOUDFORMATION_HOME
%define aws_product_name      cfn

Summary:   The command line interface to the AWS CloudFormation web service
Name:      aws-apitools-%{aws_product_name}
Version:   1.0.12
Release:   2%{?dist}
License:   Amazon Software License
Group:     Amazon/Tools
# http://aws.amazon.com/developertools/2555753788650372
URL:       http://aws.amazon.com/%{aws_product_name}
Source0:   aws-apitools-%{aws_product_name}-%{version}.zip
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Prefix:    /opt
Vendor:    Amazon AWS
Requires:  coreutils
Requires:  jre-headless >= 1.6.0
Requires:  aws-apitools-common >= 1.0.1

%define aws_path              %{prefix}/aws
%define aws_bin_path          %{aws_path}/bin
%define aws_product_name_v    %{aws_product_name}-%{version}
%define aws_product_path      %{aws_path}/apitools/%{aws_product_name_v}
%define aws_product_path_link %{aws_path}/apitools/%{aws_product_name}

%description
AWS CloudFormation gives developers and systems administrators an easy way
to create and manage a collection of related AWS resources, provisioning and
updating them in an orderly and predictable fashion.

You can use AWS CloudFormation's sample templates or create your own
templates to describe the AWS resources, and any associated dependencies or
runtime parameters, required to run your application. You don't need to
figure out the order in which AWS services need to be provisioned or the
subtleties of how to make those dependencies work. CloudFormation takes care
of this for you. Once deployed, you can modify and update the AWS resources
in a controlled and predictable way allowing you to version control your AWS
infrastructure in the same way as you version control your software.

You can deploy and update a template and its associated collection of
resources (called a stack) via the AWS Management Console, CloudFormation
command line tools or APIs. CloudFormation is available at no additional
charge, and you pay only for the AWS resources needed to run your
applications.

%prep
%setup -q -n AWSCloudFormation-%{version}

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
%{aws_product_path}/*.txt
%{aws_product_path}/*.TXT
%{aws_product_path}/environment.sh

%changelog
* Tue Apr 13 2010 KaOS <kaos@amazon.com>
- Requires: jre

* Thu Feb 25 2010 KaOS <kaos@amazon.com>
- 1.0.3.4
- Initial packaging
