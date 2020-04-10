from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="kth", channel="stable")
    builder.add_common_builds(shared_option_name="libmdbx:shared", pure_c=True)

    # filtered_builds = []
    # # for settings, options in builder.builds:
    # for settings, options, env_vars, build_requires, reference in builder.items:

    #     # # Selecting the debug runtimes (MTd, MDd) on Windows for Debug builds
    #     # if settings["compiler"] == "Visual Studio":
    #     #     if settings["compiler.runtime"].startswith("MT"):
    #     #         continue
    #     #     if settings["build_type"] == "Debug" and not settings["compiler.runtime"].endswith("d"):
    #     #         settings["compiler.runtime"] += "d"

    #     # # Build both libstdc++ and libstdc++11
    #     # elif settings["compiler"] == "gcc":
    #     #     settings["compiler.libcxx"] = "libstdc++11"
    #     #     filtered_builds.append([settings, options])

    #     #     settings["compiler.libcxx"] = "libstdc++"
    #     #     filtered_builds.append([settings, options])

    #     # else:
    #     #     filtered_builds.append([settings, options])

    # builder.builds = filtered_builds

    builder.run()

