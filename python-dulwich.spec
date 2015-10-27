#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
%bcond_without	doc	# don't build doc

%define 	module	dulwich
Summary:	A python implementation of the Git file formats and protocols
Name:		python-%{module}
Version:	0.11.2
Release:	1
License:	GPLv2+ or ASL 2.0
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/d/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	ef70dce05422015373ca2704ddf281e7
URL:		http://samba.org/~jelmer/dulwich/
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with tests}
BuildRequires:	python-nose
%endif
%if %{with doc}
BuildRequires:	python-docutils
BuildRequires:	sphinx-pdg
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Dulwich is a pure-Python implementation of the Git file formats and
protocols. The project is named after the village in which Mr. and
Mrs. Git live in the Monty Python sketch.

%prep
%setup -q -n %{module}-%{version}
rm -r %{module}.egg-info

%build
CC="%{__cc}" \
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
%{__python} setup.py build

%if %{with tests}
cd dulwich/tests
nosetests-%{py_ver} test*.py
%endif

%if %{with doc}
# sphinx fails with it from time to time with parallel build
%{__make} -C docs -j html
rm -r docs/build/html/_sources
rm docs/build/html/{.buildinfo,objects.inv}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/%{module}/*.[ch]
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/%{module}/tests
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/%{module}/contrib/test_*.py*
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/docs/tutorial

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING %{?with_doc:docs/build/html}
%attr(755,root,root) %{_bindir}/dul-receive-pack
%attr(755,root,root) %{_bindir}/dul-upload-pack
%attr(755,root,root) %{_bindir}/dulwich
%dir %{py_sitedir}/%{module}
%dir %{py_sitedir}/%{module}/contrib
%{py_sitedir}/%{module}/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{module}/_*.so
%{py_sitedir}/%{module}-%{version}-py*.egg-info
%{py_sitedir}/%{module}/contrib/*.py[co]
