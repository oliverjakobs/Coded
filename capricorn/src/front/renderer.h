#ifndef RENDERER_H
#define RENDERER_H

#include "font.h"

typedef struct { float r, g, b, a; } ColorRGBA;

extern const ColorRGBA WHITE;
extern const ColorRGBA BLACK;
extern const ColorRGBA RED;
extern const ColorRGBA GREEN;
extern const ColorRGBA BLUE;
extern const ColorRGBA CYAN;
extern const ColorRGBA MAGENTA;
extern const ColorRGBA YELLOW;

ColorRGBA* color_rgba_blend(ColorRGBA* color, float alpha);

int renderer_init(const char* vert, const char* frag);
void renderer_destroy();

void renderer_bind_font(Font* font);
void renderer_bind_font_color(Font* font, ColorRGBA color);

void renderer_set_viewport(float x, float y, float w, float h);
void renderer_set_clear_color(ColorRGBA color);
void renderer_set_clear_colorf(float r, float g, float b, float a);

void renderer_start();
void renderer_flush();

void render_text(float x, float y, const char* text);
void render_text_fmt(float x, float y, const char* fmt, ...);

#endif // !RENDERER_H
