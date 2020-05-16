#!python
import os, subprocess

opts = Variables([], ARGUMENTS)

# Gets the standard flags CC, CCX, etc.
env = DefaultEnvironment()

# Define our options
opts.Add(EnumVariable('target', "Compilation target", 'debug', ['d', 'debug', 'r', 'release']))
opts.Add(EnumVariable('platform', "Compilation platform", '', ['', 'windows', 'x11', 'linux', 'osx']))
opts.Add(EnumVariable('p', "Compilation target, alias for 'platform'", '', ['', 'windows', 'x11', 'linux', 'osx']))
opts.Add(EnumVariable('bits', 'The number of bits the application should support.', "64", ["32", "64"]))
opts.Add(BoolVariable('use_llvm', "Use the LLVM / Clang compiler", 'no'))
opts.Add(PathVariable('target_path', 'The path where the lib is installed.', 'src/bin/'))
opts.Add(PathVariable('target_name', 'The library name.', 'libgame', PathVariable.PathAccept))
opts.Add(BoolVariable('clang_complete', 'Should we generate a .clang_complete file?', "yes"))

# Generates help for the -h scons option.
Help(opts.GenerateHelpText(env))

# Local dependency paths, adapt them to your setup
godot_headers_path = "godot-cpp/godot_headers/"
cpp_bindings_path = "godot-cpp/"
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
	quit();

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
		env.Append(CCFLAGS=['-g', '-O2', '-arch', 'x86_64'])
	else:
		env.Append(CCFLAGS=['-g', '-O3', '-arch', 'x86_64'])
	if env['bits'] == '64':
		env.Append(LINKFLAGS=['-arch', 'x86_64'])
	else:
		env.Append(LINKFLAGS=['-arch', 'i386'])

elif env['platform'] in ('x11', 'linux'):
	env['target_path'] += 'x11/'
	cpp_library += '.linux'
	if env['target'] in ('debug', 'd'):
		env.Append(CCFLAGS=['-fPIC', '-g3', '-Og'])
		env.Append(CXXFLAGS=['-std=c++17'])
	else:
		env.Append(CCFLAGS=['-fPIC', '-g', '-O3'])
		env.Append(CXXFLAGS=['-std=c++17'])
	if env['bits'] == '64':
		env.Append(CCFLAGS=['-m64'])
		env.Append(LINKFLAGS=['-m64'])
	else:
		env.Append(CCFLAGS=['-m32'])
		env.Append(LINKFLAGS=['-m32'])

elif env['platform'] == "windows":
	env['target_path'] += 'win64/'
	cpp_library += '.windows'
	# This makes sure to keep the session environment variables on windows,
	# that way you can run scons in a vs 2017 prompt and it will find all the required tools
	env.Append(ENV=os.environ)

	env.Append(CPPDEFINES=['WIN32', '_WIN32', '_WINDOWS', '_CRT_SECURE_NO_WARNINGS'])
	env.Append(CCFLAGS=['-W3', '-GR'])
	if env['target'] in ('debug', 'd'):
		env.Append(CPPDEFINES=['_DEBUG'])
		env.Append(CCFLAGS=['-EHsc', '-MDd', '-ZI'])
		env.Append(LINKFLAGS=['-DEBUG'])
	else:
		env.Append(CPPDEFINES=['NDEBUG'])
		env.Append(CCFLAGS=['-O2', '-EHsc', '-MD'])
	if env['bits'] == '64':
		env.Append(TARGET_ARCH='x86_64')
	else:
		env.Append(TARGET_ARCH='x86')

if env['target'] in ('debug', 'd'):
	cpp_library += '.debug'
else:
	cpp_library += '.release'

cpp_library += '.' + env['bits']

# make sure our binding library is properly includes
env.Append(CPPPATH=['.', godot_headers_path, cpp_bindings_path + 'include/', cpp_bindings_path + 'include/core/', cpp_bindings_path + 'include/gen/'])
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
	clang_paths.remove(".")
	clang_paths = [path.replace(" ", "\ ") for path in clang_paths]
	for path in clang_paths:
		f.write("-I" + path + "\n")
	f.close()
updateClangComplete(env['CPPPATH'])

library = env.SharedLibrary(target=env['target_path'] + env['target_name'] + '.' + env['bits'] , source=sources)

Default(library)
