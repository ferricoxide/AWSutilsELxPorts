# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

%define         __spec_install_post %{nil}
%define           debug_package %{nil}
%define         __os_install_post %{_dbpath}/brp-compress

Summary: EC2 instance scripting and configuration for EC2 Instance Connect
Name: ec2-instance-connect
Version: 1.1
Release: 12%{?dist}
License: ASL2.0
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# XXX: We should BR systemd-rpm-macros but AL doesn't appear to support it?
BuildRequires: systemd
Source0: %{name}-%{version}.tar.gz
Source1: ec2-instance-connect.service
Source2: ec2-instance-connect.preset
Requires: openssh >= 6.9.0, coreutils, openssh-server >= 6.9.0, systemd-units, openssl, curl
Requires(pre): /usr/bin/getent, /usr/sbin/useradd, /usr/sbin/usermod, systemd, systemd-units
Requires(post): /bin/grep, /usr/bin/printf, openssh-server >= 6.9.0, systemd, systemd-units
Requires(preun): systemd, systemd-units
Requires(postun): /usr/sbin/userdel, systemd, systemd-units

%description
%{summary}

%prep
%setup -q

%build
# no-op

%install
/bin/rm -rf %{buildroot}
/bin/mkdir -p  %{buildroot}

/usr/bin/install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/ec2-instance-connect.service
# While the former is the RHEL standard, both are populated.  And not symlinked.
/usr/bin/install -D -m 644 %{SOURCE2} %{buildroot}/usr/lib/systemd/system-preset/95-ec2-instance-connect.preset
/usr/bin/install -D -m 644 %{SOURCE2} %{buildroot}/lib/systemd/system-preset/95-ec2-instance-connect.preset

/bin/mkdir -p %{buildroot}/lib/systemd/hostkey.d
/bin/echo 'ec2-instance-connect.service' > %{buildroot}/lib/systemd/hostkey.d/60-ec2-instance-connect.list

# in builddir
/bin/cp -a * %{buildroot}

%clean
/bin/rm -rf %{buildroot}

%files
%defattr(755, root, root, -)
/opt/aws/bin/eic_run_authorized_keys
/opt/aws/bin/eic_curl_authorized_keys
/opt/aws/bin/eic_parse_authorized_keys
/opt/aws/bin/eic_harvest_hostkeys
%defattr(644, root, root, -)
%{_unitdir}/ec2-instance-connect.service
/lib/systemd/hostkey.d/60-ec2-instance-connect.list
/lib/systemd/system-preset/95-ec2-instance-connect.preset
/usr/lib/systemd/system-preset/95-ec2-instance-connect.preset

%pre
# Create/configure system user
/usr/bin/getent passwd ec2-instance-connect || /usr/sbin/useradd -r -M -s /sbin/nologin ec2-instance-connect
/usr/sbin/usermod -L ec2-instance-connect

%post
%systemd_post ec2-instance-connect.service
# XXX: As our service is a oneshot, the RPM macros don't actually start it :(
/usr/bin/systemctl start ec2-instance-connect

AUTH_KEYS_CMD="AuthorizedKeysCommand /opt/aws/bin/eic_run_authorized_keys %u %f"
AUTH_KEYS_USR="AuthorizedKeysCommandUser ec2-instance-connect"

modified=1

# Configure sshd to use EC2 Instance Connect's AuthorizedKeysCommand
# If there's old, stale config, remove it
# Oldest: curl_authorized_keys directly
if /bin/grep -q "^AuthorizedKeysCommand[[:blank:]]\(/usr/bin/timeout[[:blank:]]5s[[:blank:]]\)\?/opt/aws/bin/curl_authorized_keys\([[:blank:]]\%u[[:blank:]]\%f\)\?$" /etc/ssh/sshd_config ; then
    if /bin/grep -q "^AuthorizedKeysCommandUser[[:blank:]]ec2-instance-connect$" /etc/ssh/sshd_config ; then
        /bin/sed -i "\~^AuthorizedKeysCommand[[:blank:]]/usr/bin/timeout[[:blank:]]5s[[:blank:]]/opt/aws/bin/curl_authorized_keys[[:blank:]]%u[[:blank:]]%f$~d" /etc/ssh/sshd_config
        /bin/sed -i "\~^AuthorizedKeysCommand[[:blank:]]/usr/bin/timeout[[:blank:]]5s[[:blank:]]/opt/aws/bin/curl_authorized_keys$~d" /etc/ssh/sshd_config
        /bin/sed -i "\~^AuthorizedKeysCommand[[:blank:]]/opt/aws/bin/curl_authorized_keys[[:blank:]]%u[[:blank:]]%f$~d" /etc/ssh/sshd_config
        /bin/sed -i "\~^AuthorizedKeysCommand[[:blank:]]/opt/aws/bin/curl_authorized_keys$~d" /etc/ssh/sshd_config
        /bin/sed -i "\~^AuthorizedKeysCommandUser[[:blank:]]ec2-instance-connect$~d" /etc/ssh/sshd_config
        /usr/bin/printf "%s\n%s\n" "#AuthorizedKeysCommand none" "#AuthorizedKeysCommandUser nobody" >> /etc/ssh/sshd_config
        modified=0
    fi
fi
# Intermediate: (eic_)run_authorized_keys
if /bin/grep -q "^AuthorizedKeysCommand[[:blank:]]/opt/aws/bin/\(eic_\)\?run_authorized_keys\([[:blank:]]\%u[[:blank:]]\%f\)\?$" /etc/ssh/sshd_config ; then
    if /bin/grep -q "^AuthorizedKeysCommandUser[[:blank:]]ec2-instance-connect$" /etc/ssh/sshd_config ; then
        /bin/sed -i "\~^AuthorizedKeysCommand[[:blank:]]/opt/aws/bin/eic_run_authorized_keys[[:blank:]]%u[[:blank:]]%f$~d" /etc/ssh/sshd_config
        /bin/sed -i "\~^AuthorizedKeysCommand[[:blank:]]/opt/aws/bin/eic_run_authorized_keys$~d" /etc/ssh/sshd_config
        /bin/sed -i "\~^AuthorizedKeysCommand[[:blank:]]/opt/aws/bin/run_authorized_keys[[:blank:]]%u[[:blank:]]%f$~d" /etc/ssh/sshd_config
        /bin/sed -i "\~^AuthorizedKeysCommand[[:blank:]]/opt/aws/bin/run_authorized_keys$~d" /etc/ssh/sshd_config
        /bin/sed -i "\~^AuthorizedKeysCommandUser[[:blank:]]ec2-instance-connect$~d" /etc/ssh/sshd_config
        /usr/bin/printf "%s\n%s\n" "#AuthorizedKeysCommand none" "#AuthorizedKeysCommandUser nobody" >> /etc/ssh/sshd_config
        modified=0
    fi
fi

# If the default, commented out none/nobody is present drop it
if ! /bin/grep -q "^.*AuthorizedKeysCommandRunAs[[:blank:]]\+.*$" /etc/ssh/sshd_config ; then
    if /bin/grep -q '^#AuthorizedKeysCommand[[:blank:]]none$' /etc/ssh/sshd_config ; then
        if /bin/grep -q '^#AuthorizedKeysCommandUser[[:blank:]]nobody$' /etc/ssh/sshd_config ; then
            /bin/sed -i '/^#AuthorizedKeysCommand[[:blank:]]none$/d' /etc/ssh/sshd_config
            /bin/sed -i '/^#AuthorizedKeysCommandUser[[:blank:]]nobody$/d' /etc/ssh/sshd_config
            # We don't need to mark for restart - all we did was remove commented-out config
        fi
    fi
fi

# If there is nothing in the AuthorizedKeysCommand field of sshd_config *and* nothing in any sshd override, add our config
if ! /bin/grep -q "^.*AuthorizedKeysCommand[[:blank:]]\+.*$" /etc/ssh/sshd_config ; then
    if ! /bin/grep -q "^.*AuthorizedKeysCommandUser[[:blank:]]\+.*$" /etc/ssh/sshd_config ; then
        if ! /bin/grep -q "^.*AuthorizedKeysCommandRunAs[[:blank:]]\+.*$" /etc/ssh/sshd_config ; then
            # If systemd unit contains AKC don't override it
            if ! /bin/grep -q "AuthorizedKeysCommand" /lib/systemd/system/sshd.service ; then
                can_modify=1
                if [ -d /lib/systemd/system/sshd.service.d ] ; then
                    # If *any* override contains an ExecStart, don't override it
                    if ! /bin/grep -Rq "ExecStart" /lib/systemd/system/sshd.service.d/ ; then
                        can_modify=0
                    fi
                else
                    # Or there are no overrides
                    can_modify=0
                fi
                if [ $can_modify -eq 0 ] ; then
                    # Add our configuration
                    /usr/bin/printf "\n%s\n%s\n" "${AUTH_KEYS_CMD}" "${AUTH_KEYS_USR}" >> /etc/ssh/sshd_config
                    modified=0
                fi
            fi
        fi
    fi
fi

if [ $modified -eq 0 ] ; then
    # Restart sshd
    %if 0%{?amzn} >= 2
        systemctl daemon-reload
        if /bin/systemctl is-active --quiet sshd ; then
            /bin/systemctl restart sshd
        fi
    %else
        if /usr/sbin/service sshd status 1>/dev/null 2>/dev/null ; then
            /usr/sbin/service sshd restart
        fi
    %endif
fi

%preun
%systemd_preun ec2-instance-connect.service

if [ $1 -eq 0 ] ; then
    modified=1

    # Remove EC2 Instance Connect sshd override if present
    if /bin/grep -q "^AuthorizedKeysCommandUser[[:blank:]]ec2-instance-connect$" /etc/ssh/sshd_config ; then
        if /bin/grep -q "^AuthorizedKeysCommand[[:blank:]]/opt/aws/bin/eic_run_authorized_keys[[:blank:]]%u[[:blank:]]%f$" /etc/ssh/sshd_config ; then
            /bin/sed -i "\%^AuthorizedKeysCommand[[:blank:]]/opt/aws/bin/eic_run_authorized_keys.*$%d" /etc/ssh/sshd_config
            /bin/sed -i "/^.*AuthorizedKeysCommandUser[[:blank:]]ec2-instance-connect$/d" /etc/ssh/sshd_config
            /usr/bin/printf "\n%s\n%s\n" "#AuthorizedKeysCommand none" "#AuthorizedKeysCommandUser nobody" >> /etc/ssh/sshd_config
            modified=0
        fi
    fi

    # Restart sshd
    if [ $modified -eq 0 ] ; then
        %if 0%{?amzn} >= 2
            /bin/systemctl daemon-reload
            if /bin/systemctl is-active --quiet sshd ; then
                /bin/systemctl restart sshd
            fi
        %else
            if /usr/sbin/service sshd status 1>/dev/null 2>/dev/null ; then
                /usr/sbin/service sshd restart
            fi
        %endif
    fi
fi

%postun
%systemd_postun_with_restart ec2-instance-connect.service

if [ $1 -eq 0 ] ; then
    # Delete system user
    /usr/sbin/userdel ec2-instance-connect
fi

%changelog
* Tue Nov 19 2019 Daniel Anderson <dnde@amazon.com> 1.1-12
- Adding support for Instance Metadata Service Version 2
- Modifying cURL invocation to avoid need for eval
- Cleaning up shellcheck catches
* Wed Aug 21 2019 Daniel Anderson <dnde@amazon.com> 1.1-11
- Removing errant write to /tmp
- Cleaning up bad bash practices, including umask race condition
* Wed Jul 3 2019  Daniel Anderson <dnde@amazon.com> 1.1-10
- Fix for an update to openssl (or dependencies) affecting behavior of CApath option on openssl verify
- Adding additional licensing headers
- Fixing Nitro behavior of hostkey harvesting and post-installation systemd hooks
* Wed May 15 2019  Daniel Anderson <dnde@amazon.com> 1.1-9
- Improved mechanism for detection if script is running on an EC2 instance
* Wed Apr 24 2019  Daniel Anderson <dnde@amazon.com> 1.1-8
- Better cleanup of sshd_config changes
- Better detection of existing user customization
* Fri Mar 29 2019  Daniel Anderson <dnde@amazon.com> 1.1-7
- Change to Amazon Linux configuration
* Wed Mar 20 2019  Daniel Anderson <dnde@amazon.com> 1.1-6
- Verification of EC2 hypervisor UUID
* Fri Mar 15 2019  Daniel Anderson <dnde@amazon.com> 1.1-5
- Added slightly stronger checks that we're getting valid data from Instance Metadata Service/on an instance
* Wed Jan 30 2019  Daniel Anderson <dnde@amazon.com> 1.1-4
- Fixed a bug in reading instance-identity credentials as part of hostkey harvesting and dropped AWS CLI dependency
- Added support for non-Amazon Linux yum distributions, such as RHEL and CentOS
- Hardened error handling
* Fri Dec 21 2018  Daniel Anderson <dnde@amazon.com> 1.1-3
- Fixing an issue with the hostkey harvesting script - it was using default creds instead of instance-identity
* Fri Dec 7 2018  Daniel Anderson <dnde@amazon.com> 1.1-2
- Minor changes to package build process to share code with Debian packaging
* Tue Oct 23 2018  Anshumali Prasad <anspr@amazon.com> 1.1-1
- Hostkey harvesting for EC2 Instance Connect.
* Mon Oct 22 2018  Daniel Anderson <dnde@amazon.com> 1.0-3
- Updating exit status on no-data case, improving support for newer openssl versions
* Tue Oct 9 2018  Daniel Anderson <dnde@amazon.com> 1.0-2
- Cleaning up package requirements & post installation hook
* Wed Jun 13 2018  Daniel Anderson <dnde@amazon.com> 1.0-1
- Initial RPM build for EC2 Instance Connect targeting Amazon Linux 2.
