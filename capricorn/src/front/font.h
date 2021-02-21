#ifndef FONT_H
#define FONT_H

#include "Ignis/Core/Texture.h"

#include "Ignis/stb/stb_truetype.h"
#include "toolbox/tb_hashmap.h"
#include "memory/arena.h"

typedef struct
{
	int first_char;
	int num_chars;
	float height;

	stbtt_bakedchar* char_data;

	IgnisTexture2D texture;
} Font;

int font_create(Font* font, const char* path, float size);
void font_delete(Font* font);

int font_load_char_quad(Font* font, char c, float* x, float* y, float* vertices, size_t offset);

float font_get_text_width(const Font* font, const char* text, size_t len);

typedef struct
{
	tb_hashmap fonts;	/* <str,IgnisFont> */
	Arena arena;
} FontManager;

int fm_load(FontManager* manager, const char* path);
void fm_destroy(FontManager* manager);

Font* fm_add_font(FontManager* manager, const char* name, const char* path, float size);

Font* fm_get_font(const FontManager* manager, const char* name);
const char* fm_get_font_name(const FontManager* manager, const Font* font);

#endif // !FONT_H
