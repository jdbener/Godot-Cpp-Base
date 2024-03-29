#!python
import os, subprocess

opts = Variables([], ARGUMENTS)

# Gets the standard flags CC, CCX, etc.
env = DefaultEnvironment()

# Define our options
opts.Add(EnumVariable('target', "Compilation target", 'debug', ['d', 'debug', 'r', 'release']))
opts.Add(EnumVariable('platform', "Compilation platform", '', ['', 'windows', 'linuxbsd', 'linux', 'osx']))
opts.Add(EnumVariable('p', "Compilation target, alias for 'platform'", '', ['', 'windows', 'linuxbsd', 'linux', 'osx']))
opts.Add(EnumVariable('bits', 'The number of bits the application should support.', "64", ["32", "64"]))
opts.Add(BoolVariable('use_llvm', "Use the LLVM / Clang compiler", 'no'))
opts.Add(PathVariable('target_path', 'The path where the lib is installed.', 'src/bin/'))
opts.Add(PathVariable('target_name', 'The library name.', 'libgame', PathVariable.PathAccept))
opts.Add(BoolVariable('clang_complete', 'Should we generate a .clang_complete file?', "yes"))

# Generates help for the -h scons option.
Help(opts.GenerateHelpText(env))

# Local dependency paths, adapt them to your setup
godot_headers_path = "thirdparty/godot-cpp/godot-headers/"
cpp_bindings_path = "thirdparty/godot-cpp/"
cpp_library = "libgodot-cpp"

# Updates the environment with the option variables.
opts.Update(env)

# Process some arguments
if env['use_llvm']:
	env['CC'] = 'clang'
	env['CXX'] = 'clang++'

if env['p'] != '':
	env['platform'] = env['p']

if env['platform'] == '':
	print("No valid target platform selected.")
	quit()

# For the reference:
# - CCFLAGS are compilation flags shared between C and C++
# - CFLAGS are for C-specific compilation flags
# - CXXFLAGS are for C++-specific compilation flags
# - CPPFLAGS are for pre-processor flags
# - CPPDEFINES are for pre-processor defines
# - LINKFLAGS are for linking flags

# Check our platform specifics
if env['platform'] == "osx":
	env['target_path'] += 'osx/'
	cpp_library += '.osx'
	if env['target'] in ('debug', 'd'):
		env.Append(CCFLAGS=['-g', '-O2'])
	else:
		env.Append(CCFLAGS=['-O3'])
	if env['bits'] == '64':
		env.Append(LINKFLAGS=['-arch', 'x86_64'])
	else:
		env.Append(LINKFLAGS=['-arch', 'i386'])

elif env['platform'] in ('linuxbsd', 'linux'):
	env['target_path'] += 'linuxbsd/'
	cpp_library += '.linux'
	if env['target'] in ('debug', 'd'):
		env.Append(CCFLAGS=['-fPIC', '-g3', '-Og'])
		env.Append(LINKFLAGS=['-g3'])
		env.Append(CXXFLAGS=['-std=c++20'])
	else:
		env.Append(CCFLAGS=['-fPIC', '-O3'])
		env.Append(CXXFLAGS=['-std=c++20'])
	if env['bits'] == '64':
		env.Append(CCFLAGS=['-m64'])
		env.Append(LINKFLAGS=['-m64'])
	else:
		env.Append(CCFLAGS=['-m32'])
		env.Append(LINKFLAGS=['-m32'])

elif env['platform'] == "windows":
	env['target_path'] += 'win/'
	cpp_library += '.windows'
	# This makes sure to keep the session environment variables on windows,
	# that way you can run scons in a vs 2017 prompt and it will find all the required tools
	env.Append(ENV=os.environ)
    # Make sure the object files aren't flagged by godot for inclusion
	env['OBJSUFFIX'] = env['OBJSUFFIX'] + "." + env['bits']

	env.Append(CPPDEFINES=['WIN32', '_WIN32', '_WINDOWS', '_CRT_SECURE_NO_WARNINGS'])
	env.Append(CCFLAGS=['/W3', '/GR', '/std:c++20'])
	if env['target'] in ('debug', 'd'):
		env.Append(CPPDEFINES=['_DEBUG'])
		env.Append(CCFLAGS=['/EHsc', '/MDd', '/ZI'])
		env.Append(LINKFLAGS=['/DEBUG'])
	else:
		env.Append(CPPDEFINES=['NDEBUG'])
		env.Append(CCFLAGS=['/O2', '/EHsc', '/MD'])
	if env['bits'] == '64':
		env.Append(TARGET_ARCH='x86_64')
	else:
		env.Append(TARGET_ARCH='x86')

if env['target'] in ('debug', 'd'):
	cpp_library += '.debug'
else:
	cpp_library += '.release'

cpp_library += ".x86" if env['bits'] == 32 else ".x86_64"

# make sure our binding library is properly included
env.Append(CPPPATH=['.', godot_headers_path, cpp_bindings_path + 'include/', cpp_bindings_path + 'gen/include/'])
env.Append(LIBPATH=[cpp_bindings_path + 'bin/'])
env.Append(LIBS=[cpp_library])

# Load the sources from the subfiles
sources = []
# Find all available subfiles
def findSubfiles():
	subfiles = []
	for root, directories, filenames in os.walk('.'):
		for filename in filenames:
			if filename.find("SCsub") != -1:
				subfiles.append(os.path.join(root, filename).replace("./",""))
	return subfiles
SConscript(findSubfiles(), 'env sources')

# Write the include paths to the .clang_complete file
def updateClangComplete(clang_paths):
	f = open(".clang_complete", "w")
	f.write("-std=c++20\n")
	clang_paths.remove(".")
	clang_paths = [path.replace(" ", "\ ") for path in clang_paths]
	for path in clang_paths:
		f.write("-I" + path + "\n")
	f.close()
updateClangComplete(env['CPPPATH'])

# Create header containing all of the godot includes
def updateGodotAllHeader():
	includePaths = [godot_headers_path, cpp_bindings_path + 'include/', cpp_bindings_path + 'gen/include/']
	files = []
	for root in includePaths:
		for r, _, f in os.walk(root):
			for file in f:
				if ".hpp" in file:
					temp = os.path.join(r, file)
					for path in includePaths:
						temp = temp.removeprefix(path)
					files.append(temp)
	newFile = "#ifndef __GODOT__ALL__HPP__\n" +\
		"#define __GODOT__ALL__HPP__\n" +\
		"#ifndef GODOT_NO_REF_DEFINE\n#\tifndef REF\n#\tdefine REF(type) godot::Ref<type>\n#\tendif\n#endif //GODOT_NO_REF_DEFINE\n\n" +\
		"#include <godot_cpp/godot.hpp>\n"
	for i in files:
		newFile += "#include <" + i + ">\n"
	newFile += "\n#endif //__GODOT__ALL__HPP__\n"
	open("src/godot-link/godot_all", "w").write(newFile)
updateGodotAllHeader()

if env['target'] in ('debug', 'd'):
	env['target'] = 'debug'
else: env['target'] = 'release'

library = env.SharedLibrary(target=env['target_path'] + env['target_name'] + '.' + env['target'] + '.' + env['bits'] , source=sources)

Default(library)