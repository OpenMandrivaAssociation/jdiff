# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define section free

%define gcj_support 1

Summary:        JDiff - An HTML Report of API Differences
Name:           jdiff
Version:        1.0.10
Release:        %mkrel 2.0.5
Epoch:          0
License:        LGPL
URL:            http://javadiff.sourceforge.net/
Group:          Development/Java
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  ant >= 0:1.6
BuildRequires:  java-rpmbuild >= 0:1.6
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
JDiff is a Javadoc doclet which generates an HTML 
report of all the packages, classes, constructors, 
methods, and fields which have been removed, added 
or changed in any way, including their documentation, 
when two APIs are compared. This is very useful for 
describing exactly what has changed between two 
releases of a product. Only the API (Application 
Programming Interface) of each version is compared. 
It does not compare what the source code does when 
executed. 

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
%{summary}.

%package        manual
Summary:        Docs and examples for %{name}
Group:          Development/Java

%description    manual
%{summary}.

%prep
%setup -q -n %{name}
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
%{__perl} -pi -e 's/\r$//g' KNOWN_LIMITATIONS.txt

%build
export CLASSPATH=$(build-classpath junit):`pwd`/lib/jdiff.jar
%{ant} -Dbuild.sysclasspath=only
%{javadoc} -classpath `pwd`/lib/jdiff.jar -d apidocs -sourcepath src -subpackages jdiff

%install
rm -rf $RPM_BUILD_ROOT

# bins
install -dm 755 $RPM_BUILD_ROOT%{_bindir}
cp -p bin/jdiff $RPM_BUILD_ROOT%{_bindir}

# jars
install -dm 755 $RPM_BUILD_ROOT%{_javadir}
cp -p lib/%{name}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# manual and examples
install -dm 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p *.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p *.xml $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p *.html $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p *.css $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr examples $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_docdir}/%{name}-%{version}/*.txt
%attr(755,root,root)                 %{_bindir}/*
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%{_docdir}/%{name}-%{version}
