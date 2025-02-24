{
  "targets": [
    {
      "target_name": "grandiose",
      "sources": [
        "src/grandiose_util.cc",
        "src/grandiose_find.cc",
        "src/grandiose_send.cc",
        "src/grandiose_receive.cc",
        "src/grandiose.cc"
      ],
      "include_dirs": [ "include", "<!(node -p \"require('node-addon-api').include_dir\")" ],
      "defines": [
        "NAPI_DISABLE_CPP_EXCEPTIONS",
        "NODE_ADDON_API_ENABLE_MAYBE"
      ],
      "conditions":[
        ["OS=='win'", {
          "msvs_settings": {
            "VCCLCompilerTool": {
              "AdditionalOptions": [ "-std:c++17", ],
            },
          },
          # windows can't do rpath, so needs to be copied next to the .node file
          "copies":[
            {
              "destination": "build/Release",
              "files": [
                "lib/win_x64/Processing.NDI.Lib.x64.dll"
              ]
            }
          ],
          "link_settings": {
            "libraries": [ "Processing.NDI.Lib.x64.lib" ],
            "library_dirs": [ "lib/win_x64" ]
          },
        }],
        ["OS=='linux'", {
          "cflags": [
            "-Wno-write-strings" # temporary, until all the C style code is replaced
          ],
          "link_settings": {
            "libraries": [
              "<(module_root_dir)/lib/linux_x64/libndi.so.5"
            ],
            "ldflags": [
              "-L<@(module_root_dir)/lib/linux_x64",
              "-Wl,-rpath=\\$$ORIGIN/../../lib/linux_x64",
            ]
          },
        }],
        ["OS=='mac'", {
          "cflags+": ["-fvisibility=hidden"],
          "xcode_settings": {
            "GCC_SYMBOLS_PRIVATE_EXTERN": "YES", # -fvisibility=hidden
            "OTHER_CPLUSPLUSFLAGS": [
              "-std=c++14",
              "-stdlib=libc++",
              "-fexceptions"
            ],
            "OTHER_LDFLAGS": [
              "-Wl,-rpath,@loader_path/../../lib/mac_universal"
            ]
          },
          "link_settings": {
            "libraries": [
              "<(module_root_dir)/lib/mac_universal/libndi.dylib"
            ],
          }
        }]
      ]
    }
  ]
}
