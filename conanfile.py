# Copyright (c) 2016-2020 Knuth Project developers.
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from conans import ConanFile, CMake, tools
import sys, os
import fileinput

def option_on_off(option):
    return "ON" if option else "OFF"

class LibMDBXConan(ConanFile):
    name = "libmdbx"
    description = "Fast embeddable key-value ACID database without WAL"
    version = "0.7.0"
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/k-nuth/conan-libmdbx"
    license = "OpenLDAP Public License"

    generators = "cmake"

    options = {"shared": [True, False],
               "fPIC": [True, False],
               "verbose": [True, False],
               "include_bins": [True, False],
    }

    default_options = {
        "shared": False,
        "fPIC": True,
        "verbose": False,
        "include_bins": False,
    }

    # exports = "conanfile.py", "mdb.def", "win32/*", "LICENSE.md"    # "CMakeLists.txt",
    # exports_sources = ["CMakeLists.txt"]
    build_policy = "missing"

    @property
    def msvc_mt_build(self):
        return "MT" in str(self.settings.get_safe("compiler.runtime"))

    @property
    def fPIC_enabled(self):
        if self.settings.compiler == "Visual Studio":
            return False
        else:
            return self.options.fPIC

    @property
    def is_shared(self):
        if self.options.shared and self.msvc_mt_build:
            return False
        else:
            return self.options.shared

    def config_options(self):
        if self.settings.compiler == "Visual Studio":
            self.options.remove("fPIC")
            if self.options.shared and self.msvc_mt_build:
                self.options.remove("shared")

    def configure(self):
        del self.settings.compiler.libcxx #Pure-C 

    def package_id(self):
        self.info.options.verbose = "ANY"

    def _fix_cmake_msvc(self):
        if self.settings.compiler != "Visual Studio":
            return
        with fileinput.FileInput(os.path.join("cmake", "compiler.cmake"), inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace('if (CMAKE_VERSION MATCHES ".*MSVC.*")', 'if (FALSE AND CMAKE_VERSION MATCHES ".*MSVC.*")'), end='')

    def source(self):
        git = tools.Git()
        # git.clone("https://github.com/erthink/libmdbx.git")
        # git.checkout("v%s" % (self.version,))
        git.clone("https://github.com/fpelliccioni/libmdbx.git")        #TODO: temp repo
        self._fix_cmake_msvc()


    def build(self):
        cmake = CMake(self)
        cmake.verbose = self.options.verbose
        cmake.definitions["BUILD_SHARED_LIBS"] = option_on_off(self.is_shared)
        cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = option_on_off(self.fPIC_enabled)
        cmake.configure(source_dir=self.source_folder)
        cmake.build()

    def package(self):
        self.copy("mdbx.h", dst="include")

        if not self.options.shared:
            self.copy("*.lib", dst="lib", keep_path=True)
            self.copy("*.a", dst="lib", keep_path=True)

        if self.options.shared:
            self.copy("*.dll", dst="lib", keep_path=True)
            self.copy("*.so", dst="lib", keep_path=True)
            self.copy("*.dylib", dst="lib", keep_path=True)

        if self.options.include_bins:
            self.copy("mdbx_chk*", dst="bin", keep_path=True)
            self.copy("mdbx_dump*", dst="bin", keep_path=True)
            self.copy("mdbx_load*", dst="bin", keep_path=True)
            self.copy("mdbx_stat*", dst="bin", keep_path=True)

        self.copy("*.pdb", dst="lib", keep_path=True)

    def package_info(self):
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["libmdbx"]
        else:
            self.cpp_info.libs = ["libmdbx"]
            
        if  self.settings.os == "Windows":
            self.cpp_info.libs.append("ntdll")
        else:
            self.cpp_info.libs.append("pthread")
