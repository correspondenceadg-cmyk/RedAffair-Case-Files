plugins {
    id("{{ plugin_id }}")
}

android {
    namespace = "{{ package_name }}"
    compileSdk = {{ compile_sdk }}
{{ ndk_line }}    ndkPath = "{{ ndk_path }}"

    defaultConfig {
{{ app_id_lines }}        minSdk = {{ min_sdk }}
        targetSdk = {{ target_sdk }}

        ndk {
            abiFilters += setOf({{ abi_filters }})
        }

        externalNativeBuild {
            cmake {
                arguments += listOf("-DANDROID_STL=c++_static")
            }
        }
    }

    packaging {
        jniLibs {
            useLegacyPackaging = true
        }
    }

    externalNativeBuild {
        cmake {
            path = file("src/main/cpp/CMakeLists.txt")
            version = "3.22.1"
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }

    sourceSets {
        getByName("main") {
            assets.srcDir(layout.buildDirectory.dir("generated/python_assets").get().asFile)
        }
    }

    androidResources {
        ignoreAssetsPatterns.clear()
        ignoreAssetsPatterns.addAll(listOf(
            "!.svn", "!.git", "!.ds_store", "!*.scc",
            "!CVS", "!thumbs.db", "!picasa.ini", "!*~",
            "python*", "lib-dynload", "site-packages"
        ))
    }
}

dependencies {
    implementation(fileTree("libs") { include("*.aar", "*.jar") })
{{ extra_deps }}
}

tasks.whenTaskAdded {
    if (name.startsWith("merge") && name.endsWith("NativeLibs")) {
        doFirst {
            val abis = listOf("arm64-v8a", "x86_64")
            for (abi in abis) {
                val src = file("src/main/jniLibs/$abi/libpython3.so")
                val dst = file("src/main/jniLibs/$abi/libpython3.13.so")
                if (src.exists() && !dst.exists()) {
                    dst.writeBytes(src.readBytes())
                    println("Duplicated libpython3.so -> libpython3.13.so for $abi")
                }
            }
        }
    }
}

{{ site_packages_tasks }}
