#
# Conditional build:
%bcond_with	tests		# unit tests (one failing)
%bcond_without	doc		# Sphinx documentation

%define 	module	dulwich
Summary:	A Python implementation of the Git file formats and protocols
Summary(pl.UTF-8):	Pythonowa implementacja formatów plików i protokołów Gita
Name:		python3-%{module}
Version:	0.20.33
Release:	1
License:	GPL v2+ or Apache 2.0+
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/dulwich/
Source0:	https://files.pythonhosted.org/packages/source/d/dulwich/%{module}-%{version}.tar.gz
# Source0-md5:	a0cf0fe3a3125874f2bc03d834611d44
URL:		https://www.dulwich.io/
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-certifi
BuildRequires:	python3-fastimport
BuildRequires:	python3-gevent
BuildRequires:	python3-geventhttpclient
BuildRequires:	python3-gpg >= 1.8
BuildRequires:	python3-setuptools >= 1:17.1
BuildRequires:	python3-urllib3 >= 1.24.1
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-docutils
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.6
# default binaries
Conflicts:	python-dulwich < 0.19.14
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Dulwich is a Python implementation of the Git file formats and
protocols, which does not depend on Git itself.

All functionality is available in pure Python. Optional C extensions
can be built for improved performance.

The project is named after the village in which Mr. and Mrs. Git live
in the Monty Python sketch.

%description -l pl.UTF-8
Dulwich to pythonowa implementacja formatów plików i protokołów Gita,
nie zależąca od samego Gita.

Cała funkcjonalność jest dostępna w czystym Pythonie. Opcjonalnie
można zbudować rozszerzenia w C poprawiające wydajność.

Nazwa projektu wywodzi się od wioski, w której żyją Pan i Pani Git w
skeczu Monty Pythona.

%package apidocs
Summary:	Documentation for Python Dulwich module
Summary(pl.UTF-8):	Dokumentacja moduły Pythona Dulwich
Group:		Documentation
BuildArch:	noarch

%description apidocs
Documentation for Python Dulwich module.

%description apidocs -l pl.UTF-8
Dokumentacja moduły Pythona Dulwich.

%prep
%setup -q -n %{module}-%{version}

%{__rm} -r %{module}.egg-info

%build
%py3_build

%if %{with tests}
%{__python3} -m unittest discover -t . -s dulwich/tests
%endif

%if %{with doc}
# sphinx fails with it from time to time with parallel build
%{__make} -C docs -j1 html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

for p in dul-receive-pack dul-upload-pack dulwich ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/$p $RPM_BUILD_ROOT%{_bindir}/${p}-3
	ln -sf ${p}-3 $RPM_BUILD_ROOT%{_bindir}/${p}
done

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/*.[ch]
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/tests
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/contrib/test_*.py*
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/docs/tutorial

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README.rst README.swift.rst SECURITY.md TODO
%attr(755,root,root) %{_bindir}/dul-receive-pack-3
%attr(755,root,root) %{_bindir}/dul-upload-pack-3
%attr(755,root,root) %{_bindir}/dulwich-3
%attr(755,root,root) %{_bindir}/dul-receive-pack
%attr(755,root,root) %{_bindir}/dul-upload-pack
%attr(755,root,root) %{_bindir}/dulwich
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/_*.cpython-*.so
%dir %{py3_sitedir}/%{module}/contrib
%{py3_sitedir}/%{module}/contrib/*.py
%{py3_sitedir}/%{module}/contrib/__pycache__
%{py3_sitedir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,tutorial,*.html,*.js}
%endif
