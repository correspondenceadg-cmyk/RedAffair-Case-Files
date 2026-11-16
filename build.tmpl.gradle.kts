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
            jniLibs.srcDir(layout.buildDirectory.dir("generated/duplicateJniLibs"))
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

val copySiteNativeTasks = tasks.matching { it.name.startsWith("copySitePackagesNativeLibs_") }

val duplicateLibpython by tasks.registering(Copy::class) {
    dependsOn(copySiteNativeTasks)
    from("src/main/jniLibs") {
        include("*/libpython3.so")
        rename { "libpython3.13.so" }
    }
    into(layout.buildDirectory.dir("generated/duplicateJniLibs"))
}

tasks.matching { it.name.startsWith("merge") && it.name.endsWith("NativeLibs") }.configureEach {
    dependsOn(duplicateLibpython)
}

{{ site_packages_tasks }}
