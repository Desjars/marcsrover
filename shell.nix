{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    packages = with pkgs; [
      uv
      linuxHeaders
  ];

  C_INCLUDE_PATH = "${pkgs.linuxHeaders}/include";

  shellHook = ''
    export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:${
      with pkgs;
        lib.makeLibraryPath [ glib libGL xorg.libX11 xorg.libXi ]
    }"
  '';
}
