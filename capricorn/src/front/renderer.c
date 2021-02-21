#include "renderer.h"

#include "Ignis/Ignis.h"
#include "Application/Logger.h"

#define FONTRENDERER_MAX_QUADS          32
#define FONTRENDERER_VERTEX_SIZE        4
#define FONTRENDERER_VERTICES_PER_QUAD  4
#define FONTRENDERER_INDICES_PER_QUAD   6

#define FONTRENDERER_INDEX_COUNT        (FONTRENDERER_MAX_QUADS * FONTRENDERER_INDICES_PER_QUAD)
#define FONTRENDERER_VERTEX_COUNT       (FONTRENDERER_MAX_QUADS * FONTRENDERER_VERTICES_PER_QUAD)
#define FONTRENDERER_BUFFER_SIZE        (FONTRENDERER_VERTEX_COUNT * FONTRENDERER_VERTEX_SIZE)

#define FONTRENDERER_MAX_LINE_LENGTH    128

const ColorRGBA WHITE	= { 1.0f, 1.0f, 1.0f, 1.0f };
const ColorRGBA BLACK	= { 0.0f, 0.0f, 0.0f, 1.0f };
const ColorRGBA RED		= { 1.0f, 0.0f, 0.0f, 1.0f };
const ColorRGBA GREEN	= { 0.0f, 1.0f, 0.0f, 1.0f };
const ColorRGBA BLUE	= { 0.0f, 0.0f, 1.0f, 1.0f };
const ColorRGBA CYAN	= { 0.0f, 1.0f, 1.0f, 1.0f };
const ColorRGBA MAGENTA = { 1.0f, 0.0f, 1.0f, 1.0f };
const ColorRGBA YELLOW	= { 1.0f, 1.0f, 0.0f, 1.0f };

ColorRGBA* color_rgba_blend(ColorRGBA* color, float alpha)
{
	color->a = alpha;
	return color;
}

typedef struct
{
	IgnisVertexArray vao;
	IgnisShader shader;

	Font* font;
	ColorRGBA color;

	float* vertices;
	size_t vertex_index;

	size_t quad_count;
	float projection[4 * 4];

	char line_buffer[FONTRENDERER_MAX_LINE_LENGTH];

	GLint uniform_location_proj;
	GLint uniform_location_color;
} FontRendererStorage;

static FontRendererStorage _render_data;

static void renderer_generate_indices(GLuint* indices, size_t max, size_t step)
{
	GLuint offset = 0;
	for (size_t i = 0; i < max - step; i += step)
	{
		indices[i + 0] = offset + 0;
		indices[i + 1] = offset + 1;
		indices[i + 2] = offset + 2;

		indices[i + 3] = offset + 2;
		indices[i + 4] = offset + 3;
		indices[i + 5] = offset + 0;

		offset += 4;
	}
}

static void ignis_error_callback(ignisErrorLevel level, const char* desc)
{
	switch (level)
	{
	case IGNIS_WARN:		DEBUG_WARN("%s", desc); break;
	case IGNIS_ERROR:		DEBUG_ERROR("%s", desc); break;
	case IGNIS_CRITICAL:	DEBUG_CRITICAL("%s", desc); break;
	}
}

int renderer_init(const char* vert, const char* frag)
{
	/* ingis initialization */
	ignisSetErrorCallback(ignis_error_callback);

	int debug = 0;
#ifdef _DEBUG
	debug = 1;
#endif

	if (!ignisInit(debug))
	{
		DEBUG_ERROR("[IGNIS] Failed to initialize Ignis");
		return 0;
	}

	DEBUG_INFO("[OpenGL] Version: %s", ingisGetGLVersion());
	DEBUG_INFO("[OpenGL] Vendor: %s", ingisGetGLVendor());
	DEBUG_INFO("[OpenGL] Renderer: %s", ingisGetGLRenderer());
	DEBUG_INFO("[OpenGL] GLSL Version: %s", ingisGetGLSLVersion());

	ignisEnableBlend(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

	ignisGenerateVertexArray(&_render_data.vao);

	IgnisBufferElement layout[] = { {GL_FLOAT, 4, GL_FALSE} };
	ignisAddArrayBufferLayout(&_render_data.vao, FONTRENDERER_BUFFER_SIZE * sizeof(float), NULL, GL_DYNAMIC_DRAW, 0, layout, 1);

	GLuint indices[FONTRENDERER_INDEX_COUNT];
	renderer_generate_indices(indices, FONTRENDERER_INDEX_COUNT, FONTRENDERER_INDICES_PER_QUAD);

	ignisLoadElementBuffer(&_render_data.vao, indices, FONTRENDERER_INDEX_COUNT, GL_STATIC_DRAW);

	_render_data.vertices = malloc(FONTRENDERER_BUFFER_SIZE * sizeof(float));
	_render_data.vertex_index = 0;
	_render_data.quad_count = 0;

	_render_data.font = NULL;
	_render_data.color = WHITE;

	ignisCreateShadervf(&_render_data.shader, vert, frag);

	_render_data.uniform_location_proj = ignisGetUniformLocation(&_render_data.shader, "u_Projection");
	_render_data.uniform_location_color = ignisGetUniformLocation(&_render_data.shader, "u_Color");

	return 1;
}

void renderer_destroy()
{
	free(_render_data.vertices);

	ignisDeleteShader(&_render_data.shader);
	ignisDeleteVertexArray(&_render_data.vao);
}

void renderer_bind_font(Font* font)
{
	_render_data.font = font;
}

void renderer_bind_font_color(Font* font, ColorRGBA color)
{
	_render_data.font = font;
	_render_data.color = color;

	ignisSetUniform4fl(&_render_data.shader, _render_data.uniform_location_color, &_render_data.color.r);
}

void renderer_set_viewport(float x, float y, float w, float h)
{
	/* create ortho projection matrix with near: -1.0f, far: 1.0f */
	float rl = 1.0f / (w - x);
	float tb = 1.0f / (y - h);

	_render_data.projection[0] = 2.0f * rl;
	_render_data.projection[1] = 0.0f;
	_render_data.projection[2] = 0.0f;
	_render_data.projection[3] = 0.0f;
	_render_data.projection[4] = 0.0f;
	_render_data.projection[5] = 2.0f * tb;
	_render_data.projection[6] = 0.0f;
	_render_data.projection[7] = 0.0f;
	_render_data.projection[8] = 0.0f;
	_render_data.projection[9] = 0.0f;
	_render_data.projection[10] = -1.0f;
	_render_data.projection[11] = 0.0f;
	_render_data.projection[12] = -(x + w) * rl;
	_render_data.projection[13] = -(y + h) * tb;
	_render_data.projection[14] = 0.0f;
	_render_data.projection[15] = 1.0f;

	glViewport(x, y, w, h);
}

void renderer_set_clear_color(ColorRGBA color)
{
	renderer_set_clear_colorf(color.r, color.g, color.b, color.a);
}

void renderer_set_clear_colorf(float r, float g, float b, float a)
{
	glClearColor(r, g, b, a);
}

void renderer_start()
{
	ignisSetUniformMat4l(&_render_data.shader, _render_data.uniform_location_proj, _render_data.projection);
}

void renderer_flush()
{
	if (_render_data.vertex_index == 0)
		return;

	ignisBindTexture2D(&_render_data.font->texture, 0);
	ignisBindVertexArray(&_render_data.vao);
	ignisBufferSubData(&_render_data.vao.array_buffers[0], 0, _render_data.vertex_index * sizeof(float), _render_data.vertices);

	ignisUseShader(&_render_data.shader);

	glDrawElements(GL_TRIANGLES, FONTRENDERER_INDICES_PER_QUAD * (GLsizei)_render_data.quad_count, GL_UNSIGNED_INT, NULL);

	_render_data.vertex_index = 0;
	_render_data.quad_count = 0;
}

void render_text(float x, float y, const char* text)
{
	if (!_render_data.font)
	{
		_ignisErrorCallback(IGNIS_WARN, "[FontRenderer] No font bound");
		return;
	}

	y += _render_data.font->height;

	for (size_t i = 0; i < strlen(text); i++)
	{
		if (_render_data.vertex_index + FONTRENDERER_VERTICES_PER_QUAD * FONTRENDERER_VERTEX_SIZE >= FONTRENDERER_BUFFER_SIZE)
			renderer_flush();

		if (!font_load_char_quad(_render_data.font, text[i], &x, &y, _render_data.vertices, _render_data.vertex_index))
			_ignisErrorCallback(IGNIS_WARN, "[FontRenderer] Failed to load quad for %c", text[i]);

		_render_data.vertex_index += FONTRENDERER_VERTICES_PER_QUAD * FONTRENDERER_VERTEX_SIZE;
		_render_data.quad_count++;
	}
}

static void render_text_va(float x, float y, const char* fmt, va_list args)
{
	size_t buffer_size = vsnprintf(NULL, 0, fmt, args);
	vsnprintf(_render_data.line_buffer, buffer_size + 1, fmt, args);

	render_text(x, y, _render_data.line_buffer);
}

void render_text_fmt(float x, float y, const char* fmt, ...)
{
	va_list args;
	va_start(args, fmt);
	render_text_va(x, y, fmt, args);
	va_end(args);
}