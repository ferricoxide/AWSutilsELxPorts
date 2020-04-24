To build the source-RPMs found in this project a couple of things will be necessary:

## Preparing the build-environment

1. The host/container used to build the binary RPMs will need the following packages and package-groups installed:

    - `createrepo`
    - `dos2unix`
    - `git`
    - `golang`
    - `libnsl`
    - `python3`
    - `python-rpm-macros`
    - `rpm-build`
    - `rpmdevtools`
    - `rpm-sign`
    - `unzip`
    - `wget`
    - `@development`

1. It will be necessary to have  correctly set up `${HOME}/.rpmmacros` file. File-contents similar to the following should suffice:

    ~~~
    %_topdir %(echo $HOME)/rpmbuild
    
    %__arch_install_post \
        [ "%{buildarch}" = "noarch" ] || QA_CHECK_RPATHS=1 ; \
        case "${QA_CHECK_RPATHS:-}" in [1yY]*) /usr/lib/rpm/check-rpaths ;; esac \
        /usr/lib/rpm/check-buildroot
    
    # Package-signing stuff
    %_gpgbin /usr/bin/gpg
    %_gpg_bin /usr/bin/gpg
    %_gpg_path %(echo $HOME)/.gnupg
    %_gpg_name <KEY_ID_HEXSTRING>
    %_signature gpg
    ## %__gpg_sign_cmd %{__gpg} gpg --batch --verbose --no-armor --passphrase-fd 3 --no-secmem-warning -u "%{_gpg_name}" -sbo %{__signature_filename} --digest-algo sha256 %{__plaintext_filename}'
    %__gpg_sign_cmd %{__gpg} gpg --batch --verbose --no-armor --no-secmem-warning -u "%{_gpg_name}" -sbo %{__signature_filename} --digest-algo sha256 %{__plaintext_filename}'
    
    %__python /usr/bin/python3

    ~~~

1. Even with the above, when invoking `rpmbuild`, it will likely to be necessary to override the value of `%_topdir` set in the `${HOME}/.rpmmacros` file. This can be done with an invocation similar to:

    ~~~
    rpmbuild --define '_topdir %(echo $HOME)/GIT/AWSutilsElx/rpmbuild' -ba ${SPEC} 
    ~~~

## Known to build

- `amazonlinux-indexhtml`
- `amazon-linux-onprem`
- `aws-amitools-ec2`
- `aws-apitools-as`
- `aws-apitools-cfn`
- `aws-apitools-common`
- `aws-apitools-ec2`
- `aws-apitools-elb`
- `aws-apitools-mon`
- `ec2-instance-connect`
- `ec2-net-utils`
- `ec2-utils`

## Known to fail building

- Python2 Dependencies in SRPMs/RPMs:
    - `amazon-linux-extras`
    - `aws-cfn-bootstrap` (installable via `pip2`)
    - `awscli` (installable via `pip3`)
    - `aws-cli-plugin-cloudwatch-logs`
    - `awslogs` (installable via `pip3`)
    - `ec2-hibinit-agent`
    - `ec2sys-autotune`

- `amazon-ecr-credential-helper` fails with:

    ~~~
    error: Missing build-id in /home/thjones2/GIT/AWSutilsElx/rpmbuild/BUILDROOT/amazon-ecr-credential-helper-0.3.0-1.el8.x86_64/usr/bin/docker-credential-ecr-login
    error: Generating build-id links failed
    
    RPM build errors:
        Missing build-id in /home/thjones2/GIT/AWSutilsElx/rpmbuild/BUILDROOT/amazon-ecr-credential-helper-0.3.0-1.el8.x86_64/usr/bin/docker-credential-ecr-login
        Generating build-id links failed
    ~~~

- `amazon-efs-utils` fails with:

    ~~~
    *** ERROR: ambiguous python shebang in /usr/bin/amazon-efs-mount-watchdog: #!/usr/bin/env python. Change it to python3 (or python2) explicitly.
    *** ERROR: ambiguous python shebang in /sbin/mount.efs: #!/usr/bin/env python. Change it to python3 (or python2) explicitly.
    error: Bad exit status from /var/tmp/rpm-tmp.L54jtz (%install)
    
    
    RPM build errors:
        Bad exit status from /var/tmp/rpm-tmp.L54jtz (%install)
    ~~~

- `amazon-ssm-agent` fails with:

    ~~~
    RPM build errors:
        Missing build-id in /home/thjones2/GIT/AWSutilsElx/rpmbuild/BUILDROOT/amazon-ssm-agent-2.3.714.0-1.el8.x86_64/usr/bin/amazon-ssm-agent
        Missing build-id in /home/thjones2/GIT/AWSutilsElx/rpmbuild/BUILDROOT/amazon-ssm-agent-2.3.714.0-1.el8.x86_64/usr/bin/ssm-document-worker
        Missing build-id in /home/thjones2/GIT/AWSutilsElx/rpmbuild/BUILDROOT/amazon-ssm-agent-2.3.714.0-1.el8.x86_64/usr/bin/ssm-session-worker
        Missing build-id in /home/thjones2/GIT/AWSutilsElx/rpmbuild/BUILDROOT/amazon-ssm-agent-2.3.714.0-1.el8.x86_64/usr/bin/ssm-session-logger
        Missing build-id in /home/thjones2/GIT/AWSutilsElx/rpmbuild/BUILDROOT/amazon-ssm-agent-2.3.714.0-1.el8.x86_64/usr/bin/ssm-cli
        Generating build-id links failed
    ~~~
