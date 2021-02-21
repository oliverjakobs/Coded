#include "Logger.h"

#define LOG_BLACK   "\x1b[30m"
#define LOG_RED     "\x1b[31m"
#define LOG_GREEN   "\x1b[32m"
#define LOG_YELLOW  "\x1b[33m"
#define LOG_BLUE    "\x1b[34m"
#define LOG_MAGENTA "\x1b[35m"
#define LOG_CYAN    "\x1b[36m"
#define LOG_WHITE   "\x1b[37m"

#define LOG_BG_BLACK    "\x1b[40m"
#define LOG_BG_RED      "\x1b[41m"
#define LOG_BG_GREEN    "\x1b[42m"
#define LOG_BG_YELLOW   "\x1b[43m"
#define LOG_BG_BLUE     "\x1b[44m"
#define LOG_BG_MAGENTA  "\x1b[45m"
#define LOG_BG_CYAN     "\x1b[46m"
#define LOG_BG_WHITE    "\x1b[47m"

#define LOG_RESET   "\x1b[0m" /* No color */

static int print_log_level(FILE* const stream, LogLevel level)
{
	switch (level)
	{
    case LOG_TRACE:     return fprintf(stream, LOG_WHITE "[TRACE]" LOG_RESET " ");
    case LOG_INFO:      return fprintf(stream, LOG_GREEN "[INFO]" LOG_RESET " ");
    case LOG_WARN:      return fprintf(stream, LOG_YELLOW "[WARN]" LOG_RESET " ");
    case LOG_ERROR:     return fprintf(stream, LOG_RED "[ERROR]" LOG_RESET " ");
    case LOG_CRITICAL:  return fprintf(stream, LOG_WHITE LOG_BG_RED "[CRITICAL]" LOG_RESET " ");
    default: return 0;
	}
}

void logger_write(FILE* const stream, LogLevel level, const char* fmt, ...)
{
    print_log_level(stream, level);

    va_list arg;
    va_start(arg, fmt);
    vfprintf(stream, fmt, arg);
    va_end(arg);

    fprintf(stream, "\n");
}
