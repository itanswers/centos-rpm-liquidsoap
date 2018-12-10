#
# spec file for package liquidsoap
#
# Copyright (c) 2018 Radio Bern RaBe
#                    http://www.rabe.ch
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as 
# published  by the Free Software Foundation, version 3 of the 
# License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
# Please submit enhancements, bugfixes or comments via GitHub:
# https://github.com/radiorabe/centos-rpm-liquidsoap
#

Name:     liquidsoap 
Version:  1.3.4
Release:  2%{?dist}
Summary:  Audio and video streaming language

License:  GPLv2
URL:      http://liquidsoap.info/
Source0:  https://github.com/savonet/liquidsoap/releases/download/%{version}/%{name}-%{version}.tar.bz2
Source1:  liquidsoap@.service

BuildRequires: file-devel
BuildRequires: flac-devel
BuildRequires: inotify-tools-devel
BuildRequires: ladspa-devel
BuildRequires: lame-devel
BuildRequires: libX11-devel
BuildRequires: libmad-devel
BuildRequires: libsamplerate-devel
BuildRequires: libstdc++-static
BuildRequires: libvorbis-devel
BuildRequires: ocaml
BuildRequires: ocaml-alsa-devel
BuildRequires: ocaml-biniou-devel
BuildRequires: ocaml-cry-devel
BuildRequires: ocaml-dtools-devel
BuildRequires: ocaml-duppy-devel
BuildRequires: ocaml-easy-format-devel
BuildRequires: ocaml-findlib
BuildRequires: ocaml-flac-devel
BuildRequires: ocaml-inotify-devel
BuildRequires: ocaml-bjack-devel
BuildRequires: ocaml-ladspa-devel
BuildRequires: ocaml-lame-devel
BuildRequires: ocaml-magic-devel
BuildRequires: ocaml-mm-devel
BuildRequires: ocaml-ogg-devel
BuildRequires: ocaml-opus-devel
BuildRequires: ocaml-pcre-devel
BuildRequires: ocaml-samplerate-devel
BuildRequires: ocaml-soundtouch-devel
BuildRequires: ocaml-speex-devel
BuildRequires: ocaml-ssl-devel
BuildRequires: ocaml-taglib-devel
BuildRequires: ocaml-theora-devel
BuildRequires: ocaml-vorbis-devel
BuildRequires: ocaml-xmlm-devel
BuildRequires: ocaml-xmlplaylist-devel
BuildRequires: ocaml-yojson-devel
BuildRequires: opus-devel
BuildRequires: soundtouch-devel
BuildRequires: speex-devel
BuildRequires: systemd
BuildRequires: taglib-devel
%{?systemd_requires}
Requires(pre): shadow-utils


%description
Liquidsoap is a powerful and flexible language for describing your streams. It
offers a rich collection of operators that you can combine at will, giving you
more power than you need for creating or transforming streams. But liquidsoap
is still very light and easy to use, in the Unix tradition of simple strong
components working together.


%prep
%setup -q
# do not use the configure rpm macro due to this not being a classical autoconf based configure script
./configure --disable-camomile --prefix=%{_exec_prefix} --sysconfdir=%{_sysconfdir} --mandir=%{_mandir} --localstatedir=%{_localstatedir} --disable-ldconf

%build
make

%install
# do not use the make_install rpm macro due to this not being a classical automake based makefile
make install %{_exec_prefix} OCAMLFIND_DESTDIR=%{buildroot}%{_exec_prefix} prefix=%{buildroot}%{_exec_prefix} sysconfdir=%{buildroot}%{_sysconfdir} mandir=%{buildroot}%{_mandir} localstatedir=%{buildroot}%{_localstatedir}
install -d %{buildroot}%{_unitdir}
install -c %{SOURCE1} -m 644 %{buildroot}%{_unitdir}

%pre
getent group liquidsoap >/dev/null || groupadd -r liquidsoap
getent passwd liquidsoap >/dev/null || \
    useradd -r -g liquidsoap -d /var/lib/liquidsoap -m \
    -c "Liquidsoap system user account" liquidsoap
exit 0

%post
%systemd_post liquidsoap@.service

%preun
%systemd_preun liquidsoap@.service

%postun
%systemd_postun_with_restart liquidsoap@.service

%files
%{_exec_prefix}/bin/liquidsoap
%{_unitdir}/liquidsoap@.service
%config/etc/liquidsoap/radio.liq.example
%config(noreplace)/etc/logrotate.d/liquidsoap
%{_exec_prefix}/lib/liquidsoap/%{version}/
%doc README
%doc
%{_exec_prefix}/share/doc/liquidsoap-%{version}/examples/*.liq
%{_mandir}/man1/liquidsoap.1.*

%changelog
* Mon Dec 10 2018 Lucas Bickel <hairmare@rabe.ch> - 1.3.4-2
- Initialize RPM changelog
- Proper installation of runtime deps
