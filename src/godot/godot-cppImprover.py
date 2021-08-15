#!python
import os

# Load list of possible inclusions
files = []
root = os.getcwd().replace("/src/godot", "") + "/godot-cpp/include"
for file in os.listdir(root + "/gen"):
	if ".hpp" in file:
		files.append(file.replace(".hpp", ""))

# Make the directory
if not os.path.exists(root + "/gen/godot"): os.mkdir(root + "/gen/godot")

# Make all of the include connections
for file in files:
	# Search through the current file and see if it references any other files
	includes = []
	f = open(root + "/gen/" + file + ".hpp", "r").read()
	for possibleInclude in files:
		if possibleInclude in f:
			includes.append(possibleInclude)
	includes.sort()

	# Create the generated file based on the following template
	newFile = "#ifndef __GODOT__" + file.upper() + "__HPP__\n" +\
		"#define __GODOT__" + file.upper() + "__HPP__\n\n"
	for i in includes:
		newFile += "#include <" + i + ".hpp>\n"
	newFile += "#endif //__GODOT__" + file.upper() + "__HPP__\n"

	# Write the file
	open(root + "/gen/godot/" + file, "w").write(newFile)
	print("\n\n\n", newFile)

# File which includes all of Godot
newFile = "#ifndef __GODOT__ALL__HPP__\n" +\
	"#define __GODOT__ALL__HPP__\n" +\
	"#ifndef GODOT_NO_REF_DEFINE\n#\tifndef REF\n#\tdefine REF(type) godot::Ref<type>\n#\tendif\n#endif //GODOT_NO_REF_DEFINE\n\n" +\
	"#include <core/Godot.hpp>\n"
for i in files:
	newFile += "#include <" + i + ".hpp>\n"
newFile += "#endif //__GODOT__ALL__HPP__\n"
open(root + "/gen/godot/GodotAll", "w").write(newFile)
print("\n\n\n",newFile)

# File which includes the common Godot nessecities
includes = ["ResourceLoader", "ResourceSaver", "SceneTree", "Node2D", "Spatial", "Reference", "Input"]
newFile = "#ifndef __GODOT__COMMON__HPP__\n" +\
	"#define __GODOT__COMMON__HPP__\n" +\
	"#ifdef GODOT_INCLUDE_ALL\n#include <GodotAll>\n#else\n" +\
	"#ifndef GODOT_NO_REF_DEFINE\n#\tifndef REF\n#\tdefine REF(type) godot::Ref<type>\n#\tendif\n#endif //GODOT_NO_REF_DEFINE\n\n" +\
	"#include <core/Godot.hpp>\n"
for i in includes:
	newFile += "#include <" + i + ">\n"
newFile += "#endif //GODOT_INCLUDE_ALL\n" +\
	"#endif //__GODOT__COMMON__HPP__\n"
open(root + "/gen/godot/GodotCommon", "w").write(newFile)
print("\n\n\n",newFile)

# Replace the relevant line of code in Gstream.hpp
if os.path.exists(os.getcwd().replace("/src/godot", "") + "/src/godot/Gstream.hpp"):
	f = open(os.getcwd().replace("/src/godot", "") + "/src/godot/Gstream.hpp", "r").read()
	if "#include <Godot.hpp>" in f: f = f.replace("#include <Godot.hpp>", "#include <GodotCommon>")
	open(os.getcwd().replace("/src/godot", "") + "/src/godot/Gstream.hpp", "w").write(f)
