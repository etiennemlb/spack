# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CxiDriver(Package):
    """This are the Linux driver headers for the Cray/HPE Cassini 1 and 2
    high-speed network interconnect (aka. Slingshot), and its Ethernet driver."""

    homepage = "https://github.com/HewlettPackard/shs-cxi-driver"
    git = "https://github.com/HewlettPackard/shs-cxi-driver.git"

    license("GPL-2.0")

    version("main", branch="main")
    # Something changed in the headers which the libfabric 1.22 is not aware of.
    # We thus get build issues.
    version("1.0.0", commit="cab7fca6b17f3e3efbe5a48f99c4158af87c654c")

    def install(self, spec, prefix):
        with working_dir(self.stage.source_path):
            copy_tree("include", prefix.include)
