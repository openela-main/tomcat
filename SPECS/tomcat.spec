# Copyright (c) 2000-2008, JPackage Project
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

%global jspspec 2.3
%global major_version 9
%global minor_version 0
%global micro_version 62
%global packdname  %{name}-%{major_version}.%{minor_version}.%{micro_version}.redhat-00018-src
%global servletspec 4.0
%global elspec 3.0
%global tcuid 53
# Recommended version is specified in java/org/apache/catalina/core/AprLifecycleListener.java
%global native_version 1.2.21


# FHS 2.3 compliant tree structure - http://www.pathname.com/fhs/2.3/
%global basedir %{_var}/lib/%{name}
%global appdir %{basedir}/webapps
%global homedir %{_datadir}/%{name}
%global bindir %{homedir}/bin
%global confdir %{_sysconfdir}/%{name}
%global libdir %{_javadir}/%{name}
%global logdir %{_var}/log/%{name}
%global cachedir %{_var}/cache/%{name}
%global tempdir %{cachedir}/temp
%global workdir %{cachedir}/work
%global _systemddir /lib/systemd/system

Name:          tomcat
Epoch:         1
Version:       %{major_version}.%{minor_version}.%{micro_version}
Release:       27%{?dist}.3
Summary:       Apache Servlet/JSP Engine, RI for Servlet %{servletspec}/JSP %{jspspec} API

License:       ASL 2.0
URL:           http://tomcat.apache.org/
Source0:       %{packdname}.zip
Source1:       %{name}-%{major_version}.%{minor_version}.conf
Source3:       %{name}-%{major_version}.%{minor_version}.sysconfig
Source4:       %{name}-%{major_version}.%{minor_version}.wrapper
Source5:       %{name}-%{major_version}.%{minor_version}.logrotate
Source6:       %{name}-%{major_version}.%{minor_version}-digest.script
Source7:       %{name}-%{major_version}.%{minor_version}-tool-wrapper.script
Source11:      %{name}-%{major_version}.%{minor_version}.service
Source21:      tomcat-functions
Source30:      tomcat-preamble
Source31:      tomcat-server
Source32:      tomcat-named.service
Source33:      java-9-start-up-parameters.conf

Patch0:        %{name}-%{major_version}.%{minor_version}-bootstrap-MANIFEST.MF.patch
Patch1:        %{name}-%{major_version}.%{minor_version}-tomcat-users-webapp.patch
Patch2:        %{name}-build.patch
Patch3:        %{name}-%{major_version}.%{minor_version}-catalina-policy.patch
Patch4:        rhbz-1857043.patch
# remove bnd dependency which version is too low on rhel8
Patch6:        remove-bnd-annotation.patch
Patch7:        JmxRemoteLifecycleListener.patch
Patch8:        fix-malformed-dtd.patch

BuildArch:     noarch

BuildRequires: ant
BuildRequires: ecj
BuildRequires: findutils
BuildRequires: javapackages-local
BuildRequires: aqute-bnd
BuildRequires: aqute-bndlib
BuildRequires: systemd

Requires:      (java-headless >= 1:1.8 or java-1.8.0-headless or java-11-headless or java-17-headless or java >= 1:1.8)
Requires:      javapackages-tools
Requires:      %{name}-lib = %{epoch}:%{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} > 7
Recommends:    tomcat-native >= %{native_version}
%endif
Requires(pre):    shadow-utils
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

Conflicts: pki-servlet-engine <= 1:9.0.50

# added after log4j sub-package was removed
Provides:         %{name}-log4j = %{epoch}:%{version}-%{release}

%description
Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.

Tomcat is developed in an open and participatory environment and
released under the Apache Software License version 2.0. Tomcat is intended
to be a collaboration of the best-of-breed developers from around the world.

%package admin-webapps
Summary: The host-manager and manager web applications for Apache Tomcat
Requires: %{name} = %{epoch}:%{version}-%{release}

%description admin-webapps
The host-manager and manager web applications for Apache Tomcat.

%package docs-webapp
Summary: The docs web application for Apache Tomcat
Requires: %{name} = %{epoch}:%{version}-%{release}

%description docs-webapp
The docs web application for Apache Tomcat.

%package jsp-%{jspspec}-api
Summary: Apache Tomcat JavaServer Pages v%{jspspec} API Implementation Classes
Provides: jsp = %{jspspec}
Obsoletes: %{name}-jsp-2.2-api
Requires: %{name}-servlet-%{servletspec}-api = %{epoch}:%{version}-%{release}
Requires: %{name}-el-%{elspec}-api = %{epoch}:%{version}-%{release}
Conflicts: pki-servlet-engine <= 1:9.0.50

%description jsp-%{jspspec}-api
Apache Tomcat JSP API Implementation Classes.

%package lib
Summary: Libraries needed to run the Tomcat Web container
Requires: %{name}-jsp-%{jspspec}-api = %{epoch}:%{version}-%{release}
Requires: %{name}-servlet-%{servletspec}-api = %{epoch}:%{version}-%{release}
Requires: %{name}-el-%{elspec}-api = %{epoch}:%{version}-%{release}
Requires: ecj >= 1:4.10
Requires(preun): coreutils
Conflicts: pki-servlet-engine <= 1:9.0.50

%description lib
Libraries needed to run the Tomcat Web container.

%package servlet-%{servletspec}-api
Summary: Apache Tomcat Java Servlet v%{servletspec} API Implementation Classes
Provides: servlet = %{servletspec}
Provides: servlet6
Provides: servlet3
Obsoletes: %{name}-servlet-3.1-api
Conflicts: pki-servlet-4.0-api <= 1:9.0.50

%description servlet-%{servletspec}-api
Apache Tomcat Servlet API Implementation Classes.

%package el-%{elspec}-api
Summary: Apache Tomcat Expression Language v%{elspec} API Implementation Classes
Provides: el_api = %{elspec}
Obsoletes: %{name}-el-2.2-api
Conflicts: pki-servlet-engine <= 1:9.0.50 and pki-servlet-container <= 1:9.0.7

%description el-%{elspec}-api
Apache Tomcat EL API Implementation Classes.

%package webapps
Summary: The ROOT web application for Apache Tomcat
Requires: %{name} = %{epoch}:%{version}-%{release}

%description webapps
The ROOT web application for Apache Tomcat.

%prep
%setup -q -n apache-%{packdname}
# remove pre-built binaries and windows files
find . -type f \( -name "*.bat" -o -name "*.class" -o -name Thumbs.db -o -name "*.gz" -o \
   -name "*.jar" -o -name "*.war" -o -name "*.zip" \) -delete

%patch -P0 -p0
%patch -P1 -p0
%patch -P2 -p0
%patch -P3 -p0
%patch -P4 -p0
%patch -P6 -p1
%patch -P7 -p1
%patch -P8 -p1

# Remove webservices naming resources as it's generally unused
%{__rm} -rf java/org/apache/naming/factory/webservices

# Configure maven files
%mvn_package ":tomcat-el-api" tomcat-el-api
%mvn_alias "org.apache.tomcat:tomcat-el-api" "org.eclipse.jetty.orbit:javax.el"
%mvn_package ":tomcat-jsp-api" tomcat-jsp-api
%mvn_alias "org.apache.tomcat:tomcat-jsp-api" "org.eclipse.jetty.orbit:javax.servlet.jsp"
%mvn_package ":tomcat-servlet-api" tomcat-servlet-api


%build
export OPT_JAR_LIST="xalan-j2-serializer"
# we don't care about the tarballs and we're going to replace
# tomcat-dbcp.jar with apache-commons-{collections,dbcp,pool}-tomcat5.jar
# so just create a dummy file for later removal
touch HACK

# who needs a build.properties file anyway
%{ant} -Dbase.path="." \
  -Dbuild.compiler="modern" \
  -Dcommons-daemon.jar="HACK" \
  -Dcommons-daemon.native.src.tgz="HACK" \
  -Djdt.jar="$(build-classpath ecj/ecj)" \
  -Dtomcat-native.tar.gz="HACK" \
  -Dtomcat-native.home="." \
  -Dcommons-daemon.native.win.mgr.exe="HACK" \
  -Dnsis.exe="HACK" \
  -Djaxrpc-lib.jar="HACK" \
  -Dwsdl4j-lib.jar="HACK" \
  -Dbnd.jar="HACK" \
  -Dversion="%{version}" \
  -Dversion.build="%{micro_version}" \
  deploy

# remove some jars that we'll replace with symlinks later
%{__rm} output/build/lib/ecj.jar
# Remove the example webapps per Apache Tomcat Security Considerations
# see https://tomcat.apache.org/tomcat-9.0-doc/security-howto.html
%{__rm} -rf output/build/webapps/examples


%install
# build initial path structure
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_bindir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_sbindir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_systemddir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{appdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{bindir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{confdir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{confdir}/Catalina/localhost
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{confdir}/conf.d
/bin/echo "Place your custom *.conf files here. Shell expansion is supported." > ${RPM_BUILD_ROOT}%{confdir}/conf.d/README
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{libdir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{logdir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{_localstatedir}/lib/tomcats
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{homedir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{tempdir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{workdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_unitdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}

# move things into place
# First copy supporting libs to tomcat lib
pushd output/build
    %{__cp} -a bin/*.{jar,xml} ${RPM_BUILD_ROOT}%{bindir}
    %{__cp} -a conf/*.{policy,properties,xml,xsd} ${RPM_BUILD_ROOT}%{confdir}
    %{__cp} -a lib/*.jar ${RPM_BUILD_ROOT}%{libdir}
    %{__cp} -a webapps/* ${RPM_BUILD_ROOT}%{appdir}
popd

%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE1} \
    > ${RPM_BUILD_ROOT}%{confdir}/%{name}.conf
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE3} \
    > ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/%{name}
%{__install} -m 0644 %{SOURCE4} \
    ${RPM_BUILD_ROOT}%{_sbindir}/%{name}
%{__install} -m 0644 %{SOURCE11} \
    ${RPM_BUILD_ROOT}%{_unitdir}/%{name}.service
%{__sed} -e "s|\@\@\@TCLOG\@\@\@|%{logdir}|g" %{SOURCE5} \
    > ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}.disabled
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE6} \
    > ${RPM_BUILD_ROOT}%{_bindir}/%{name}-digest
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE7} \
    > ${RPM_BUILD_ROOT}%{_bindir}/%{name}-tool-wrapper

%{__install} -m 0644 %{SOURCE21} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}/functions
%{__install} -m 0755 %{SOURCE30} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}/preamble
%{__install} -m 0755 %{SOURCE31} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}/server
%{__install} -m 0644 %{SOURCE32} \
    ${RPM_BUILD_ROOT}%{_unitdir}/%{name}@.service

%{__install} -m 0644 %{SOURCE33} ${RPM_BUILD_ROOT}%{confdir}/conf.d/

# Substitute libnames in catalina-tasks.xml
sed -i \
   "s,el-api.jar,%{name}-el-%{elspec}-api.jar,;
    s,servlet-api.jar,%{name}-servlet-%{servletspec}-api.jar,;
    s,jsp-api.jar,%{name}-jsp-%{jspspec}-api.jar,;" \
    ${RPM_BUILD_ROOT}%{bindir}/catalina-tasks.xml

# create jsp and servlet API symlinks
pushd ${RPM_BUILD_ROOT}%{_javadir}
   %{__mv} %{name}/jsp-api.jar %{name}-jsp-%{jspspec}-api.jar
   %{__ln_s} %{name}-jsp-%{jspspec}-api.jar %{name}-jsp-api.jar
   %{__mv} %{name}/servlet-api.jar %{name}-servlet-%{servletspec}-api.jar
   %{__ln_s} %{name}-servlet-%{servletspec}-api.jar %{name}-servlet-api.jar
   %{__mv} %{name}/el-api.jar %{name}-el-%{elspec}-api.jar
   %{__ln_s} %{name}-el-%{elspec}-api.jar %{name}-el-api.jar
popd

pushd output/build
    %{_bindir}/build-jar-repository lib ecj 2>&1
popd

pushd ${RPM_BUILD_ROOT}%{libdir}
    # symlink JSP and servlet API jars
    %{__ln_s} ../../java/%{name}-jsp-%{jspspec}-api.jar .
    %{__ln_s} ../../java/%{name}-servlet-%{servletspec}-api.jar .
    %{__ln_s} ../../java/%{name}-el-%{elspec}-api.jar .
    %{__ln_s} $(build-classpath ecj/ecj) jasper-jdt.jar
    %{__cp} -a ../../%{name}/bin/tomcat-juli.jar .
popd

# symlink to the FHS locations where we've installed things
pushd ${RPM_BUILD_ROOT}%{homedir}
    %{__ln_s} %{appdir} webapps
    %{__ln_s} %{confdir} conf
    %{__ln_s} %{libdir} lib
    %{__ln_s} %{logdir} logs
    %{__ln_s} %{tempdir} temp
    %{__ln_s} %{workdir} work
popd

# Install the maven metadata for the spec impl artifacts as other projects use them
#%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_mavenpomdir}
pushd res/maven
    for pom in *.pom; do
        # fix-up version in all pom files
        sed -i 's/@MAVEN.DEPLOY.VERSION@/%{version}/g' $pom
    done
popd

# Configure and install maven artifacts
%mvn_artifact res/maven/tomcat-el-api.pom output/build/lib/el-api.jar
%mvn_artifact res/maven/tomcat-jsp-api.pom output/build/lib/jsp-api.jar
%mvn_artifact res/maven/tomcat-servlet-api.pom output/build/lib/servlet-api.jar

%mvn_file org.apache.tomcat:tomcat-annotations-api tomcat/annotations-api
%mvn_artifact res/maven/tomcat-annotations-api.pom ${RPM_BUILD_ROOT}%{libdir}/annotations-api.jar
%mvn_artifact res/maven/tomcat-api.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-api.jar
%mvn_file org.apache.tomcat:tomcat-catalina-ant tomcat/catalina-ant
%mvn_artifact res/maven/tomcat-catalina-ant.pom ${RPM_BUILD_ROOT}%{libdir}/catalina-ant.jar
%mvn_file org.apache.tomcat:tomcat-catalina-ha tomcat/catalina-ha
%mvn_artifact res/maven/tomcat-catalina-ha.pom ${RPM_BUILD_ROOT}%{libdir}/catalina-ha.jar
%mvn_file org.apache.tomcat:tomcat-catalina tomcat/catalina
%mvn_artifact res/maven/tomcat-catalina.pom ${RPM_BUILD_ROOT}%{libdir}/catalina.jar
%mvn_artifact res/maven/tomcat-coyote.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-coyote.jar
%mvn_artifact res/maven/tomcat-dbcp.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-dbcp.jar
%mvn_artifact res/maven/tomcat-i18n-cs.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-i18n-cs.jar
%mvn_artifact res/maven/tomcat-i18n-de.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-i18n-de.jar
%mvn_artifact res/maven/tomcat-i18n-es.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-i18n-es.jar
%mvn_artifact res/maven/tomcat-i18n-fr.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-i18n-fr.jar
%mvn_artifact res/maven/tomcat-i18n-ja.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-i18n-ja.jar
%mvn_artifact res/maven/tomcat-i18n-ko.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-i18n-ko.jar
%mvn_artifact res/maven/tomcat-i18n-pt-BR.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-i18n-pt-BR.jar
%mvn_artifact res/maven/tomcat-i18n-ru.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-i18n-ru.jar
%mvn_artifact res/maven/tomcat-i18n-zh-CN.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-i18n-zh-CN.jar
%mvn_file org.apache.tomcat:tomcat-jasper-el tomcat/jasper-el
%mvn_artifact res/maven/tomcat-jasper-el.pom ${RPM_BUILD_ROOT}%{libdir}/jasper-el.jar
%mvn_file org.apache.tomcat:tomcat-jasper tomcat/jasper
%mvn_artifact res/maven/tomcat-jasper.pom ${RPM_BUILD_ROOT}%{libdir}/jasper.jar
%mvn_file org.apache.tomcat:tomcat-jaspic-api tomcat/jaspic-api
%mvn_artifact res/maven/tomcat-jaspic-api.pom ${RPM_BUILD_ROOT}%{libdir}/jaspic-api.jar
%mvn_artifact res/maven/tomcat-jdbc.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-jdbc.jar
%mvn_artifact res/maven/tomcat-jni.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-jni.jar
%mvn_artifact res/maven/tomcat-juli.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-juli.jar
%mvn_file org.apache.tomcat:tomcat-ssi tomcat/catalina-ssi
%mvn_artifact res/maven/tomcat-ssi.pom ${RPM_BUILD_ROOT}%{libdir}/catalina-ssi.jar
%mvn_file org.apache.tomcat:tomcat-storeconfig tomcat/catalina-storeconfig
%mvn_artifact res/maven/tomcat-storeconfig.pom ${RPM_BUILD_ROOT}%{libdir}/catalina-storeconfig.jar
%mvn_file org.apache.tomcat:tomcat-tribes tomcat/catalina-tribes
%mvn_artifact res/maven/tomcat-tribes.pom ${RPM_BUILD_ROOT}%{libdir}/catalina-tribes.jar
%mvn_artifact res/maven/tomcat-util-scan.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-util-scan.jar
%mvn_artifact res/maven/tomcat-util.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-util.jar
%mvn_file org.apache.tomcat:tomcat-websocket-api tomcat/websocket-api
%mvn_artifact res/maven/tomcat-websocket-api.pom ${RPM_BUILD_ROOT}%{libdir}/websocket-api.jar
%mvn_artifact res/maven/tomcat-websocket.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-websocket.jar
%mvn_artifact res/maven/tomcat.pom

%mvn_install

%pre
# add the tomcat user and group
getent group tomcat >/dev/null || %{_sbindir}/groupadd -f -g %{tcuid} -r tomcat
if ! getent passwd tomcat >/dev/null ; then
    if ! getent passwd %{tcuid} >/dev/null ; then
        %{_sbindir}/useradd -r -u %{tcuid} -g tomcat -d %{homedir} -s /sbin/nologin -c "Apache Tomcat" tomcat
        # Tomcat uses a reserved ID, so there should never be an else
    fi
fi
exit 0

%post
# install but don't activate
%systemd_post %{name}.service

%post jsp-%{jspspec}-api
%{_sbindir}/update-alternatives --install %{_javadir}/jsp.jar jsp \
    %{_javadir}/%{name}-jsp-%{jspspec}-api.jar 20200

%post servlet-%{servletspec}-api
%{_sbindir}/update-alternatives --install %{_javadir}/servlet.jar servlet \
    %{_javadir}/%{name}-servlet-%{servletspec}-api.jar 30000

%post el-%{elspec}-api
%{_sbindir}/update-alternatives --install %{_javadir}/elspec.jar elspec \
   %{_javadir}/%{name}-el-%{elspec}-api.jar 20300

%preun
# clean tempdir and workdir on removal or upgrade
%{__rm} -rf %{workdir}/* %{tempdir}/*
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service 

%postun jsp-%{jspspec}-api
if [ "$1" = "0" ]; then
    %{_sbindir}/update-alternatives --remove jsp \
        %{_javadir}/%{name}-jsp-%{jspspec}-api.jar
fi

%postun servlet-%{servletspec}-api
if [ "$1" = "0" ]; then
    %{_sbindir}/update-alternatives --remove servlet \
        %{_javadir}/%{name}-servlet-%{servletspec}-api.jar
fi

%postun el-%{elspec}-api
if [ "$1" = "0" ]; then
    %{_sbindir}/update-alternatives --remove elspec \
        %{_javadir}/%{name}-el-%{elspec}-api.jar
fi

%files 
%defattr(0664,root,tomcat,0755)
%doc {LICENSE,NOTICE,RELEASE*}
%attr(0755,root,root) %{_bindir}/%{name}-digest
%attr(0755,root,root) %{_bindir}/%{name}-tool-wrapper
%attr(0755,root,root) %{_sbindir}/%{name}
%attr(0644,root,root) %{_unitdir}/%{name}.service
%attr(0644,root,root) %{_unitdir}/%{name}@.service
%attr(0755,root,root) %dir %{_libexecdir}/%{name}
%attr(0755,root,root) %dir %{_localstatedir}/lib/tomcats
%attr(0644,root,root) %{_libexecdir}/%{name}/functions
%attr(0755,root,root) %{_libexecdir}/%{name}/preamble
%attr(0755,root,root) %{_libexecdir}/%{name}/server
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}.disabled
%attr(0755,root,tomcat) %dir %{basedir}
%attr(0755,root,tomcat) %dir %{confdir}

%defattr(0664,tomcat,root,0770)
%attr(0770,tomcat,root) %dir %{logdir}

%defattr(0664,root,tomcat,0770)
%attr(0770,root,tomcat) %dir %{cachedir}
%attr(0770,root,tomcat) %dir %{tempdir}
%attr(0770,root,tomcat) %dir %{workdir}

%defattr(0644,root,tomcat,0775)
%attr(0775,root,tomcat) %dir %{appdir}
%attr(0775,root,tomcat) %dir %{confdir}/Catalina
%attr(0775,root,tomcat) %dir %{confdir}/Catalina/localhost
%attr(0755,root,tomcat) %dir %{confdir}/conf.d
%{confdir}/conf.d/README
%{confdir}/conf.d/java-9-start-up-parameters.conf
%config(noreplace) %{confdir}/%{name}.conf
%config(noreplace) %{confdir}/*.policy
%config(noreplace) %{confdir}/*.properties
%config(noreplace) %{confdir}/context.xml
%config(noreplace) %{confdir}/server.xml
%attr(0640,root,tomcat) %config(noreplace) %{confdir}/tomcat-users.xml
%attr(0664,root,tomcat) %{confdir}/tomcat-users.xsd
%attr(0664,root,tomcat) %config(noreplace) %{confdir}/jaspic-providers.xml
%attr(0664,root,tomcat) %{confdir}/jaspic-providers.xsd
%config(noreplace) %{confdir}/web.xml
%dir %{homedir}
%{bindir}/bootstrap.jar
%{bindir}/catalina-tasks.xml
%{homedir}/lib
%{homedir}/temp
%{homedir}/webapps
%{homedir}/work
%{homedir}/logs
%{homedir}/conf

%files admin-webapps
%defattr(0664,root,tomcat,0755)
%{appdir}/host-manager
%{appdir}/manager

%files docs-webapp
%{appdir}/docs

%files lib -f .mfiles
%dir %{libdir}
%{libdir}/*.jar
%{_javadir}/*.jar
%{bindir}/tomcat-juli.jar
%exclude %{libdir}/%{name}-el-%{elspec}-api.jar
%exclude %{libdir}/%{name}-servlet-%{servletspec}*.jar
%exclude %{libdir}/%{name}-jsp-%{jspspec}*.jar
%exclude %{_javadir}/%{name}-servlet-%{servletspec}*.jar
%exclude %{_javadir}/%{name}-el-%{elspec}-api.jar
%exclude %{_javadir}/%{name}-jsp-%{jspspec}*.jar
%exclude %{_javadir}/%{name}-servlet-api.jar
%exclude %{_javadir}/%{name}-el-api.jar
%exclude %{_javadir}/%{name}-jsp-api.jar
%exclude %{_jnidir}/*

%files jsp-%{jspspec}-api -f .mfiles-tomcat-jsp-api
%{_javadir}/%{name}-jsp-%{jspspec}*.jar
%{libdir}/%{name}-jsp-%{jspspec}*.jar
%{_javadir}/%{name}-jsp-api.jar

%files servlet-%{servletspec}-api -f .mfiles-tomcat-servlet-api
%doc LICENSE
%{_javadir}/%{name}-servlet-%{servletspec}*.jar
%{libdir}/%{name}-servlet-%{servletspec}*.jar
%{_javadir}/%{name}-servlet-api.jar

%files el-%{elspec}-api -f .mfiles-tomcat-el-api
%doc LICENSE
%{_javadir}/%{name}-el-%{elspec}-api.jar
%{libdir}/%{name}-el-%{elspec}-api.jar
%{_javadir}/%{name}-el-api.jar

%files webapps
%defattr(0644,tomcat,tomcat,0755)
%{appdir}/ROOT


%changelog
* Thu Jan 18 2024 Hui Wang <huwang@redhat.com> - 1:9.0.62-27.3
- Resolves: RHEL-20721

* Wed Dec 06 2023 Hui Wang <huwang@redhat.com> - 1:9.0.62-27.2
- Resolves: RHEL-13907
- Resolves: RHEL-13904
- Resolves: RHEL-12951
- Resolves: RHEL-2386
- Revert change for obsoleting pki-servlet-engine

* Fri Nov 03 2023 Hui Wang <huwang@redhat.com> - 1:9.0.62-27.1
- Resolves: RHEL-6971 Add Obsoletes to tomcat package

* Fri Oct 13 2023 Hui Wang <huwang@redhat.com> - 1:9.0.62-27
- Related: RHEL-12543
- Bump release number

* Thu Oct 12 2023 Hui Wang <huwang@redhat.com> - 1:9.0.62-16
- Resolves: RHEL-12543 HTTP/2: Multiple HTTP/2 enabled web servers are vulnerable to a DDoS attack (Rapid Reset Attack)
- Remove JDK subpackges which are unused

* Fri Sep 08 2023 Hui Wang <huwang@redhat.com> - 1:9.0.62-14
- Related: RHEL-2330 Bump release number

* Thu Sep 07 2023 Hui Wang <huwang@redhat.com> - 1:9.0.62-13
- Resolves: RHEL-2330 Revert the fix for pki-servlet-engine

* Fri Aug 25 2023 Coty Sutherland <csutherl@redhat.com> - 1:9.0.62-12
- Related: #2184135 Declare file conflicts

* Fri Aug 25 2023 Coty Sutherland <csutherl@redhat.com> - 1:9.0.62-11
- Resolves: #2184135 Fix bug introduced in initial commit

* Fri Aug 18 2023 Hui Wang <huwang@redhat.com> - 1:9.0.62-10
- Resolves: #2210630 CVE-2023-28709 tomcat
- Resolves: #2181448 CVE-2023-28708 tomcat: not including the secure attribute causes information disclosure

* Thu Aug 17 2023 Hui Wang <huwang@redhat.com> - 1:9.0.62-9
- Resolves: #2184135 Add Obsoletes to tomcat package

* Thu Aug 17 2023 Hui Wang <huwang@redhat.com> - 1:9.0.62-8
- Resolves: #2189676 Missing Tomcat POM files in RHEL 8.9

* Tue Aug 15 2023 Hui Wang <huwang@redhat.com> - 1:9.0.62-7
- Related: #2173874 Tomcat installs older java even though newer java is installed
- Bump release number

* Fri Aug 11 2023 Hui Wang <huwang@redhat.com> - 1:9.0.62-6
- Resolves: #2173874 Tomcat installs older java even though newer java is installed
- Sync with rhel-8.8.0 branch

* Thu Feb 16 2023 Coty Sutherland <csutherl@redhat.com> - 1:9.0.62-5
- Related: #2160455 Add conflicts to subpackage

* Wed Feb 15 2023 Hui Wang <huwang@redhat.com> - 1:9.0.62-4
- Resolves: #2160455 Add Tomcat 9 to RHEL8
