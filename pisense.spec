#
# spec file for package pisense
#
# Copyright (c) 2016 Richard Ashford, Peter Linnell
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#
Name:			pisense
License:		GPL-2.0 
Group:			System/Kernel 
Summary:		Raspberry Pi Sense-Hat Drivers
Version:		1.0 
Release:		0 
Source0:		%name-%version.tar.bz2 
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
URL: 			https://github.com/darthzen/pisense
BuildRequires:	%kernel_module_package_buildreqs 

%kernel_module_package

%description 
This package contains the Raspberry Pi Sense-Hat drivers. 

%prep 
%setup 
set -- * 
mkdir source 
mv "$@" source/ 
mkdir obj 

%build 
for flavor in %flavors_to_build; do 
        rm -rf obj/$flavor 
        cp -r source obj/$flavor 
        make -C %{kernel_source $flavor} modules M=$PWD/obj/$flavor 
done 

%install 
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=updates 
for flavor in %flavors_to_build; do 
        make -C %{kernel_source $flavor} modules_install M=$PWD/obj/$flavor 
done

%changelog