#norootforbuild 

Name:			pisense
BuildRequires:	%kernel_module_package_buildreqs 
License:		GPL 
Group:			System/Kernel 
Summary:		Raspberry Pi Sense-Hat
Version:		1.0 
Release:		0 
Source0:		%name-%version.tar.bz2 
BuildRoot:		%{_tmppath}/%{name}-%{version}-build

%kernel_module_package

%description 
This package contains the Raspberry Pi Sense-Hat drivers

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
export INSTALL_MOD_PATH=$RPM_BUILD_ROOT 
export INSTALL_MOD_DIR=updates 
for flavor in %flavors_to_build; do 
        make -C %{kernel_source $flavor} modules_install M=$PWD/obj/$flavor 
done

%changelog
* Tue Dec 13 2016 – rick.ashford@suse.com
- Initial version.
