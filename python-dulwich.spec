#
# Conditional build:
%bcond_without	python2		# CPython 2.x module
%bcond_without	python3		# CPython 3.x module
%bcond_without	tests		# unit tests
%bcond_without	doc		# Sphinx documentation

%define 	module	dulwich
Summary:	A Python implementation of the Git file formats and protocols
Summary(pl.UTF-8):	Pythonowa implementacja formatów plików i protokołów Gita
Name:		python-%{module}
Version:	0.19.14
Release:	2
License:	GPL v2+ or Apache 2.0+
Group:		Libraries/Python
Source0:	https://www.dulwich.io/releases/%{module}-%{version}.tar.gz
# Source0-md5:	ed939b01bf60f1d217a0ae7b2828a225
URL:		https://www.dulwich.io/
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-certifi
BuildRequires:	python-gevent
BuildRequires:	python-geventhttpclient
BuildRequires:	python-setuptools >= 17.1
BuildRequires:	python-urllib3 >= 1.24.1
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-certifi
BuildRequires:	python3-gevent
BuildRequires:	python3-geventhttpclient
BuildRequires:	python3-setuptools >= 17.1
BuildRequires:	python3-urllib3 >= 1.24.1
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-docutils
BuildRequires:	sphinx-pdg-3
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

%package -n python3-%{module}
Summary:	A Python implementation of the Git file formats and protocols
Summary(pl.UTF-8):	Pythonowa implementacja formatów plików i protokołów Gita
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4
# default binaries
Conflicts:	python-dulwich < 0.19.14

%description -n python3-%{module}
Dulwich is a Python implementation of the Git file formats and
protocols, which does not depend on Git itself.

All functionality is available in pure Python. Optional C extensions
can be built for improved performance.

The project is named after the village in which Mr. and Mrs. Git live
in the Monty Python sketch.

%description -n python3-%{module} -l pl.UTF-8
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
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m unittest discover -t . -s dulwich/tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m unittest discover -t . -s dulwich/tests
%endif
%endif

%if %{with doc}
# sphinx fails with it from time to time with parallel build
%{__make} -C docs -j1 html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

for p in dul-receive-pack dul-upload-pack dulwich ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/$p $RPM_BUILD_ROOT%{_bindir}/${p}-2
done

%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/%{module}/*.[ch]
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/%{module}/tests
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/%{module}/contrib/test_*.py*
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/docs/tutorial
%endif

%if %{with python3}
%py3_install

for p in dul-receive-pack dul-upload-pack dulwich ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/$p $RPM_BUILD_ROOT%{_bindir}/${p}-3
	ln -sf ${p}-3 $RPM_BUILD_ROOT%{_bindir}/${p}
done

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/*.[ch]
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/tests
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/contrib/test_*.py*
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/docs/tutorial
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README.rst README.swift.rst TODO
%attr(755,root,root) %{_bindir}/dul-receive-pack-2
%attr(755,root,root) %{_bindir}/dul-upload-pack-2
%attr(755,root,root) %{_bindir}/dulwich-2
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{module}/_*.so
%dir %{py_sitedir}/%{module}/contrib
%{py_sitedir}/%{module}/contrib/*.py[co]
%{py_sitedir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README.rst README.swift.rst TODO
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
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,tutorial,*.html,*.js}
%endif
