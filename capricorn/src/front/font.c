#include "font.h"

#define STB_TRUETYPE_IMPLEMENTATION
#include "Ignis/stb/stb_truetype.h"

#include "toolbox/tb_json.h"
#include "toolbox/tb_file.h"

#include "Application/Logger.h"
#include "Application/Application.h"

/* Font */
#define IGNIS_FONT_FIRST_CHAR		32
#define IGNIS_FONT_NUM_CHARS		96	/* ASCII 32..126 is 95 glyphs */
#define IGNIS_FONT_BITMAP_WIDTH		512
#define IGNIS_FONT_BITMAP_HEIGHT	512

int font_create(Font* font, const char* path, float size)
{
	if (!font) return 0;

	font->first_char = IGNIS_FONT_FIRST_CHAR;
	font->num_chars = IGNIS_FONT_NUM_CHARS;

	/* load char data */
	font->char_data = malloc(sizeof(stbtt_bakedchar) * font->num_chars);
	if (!font->char_data)
	{
		DEBUG_ERROR("[Font] Failed to allocate memory for char data");
		return 0;
	}

	int bitmap_width = IGNIS_FONT_BITMAP_WIDTH;
	int bitmap_height = IGNIS_FONT_BITMAP_HEIGHT;
	unsigned char* bitmap = malloc(sizeof(unsigned char) * bitmap_width * bitmap_height);
	if (!bitmap)
	{
		DEBUG_ERROR("[Font] Failed to allocate memory for bitmap");
		font_delete(font);
		return 0;
	}

	char* buffer = tb_file_read(path, "rb", NULL);
	if (!buffer)
	{
		DEBUG_ERROR("[Font] Failed to read file: %s", path);
		font_delete(font);
		free(bitmap);
		return 0;
	}

	/* init stbfont */
	stbtt_fontinfo info;
	if (!stbtt_InitFont(&info, buffer, 0))
	{
		DEBUG_ERROR("[Font] Failed to load font info: %s", path);
		font_delete(font);
		free(bitmap);
		return 0;
	}

	/* get height and scale */
	int ascent, descent, linegap;
	stbtt_GetFontVMetrics(&info, &ascent, &descent, &linegap);
	float scale = stbtt_ScaleForMappingEmToPixels(&info, size);
	font->height = (ascent - descent + linegap) * scale + 0.5;

	/* load glyphs */
	float s = stbtt_ScaleForMappingEmToPixels(&info, 1) / stbtt_ScaleForPixelHeight(&info, 1);
	stbtt_BakeFontBitmap(buffer, 0, size * s, bitmap, bitmap_width, bitmap_height, font->first_char, font->num_chars, font->char_data);

	free(buffer);

	IgnisTextureConfig config = IGNIS_DEFAULT_CONFIG;
	config.internal_format = GL_R8;
	config.format = GL_RED;

	if (!ignisGenerateTexture2D(&font->texture, bitmap_width, bitmap_height, bitmap, &config))
	{
		DEBUG_ERROR("[Font] Failed to create texture");
		font_delete(font);
		return 0;
	}

	free(bitmap);
	return 1;
}

void font_delete(Font* font)
{
	if (font->char_data) free(font->char_data);

	ignisDeleteTexture2D(&font->texture);
}

int font_load_char_quad(Font* font, char c, float* x, float* y, float* vertices, size_t offset)
{
	if (c >= font->first_char && c < font->first_char + font->num_chars)
	{
		stbtt_aligned_quad q;
		stbtt_GetBakedQuad(font->char_data, font->texture.width, font->texture.height, c - font->first_char, x, y, &q, 1);

		vertices[offset + 0] = q.x0;
		vertices[offset + 1] = q.y0;
		vertices[offset + 2] = q.s0;
		vertices[offset + 3] = q.t0;
		vertices[offset + 4] = q.x0;
		vertices[offset + 5] = q.y1;
		vertices[offset + 6] = q.s0;
		vertices[offset + 7] = q.t1;
		vertices[offset + 8] = q.x1;
		vertices[offset + 9] = q.y1;
		vertices[offset + 10] = q.s1;
		vertices[offset + 11] = q.t1;
		vertices[offset + 12] = q.x1;
		vertices[offset + 13] = q.y0;
		vertices[offset + 14] = q.s1;
		vertices[offset + 15] = q.t0;

		return 1;
	}

	return 0;
}

float font_get_text_width(const Font* font, const char* text, size_t len)
{
	float x = 0.0f;
	float y = 0.0f;
	for (size_t i = 0; i < len; i++)
	{
		if (text[i] >= font->first_char && text[i] < font->first_char + font->num_chars)
		{
			stbtt_aligned_quad q;
			stbtt_GetBakedQuad(font->char_data, font->texture.width, font->texture.height, text[i] - font->first_char, &x, &y, &q, 1);
		}
	}
	return x;
}

int fm_load(FontManager* manager, const char* path)
{
	char* json = tb_file_read(path, "rb", NULL);

	if (!json)
	{
		DEBUG_ERROR("[FontManager] Failed to read index (%s)\n", path);
		return 0;
	}

	manager->arena.blocks = NULL;
	manager->arena.ptr = NULL;
	manager->arena.end = NULL;

	if (tb_hashmap_alloc(&manager->fonts, tb_hash_string, tb_hashmap_str_cmp, 0) != TB_HASHMAP_OK)
	{
		DEBUG_ERROR("[FontManager] Failed to allocate hashmap index\n");
		return 0;
	}

	tb_hashmap_set_key_alloc_funcs(&manager->fonts, tb_hashmap_str_alloc, tb_hashmap_str_free);

	/* load fonts */
	tb_json_element fonts;
	tb_json_read(json, &fonts, NULL);

	for (int i = 0; i < fonts.elements; i++)
	{
		char font_name[APPLICATION_STR_LEN];
		tb_json_string(fonts.value, "{*", font_name, APPLICATION_STR_LEN, &i);

		tb_json_element font;
		tb_json_read_format(fonts.value, &font, "{'%s'", font_name);

		char font_path[APPLICATION_PATH_LEN];
		tb_json_string(font.value, "{'path'", font_path, APPLICATION_PATH_LEN, NULL);

		float font_size = tb_json_float(font.value, "{'size'", NULL, 0.0f);

		fm_add_font(manager, font_name, font_path, font_size);
	}

	free(json);

	return 1;
}

void fm_destroy(FontManager* manager)
{
	for (tb_hashmap_iter* iter = tb_hashmap_iterator(&manager->fonts); iter; iter = tb_hashmap_iter_next(&manager->fonts, iter))
	{
		Font* font = tb_hashmap_iter_get_value(iter);
		font_delete(font);
	}
	tb_hashmap_free(&manager->fonts);

	arena_free(&manager->arena);
}

Font* fm_add_font(FontManager* manager, const char* name, const char* path, float size)
{
	Font* font = arena_alloc(&manager->arena, sizeof(Font));
	if (font_create(font, path, size))
	{
		if (tb_hashmap_insert(&manager->fonts, name, font) == font)
			return font;

		DEBUG_ERROR("[FontManager] Failed to add font: %s (%s)\n", name, path);
		font_delete(font);
	}
	return NULL;
}

Font* fm_get_font(const FontManager* manager, const char* name)
{
	Font* font = tb_hashmap_find(&manager->fonts, name);
	if (!font) DEBUG_WARN("[FontManager] Could not find font: %s\n", name);
	return font;
}

const char* fm_get_font_name(const FontManager* manager, const Font* font)
{
	for (tb_hashmap_iter* iter = tb_hashmap_iterator(&manager->fonts); iter; iter = tb_hashmap_iter_next(&manager->fonts, iter))
	{
		if (font == tb_hashmap_iter_get_value(iter))
			return tb_hashmap_iter_get_key(iter);
	}

	return NULL;
}