#include "Ignis.h"

void APIENTRY _ignisDebugOutput(GLenum source, GLenum type, GLuint id, GLenum severity, GLsizei length, const GLchar* message, const void* userParam)
{
	/* ignore non-significant error/warning codes */
	if (id == 131169 || id == 131185 || id == 131218 || id == 131204) return;

	_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Debug output (%d):", id);
	_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] %s", message);

	switch (source)
	{
	case GL_DEBUG_SOURCE_API:				_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Source: API"); break;
	case GL_DEBUG_SOURCE_WINDOW_SYSTEM:		_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Source: Window System"); break;
	case GL_DEBUG_SOURCE_SHADER_COMPILER:	_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Source: Shader Compiler"); break;
	case GL_DEBUG_SOURCE_THIRD_PARTY:		_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Source: Third Party"); break;
	case GL_DEBUG_SOURCE_APPLICATION:		_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Source: Application"); break;
	case GL_DEBUG_SOURCE_OTHER:				_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Source: Other"); break;
	}

	switch (type)
	{
	case GL_DEBUG_TYPE_ERROR:				_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Type: Error"); break;
	case GL_DEBUG_TYPE_DEPRECATED_BEHAVIOR:	_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Type: Deprecated Behaviour"); break;
	case GL_DEBUG_TYPE_UNDEFINED_BEHAVIOR:	_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Type: Undefined Behaviour"); break;
	case GL_DEBUG_TYPE_PORTABILITY:			_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Type: Portability"); break;
	case GL_DEBUG_TYPE_PERFORMANCE:			_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Type: Performance"); break;
	case GL_DEBUG_TYPE_MARKER:				_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Type: Marker"); break;
	case GL_DEBUG_TYPE_PUSH_GROUP:			_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Type: Push Group"); break;
	case GL_DEBUG_TYPE_POP_GROUP:			_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Type: Pop Group"); break;
	case GL_DEBUG_TYPE_OTHER:				_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Type: Other"); break;
	}

	switch (severity)
	{
	case GL_DEBUG_SEVERITY_HIGH:			_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Severity: high"); break;
	case GL_DEBUG_SEVERITY_MEDIUM:			_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Severity: medium"); break;
	case GL_DEBUG_SEVERITY_LOW:				_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Severity: low"); break;
	case GL_DEBUG_SEVERITY_NOTIFICATION:	_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Severity: notification"); break;
	}
}

int ignisInit(int debug)
{
	/* loading glad */
	if (!gladLoadGL())
	{
		_ignisErrorCallback(IGNIS_ERROR, "[GLAD] Failed to initialize GLAD");
		return 0;
	}

	if (debug)
	{
		/* Set up opengl debug output */
		GLint flags, minor, major;
		glGetIntegerv(GL_CONTEXT_FLAGS, &flags);
		glGetIntegerv(GL_MINOR_VERSION, &minor);
		glGetIntegerv(GL_MAJOR_VERSION, &major);

		if ((flags & GL_CONTEXT_FLAG_DEBUG_BIT) && (major >= 4 && minor >= 3))
		{
			glEnable(GL_DEBUG_OUTPUT);
			glEnable(GL_DEBUG_OUTPUT_SYNCHRONOUS);
			glDebugMessageCallback(_ignisDebugOutput, NULL);
			glDebugMessageControl(GL_DONT_CARE, GL_DONT_CARE, GL_DONT_CARE, 0, NULL, GL_TRUE);
		}
		else
		{
			_ignisErrorCallback(IGNIS_ERROR, "[OpenGL] Could not create debug context");
		}
	}

	return 1;
}

static void (*s_ignisErrorCallback)(ignisErrorLevel level, const char* fmt);

void ignisSetErrorCallback(void (*callback)(ignisErrorLevel, const char*))
{
	s_ignisErrorCallback = callback;
}

void _ignisErrorCallback(ignisErrorLevel level, const char* fmt, ...)
{
	va_list args;
	va_start(args, fmt);
	size_t buffer_size = vsnprintf(NULL, 0, fmt, args);
	char* buffer = ignisAlloc(buffer_size + 1);
	vsnprintf(buffer, buffer_size + 1, fmt, args);
	va_end(args);

	s_ignisErrorCallback(level, buffer);

	ignisFree(buffer);
}

GLuint ignisGetOpenGLTypeSize(GLenum type)
{
	switch (type)
	{
	case GL_FLOAT:			return sizeof(GLfloat);
	case GL_INT:			return sizeof(GLint);
	case GL_UNSIGNED_INT:	return sizeof(GLuint);
	default: return 0;
	}
}

int ignisEnableBlend(GLenum sfactor, GLenum dfactor)
{
	if (sfactor == GL_NONE && dfactor == GL_NONE)
	{
		glDisable(GL_BLEND);
		return 0;
	}

	glEnable(GL_BLEND);
	glBlendFunc(sfactor, dfactor);
	return 1;
}

char* ignisReadFile(const char* path, size_t* sizeptr)
{
	FILE* file = fopen(path, "rb");
	if (!file)
	{
		_ignisErrorCallback(IGNIS_ERROR, "[Ignis] Failed to open file: %s", path);
		return NULL;
	}

	/* find file size */
	fseek(file, 0, SEEK_END);
	size_t size = ftell(file);
	rewind(file);

	char* buffer = ignisAlloc(size + 1);
	if (!buffer)
	{
		_ignisErrorCallback(IGNIS_ERROR, "[Ignis] Failed to allocate memory for file: %s", path);
		fclose(file);
		return NULL;
	}

	if (fread(buffer, size, 1, file) != 1)
	{
		ignisFree(buffer);
		fclose(file);
		return NULL;
	}

	buffer[size] = '\0'; /* zero terminate buffer */

	if (sizeptr)
		*sizeptr = size + 1;

	fclose(file);
	return buffer;
}

const char* ingisGetGLVersion()		{ return glGetString(GL_VERSION); }
const char* ingisGetGLVendor()		{ return glGetString(GL_VENDOR); }
const char* ingisGetGLRenderer()	{ return glGetString(GL_RENDERER); }
const char* ingisGetGLSLVersion()	{ return glGetString(GL_SHADING_LANGUAGE_VERSION); }

void* ignisAlloc(size_t size)
{
	return malloc(size);
}

void* ignisRealloc(void* block, size_t size)
{
	return realloc(block, size);
}

void ignisFree(void* block)
{
	free(block);
}