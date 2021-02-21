#include "front/renderer.h"
#include "Application/Application.h"
#include "Application/Logger.h"

FontManager fonts;

int OnInit(Application* app)
{
	renderer_init("res/shaders/font.vert", "res/shaders/font.frag");
	renderer_set_viewport(0, 0, app->width, app->height);
	renderer_set_clear_colorf(0.2f, 0.2f, 0.2f, 1.0f);

	fm_load(&fonts, "res/fonts.json");
	renderer_bind_font_color(fm_get_font(&fonts, "gui"), WHITE);

	ApplicationEnableDebugMode(app, 1);
	ApplicationEnableVsync(app, 0);

	return 1;
}

void OnDestroy(Application* app)
{
	renderer_destroy();

	fm_destroy(&fonts);
}

void OnEvent(Application* app, Event e)
{
	if (EventCheckType(&e, EVENT_WINDOW_RESIZE))
		renderer_set_viewport(0, 0, e.window.width, e.window.height);

	switch (EventKeyPressed(&e))
	{
	case KEY_ESCAPE:	ApplicationClose(app); break;
	case KEY_F5:		ApplicationPause(app); break;
	case KEY_F6:		ApplicationToggleVsync(app); break;
	case KEY_F7:		ApplicationToggleDebugMode(app); break;
	}
}

void OnUpdate(Application* app, float deltatime)
{

}

void OnRender(Application* app)
{

}

void OnRenderDebug(Application* app)
{
	renderer_start();
	
	/* fps */
	render_text_fmt(8.0f, 8.0f, "FPS: %d", app->timer.fps);

	renderer_flush();
}

int main()
{
	Application app;

	ApplicationSetOnInitCallback(&app, OnInit);
	ApplicationSetOnDestroyCallback(&app, OnDestroy);
	ApplicationSetOnEventCallback(&app, OnEvent);
	ApplicationSetOnUpdateCallback(&app, OnUpdate);
	ApplicationSetOnRenderCallback(&app, OnRender);
	ApplicationSetOnRenderDebugCallback(&app, OnRenderDebug);

	ApplicationLoadConfig(&app, "config.json");

	ApplicationRun(&app);

	ApplicationDestroy(&app);

	return 0;
}