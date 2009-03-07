%define version 2.1.5
%define release %mkrel 5

Summary: 	Graphics file browser utility
Name: 		gqview
Version: 	%{version}
Release: 	%{release}
License: 	GPL+
Group: 		Graphics
URL: 		http://gqview.sourceforge.net/
BuildRoot:	%_tmppath/%{name}-%version-%release-root
Source: 	http://prdownloads.sourceforge.net/gqview/%{name}-%{version}.tar.bz2
#gw http://qa.mandriva.com/show_bug.cgi?id=22966
#Patch: http://glenux2.free.fr/pub/Contrib/GQView/gqview-multi-2005-11-01-223248.patch.bz2
Patch1:		gqview-2.1.1-remote.patch
BuildRequires:	gtk+2-devel
BuildRequires:	libpng-devel
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
Requires:	jpeg-progs

Requires(post):		desktop-file-utils
Requires(postun):	desktop-file-utils


%description
GQview is a browser for graphics files.

Offering single click viewing of your graphics files.
Includes thumbnail view, zoom and filtering features.
And external editor support.

%prep
%setup -q
%patch1 -p1 -b .remote
perl -pi -e 's,%{name}.png,%{name},g' %{name}.desktop

%build
%configure2_5x
perl -pi -e 's|#define GQVIEW_HELPDIR .*|#define GQVIEW_HELPDIR "%_docdir/%{name}-%{version}"|' config.h
%make

%install
rm -fr %{buildroot}
%makeinstall GNOME_DATADIR=%{buildroot}/%{_datadir}
install -m 0644 -D gqview.png %{buildroot}%{_datadir}/pixmaps/gqview.png

# icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m 0644 gqview.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32 gqview.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 gqview.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

# removing unneeded stuff
rm -rf %{buildroot}%{_datadir}/gqview/README %{buildroot}%{_datadir}/gnome/apps/ %{buildroot}%{_datadir}/doc/%{name}-%{version}

# menu
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GTK" \
  --add-category="2DGraphics" \
  --remove-key="Encoding" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

# locale name fix
mv %{buildroot}%{_datadir}/locale/zh_CN{.GB2312,}

%{find_lang} %{name}

%if %mdkversion < 200900
%post
%update_menus
%update_desktop_database
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_desktop_database
%clean_icon_cache hicolor
%endif

%clean
rm -fr %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README COPYING TODO doc/*.html
%{_bindir}/*
%{_mandir}/man1/*
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*

