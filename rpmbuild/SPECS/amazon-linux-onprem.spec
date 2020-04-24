Name:           amazon-linux-onprem
Version:        1.0
Release:        0%{?dist}
Summary:        Meta Package for Amazon Linux onprem images
Group:          System Environment/Base
License:        ASL 2.0
URL:            https://amazonlinux.com/
BuildArch:	noarch
Conflicts:      ec2-net-utils


%description
Meta package for Amazon Linux to prevent accidental installation of conflicting
packages. This package should soley be used in onprem images.

%files
