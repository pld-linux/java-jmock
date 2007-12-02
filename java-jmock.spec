%include	/usr/lib/rpm/macros.java
Summary:	Test Java code using mock objects
Name:		jmock
Version:	1.0.1
Release:	0.1
Epoch:		0
License:	Open Source
Group:		Development/Languages/Java
URL:		http://jmock.codehaus.org/
Source0:	http://mirrors.ibiblio.org/pub/mirrors/maven2/jmock/jmock/1.0.1/%{name}-%{version}-sources.jar
# Source0-md5:	b845738bd6cb63f9e21e8b11f629382f
Patch0:		%{name}-MethodFactory.patch
BuildRequires:	ant >= 0:1.6
BuildRequires:	ant-junit >= 0:1.6
BuildRequires:	asm >= 0:1.5.3
BuildRequires:	cglib >= 0:2.1
BuildRequires:	jpackage-utils >= 0:1.5.37
BuildRequires:	junit >= 0:3.8.1
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	asm >= 0:1.5.3
Requires:	cglib >= 0:2.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
jMock is a library for testing Java code using mock objects. Mock
objects help you design and test the interactions between the objects
in your programs. The jMock package:
- makes it quick and easy to define mock objects, so you don't break
  the rhythm of programming.
- lets you define flexible constraints over object interactions,
  reducing the brittleness of your tests.
- is easy to extend.

%package  javadoc
Summary:	Javadoc for %{name}
Group:		Documentation
Requires:	jpackage-utils

%description    javadoc
Documentation for %{name}.

%package demo
Summary:	Examples for %{name}
Group:		Documentation

%description demo
Demonstrations and samples for %{name}.

%description demo -l pl.UTF-8
Pliki demonstracyjne i przykłady dla pakietu %{name}.

%prep
%setup -qc
find -name '*.jar' | xargs rm -vf
#%patch0

%build
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=$(build-classpath \
asm \
cglib)
CLASSPATH=build/core:build/cglib:$CLASSPATH
%ant -Dbuild.sysclasspath=only

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

install build/dist/jars/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

install build/dist/jars/%{name}-cglib-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-cglib-%{version}.jar
ln -s %{name}-cglib-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-cglib.jar

install $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/javadoc-%{version}/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

install $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc LICENSE.txt overview.html
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}

%files demo
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
