#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Extension module for click to enable registering CLI commands via setuptools entry-points
Summary(pl.UTF-8):	Moduł rozszerzenia clicka pozwalający rejestrować polecenia CLI poprzez punkty wejściowe setuptools
Name:		python-click-plugins
Version:	1.1.1
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/click-plugins/
Source0:	https://files.pythonhosted.org/packages/source/c/click-plugins/click-plugins-%{version}.tar.gz
# Source0-md5:	969268b5b005b2b56115c66c55013252
URL:		https://pypi.org/project/click-plugins/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.5
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-click >= 4.0
BuildRequires:	python-pytest >= 3.6
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-click >= 4.0
BuildRequires:	python3-pytest >= 3.6
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Extension module for click to enable registering CLI commands via
setuptools entry-points.

%description -l pl.UTF-8
Moduł rozszerzenia clicka pozwalający rejestrować polecenia CLI
poprzez punkty wejściowe setuptools

%package -n python3-click-plugins
Summary:	Extension module for click to enable registering CLI commands via setuptools entry-points
Summary(pl.UTF-8):	Moduł rozszerzenia clicka pozwalający rejestrować polecenia CLI poprzez punkty wejściowe setuptools
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-click-plugins
Extension module for click to enable registering CLI commands via
setuptools entry-points.

%description -n python3-click-plugins -l pl.UTF-8
Moduł rozszerzenia clicka pozwalający rejestrować polecenia CLI
poprzez punkty wejściowe setuptools

%prep
%setup -q -n click-plugins-%{version}

%if %{with python2}
# adjust py2 tests for Unicode icon change
install -d tests-py2
cp -pr tests tests-py2
%{__sed} -i -e "s/assert u'.*in result\.output$/assert '* Warning' in result.output/" tests-py2/tests/test_plugins.py
%endif

%build
%if %{with python2}
%py_build

# Unicode icon breaks click formatter with python 2
%{__sed} -i -e "/^ *icon = u'/ s/u'[^']*'/'*'/" build-2/lib/click_plugins/core.py

%if %{with tests}
cd tests-py2
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
PYTHONPATH=$(pwd)/../build-2/lib \
%{__python} -m pytest tests
cd ..
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS.txt CHANGES.md LICENSE.txt README.rst
%{py_sitescriptdir}/click_plugins
%{py_sitescriptdir}/click_plugins-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-click-plugins
%defattr(644,root,root,755)
%doc AUTHORS.txt CHANGES.md LICENSE.txt README.rst
%{py3_sitescriptdir}/click_plugins
%{py3_sitescriptdir}/click_plugins-%{version}-py*.egg-info
%endif
