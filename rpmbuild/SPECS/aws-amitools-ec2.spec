%define     aws_product_name_long         EC2_AMITOOL_HOME
%define       aws_product_version                      1.5.13
%define       aws_product_release                        0
%define          aws_product_name                      ec2

%define aws_product_summary  AWS %{aws_product_name} AMI tools - package %{aws_product_name} AMIs from the command line
%define aws_product_url      http://aws.amazon.com/{%aws_product_name}
%define aws_product_desc     %{aws_product_name} AMI Tools - Amazon-provided tools to bundle %{aws_product_name} AMIs.
%define aws_product_name_env %{aws_product_name_long}

Summary:   %{aws_product_summary}
Name:      aws-amitools-%{aws_product_name}
Version:   %{aws_product_version}
Release:   %{aws_product_release}%{?dist}
License:   Amazon Software License
Group:     System Environment/Base
URL:       http://aws.amazon.com/%{aws_product_name}
Source0:   http://s3.amazonaws.com/ec2-downloads/ec2-ami-tools-%{version}.zip
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Prefix:    /opt
Vendor:    Amazon AWS

Requires:  /sbin/blkid
Requires:  coreutils
Requires:  curl
Requires:  e2fsprogs
Requires:  gzip
Requires:  openssl
Requires:  rsync
Requires:  ruby >= 1.8.2
Requires:  tar

%define aws_path              %{prefix}/aws
%define aws_bin_path          %{aws_path}/bin
%define aws_product_name_v    %{aws_product_name}-%{aws_product_version}
%define aws_product_path      %{aws_path}/amitools/%{aws_product_name_v}
%define aws_product_path_link %{aws_path}/amitools/%{aws_product_name}

%description
%{aws_product_desc}


%prep
%setup -q -n ec2-ami-tools-%{version}


%build
#Released as rb files at this point, no need to build

%___build_post


%install
[ ${RPM_BUILD_ROOT} != "/" ] && %__rm -rf ${RPM_BUILD_ROOT}

# Build installation directory structure
%__mkdir_p %{buildroot}/%{aws_product_path}
%__mkdir   %{buildroot}/%{aws_product_path}/bin
%__mkdir_p %{buildroot}/%{aws_product_path}/lib/%{aws_product_name}
%__mkdir_p %{buildroot}/%{aws_product_path}/etc/%{aws_product_name}

# Install all scripts in bin directory
%__install -m 755 bin/* %{buildroot}/%{aws_product_path}/bin

# Install all text files:
%__install -m 644 *.txt %{buildroot}/%{aws_product_path}/

# Install localized rb files (should go away in future release)
%__cp -a lib/ %{buildroot}/%{aws_product_path}/

# Install etc directory
%__cp -a etc/ %{buildroot}/%{aws_product_path}/

# Build the environment script
echo "#Set %{aws_product_name_env}.  Called from /etc/profile.d/aws-product-common" > %{buildroot}/%{aws_product_path}/environment.sh
echo "[ -z \"\$%{aws_product_name_env}\" ] && %{aws_product_name_env}=\"%{aws_product_path_link}\"" >> %{buildroot}/%{aws_product_path}/environment.sh
echo "export %{aws_product_name_env}" >> %{buildroot}/%{aws_product_path}/environment.sh

%post

# Upgrade- remove old symlink
if [ "$1" = "2" ]; then
    %__rm -f %{aws_product_path_link}
fi

# Install/Upgrade - Create symlink from versioned 
# directory to product name directory if it doesn't exist
if [ ! -e  %{aws_product_path_link} ]; then
    %__ln_s  ./%{aws_product_name_v}  %{aws_product_path_link}
fi

# Create aws bin directory if it doesn't exist:
if [ ! -d %{aws_bin_path} ]; then
    %__mkdir %{aws_bin_path}
fi

# All commands copied to aws bin directory should start
# with product name
for command in %{aws_product_path_link}/bin/%{aws_product_name}*; do
    %define command_name $(basename $command)
    if [ -e %{aws_bin_path}/%{command_name} ]; then
        if [ "$1" = "2" ]; then
            # Upgrade- remove old symlinks
            %__rm -f %{aws_bin_path}/%{command_name}
        fi
    fi
    if [ ! -h %{aws_bin_path}/%{command_name} ]; then
	# Install relative symlink from generic directory to aws shared directory
        %__ln_s ../amitools/%{aws_product_name}/bin/%{command_name}  %{aws_bin_path}/%{command_name}
    fi
done


%preun
# Uninstall: 
if [ "$1" = "0" ]; then
    #Clean up the symlinks if it points to this version
    if [ "x$(readlink %{aws_product_path_link})" == "x./%{aws_product_name_v}" ]; then
        for command in %{aws_bin_path}/%{aws_product_name}*; do
            if [ "x$(readlink $command)" == "x../amitools/%{aws_product_name}/bin/$(basename $command)" ]; then
                %__rm -f $command
            fi
        done
    fi
fi


%postun
if [ "$1" = "0" ]; then
    if [ ! "$(ls -A %{aws_bin_path})" ]; then
        rmdir %{aws_bin_path}
    fi

    %__rm -f %{aws_product_path_link}

    if [ ! "$(ls -A %{aws_path}/amitools)" ]; then
        rmdir %{aws_path}/amitools
    fi

    if [ ! "$(ls -A %{aws_path})" ]; then
        rmdir %{aws_path}
    fi
fi


%clean
[ ${RPM_BUILD_ROOT} != "/" ] && %__rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(0644,root,root,-)

%attr(0755,root,root) %dir %{aws_product_path}

# Scripts installed with execute permission
%attr(0755,root,root) %{aws_product_path}/bin

# Directory structure:
%attr(0755,root,root) %dir %{aws_product_path}/etc
%attr(0755,root,root) %dir %{aws_product_path}/etc/ec2
%attr(0755,root,root) %dir %{aws_product_path}/etc/ec2/amitools
%attr(0755,root,root) %dir %{aws_product_path}/lib
%attr(0755,root,root) %dir %{aws_product_path}/lib/ec2
%attr(0755,root,root) %dir %{aws_product_path}/lib/ec2/common
%attr(0755,root,root) %dir %{aws_product_path}/lib/ec2/amitools
%attr(0755,root,root) %dir %{aws_product_path}/lib/ec2/oem
%attr(0755,root,root) %dir %{aws_product_path}/lib/ec2/platform
%attr(0755,root,root) %dir %{aws_product_path}/lib/ec2/platform/linux
%attr(0755,root,root) %dir %{aws_product_path}/lib/ec2/platform/base
%attr(0755,root,root) %dir %{aws_product_path}/lib/ec2/platform/solaris

# All ruby packages:
%{aws_product_path}/lib/ec2/*.rb
%{aws_product_path}/lib/ec2/common/*.rb
%{aws_product_path}/lib/ec2/amitools/*.rb
%{aws_product_path}/lib/ec2/oem/*.rb
%{aws_product_path}/lib/ec2/platform/*.rb
%{aws_product_path}/lib/ec2/platform/linux/*.rb
%{aws_product_path}/lib/ec2/platform/base/*.rb
%{aws_product_path}/lib/ec2/platform/solaris/*.rb

%{aws_product_path}/lib/ec2/oem/LICENSE.txt

%{aws_product_path}/etc/ec2/amitools/*

%{aws_product_path}/*.txt
%{aws_product_path}/environment.sh

%changelog

* Tue Apr 13 2010 KaOS <kaos@amazon.com>
- Requires: ruby

* Thu Feb 25 2010 KaOS <kaos@amazon.com>
- 1.3.46266
- Initial packaging
