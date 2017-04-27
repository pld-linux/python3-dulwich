# TODO
# - python3 package
#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
%bcond_without	doc	# don't build doc

%define 	module	dulwich
Summary:	A Python implementation of the Git file formats and protocols
Summary(pl.UTF-8):	Pythonowa implementacja formatów plików i protokołów Gita
Name:		python-%{module}
Version:	0.17.3
Release:	1
License:	GPL v2+ or Apache 2.0+
Group:		Libraries/Python
Source0:	https://www.dulwich.io/releases/%{module}-%{version}.tar.gz
# Source0-md5:	2e5a14b1f4cbc9207b8a4134683a6054
URL:		https://www.dulwich.io/
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with tests}
BuildRequires:	python-gevent
BuildRequires:	python-geventhttpclient
BuildRequires:	python-nose
BuildRequires:	python-setuptools >= 17.1
%endif
%if %{with doc}
BuildRequires:	python-docutils
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
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

%description apidocs
Documentation for Python Dulwich module.

%description apidocs -l pl.UTF-8
Dokumentacja moduły Pythona Dulwich.

%prep
%setup -q -n %{module}-%{version}

%{__rm} -r %{module}.egg-info

%build
%py_build

%if %{with tests}
cd dulwich/tests
nosetests-%{py_ver} test*.py
cd ../..
%endif

%if %{with doc}
# sphinx fails with it from time to time with parallel build
%{__make} -C docs -j1 html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py_install

%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/%{module}/*.[ch]
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/%{module}/tests
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/%{module}/contrib/test_*.py*
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/docs/tutorial

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README.md README.swift.md TODO
%attr(755,root,root) %{_bindir}/dul-receive-pack
%attr(755,root,root) %{_bindir}/dul-upload-pack
%attr(755,root,root) %{_bindir}/dulwich
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{module}/_*.so
%dir %{py_sitedir}/%{module}/contrib
%{py_sitedir}/%{module}/contrib/*.py[co]
%{py_sitedir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,tutorial,*.html,*.js}
%endif
