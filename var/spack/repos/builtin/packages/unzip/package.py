# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Unzip(MakefilePackage):
    """Unzip is a compression and file packaging/archive utility."""

    homepage = "http://www.info-zip.org/Zip.html"
    url = "https://downloads.sourceforge.net/infozip/unzip60.tar.gz"

    license("custom")

    version(
        "6.0", sha256="036d96991646d0449ed0aa952e4fbe21b476ce994abc276e49d30e686708bd37"
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # clang and oneapi need this patch, likely others
    # There is no problem with it on gcc, so make it a catch all
    patch("configure-cflags.patch")
    patch("strip.patch")

    def get_make_args(self):
        make_args = ["-f", join_path("unix", "Makefile")]

        cflags = []
        cflags.append("-Wno-error=implicit-function-declaration")
        cflags.append("-Wno-error=implicit-int")
        cflags.append("-DLARGE_FILE_SUPPORT")

        # NOTE: No quotes around the flags, its already going to be passed as
        # one argument. If we use quotes, we'll call make like so:
        # $ make ... 'LOC="-Wno-error=implicit-function-declaration -Wno-error=implicit-int -DLARGE_FILE_SUPPORT"'
        # Which will execute target `flags:  unix/configure` giving:
        # $ sh unix/configure "cc" "-I. -Ibzip2 -DUNIX "-Wno-error=implicit-function-declaration -Wno-error=implicit-int -DLARGE_FILE_SUPPORT"" "bzip2"
        # Notice how the double quoting is broken. This misleads the script into
        # promoting `-Wno-error=implicit-int` as the directory containing the
        # bzip2 libraries. For instance:
        # $ cc -o unzip -L-Wno-error=implicit-int unzip.o ... unshrink.o zipinfo.o unix.o -s
        # Now that issue in itself is not that bad, it wont change the build
        # process.
        # The next issue is that the "-s" flag that gcc takes in and passes
        # automatically to the linker is not supported by all compiler (it
        # crashes cray's crayclang..). One can instead use `-Wl,-s`.
        # Lastly, if `-Wl,-s` is not felt like a good fix, we should probably
        # restrict unzip to the gcc compiler ?
        make_args.append(f"LOC={' '.join(cflags)}")
        return make_args

    @property
    def build_targets(self):
        target = "macosx" if "platform=darwin" in self.spec else "generic"
        return self.get_make_args() + [target]

    def url_for_version(self, version):
        return f"http://downloads.sourceforge.net/infozip/unzip{version.joined}.tar.gz"

    @property
    def install_targets(self):
        return self.get_make_args() + [f"prefix={self.prefix}", "install"]
