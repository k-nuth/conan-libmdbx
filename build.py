from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="kth", channel="stable", archs=["x86_64"]
                               , remotes="https://api.bintray.com/conan/k-nuth/kth")
    builder.add_common_builds(shared_option_name="libmdbx:shared", pure_c=True)
    builder.run()

