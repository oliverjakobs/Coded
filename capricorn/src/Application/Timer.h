#ifndef TIMER_H
#define TIMER_H

typedef struct
{
	double seconds;
	int frames;
	int fps;

	double deltatime;
	double lastframe;
} Timer;

void TimerReset(Timer* timer);
void TimerStart(Timer* timer, double seconds);
void TimerEnd(Timer* timer, double seconds);


#endif /* !TIMER_H */
