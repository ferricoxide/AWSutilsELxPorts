To build the source-RPMs found in this project a couple of things will be necessary:

## Preparing the build-environment

1. The host/container used to build the binary RPMs will need the following packages and package-groups installed:

    - `createrepo`
    - `dos2unix`
    - `git`
    - `rpm-build`
    - `rpmdevtools`
    - `rpm-sign`
    - `unzip`
    - `@development`

1. It will be necessary to have correctly set up `${HOME}/.rpmmacros` file. File-contents similar to the following should suffice:

    ~~~
    %_topdir %(echo $HOME)/rpmbuild
    
    # Package-signing stuff
    %_gpgbin /usr/bin/gpg
    %_gpg_bin /usr/bin/gpg
    %_gpg_path %(echo $HOME)/.gnupg
    %_gpg_name <KEY_ID_HEXSTRING>
    %_signature gpg
    %__gpg_sign_cmd %{__gpg} gpg --batch --verbose --no-armor --passphrase-fd 3 --no-secmem-warning -u "%{_gpg_name}" -sbo %{__signature_filename} --digest-algo sha256 %{__plaintext_filename}'
    ~~~

1. Even with the above, when invoking `rpmbuild`, it will likely to be necessary to override the value of `%_topdir` set in the `${HOME}/.rpmmacros` file. This can be done with an invocation similar to:

    ~~~
    rpmbuild --define '_topdir %(echo $HOME)/GIT/AWSutilsElx/rpmbuild' -ba ${SPEC} 
    ~~~

## Known to build

- `amazon-efs-utils`
- `amazon-linux-extras`
- `amazon-linux-extras-yum-plugin`
- `amazonlinux-indexhtml`
- `aws-amitools-ec2`
- `aws-apitools-as`
- `aws-apitools-cfn`
- `aws-apitools-common`
- `aws-apitools-ec2`
- `aws-apitools-elb`
- `aws-apitools-iam`
- `aws-apitools-mon`
- `aws-apitools-rds`
- `aws-cfn-bootstrap`
- `awslogs`
- `aws-scripts-ses`
- `ec2-hibinit-agent`
- `ec2-instance-connect`
- `ec2-net-utils`
- `ec2sys-autotune`
- `ec2-utils`
