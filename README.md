# Godot-Cpp-Base
A base repository which contains the base c++ bindings setup to use GDNative. It is designed so that a new C++ Godot project can be quickly set up with minimal hassle.

To use it in the simplest way possible to use this repository is through the following git commands executed in the same folder as a **newly created Godot project.**
```
git init
git remote add origin https://github.com/jdbener/Godot-Cpp-Base.git -f
git checkout master
cd thirdparty/godot-cpp
git submodule update --init --recursive
cd ../..
git remote rm origin
```
When run, these commands will setup the base files and include the necessary Godot libraries. However the Godot libraries will need to be built with the following commands or the optional python script found [here](https://gist.github.com/jdbener/c096d0153c0534f83b4e73d88980f898):
```
cd thirdparty/godot-cpp
scons platform=<your platform here> generate_bindings=yes bits=64 -j4
```
The -j4 can be replaced with -j[the number of cores in your computer] to speed up the build time.
The bits=64 can be replaced with bits=32 if you are running on or targeting a 32 bit system.

The build script (both for this base and the Godot library) is designed around the [Scons](https://scons.org/) build environment, so make sure you have [Scons](https://scons.org/). Then run `scons platform=[windows, linux, or osx]` to build your c++ code. The build script will automatically find `SCsub` files in your directory which it uses to determine which c++ files to build (an example is in the src directory, setup to build the required Godot linking file which tells Godot about your classes). Additionally a small header library is included which implements a (w)cout like wostream implemented using Godot's print function, try including `gstream.hpp` instead of `Godot.hpp` and then using `godot::print << "Hello World" << std::endl;`.

Finally, to build your scripts run:
```
scons platform=<your platform here> bits=64 -j4
```
**NOTE: that if you wish to build a 32 bit version of your game you must also build a 32 bit version of the Godot libraries.**
For more information about how to bind c++ code with Godot, read through their tutorial here: https://docs.godotengine.org/en/stable/tutorials/plugins/gdnative/gdnative-cpp-example.html, much of the code in this base is from this tutorial.
