%global pkg_name jai-imageio-core
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%global cvs_ver 20100217

Name:		%{?scl_prefix}%{pkg_name}
Version:	1.2
Release:	0.14.%{cvs_ver}cvs.9%{?dist}
Summary:	Core Java Advanced Imaging Image I/O Tools API

License:	BSD
URL:		https://jai-imageio.dev.java.net/
Source0:	jai-imageio-core-cvs%{cvs_ver}-CLEANED.tar.xz
Source1:	README-RHSCL.txt

# jai-imageio-core contains code under a restrictive licence that we
# cannot ship. This script will download and generate a tarball from
# CVS. Unfortunately, a login is required to download from CVS and
# there are no source tarballs.
#
# Register at:
# https://www.dev.java.net/servlets/Join
#
# Then, run:
# ./generate-tarball.sh USERNAME DATE
Source2:	generate-tarball.sh

BuildRequires:	%{?scl_prefix}ant
BuildRequires:	%{?scl_prefix}javapackages-tools
BuildRequires:	recode
Requires:	%{?scl_prefix}javapackages-tools


Patch0:		jai-imageio-core-remove-imageio-services.patch
Patch1:		jai-imageio-core-remove-codeclib-plugins.patch
Patch2:		jai-imageio-core-remove-jai-operations.patch
Patch3:		jai-imageio-core-remove-jpeg2000-plugin.patch
Patch4:		jai-imageio-core-no-sun-classes.patch

BuildArch:	noarch

%description
This package contains the core Java Advanced Imaging Image I/O Tools API,
minus JPEG 2000, JAI Image I/O operations, and the C-based codecLib.


%package javadoc
Summary:	Javadocs for %{pkg_name}


%description javadoc
This package contains the API documentation for %{pkg_name}.


%prep
%setup -q -n jai-imageio-core-cvs%{cvs_ver}-CLEANED
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

# remove unbuildable items
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# remove use of sun.*
# https://jai-imageio-core.dev.java.net/issues/show_bug.cgi?id=186
%patch4 -p0

# fix latin-1 documentation
recode latin1..utf-8 COPYRIGHT.txt

# install our documentation
cp -av %{SOURCE1} .
%{?scl:EOF}


%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# note: BUILD_TARGET is pretty much ignored, but we need it
# to know where the built files will be located
ant -DBUILD_TARGET=linux-i586 jar-opt docs-jcp
%{?scl:EOF}


%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
mkdir -p $RPM_BUILD_ROOT%{_javadir}
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}

cp -av build/linux-i586/opt/lib/ext/jai_imageio.jar $RPM_BUILD_ROOT%{_javadir}/jai_imageio.jar

cp -av build/linux-i586/javadocs/docs-jcp/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%{?scl:EOF}

%files
%doc LICENSE.txt COPYRIGHT.txt README-RHSCL.txt
%{_javadir}/*.jar

%files javadoc
%doc LICENSE.txt COPYRIGHT.txt
%{_javadocdir}/%{name}


%changelog
* Mon Jun  2 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-0.14.20100217cvs.9
- Rename README-fedora-epel.txt to README-RHSCL.txt

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-0.14.20100217cvs.8
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-0.14.20100217cvs.7
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-0.14.20100217cvs.6
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-0.14.20100217cvs.5
- Remove requires on java

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-0.14.20100217cvs.4
- SCL-ize build-requires

* Mon Feb 17 2014 Michal Srb <msrb@redhat.com> - 1.2-0.14.20100217cvs.3
- SCL-ize BR/R

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-0.14.20100217cvs.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-0.14.20100217cvs.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.2-0.14.20100217cvs
- Mass rebuild 2013-12-27

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-0.13.20100217cvs
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.12.20100217cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 18 2012 Michal Srb <msrb@redhat.com> - 1.2-0.11.20100217cvs
- Install license in javadoc package (Resolves: #888420)
- Removed dependency on jai-imageio-core from javadoc package (Resolves: #888423)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.10.20100217cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 12 2012 Alexander Kurtakov <akurtako@redhat.com> 1.2-0.9.20100217cvs
- Drop gcj_support.
- Adapt to current guidelines.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.7.20100217cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.6.20100217cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug  2 2010 Adam Goode <adam@spicenitz.org> - 1.2-0.5.20100217cvs
- Unify Fedora and EPEL readme files

* Thu Feb 18 2010 Adam Goode <adam@spicenitz.org> - 1.2-0.4.20100217cvs
- First Fedora release

* Wed Feb  3 2010 Adam Goode <adam@spicenitz.org> - 1.2-0.3.20100202cvs
- Update generate-tarball.sh to canonicalize owner/group and date

* Mon Jan 11 2010 Adam Goode <adam@spicenitz.org> - 1.2-0.2.20100111cvs
- Add generate-tarball.sh

* Wed Nov 11 2009 Adam Goode <adam@spicenitz.org> - 1.2-0.1.20091111cvs
- Initial release
