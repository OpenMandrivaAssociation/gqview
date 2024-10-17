%define version 2.1.5
%define release %mkrel 12

Summary:	Graphics file browser utility
Name:		gqview
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		Graphics
URL:		https://gqview.sourceforge.net/
BuildRoot:	%_tmppath/%{name}-%version-%release-root
Source:		http://prdownloads.sourceforge.net/gqview/%{name}-%{version}.tar.bz2
#gw http://qa.mandriva.com/show_bug.cgi?id=22966
#Patch: http://glenux2.free.fr/pub/Contrib/GQView/gqview-multi-2005-11-01-223248.patch.bz2
Patch1:		gqview-2.1.1-remote.patch
Patch2:		gqview-2.1.5-fix-str-fmt.patch
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
%patch2 -p0 -b .str
perl -pi -e 's,%{name}.png,%{name},g' %{name}.desktop

%build
%configure2_5x
perl -pi -e 's|#define GQVIEW_HELPDIR .*|#define GQVIEW_HELPDIR "%_docdir/%{name}"|' config.h
%make

%install
rm -fr %{buildroot}
%makeinstall_std
# GNOME_DATADIR=%{buildroot}/%{_datadir}
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


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2.1.5-11mdv2011.0
+ Revision: 664923
- mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 2.1.5-10mdv2011.0
+ Revision: 605498
- rebuild

* Fri Nov 27 2009 StÃ©phane TÃ©letchÃ©a <steletch@mandriva.org> 2.1.5-9mdv2010.1
+ Revision: 470561
- Fix license tag
- Fix mixed-use-of-spaces-and-tabs rpmlint error

* Sat Nov 21 2009 Ahmad Samir <ahmadsamir@mandriva.org> 2.1.5-8mdv2010.1
+ Revision: 468013
- Change non-existent gimp-remote to gimp

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.1.5-7mdv2010.0
+ Revision: 425023
- rebuild

* Thu Apr 09 2009 Funda Wang <fwang@mandriva.org> 2.1.5-6mdv2009.1
+ Revision: 365302
- fix str fmt
- fix docdir

  + Antoine Ginies <aginies@mandriva.com>
    - rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 2.1.5-4mdv2009.0
+ Revision: 218421
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 2.1.5-4mdv2008.1
+ Revision: 178710
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Sep 20 2007 Adam Williamson <awilliamson@mandriva.org> 2.1.5-2mdv2008.0
+ Revision: 91350
- fix doc install location
- rebuild for 2008
- fix icon name and drop obsolete Encoding key from .desktop file
- drop old menu and X-Mandriva menu category
- fd.o icons
- spec clean
- new license policy


* Sun Dec 03 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.1.5-1mdv2007.0
+ Revision: 90214
- new version

* Sun Nov 05 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.1.4-1mdv2007.1
+ Revision: 76712
- new version

* Sat Nov 04 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.1.3-1mdv2007.1
+ Revision: 76630
- Import gqview

* Sat Nov 04 2006 Götz Waschk <waschk@mandriva.org> 2.1.3-1mdv2007.1
- disable patch 0
- New version 2.1.3

* Mon Sep 18 2006 Olivier Blin <blino@mandriva.com> 2.1.1-5mdv2007.0
- Patch1: don't pass -n option to gimp-remote (#25880)
- really apply Patch0

* Thu Aug 03 2006 Götz Waschk <waschk@mandriva.org> 2.1.1-4mdv2007.0
- xdg menu

* Wed Jun 07 2006 Götz Waschk <waschk@mandriva.org> 2.1.1-3mdv2007.0
- fix multiple file actions (bug #22966)

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 2.1.1-2mdk
- Rebuild

* Wed Jun 15 2005 Götz Waschk <waschk@mandriva.org> 2.1.1-1mdk
- New release 2.1.1

* Mon Mar 07 2005 GÃ¶tz Waschk <waschk@linux-mandrake.com> 2.1.0-1mdk
- New release 2.1.0

* Sun Feb 27 2005 GÃ¶tz Waschk <waschk@linux-mandrake.com> 2.0.0-1mdk
- New release 2.0.0

* Wed Feb 16 2005 GÃ¶tz Waschk <waschk@linux-mandrake.com> 1.5.9-1mdk
- New release 1.5.9

* Thu Feb 10 2005 GÃ¶tz Waschk <waschk@linux-mandrake.com> 1.5.8-1mdk
- New release 1.5.8

* Tue Feb 01 2005 Götz Waschk <waschk@linux-mandrake.com> 1.5.7-1mdk
- update file list
- New release 1.5.7

* Fri Jan 07 2005 Goetz Waschk <waschk@linux-mandrake.com> 1.5.6-1mdk
- New release 1.5.6

* Tue Dec 28 2004 Goetz Waschk <waschk@linux-mandrake.com> 1.5.5-1mdk
- New release 1.5.5

* Wed Nov 10 2004 Goetz Waschk <waschk@linux-mandrake.com> 1.5.4-1mdk
- New release 1.5.4

* Fri Aug 27 2004 Götz Waschk <waschk@linux-mandrake.com> 1.5.2-1mdk
- update file list
- New release 1.5.2

* Fri Jul 09 2004 Robert Vojta <robert.vojta@mandrake.org> 1.5.1-2mdk
- requires libjpeg-progs (#10200)

* Thu May 06 2004 Damien Chaumette <dchaumette@mandrakesoft.com> 1.5.1-1mdk
- New release 1.5.1

* Sat May 01 2004 Goetz Waschk <waschk@linux-mandrake.com> 1.4.3-1mdk
- New release 1.4.3

* Tue Apr 06 2004 Götz Waschk <waschk@linux-mandrake.com> 1.4.2-1mdk
- new version

* Sat Apr 03 2004 Götz Waschk <waschk@linux-mandrake.com> 1.4.1-1mdk
- new version

* Fri Jan 23 2004 Götz Waschk <waschk@linux-mandrake.com> 1.3.8-1mdk
- new version

* Tue Dec 30 2003 Götz Waschk <waschk@linux-mandrake.com> 1.3.7-1mdk
- new version

* Tue Dec 16 2003 Götz Waschk <waschk@linux-mandrake.com> 1.3.6-1mdk
- remove the patch, the new warning message is less scary
- new version

