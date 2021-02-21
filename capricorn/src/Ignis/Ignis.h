#ifndef IGNIS_H
#define IGNIS_H

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>

/* You can #define IGNIS_ASSERT(x) before the #include to avoid using assert.h */
#ifndef IGNIS_ASSERT
#include <assert.h>
#define IGNIS_ASSERT(x) assert(x)
#endif

/* defines */
#define IGNIS_SUCCESS	1
#define IGNIS_FAILURE	0

/* Core */
#include "Core/Texture.h"
#include "Core/Shader.h"
#include "Core/Buffer.h"

/* Vertex Array */
#define IGNIS_BUFFER_ARRAY_INITIAL_SIZE		4
#define IGNIS_BUFFER_ARRAY_GROWTH_FACTOR	2

#include "VertexArray.h"

int ignisInit(int debug);

typedef enum
{
	IGNIS_WARN = 0,
	IGNIS_ERROR = 1,
	IGNIS_CRITICAL = 2
} ignisErrorLevel;

void ignisSetErrorCallback(void (*callback)(ignisErrorLevel, const char*));
void _ignisErrorCallback(ignisErrorLevel level, const char* fmt, ...);

GLuint ignisGetOpenGLTypeSize(GLenum type);

int ignisEnableBlend(GLenum sfactor, GLenum dfactor);

char* ignisReadFile(const char* path, size_t* sizeptr);

/* Infos */
const char* ingisGetGLVersion();
const char* ingisGetGLVendor();
const char* ingisGetGLRenderer();
const char* ingisGetGLSLVersion();

/* Memory */
void* ignisAlloc(size_t size);
void* ignisRealloc(void* block, size_t size);
void ignisFree(void* block);

#ifdef __cplusplus
}
#endif

#endif /* !IGNIS_H */