%define version 2.1.5
%define release %mkrel 1

Summary: 	Graphics file browser utility
Name: 		gqview
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Graphics
URL: 		http://gqview.sourceforge.net/
BuildRoot:	%_tmppath/%{name}-%version-%release-root

Source: 	http://prdownloads.sourceforge.net/gqview/%{name}-%{version}.tar.bz2
#gw http://qa.mandriva.com/show_bug.cgi?id=22966
#Patch: http://glenux2.free.fr/pub/Contrib/GQView/gqview-multi-2005-11-01-223248.patch.bz2
Patch1:		gqview-2.1.1-remote.patch
BuildRequires:  gtk+2-devel
BuildRequires:  libpng-devel
BuildRequires:	ImageMagick
BuildRequires:  desktop-file-utils
Requires: jpeg-progs
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils


%description
GQview is a browser for graphics files.

Offering single click viewing of your graphics files.
Includes thumbnail view, zoom and filtering features.
And external editor support.

%prep
%setup -q
#%patch0 -p1 -b .multi
%patch1 -p1 -b .remote

%build
%configure2_5x
perl -pi -e 's|#define GQVIEW_HELPDIR .*|#define GQVIEW_HELPDIR "%_docdir/%{name}-%{version}"|' config.h

%make

%install
rm -fr %{buildroot}
%makeinstall GNOME_DATADIR=%{buildroot}/%{_datadir}
install -m 0644 -D gqview.desktop %{buildroot}%{_datadir}/gnome/apps/Graphics/gqview.desktop
install -m 0644 -D gqview.png %{buildroot}%{_datadir}/pixmaps/gqview.png

# icons
mkdir -p %{buildroot}%{_iconsdir} %{buildroot}%{_miconsdir}
install -m 0644 -D      gqview.png %{buildroot}%{_liconsdir}/%{name}.png
convert -geometry 32x32 gqview.png %{buildroot}%{_iconsdir}/%{name}.png
convert -geometry 16x16 gqview.png %{buildroot}%{_miconsdir}/%{name}.png

# removing uneeded stuff
rm -rf %{buildroot}%{_datadir}/gqview/README %buildroot%{_datadir}/gnome/apps/

# menu
mkdir -p %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}): \
 command="%{_bindir}/%{name}" \
 icon="%{name}.png" \
 title="GQview" \
 longtitle="A browser for graphics files" \
 needs="x11" \
 section="Multimedia/Graphics" xdg="true"
EOF
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Multimedia-Graphics" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


# locale name fix
mv %{buildroot}%{_datadir}/locale/zh_CN{.GB2312,}

%{find_lang} %{name}

%post
%update_menus
%update_desktop_database

%postun
%clean_menus
%clean_desktop_database

%clean
rm -fr %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README COPYING TODO 
%{_bindir}/*
%{_mandir}/man1/*

%{_menudir}/*
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*


