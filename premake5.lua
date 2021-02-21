workspace "capricorn"
	architecture "x64"
	startproject "capricorn"

	configurations
	{
		"Debug",
		"Release"
	}

outputDir = "%{cfg.buildcfg}"   

group "Packages"

include "capricorn/packages/glfw"

group ""

project "capricorn"
	location "capricorn"
	kind "ConsoleApp"
	language "C"
	cdialect "C99"
	staticruntime "On"
	
	targetdir ("bin/" .. outputDir .. "/%{prj.name}")
	objdir ("bin-int/" .. outputDir .. "/%{prj.name}")

	files
	{
		"%{prj.name}/src/**.h",
		"%{prj.name}/src/**.c",
		--Config
		"%{prj.name}/config.ini",
		"%{prj.name}/config.json",
		--Resources
		"%{prj.name}/res/**.json",
		"%{prj.name}/res/fonts/**.ttf",
		"%{prj.name}/res/shaders/**.vert",
		"%{prj.name}/res/shaders/**.frag"
	}

	links
	{
		"GLFW",
		"opengl32"
	}

	includedirs
	{
		"%{prj.name}/src",
		"%{prj.name}/packages/glfw/include"
	}

	filter "system:windows"
		systemversion "latest"
		defines { "_CRT_SECURE_NO_WARNINGS" }

	filter "configurations:Debug"
		runtime "Debug"
		symbols "On"

	filter "configurations:Release"
		runtime "Release"
		optimize "On"