#include "Input.h"

typedef struct
{
	int state;
	int prev;
} InputKeyState;

static InputKeyState key_states[KEY_LAST + 1];

void InputUpdate(GLFWwindow* context)
{
	for (int i = KEY_SPACE; i <= KEY_LAST; ++i)
	{
		key_states[i].prev = key_states[i].state;
		key_states[i].state = (glfwGetKey(context, i) == GLFW_PRESS);
	}
}

int InputKeyPressed(Key keycode)
{
	if (keycode > KEY_LAST || keycode == KEY_UNKNOWN)
		return 0;

	int state = glfwGetKey(glfwGetCurrentContext(), keycode);
	return state == GLFW_PRESS || state == GLFW_REPEAT;
}

int InputKeyReleased(Key keycode)
{
	if (keycode > KEY_LAST || keycode == KEY_UNKNOWN)
		return 0;

	int state = glfwGetKey(glfwGetCurrentContext(), keycode);
	return state == GLFW_RELEASE;
}

int InputKeyHit(Key keycode)
{
	if (keycode > KEY_LAST || keycode == KEY_UNKNOWN)
		return 0;

	return key_states[keycode].state && !key_states[keycode].prev;
}

int InputKeyDown(Key keycode)
{
	if (keycode > KEY_LAST || keycode == KEY_UNKNOWN)
		return 0;

	return key_states[keycode].state;
}

int InputKeyUp(Key keycode)
{
	if (keycode > KEY_LAST || keycode == KEY_UNKNOWN)
		return 0;

	return key_states[keycode].prev && !key_states[keycode].state;
}

int InputMousePressed(MouseButton button)
{
	if (button > MOUSE_BUTTON_LAST || button < MOUSE_BUTTON_1)
		return 0;

	int state = glfwGetMouseButton(glfwGetCurrentContext(), button);
	return state == GLFW_PRESS;
}

int InputMouseReleased(MouseButton button)
{
	if (button > MOUSE_BUTTON_LAST || button < MOUSE_BUTTON_1)
		return 0;

	int state = glfwGetMouseButton(glfwGetCurrentContext(), button);
	return state == GLFW_RELEASE;
}

void InputMousePosition(float* x, float* y)
{
	double xpos, ypos;
	glfwGetCursorPos(glfwGetCurrentContext(), &xpos, &ypos);

	if (x) *x = (float)xpos;
	if (y) *y = (float)ypos;
}

float InputMouseX()
{
	float x;
	InputMousePosition(&x, NULL);
	return x;
}

float InputMouseY()
{
	float y;
	InputMousePosition(NULL, &y);
	return y;
}
