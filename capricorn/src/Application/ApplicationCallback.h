#ifndef APPLICATION_CALLBACK_H
#define APPLICATION_CALLBACK_H

#include "Application.h"

/*
 * Gets called when an event is processed, handles some (e.g. WindowCloseEvents) 
 * and passes the rest to the on_event callback of app
 */
void ApplicationEventCallback(Application* app, Event e);

/* 
 * Translates GLFW events to application events
 */
void ApplicationGLFWErrorCallback(int error, const char* desc);
void ApplicationGLFWWindowSizeCallback(GLFWwindow* window, int width, int height);
void ApplicationGLFWWindowCloseCallback(GLFWwindow* window);
void ApplicationGLFWKeyCallback(GLFWwindow* window, int key, int scancode, int action, int mods);
void ApplicationGLFWCharCallback(GLFWwindow* window, unsigned int keycode);
void ApplicationGLFWMouseButtonCallback(GLFWwindow* window, int button, int action, int mods);
void ApplicationGLFWScrollCallback(GLFWwindow* window, double xOffset, double yOffset);
void ApplicationGLFWCursorPosCallback(GLFWwindow* window, double xPos, double yPos);

#endif /* !APPLICATION_CALLBACK_H */
