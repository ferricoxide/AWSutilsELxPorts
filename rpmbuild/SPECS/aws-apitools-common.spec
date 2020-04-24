%define  aws_product_version     1.1.0
%define  aws_product_release         2
%define     aws_product_name    common

%define aws_product_summary  AWS %{aws_product_name} - provides directory structure and common configuration files 
%define aws_product_url      http://aws.amazon.com
%define aws_product_desc     %{aws_product_summary}

Summary:   %{aws_product_summary}
Name:      aws-apitools-%{aws_product_name}
Version:   %{aws_product_version}
Release:   %{aws_product_release}%{?dist}
License:   Amazon Software License
Group:     System Environment/Base
URL:       %{aws_product_url}
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Prefix:    /opt
Vendor:    Amazon AWS

Requires:  coreutils
Requires:  jre-headless >= 1.6.0

%define aws_path              %{prefix}/aws
%define aws_bin_path          %{aws_path}/bin
%define aws_profile_path      %{_sysconfdir}/profile.d

%description
%{aws_product_desc}

%prep

%build
# Nothing to build
%___build_post

%install
%__mkdir_p %{buildroot}%{aws_path}
%__mkdir_p %{buildroot}%{aws_path}/amitools
%__mkdir_p %{buildroot}%{aws_path}/apitools
%__mkdir_p %{buildroot}%{aws_path}/bin
%__mkdir_p %{buildroot}%{aws_profile_path}

# Create credential-file-path.template
cat <<EOF> %{buildroot}%{aws_path}/credential-file-path.template
AWSAccessKeyId=<Write your AWS access ID>
AWSSecretKey=<Write your AWS secret key>
EOF

# Create profile.d script
cat <<EOF> %{buildroot}%{aws_profile_path}/%{name}.sh
# Set path for AWS API tools packages
export AWS_PATH=/opt/aws
export PATH=\$PATH:\$AWS_PATH/bin

if [ -z "\${JAVA_HOME}" ]; then
    if [ -d /usr/java/latest ]; then
        # prefer third-party JDK if present
        export JAVA_HOME=/usr/java/latest
    elif [ -d /usr/lib/jvm/java ]; then
        export JAVA_HOME=/usr/lib/jvm/java
    elif [ -d /usr/lib/jvm/jre ]; then
        export JAVA_HOME=/usr/lib/jvm/jre
    fi
fi

# Source environment variables for each set of tools

for aws_product in \$(find %{aws_path}/apitools %{aws_path}/amitools -maxdepth 1 -type l 2>/dev/null); do
    [ -e \$aws_product/environment.sh ] && source \$aws_product/environment.sh
done
unset aws_product

# Uncomment this line to specify AWS_CREDENTIAL_FILE
# (see %{aws_path}/credential-file-path.template)
#export AWS_CREDENTIAL_FILE=/opt/aws/credentials.txt
EOF

%clean
[ %{buildroot} != "/" ] && %__rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{aws_path}
%dir %{aws_path}/amitools
%dir %{aws_path}/apitools
%dir %{aws_path}/bin
%{aws_path}/credential-file-path.template
%{aws_profile_path}/%{name}.sh

%changelog
* Tue Jul 22 2010 KaOS <kaos@amazon.com>
- No longer setting AWS_CREDENTIAL_FILE by default

* Tue Apr 13 2010 KaOS <kaos@amazon.com>
- Requires: jre
- Set JAVA_HOME in profile.d

* Thu Mar 8 2010 KaOS <kaos@amazon.com>
- 1.0.0
- Initial packaging
