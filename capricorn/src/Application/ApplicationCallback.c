#include "ApplicationCallback.h"

#include "Application.h"
#include "Logger.h"

void ApplicationEventCallback(Application* app, Event e)
{
	switch (e.type)
	{
	case EVENT_WINDOW_CLOSE:	app->running = 0; break;
	default:					app->on_event(app, e); break;
	}
}

void ApplicationGLFWErrorCallback(int error, const char* desc)
{
	DEBUG_ERROR("[GLFW] (%d) %s", error, desc);
}

void ApplicationGLFWWindowSizeCallback(GLFWwindow* window, int width, int height)
{
	Application* app = (Application*)glfwGetWindowUserPointer(window);

	app->width = width;
	app->height = height;

	EventHandlerThrowWindowEvent(EVENT_WINDOW_RESIZE, width, height);
}

void ApplicationGLFWWindowCloseCallback(GLFWwindow* window)
{
	EventHandlerThrowWindowEvent(EVENT_WINDOW_CLOSE, 0, 0);
}

void ApplicationGLFWKeyCallback(GLFWwindow* window, int key, int scancode, int action, int mods)
{
	switch (action)
	{
	case GLFW_PRESS:	EventHandlerThrowKeyEvent(EVENT_KEY_PRESSED, key, 0); break;
	case GLFW_RELEASE:	EventHandlerThrowKeyEvent(EVENT_KEY_RELEASED, key, 0); break;
	case GLFW_REPEAT:	EventHandlerThrowKeyEvent(EVENT_KEY_PRESSED, key, 1); break;
	}
}

void ApplicationGLFWCharCallback(GLFWwindow* window, unsigned int keycode)
{
	EventHandlerThrowKeyEvent(EVENT_KEY_TYPED, keycode, 0);
}

void ApplicationGLFWMouseButtonCallback(GLFWwindow* window, int button, int action, int mods)
{
	switch (action)
	{
	case GLFW_PRESS:	EventHandlerThrowMouseButtonEvent(EVENT_MOUSE_BUTTON_PRESSED, button); break;
	case GLFW_RELEASE:	EventHandlerThrowMouseButtonEvent(EVENT_MOUSE_BUTTON_RELEASED, button); break;
	}
}

void ApplicationGLFWScrollCallback(GLFWwindow* window, double xOffset, double yOffset)
{
	EventHandlerThrowMouseEvent(EVENT_MOUSE_SCROLLED, (float)xOffset, (float)yOffset);
}

void ApplicationGLFWCursorPosCallback(GLFWwindow* window, double xPos, double yPos)
{
	EventHandlerThrowMouseEvent(EVENT_MOUSE_MOVED, (float)xPos, (float)yPos);
}
