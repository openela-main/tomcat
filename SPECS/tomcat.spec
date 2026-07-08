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

%global jspspec 3.1
%global major_version 10
%global minor_version 1
%global micro_version 49
%global packdname %{name}-%{major_version}.%{minor_version}.%{micro_version}.redhat-00011-src
%global servletspec 6.0
%global elspec 5.0
%global tcuid 53


# FHS 3.0 compliant tree structure - http://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html
%global basedir %{_var}/lib/%{name}
%global appdir %{basedir}/webapps
%global appdir_javaee %{basedir}/webapps-javaee
%global homedir %{_datadir}/%{name}
%global bindir %{homedir}/bin
%global confdir %{_sysconfdir}/%{name}
%global libdir %{_javadir}/%{name}
%global logdir %{_var}/log/%{name}
%global cachedir %{_var}/cache/%{name}
%global tempdir %{cachedir}/temp
%global workdir %{cachedir}/work

Name:          tomcat
Epoch:         1
Version:       %{major_version}.%{minor_version}.%{micro_version}
Release:       3%{?dist}
Summary:       Apache Servlet/JSP Engine, RI for Servlet %{servletspec}/JSP %{jspspec} API

License:       Apache-2.0
URL:           http://tomcat.apache.org/
Source0:       %{packdname}.zip
Source1:       %{name}-%{major_version}.%{minor_version}.conf
Source2:       %{name}-%{major_version}.%{minor_version}.sysconfig
Source3:       %{name}-%{major_version}.%{minor_version}.wrapper
Source4:       %{name}-%{major_version}.%{minor_version}.logrotate
Source5:       %{name}-%{major_version}.%{minor_version}-digest.script
Source6:       %{name}-%{major_version}.%{minor_version}-tool-wrapper.script
Source7:       %{name}-%{major_version}.%{minor_version}.service
Source8:       %{name}-functions
Source9:       %{name}-preamble
Source10:      %{name}-server
Source11:      %{name}-named.service
Source12:      module-start-up-parameters.conf

Patch0:        %{name}-%{major_version}.%{minor_version}-bootstrap-MANIFEST.MF.patch
Patch1:        %{name}-%{major_version}.%{minor_version}-tomcat-users-webapp.patch
Patch3:        %{name}-%{major_version}.%{minor_version}-catalina-policy.patch
Patch4:        %{name}-%{major_version}.%{minor_version}-bnd-annotation.patch
Patch5:        %{name}-%{major_version}.%{minor_version}-JDTCompiler.patch
Patch6:        rhbz-1857043.patch
# Patch 7 can be dropped when ECJ is updated to a newer version
Patch7:        build-with-java-25.patch

BuildArch:     noarch
ExclusiveArch:  %{java_arches} noarch

BuildRequires: ant >= 1.10.2
BuildRequires: ecj >= 4.20
BuildRequires: findutils
BuildRequires: javapackages-local
BuildRequires: aqute-bnd
BuildRequires: aqute-bndlib
BuildRequires: systemd
BuildRequires: tomcat-jakartaee-migration
BuildRequires: java-25-devel

Requires:      (java-headless or java-25-headless)
Requires:      javapackages-tools
Requires:      %{name}-lib = %{epoch}:%{version}-%{release}

Requires(pre):    shadow-utils
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

Conflicts: tomcat9

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
Conflicts: tomcat9
Conflicts: tomcat9-admin-webapps

%description admin-webapps
The host-manager and manager web applications for Apache Tomcat.

%package docs-webapp
Summary: The docs web application for Apache Tomcat
Requires: %{name} = %{epoch}:%{version}-%{release}
Conflicts: tomcat9
Conflicts: tomcat9-docs-webapp

%description docs-webapp
The docs web application for Apache Tomcat.

%package jsp-%{jspspec}-api
Summary: Apache Tomcat JavaServer Pages v%{jspspec} API Implementation Classes
Provides: jsp = %{jspspec}
Obsoletes: %{name}-jsp-api < %{jspspec}
Obsoletes: %{name}-jsp-2.3-api < %{version}
Requires: %{name}-servlet-%{servletspec}-api = %{epoch}:%{version}-%{release}
Requires: %{name}-el-%{elspec}-api = %{epoch}:%{version}-%{release}
Conflicts: tomcat9
Conflicts: tomcat9-jsp-2.3-api

%description jsp-%{jspspec}-api
Apache Tomcat JSP API Implementation Classes.

%package lib
Summary: Libraries needed to run the Tomcat Web container
Requires: %{name}-jsp-%{jspspec}-api = %{epoch}:%{version}-%{release}
Requires: %{name}-servlet-%{servletspec}-api = %{epoch}:%{version}-%{release}
Requires: %{name}-el-%{elspec}-api = %{epoch}:%{version}-%{release}
Requires: ecj >= 4.20
Recommends: tomcat-jakartaee-migration
Requires(preun): coreutils
Conflicts: tomcat9
Conflicts: tomcat9-lib
Conflicts: tomcat9-jsp-2.3-api
Conflicts: tomcat9-servlet-4.0-api
Conflicts: tomcat9-el-3.0-api

%description lib
Libraries needed to run the Tomcat Web container.

%package servlet-%{servletspec}-api
Summary: Apache Tomcat Java Servlet v%{servletspec} API Implementation Classes
Provides: servlet = %{servletspec}
Obsoletes: %{name}-servlet-api < %{servletspec}
Obsoletes: %{name}-servlet-4.0-api < %{version}
Conflicts: tomcat9
Conflicts: tomcat9-servlet-4.0-api

%description servlet-%{servletspec}-api
Apache Tomcat Servlet API Implementation Classes.

%package el-%{elspec}-api
Summary: Apache Tomcat Expression Language v%{elspec} API Implementation Classes
Provides: el_api = %{elspec}
Obsoletes: %{name}-el-api < %{elspec}
Obsoletes: %{name}-el-3.0-api < %{version}
Conflicts: tomcat9
Conflicts: tomcat9-el-3.0-api

%description el-%{elspec}-api
Apache Tomcat EL API Implementation Classes.

%package webapps
Summary: The ROOT web application for Apache Tomcat
Requires: %{name} = %{epoch}:%{version}-%{release}
Conflicts: tomcat9
Conflicts: tomcat9-webapps

%description webapps
The ROOT web application for Apache Tomcat.

%prep
%setup -q -n apache-%{packdname}
# remove pre-built binaries and windows files
find . -type f \( -name "*.bat" -o -name "*.class" -o -name Thumbs.db -o -name "*.gz" -o \
   -name "*.jar" -o -name "*.war" -o -name "*.zip" \) -delete

%patch 0 -p0
%patch 1 -p0
%patch 3 -p0
%patch 4 -p0
%patch 5 -p0
%patch 6 -p0
%patch 7 -p0

# Remove webservices naming resources as it's generally unused
%{__rm} -rf java/org/apache/naming/factory/webservices

# Configure maven files
%mvn_package ":tomcat-el-api" tomcat-el-api
%mvn_alias "org.apache.tomcat:tomcat-el-api" "jakarta.servlet:jakarta.servlet-api"
%mvn_package ":tomcat-jsp-api" tomcat-jsp-api
%mvn_alias "org.apache.tomcat:tomcat-jsp-api" "jakarta.servlet:jakarta.servlet.jsp"
%mvn_package ":tomcat-servlet-api" tomcat-servlet-api

%pom_remove_dep org.apache.tomcat:tomcat-tribes res/maven/tomcat-storeconfig.pom
%pom_remove_dep org.apache.tomcat:tomcat-catalina-ha res/maven/tomcat-storeconfig.pom


%build
# we don't care about the tarballs and we're going to replace jars
# so just create a dummy file for later removal
touch HACK

# Adding JAVA_HOME to always compile with java-25 instead of autodetecting
export JAVA_HOME=%{_jvmdir}/java-25-openjdk
export PATH=$JAVA_HOME/bin:$PATH

# who needs a build.properties file anyway
ant -Dbase.path="." \
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
  -Dbnd.jar="$(build-classpath aqute-bnd/biz.aQute.bnd)" \
  -Dbnd-annotation.jar="$(build-classpath aqute-bnd/biz.aQute.bnd.annotation)" \
  -Dversion="%{version}" \
  -Dversion.build="%{micro_version}" \
  -Dmigration-lib.jar="$(build-classpath tomcat-jakartaee-migration/jakartaee-migration.jar)" \
  deploy

# remove some jars that we'll replace with symlinks later
%{__rm} output/build/bin/commons-daemon.jar output/build/lib/ecj.jar output/build/lib/jakartaee-migration.jar
# Remove the example webapps per Apache Tomcat Security Considerations
# see https://tomcat.apache.org/tomcat-10.1-doc/security-howto.html
%{__rm} -rf output/build/webapps/examples


%install
# build initial path structure
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_bindir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_sbindir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{appdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{appdir_javaee}
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

# Clustering is unsupported in RHEL
rm -f ${RPM_BUILD_ROOT}%{libdir}/catalina-ha.jar
rm -f ${RPM_BUILD_ROOT}%{libdir}/catalina-tribes.jar

%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE1} \
    > ${RPM_BUILD_ROOT}%{confdir}/%{name}.conf
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE2} \
    > ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/%{name}
%{__install} -m 0755 %{SOURCE3} \
    ${RPM_BUILD_ROOT}%{_sbindir}/%{name}
%{__install} -m 0644 %{SOURCE7} \
    ${RPM_BUILD_ROOT}%{_unitdir}/%{name}.service
%{__sed} -e "s|\@\@\@TCLOG\@\@\@|%{logdir}|g" %{SOURCE4} \
    > ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}.disabled
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE5} \
    > ${RPM_BUILD_ROOT}%{_bindir}/%{name}-digest
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE6} \
    > ${RPM_BUILD_ROOT}%{_bindir}/%{name}-tool-wrapper

%{__install} -m 0644 %{SOURCE8} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}/functions
%{__install} -m 0755 %{SOURCE9} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}/preamble
%{__install} -m 0755 %{SOURCE10} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}/server
%{__install} -m 0644 %{SOURCE11} \
    ${RPM_BUILD_ROOT}%{_unitdir}/%{name}@.service

%{__install} -m 0644 %{SOURCE12} ${RPM_BUILD_ROOT}%{confdir}/conf.d/

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
    %{_bindir}/build-jar-repository lib tomcat-jakartaee-migration 2>&1
popd

pushd ${RPM_BUILD_ROOT}%{libdir}
    # symlink JSP and servlet API jars
    %{__ln_s} ../../java/%{name}-jsp-%{jspspec}-api.jar .
    %{__ln_s} ../../java/%{name}-servlet-%{servletspec}-api.jar .
    %{__ln_s} ../../java/%{name}-el-%{elspec}-api.jar .
    %{__ln_s} $(build-classpath ecj/ecj) jasper-jdt.jar
    %{__ln_s} $(build-classpath tomcat-jakartaee-migration/jakartaee-migration) jakartaee-migration.jar
    %{__ln_s} $(build-classpath apache-commons-compress/commons-compress) commons-compress.jar
    %{__ln_s} $(build-classpath apache-commons-io/commons-io) commons-io.jar
    %{__ln_s} $(build-classpath apache-commons-lang3/commons-lang3) commons-lang3.jar
    %{__ln_s} $(build-classpath bcel/bcel) bcel.jar

    cp ../../%{name}/bin/tomcat-juli.jar .
popd

# symlink to the FHS locations where we've installed things
pushd ${RPM_BUILD_ROOT}%{homedir}
    %{__ln_s} %{appdir} webapps
    %{__ln_s} %{appdir_javaee} webapps-javaee
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
%mvn_file org.apache.tomcat:tomcat-catalina tomcat/catalina
%mvn_artifact res/maven/tomcat-catalina.pom ${RPM_BUILD_ROOT}%{libdir}/catalina.jar
%mvn_artifact res/maven/tomcat-coyote.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-coyote.jar
%mvn_artifact res/maven/tomcat-coyote-ffm.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-coyote-ffm.jar
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
%mvn_artifact res/maven/tomcat-util-scan.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-util-scan.jar
%mvn_artifact res/maven/tomcat-util.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-util.jar
%mvn_file org.apache.tomcat:tomcat-websocket-api tomcat/websocket-api
%mvn_artifact res/maven/tomcat-websocket-api.pom ${RPM_BUILD_ROOT}%{libdir}/websocket-api.jar
%mvn_artifact res/maven/tomcat-websocket.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-websocket.jar
%mvn_artifact res/maven/tomcat-websocket-client-api.pom ${RPM_BUILD_ROOT}%{libdir}/websocket-client-api.jar
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

%preun
# clean tempdir and workdir on removal or upgrade
%{__rm} -rf %{workdir}/* %{tempdir}/*
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

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
%attr(0775,root,tomcat) %dir %{appdir_javaee}
%attr(0775,root,tomcat) %dir %{confdir}/Catalina
%attr(0775,root,tomcat) %dir %{confdir}/Catalina/localhost
%attr(0755,root,tomcat) %dir %{confdir}/conf.d
%{confdir}/conf.d/README
%{confdir}/conf.d/module-start-up-parameters.conf
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
%{homedir}/webapps-javaee
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
* Mon Jul 6 2026 Pietro Meloni <pmeloni@redhat.com> - 1:10.1.49-3
- Related: RHEL-168577 Remove unnecessary patch

* Thu Jun 4 2026 Pietro Meloni <pmeloni@redhat.com> - 1:10.1.49-2
- Resolves: RHEL-168577 Remove tomcat clustering JAR from RPM builds
  Resolves: CVE-2026-29146
  tomcat: Apache Tomcat: Information disclosure via Padding Oracle vulnerability in EncryptInterceptor
  Resolves: CVE-2026-34486
  tomcat: Apache Tomcat: Missing Encryption of Sensitive Data due to EncryptInterceptor bypass


* Wed Apr 22 2026 Pietro Meloni <pmeloni@redhat.com> - 1:10.1.36-3.el10_1.1
- Resolves: RHEL-150719
  Certificate revocation bypass due to improper OCSP response validation (CVE-2026-24734)

* Mon Feb 16 2026 Coty Sutherland <csutherl@redhat.com> - 1:10.1.49-1
- Resolves: RHEL-150099 Rebase tomcat package to enable PQC features

* Fri Jan 23 2026 Pietro Meloni <pmeloni@redhat.com> - 1:10.1.36-4
- Resolves: RHEL-124493
  tomcat: Directory traversal via rewrite with possible RCE (CVE-2025-55752)
- Resolves: RHEL-132560
  tomcat: Bypass of rules in Rewrite Valve (CVE-2025-31651)
- Resolves: RHEL-132526
  tomcat: Denial of service (CVE-2025-61795)

* Mon Dec 15 2025 Eduard Abdullin <eabdullin@almalinux.org> - 1:10.1.36-4
- Exclude i686 architecture from build

* Thu Aug 14 2025 Adam Krajcik <akrajcik@redhat.com> - 1:10.1.36-3
- Resolves: RHEL-102184
  tomcat: http/2 "MadeYouReset" DoS attack through HTTP/2 control frames (CVE-2025-48989)
- Resolves: RHEL-108906
  tomcat: Denial of service (CVE-2025-52520)

* Wed Aug 13 2025 Adam Krajcik <akrajcik@redhat.com> - 1:10.1.36-2
- Resolves: RHEL-108900
  tomcat: Apache  FileUpload DOS via part headers (CVE-2025-48976)
- Resolves: RHEL-108902
  tomcat: Dos in multipart upload (CVE-2025-48988)
- Resolves: RHEL-108904
  tomcat: Security constraint bypass for pre/post-resources (CVE-2025-49125)
- Resolves: RHEL-108908
  tomcat: Denial of service (CVE-2025-53506)

* Mon Apr 14 2025 Adam Krajcik <akrajcik@redhat.com> - 1:10.1.36-1
- Rebase tomcat to 10.1.36
- Resolves: RHEL-82925
  tomcat: Potential RCE and/or information disclosure and/or information corruption with partial PUT (CVE-2025-24813)
- Resolves: RHEL-87272
  tomcat: DoS in examples web application (CVE-2024-54677)
- Resolves: RHEL-87273
  tomcat: Authentication bypass when using Jakarta Authentication API (CVE-2024-52316)
- Resolves: RHEL-85343 - NoClassDefFoundError when using migration tool

* Tue Feb 11 2025 Adam Krajcik <akrajcik@redhat.com> - 1:10.1.8-2
- Resolves: RHEL-78899 Add missing Obsoletes

* Wed Feb 05 2025 Adam Krajcik <akrajcik@redhat.com> - 1:10.1.8-1
- Resolves: RHEL-51222 Upgrade tomcat to 10.1.8

* Tue Oct 29 2024 Troy Dawson <tdawson@redhat.com> - 1:9.0.87-3
- Bump release for October 2024 mass rebuild:
  Resolves: RHEL-64018

* Mon Aug 12 2024 Adam Krajcik <akrajcik@redhat.com> - 1:9.0.87-2
- Resolves: RHEL-50166 - Rebase tomcat to version 9.0.87
- Resolves: RHEL-12274 - Use src.zip file as a Source0 instead of tar.gz
- Resolves: RHEL-51277 - Prune changelog to remove non-relevant history
- Resolves: RHEL-52906 - tomcat: Switch to using Java 21 as the default JDK
- Resolves: RHEL-55194 - Fix changelog version
- Resolves: RHEL-46156
  tomcat: Improper Handling of Exceptional Conditions (CVE-2024-34750)

* Mon Jun 24 2024 Troy Dawson <tdawson@redhat.com> - 1:9.0.83-3
- Bump release for June 2024 mass rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:9.0.83-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 01 2023 Hui Wang <huwang@redhat.com> - 1:9.0.83-1
- Update to 9.0.83
