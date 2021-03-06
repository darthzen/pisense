#norootforbuild 

%define dts_overlay_dir arch/arm64/boot/dts
%define dts_rpi_overlay rpi-overlays
%define dts_rpi_overlay_dir %{dts_overlay_dir}/%{dts_rpi_overlay}
%define dts_makefile %{dts_overlay_dir}/Makefile

Name:			pisense
BuildRequires:	%kernel_module_package_buildreqs 
BuildRequires:  kernel-source
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

mkdir -p source/src/%{dts_rpi_overlay_dir}
mv -fv source/rpi-sense-overlay.dts source/src/%{dts_rpi_overlay_dir}/

export SOURCE_VER=`rpm -qa |grep kernel-source |sed -E 's/kernel-source-([0-9]+)\.([0-9]+)\.([0-9]+)-([0-9]+)\.([0-9]+)\.noarch/\1.\2.\3-\4/g'`
export SOURCE_DIR="${PWD}/linux-${SOURCE_VER}/"

cp -Rf --no-preserve=ownership /usr/src/linux-${SOURCE_VER} ./

if [ -f ${SOURCE_DIR}/%{dts_makefile} ] ; then
    patch ${SOURCE_DIR}/%{dts_makefile} source/rpisense-overlay-makefile.patch
fi

mv -fv source/src source/%{name}-%{version}

%build 
for flavor in %flavors_to_build; do 
            rm -rf obj/$flavor 
            cp -r source obj/$flavor 
            make -C %{kernel_source $flavor} modules M=$PWD/obj/$flavor 
#            make -C ${SOURCE_DIR} dtbs
done 

%install 
export INSTALL_MOD_PATH="$RPM_BUILD_ROOT" 
export INSTALL_MOD_DIR=updates 
export INSTALL_DTBS_PATH="$RPM_BUILD_ROOT/boot/dtb-${SOURCE_VER}"
mkdir -p $RPM_BUILD_ROOT/boot/dtb-${SOURCE_VER}
#make -C ${SOURCE_DIR} dtbs_install

for flavor in %flavors_to_build; do 
        make -C %{kernel_source $flavor} modules_install M=$PWD/obj/$flavor 
done

%changelog
* Tue Dec 13 2016 – rick.ashford@suse.com
- Initial version.
