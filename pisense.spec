#norootforbuild 

%define dts_overlay_dir arch/arm64/boot/dts
%define dts_rpi_overlay rpi-overlays
%define dts_rpi_overlay_dir %{dts_overlay_dir}/%{dts_rpi_overlay}
%define dts_makefile %{dts_overlay_dir}/Makefile

Name:			pisense
BuildRequires:	%kernel_module_package_buildreqs 
License:		GPL 
Group:			System/Kernel 
Summary:		Raspberry Pi Sense-Hat drivers 
Version:		1.0 
Release:		0 
Source0:		%name-%version.tar.xz
BuildRoot:		%{_tmppath}/%{name}-%{version}-build

%kernel_module_package

%description 
This package contains the Raspberry Pi Sense-Hat drivers

%prep 
%setup 
set -- * 
mkdir source 
mv "$@" source/ 
mkdir obj/

cd source

mkdir -p src/%{dts_rpi_overlay_dir}
mv -fv rpi-sense-overlay.dts src/%{dts_rpi_overlay_dir}/

cd ..

%build 
for flavor in %flavors_to_build; do 
        rm -rf obj/$flavor 
        cp -r source obj/$flavor 
        ls -lha %{kernel_source $flavor}/
        patch %{kernel_source $flavor}/%{dts_makefile} obj/$flavor/rpisense-overlay-makefile.patch
        make -C %{kernel_source $flavor} modules M=$PWD/obj/$flavor 
        make -C %{kernel_source $flavor} dtbs
done 

%install 
export INSTALL_MOD_PATH=$RPM_BUILD_ROOT 
export INSTALL_MOD_DIR=updates 
for flavor in %flavors_to_build; do 
        make -C %{kernel_source $flavor} modules_install M=$PWD/obj/$flavor 
        make -C %{kernel_source $flavor} dtbs_install
done

%changelog
* Tue Dec 13 2016 – rick.ashford@suse.com
- Initial version.
